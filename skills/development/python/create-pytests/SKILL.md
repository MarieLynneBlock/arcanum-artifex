---
name: create-pytests
description: >
  Generate pytest test files targeting 80% line coverage for a Python codebase or
  a specific file, module, or function — with a pyproject.toml setup using hatchling
  and importlib import mode, and a Coverage Gap Report explaining what was skipped
  and why. Use when a user asks to write tests, generate test coverage, or add pytest
  to a Python project.
version: 1.0.0
authors:
  - Marie-Lynne Block
tags:
  - testing
  - pytest
  - python
  - coverage
  - pyproject
---

## What this skill does

Generates pytest test files for a Python codebase (or a targeted scope) that:

- Target 80% line coverage as a floor, prioritising public API surface, business logic, and error branches.
- Follow pytest naming conventions (`test_*.py` files, `test_` prefix functions and methods, `Test` prefix classes).
- Use real implementations rather than mocked stubs wherever the real code is importable within the same process.
- Mark tests that require live external services with `@pytest.mark.integration`.
- Create or update `pyproject.toml` with the `[tool.pytest.ini_options]` block using `--import-mode=importlib`.
- Detect project layout (`src/` vs flat) and configure accordingly.
- Output a **Coverage Gap Report** after the tests listing what is covered, what is skipped, and why each skip is justified.

## When to use it

- User asks to "write tests", "generate pytest tests", "add test coverage", or "test this module/function".
- A new Python project has no `tests/` directory and no `pyproject.toml` pytest configuration.
- A user wants to understand what is and is not covered after a test generation pass.
- User says "get me to 80% coverage" or "what's not tested?".

Do NOT use this skill for:

- Test strategy design — use the `test-strategy` skill instead.
- Acceptance or UAT test cases derived from user stories.
- TypeScript, JavaScript, or other non-Python projects.

## Key concepts

### Layout detection

| Layout | Indicator | testpaths | Import mode |
| --- | --- | --- | --- |
| `src/` layout | `src/` directory at root | `["tests"]` | `importlib` |
| Flat layout | Package at root, no `src/` | `["tests"]` | `importlib` |
| Inline tests | No `tests/` dir — tests live next to source | auto-discovery | `importlib` |

Always prefer tests outside application code (`tests/` at root). Do not create an init file in `tests/` — it is not needed under `importlib` mode and causes import confusion.

### Coverage target priority

Test in this order when 80% coverage is the target:

1. All public functions and methods — always cover these.
2. All error branches and exception paths — at least one failure case per public function.
3. Boundary values and edge cases — parametrize with zero, negative, empty, and type-mismatch inputs.
4. Private helpers (`_name`) — test indirectly through their public callers; mark skipped in the gap report.
5. CLI entrypoints (`if __name__ == "__main__":`) — note as manual test candidates; apply `# pragma: no cover`.
6. Tests requiring live databases or network — mark with `@pytest.mark.integration`; exclude from the 80% threshold.

### What not to generate

- `setup.py test` or any `pytest-runner` invocation — deprecated and removed.
- Tests that `mock.patch` a real, in-process implementation — use the real class.
- Assertion-free tests that always pass regardless of the implementation.
- An init file inside `tests/`.

## Instructions

### Step 1 — Determine scope

Read the user's request:

- **No scope given** — whole codebase. Walk the source tree and identify all Python modules.
- **File given** — test that file only; still produce a gap report for it.
- **Module given** — test the whole module.
- **Function given** — write focused tests for that function; note what is out of scope.

For a large codebase, list the files to be created and ask for confirmation before generating.

### Step 2 — Detect layout

Check for the presence of:

1. A `src/` directory at the project root → `src/` layout.
2. A package directory at root (contains an init file) → flat layout.
3. An existing `tests/` directory → confirm placement; use it.
4. An existing `pyproject.toml` → read `[tool.pytest.ini_options]` before updating.

### Step 3 — Generate or update `pyproject.toml`

If `pyproject.toml` does not exist, create it. If it exists but has no `[tool.pytest.ini_options]` section, add only that section. Never overwrite an existing `[project]` block.

Required minimum:

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "PACKAGENAME"
version = "PACKAGEVERSION"

[tool.pytest.ini_options]
addopts = ["--import-mode=importlib"]
testpaths = ["tests"]
markers = [
  "integration: tests that require live external services (deselect with '-m not integration')",
]
```

Replace `PACKAGENAME` with the detected package name and `PACKAGEVERSION` with `"0.1.0"` if none exists.

### Step 4 — Generate test files

For each module in scope:

1. Read the source file to identify all public classes, methods, and functions.
2. Write a `tests/test_<module>.py` file.
3. Cover the happy path for every public function.
4. Cover at least one error path or edge case per function.
5. Mark tests that call live external services with `@pytest.mark.integration`.
6. For private functions (`_name`), do NOT write direct tests — test them indirectly through their callers.
7. Use `@pytest.mark.parametrize` when multiple inputs test the same logic.
8. Use `pytest.raises(ExceptionType, match="pattern")` for all exception cases — never omit `match=`.

Enforce these naming rules:

- Files: `test_<module>.py` (preferred) or `<module>_test.py`
- Functions: `test_<what_it_tests>`
- Classes: `TestClassName` (PascalCase, `Test` prefix, no init method)
- No init file in `tests/`

### Step 5 — Output the Coverage Gap Report

After the test files, always output a `## Coverage Gap Report` section:

```markdown
## Coverage Gap Report

### Covered

| Module | Items tested | Test file |
| --- | --- | --- |
| `src/mypkg/app.py` | `create_app`, all routes, 404 handler | `tests/test_app.py` |
| `src/mypkg/models.py` | `Item` init, `to_dict`, `from_dict` (valid + invalid), `save` | `tests/test_models.py` |

### Skipped

| Module | Item | Reason |
| --- | --- | --- |
| `src/mypkg/app.py` | `_configure_logging()` | Private helper — exercised indirectly via every `create_app()` call |
| `src/mypkg/app.py` | `if __name__ == "__main__":` | CLI entrypoint — `# pragma: no cover` applied |

### Estimated coverage

| Module | Estimated line coverage | At 80% target? |
| --- | --- | --- |
| `app.py` | ~87% | Yes |
| `models.py` | ~93% | Yes |
```

## Output format

For each run the skill produces:

1. **`pyproject.toml`** — created or updated with `[tool.pytest.ini_options]`.
2. **Test files** — one per module (or one per targeted scope), with full pytest-compliant content.
3. **Coverage Gap Report** — inline in the response, in the format above.

When generating for a whole codebase, list all files to be created before generating them.

## Examples

### Example 1 — Whole codebase, no prior tests

**Input:** "Write pytest tests for my Flask API project."

Steps the skill takes:

- Detects `src/flaskapi/` layout.
- Creates `pyproject.toml` with hatchling backend and `--import-mode=importlib`.
- Creates `tests/test_app.py` covering all public routes (happy path, 404, validation errors).
- Creates `tests/test_models.py` covering all `Item` methods including `save`.
- Marks any tests calling real external services with `@pytest.mark.integration`.
- Outputs a Coverage Gap Report noting `_configure_logging` skipped as a private helper.

### Example 2 — Scoped to a single function

**Input:** "Write tests for the `parse_date` function in `utils.py`."

Steps the skill takes:

- Writes `tests/test_utils.py` covering: valid ISO date string, invalid format raises `ValueError`, empty string raises `ValueError`, timezone-aware input, leap year boundary.
- Coverage Gap Report notes all other functions in `utils.py` are out of scope.

### Example 3 — Existing `pyproject.toml`, missing pytest config

**Input:** "Add pytest config — I already have a `pyproject.toml`."

Steps the skill takes:

- Reads existing `pyproject.toml`.
- Merges only the `[tool.pytest.ini_options]` block with `addopts = ["--import-mode=importlib"]`.
- Does not overwrite `[project]`, `[build-system]`, or any other existing section.
- Confirms the merged result.

## Notes

- Always use `--import-mode=importlib`. It avoids `sys.path` manipulation and will become the default in a future pytest major version. See `references/test-layout.md`.
- No init file in `tests/`. Under `importlib` mode it is not needed, and adding one causes import confusion.
- When the real implementation is available and in-process, do not mock it. Mocking real classes tests the mock, not the system.
- `@pytest.mark.integration` tests go in the same test files as unit tests but are excluded from the default run with `-m "not integration"`. Declare the marker in `[tool.pytest.ini_options]`.
- This skill pairs with `test-strategy` (define what to test before generating) and `code-review` (review generated tests for correctness and quality).
- Reference files: `references/project-setup.md`, `references/test-layout.md`, `references/pytest-config.md`, `references/discovery-conventions.md`, `references/coverage-and-quality.md`.
