"""Prepare a release from first-parent squash commits; never publish it."""
import json
import re
import subprocess
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / '.release-state.json'
PATTERN = re.compile(r'^(feat|fix|perf)(?:\(([^)]+)\))?(!)?: .+')
SUPPORT_SCOPES = {'ci', 'tests', 'test', 'docs', 'build', 'release', 'deps', 'dependencies'}


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT, text=True).strip()


def bump_for(subject, body, paths):
    match = PATTERN.match(subject)
    if not match or (match.group(2) or '').lower() in SUPPORT_SCOPES:
        return 0
    if not any(path.startswith('src/pinba/') and path.endswith('.py') for path in paths):
        return 0
    if match.group(3) or re.search(r'^BREAKING[ -]CHANGE:', body, re.MULTILINE):
        return 3
    return 2 if match.group(1) == 'feat' else 1


def next_version(version, bump):
    major, minor, patch = map(int, version.split('.'))
    if bump == 3:
        return f'{major + 1}.0.0'
    if bump == 2:
        return f'{major}.{minor + 1}.0'
    return f'{major}.{minor}.{patch + 1}'


def main():
    state = json.loads(STATE.read_text())
    base = state['baseline']
    subprocess.run(['git', 'merge-base', '--is-ancestor', base, 'HEAD'], cwd=ROOT, check=True)
    commits = git('rev-list', '--first-parent', '--reverse', f'{base}..HEAD').splitlines()
    eligible = []
    for commit in commits:
        subject = git('show', '-s', '--format=%s', commit)
        body = git('show', '-s', '--format=%b', commit)
        paths = git('diff-tree', '--root', '--no-commit-id', '--name-only', '-r', commit).splitlines()
        bump = bump_for(subject, body, paths)
        if bump:
            eligible.append((bump, subject, commit))
    if not eligible:
        print('No eligible runtime changes; no release prepared.')
        return
    version = next_version(state['version'], max(item[0] for item in eligible))
    project = ROOT / 'pyproject.toml'
    text = project.read_text()
    text, count = re.subn(r'(?m)^version = "' + re.escape(state['version']) + r'"$', f'version = "{version}"', text, count=1)
    if count != 1:
        raise ValueError('project version does not match release state')
    project.write_text(text)
    changelog = ROOT / 'CHANGELOG.md'
    old = changelog.read_text() if changelog.exists() else '# Changelog\n'
    if not old.startswith('# Changelog\n'):
        raise ValueError('unexpected changelog format')
    lines = ''.join(f'- {subject} ({sha[:7]})\n' for _, subject, sha in eligible)
    changelog.write_text(f'# Changelog\n\n## {version} ({date.today().isoformat()})\n\n{lines}' + old[len('# Changelog\n'):])
    STATE.write_text(json.dumps({'version': version, 'baseline': git('rev-parse', 'HEAD')}, indent=2) + '\n')
    print(f'Prepared {version}')


if __name__ == '__main__':
    main()
