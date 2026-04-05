# Copilot Instructions

<!--
  Deploy to: .github/copilot-instructions.md
  Stack: Python / FastAPI
-->

## Project

[One sentence describing what this API does.]

## Stack

- Language: Python 3.12+
- Framework: FastAPI
- Data validation: Pydantic v2
- Database: [SQLAlchemy / SQLModel / asyncpg]
- Test: pytest, httpx (async test client)
- Package manager: [uv / pip + requirements.txt]

## Conventions

- Use `APIRouter` per feature domain. Register routers in `main.py` with a prefix and tags.
- Pydantic models for all request bodies and responses. Never use raw `dict`.
- Dependency injection via `Depends()` for auth, DB sessions, and shared services.
- Use `async def` for all route handlers and any I/O-bound operations.
- HTTP exceptions via `HTTPException(status_code=..., detail=...)`. No bare `raise Exception`.
- Separate concerns: `schemas.py` for Pydantic models, `services.py` for business logic, `repositories.py` for DB queries.
- `snake_case` for functions and variables. `PascalCase` for classes. `UPPER_SNAKE_CASE` for constants.
- Type hints on all function signatures.
- Environment config via `pydantic-settings` or `python-decouple`. No hardcoded config.

## Testing

- Use `pytest` with `httpx.AsyncClient` for endpoint tests.
- Test files: `test_[module].py` in a `tests/` directory.
- Use `pytest.mark.asyncio` for async tests.
- Mock external services and DB calls — do not hit real external APIs in tests.

## What not to do

- Do not write business logic in route handlers — use service functions.
- Do not use synchronous blocking calls (`requests`, `time.sleep`) inside `async def` — use `httpx.AsyncClient` and `asyncio.sleep`.
- Do not use `except Exception` — catch specific exceptions.
- Do not return raw `dict` from endpoints — always use a Pydantic response model.
- Do not use `pathlib` alternatives — `pathlib.Path` over `os.path`.
