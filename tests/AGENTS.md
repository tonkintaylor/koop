# Testing Guidelines

## Overview

- Use `pytest` for all unit tests.
- Structure tests to mirror the `src/` directory: `src/x/y/z.py` → `tests/x/y/test_z.py`.
- Do not add `__init__.py` files in the `tests/` folder.

## Writing Tests

- Write one test case per function with one assertion, assuming the happy path, unless instructed otherwise.
- Do not test for edge cases unless explicitly requested.
- Use test fixtures when appropriate to set up common test data.
- Use `@pytest.mark.parametrize` for similar tests with different inputs.
- Group related tests into classes when it improves organization.
- Use `pytest.approx` for floating-point comparisons instead of exact equality.
- Use only one assert statement per test function for clarity and simplicity.

## Test Data and Fixtures

- Access test data in the `assets/` folder via `tests/conftest.py`.
- Define shared fixtures in `conftest.py` for reuse across test files.

## Running Tests

- After modifying a function, run its unit tests using pytest.
- Run tests in the virtual environment: `.\.venv\Scripts\activate; python -m pytest tests/path/to/test_file.py -v`
- For all tests: `python -m pytest tests/ -v`

## Best Practices

- Ensure tests are passing before committing changes.
- Keep tests focused and minimal to avoid bloat.
