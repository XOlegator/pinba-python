# Contributing

Use Python 3.15 or newer. Install the package with `python -m pip install -e '.[test,dev]'`, enable hooks with `pre-commit install`, and run `pre-commit run --all-files`, `ty check`, and `python -m pytest`. Hooks may format files automatically; review changes and run them again. The generated `pinba_pb2.py` and `pinba_pb2.pyi` are excluded from formatting, linting and type checking; CI verifies the Python bindings against the schema. Please include tests for behavioral changes and describe the motivation and validation in pull requests.

The Pinba wire schema must remain compatible with Pinba Engine and the PHP extension. When changing it, regenerate the Python bindings and verify field numbers and types against both projects.

After changing `pinba.proto`, regenerate the Python bindings and type stub with `protoc -I src/pinba --python_out=src/pinba --pyi_out=src/pinba src/pinba/pinba.proto`.
