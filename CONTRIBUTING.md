# Contributing

Use Python 3.15 or newer. Install the package with `python -m pip install -e '.[test,dev]'`, enable hooks with `pre-commit install`, and run `pre-commit run --all-files` and `python -m pytest`. Hooks may format files automatically; review changes and run them again. The generated `pinba_pb2.py` is excluded from formatting and linting and verified against the schema in CI. Please include tests for behavioral changes and describe the motivation and validation in pull requests.

The Pinba wire schema must remain compatible with Pinba Engine and the PHP extension. When changing it, regenerate the Python bindings and verify field numbers and types against both projects.
