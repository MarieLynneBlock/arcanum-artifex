# multi-framework-api — pytest example

This example shows the `create-pytests` skill applied to a project with two HTTP API packages in the same `src/` layout: one built with Flask and one with FastAPI. Both expose identical routes so the test structure can be compared side by side.

## Project structure

```text
src/
├── flaskapi/         Flask application factory (create_app)
└── fastapiapp/       FastAPI application factory (create_app)
tests/
├── test_models.py        shared Item model tests (Flask dataclass)
├── test_flask_app.py     Flask route tests via app.test_client()
└── test_fastapi_app.py   FastAPI route tests via starlette TestClient
pyproject.toml
```

> **Why `fastapiapp/` and not `fastapi/`?** A directory named `src/fastapi/` would shadow the installed `fastapi` library under `importlib` import mode, causing `from fastapi import FastAPI` to fail with an `ImportError`. Using `fastapiapp/` as the package name avoids this collision. When deploying to a real project, name the package after your application domain, not after its framework.

## Running the tests

```sh
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest -v
pytest --cov=src/ --cov-report=term-missing
pytest -m "not integration"
```

## What is covered

| Module | Items tested | Test file |
| --- | --- | --- |
| `src/flaskapi/models.py` | `Item` creation via `from_dict` (valid, invalid name, invalid price — parametrized), `to_dict`, `save`, ID auto-increment | `tests/test_models.py` |
| `src/flaskapi/app.py` | `create_app`, `GET /items` (empty, populated), `POST /items` (success, missing name, invalid price, zero price), `GET /items/<id>` (found, 404), `DELETE /items/<id>` (success, deleted confirms 404, 404) | `tests/test_flask_app.py` |
| `src/fastapiapp/app.py` | Same 12 route scenarios via `TestClient`; Pydantic validation returns 422 (not 400) | `tests/test_fastapi_app.py` |

## What is skipped

| Module | Item | Reason |
| --- | --- | --- |
| `src/flaskapi/app.py` | `_configure_logging()` body | Private helper; exercised indirectly via every `create_app()` call; direct test would only assert against Flask's logging configuration, not application logic |
| `src/fastapiapp/app.py` | `lifespan` async context manager body | Startup/teardown path; the `with TestClient(application) as c:` pattern in the `client` fixture exercises the lifespan automatically; no additional test needed |

## Estimated coverage

| Module | Estimated line coverage | At 80% target? |
| --- | --- | --- |
| `src/flaskapi/app.py` | ~87% | Yes |
| `src/fastapiapp/app.py` | ~85% | Yes |
| `src/flaskapi/models.py` | ~93% | Yes |
| `src/fastapiapp/models.py` | ~91% | Yes |

## Key patterns demonstrated

- `src/` layout with two sibling packages — single `tests/` directory at project root
- `pyproject.toml` with hatchling build backend and `--import-mode=importlib`
- Function-scoped `client` fixture for both Flask (`app.test_client()`) and FastAPI (`TestClient(app)`)
- `autouse` fixture (`clear_store`) that resets in-memory state between tests — prevents test order dependence
- `@pytest.mark.parametrize` for testing multiple invalid inputs against the same logic
- `pytest.raises(ValueError, match="pattern")` for all exception cases (PT011 compliance)
- Test class grouping (`class TestCreateItem:`) to mirror the route being tested
- Flask returns 400 for validation errors; FastAPI returns 422 (Pydantic default) — both are tested for the correct status code
