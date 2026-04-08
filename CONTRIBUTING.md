# Contributing to pyiiko

Thank you for your interest in contributing!

## Development setup

```bash
git clone https://github.com/gadzhi/pyiiko.git
cd pyiiko
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
```

## Running tests

```bash
pytest                          # all tests
pytest --cov=Pyiiko             # with coverage
pytest tests/test_server.py -v  # single file
```

Tests use `responses` to mock HTTP — no live iiko server required.

## Adding a new API method

1. Add the method to the appropriate class (`IikoServer` or `Transport`).
2. Follow the existing pattern:
   - Use `self._get(path, params=self._key(...))` / `self._post(...)`.
   - Add a Google-style or Sphinx-style docstring with param types.
   - Add a type hint to the signature.
3. Write a unit test in `tests/test_server.py` or `tests/test_transport.py`
   using `@responses.activate`.

## Commit messages

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: add Transport.menu() method
fix: correct currentYear param type in invoice_number_in
docs: update README example for Transport
```

## Pull requests

- Target the `master` branch.
- Ensure all CI checks pass before requesting review.
- One logical change per PR.
