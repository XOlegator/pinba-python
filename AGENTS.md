# Agent Instructions

- Use Python 3.15 or newer. Write code comments, docstrings, documentation, commit messages, and pull request titles and descriptions in English unless the developer explicitly requests another language.
- Install development dependencies with `python -m pip install -e '.[test,dev]'`.
- Before submitting changes, run `pre-commit run --all-files`, `ty check`, and `python -m pytest`. Run `python -m build` when changing packaging or release artifacts.
- Do not edit generated `src/pinba/pinba_pb2.py` or `src/pinba/pinba_pb2.pyi` by hand. When changing the schema, regenerate both as documented in `CONTRIBUTING.md` and verify protocol compatibility.
- Preserve request isolation, bounded best-effort UDP reporting, and compatibility with the Pinba Engine wire protocol. Keep release policy aligned with `RELEASING.md`.
- Use Conventional Commit titles and squash pull requests. Keep local-only files out of commits.
