# Contributing

Use Python 3.15 or newer. Install the package with `python -m pip install -e '.[test]'` and run `python -m pytest`. Please include tests for behavioral changes and describe the motivation and validation in pull requests.

The Pinba wire schema must remain compatible with Pinba Engine and the PHP extension. When changing it, regenerate the Python bindings and verify field numbers and types against both projects.
