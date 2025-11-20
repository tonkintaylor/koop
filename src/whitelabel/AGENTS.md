# whitelabel Package Guidelines

## API Communication

- When communicating with APIs, use the `httpx` package unless explicitly instructed otherwise.
- When using HTTP status codes, use constants from the `http` package instead of hardcoding them (e.g., `http.HTTPStatus.OK`).

## Imports

- When importing internal modules, do not include the "src" folder in the import path as it is already defined in `pyproject.toml`.
- Example: `from whitelabel.functions import hello_world` instead of `from src.whitelabel.functions import hello_world`.

## Package API Guidelines

- Every package (mypkg/) must define a clear public API in its `__init__.py`.
- If submodules provide functionality that is likely to be directly consumed, re-export the relevant classes, functions, or constants in `__init__.py`.
- Use `__all__` to explicitly mark what is public.
- Internal utilities should remain private (prefix with `_` and do not re-export).
- This helps consumers of the package avoid deep imports like `mypkg.submodule.foo`.
