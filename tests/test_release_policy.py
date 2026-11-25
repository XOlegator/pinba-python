import importlib.util
from pathlib import Path

spec = importlib.util.spec_from_file_location(
    "release_policy", Path(__file__).parents[1] / "scripts" / "prepare_release.py"
)
assert spec is not None and spec.loader is not None
policy = importlib.util.module_from_spec(spec)
spec.loader.exec_module(policy)


def test_release_policy_requires_runtime_and_type():
    assert policy.bump_for("feat: new timer", "", ["src/pinba/collector.py"]) == 2
    assert policy.bump_for("fix: docs", "", ["README.md"]) == 0
    assert policy.bump_for("feat(docs)!: docs", "", ["src/pinba/collector.py"]) == 0
    assert policy.bump_for("chore: implementation", "", ["src/pinba/collector.py"]) == 0
    assert policy.bump_for("fix: generated bindings", "", ["src/pinba/pinba_pb2.py"]) == 1
    assert policy.bump_for("perf: speed", "", ["src/pinba/reporter.py"]) == 1
    assert policy.bump_for("fix!: incompatible", "", ["src/pinba/reporter.py"]) == 3
    assert (
        policy.bump_for("fix: incompatible", "BREAKING CHANGE: new API", ["src/pinba/reporter.py"])
        == 3
    )
    assert policy.next_version("0.1.2", 3) == "1.0.0"
