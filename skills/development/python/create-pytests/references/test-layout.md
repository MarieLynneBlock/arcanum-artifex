# Test layout — src vs flat layout and importlib mode

## The two recommended layouts

### Layout A: tests outside application code (preferred for new projects)

```text
pyproject.toml
src/
    mypkg/
        app.py
        models.py
tests/
    test_app.py
    test_models.py
```

Benefits:

- Tests run against the installed package (editable or regular), catching packaging mistakes.
- No `sys.path` manipulation needed under `importlib` mode.
- Clean separation of shipped code and test code.
- Works correctly with `pip install -e ".[dev]"`.

### Layout B: tests inside application code (inline)

```text
pyproject.toml
mypkg/
    app.py
    models.py
    tests/
        test_app.py
        test_models.py
```

Use when tests are a core deliverable shipped with the package (e.g. a library that documents its API through tests). Not recommended for applications or services.

## Import modes compared

| Mode | `sys.path` change | Unique test file names required | Recommendation |
| --- | --- | --- | --- |
| `prepend` (default) | Inserts `testpaths` root at position 0 | Yes | Legacy only |
| `append` | Appends `testpaths` root | Yes | Rarely needed |
| `importlib` | No change | No | Use for all new projects |

Always use `importlib` for new projects:

```toml
[tool.pytest.ini_options]
addopts = ["--import-mode=importlib"]
```

## No init file in tests/

Under `importlib` mode, the `tests/` directory does not need an `__init__.py` file. Adding one:

- Creates a `tests` package that can conflict with other installed packages.
- Causes conftest.py scope confusion when the package is nested under another.
- Adds deployment surface for a directory that should never ship.

If test files share a name across subdirectories (e.g. `tests/foo/test_view.py` and `tests/bar/test_view.py`), `importlib` mode handles this correctly without any init file.

## conftest.py placement

| Location | Fixture scope |
| --- | --- |
| `tests/conftest.py` | Available to all tests in `tests/` |
| `tests/foo/conftest.py` | Available only to tests in `tests/foo/` |
| `conftest.py` (project root) | Available everywhere, including plugins loaded at collection time |

Put project-wide fixtures (e.g. database session, app factory) in `tests/conftest.py`. Put subsystem-specific fixtures in the relevant subdirectory conftest.

## Non-src flat layout

If the package lives directly at the project root (no `src/` wrapper):

```text
pyproject.toml
mypkg/
    app.py
    models.py
tests/
    test_app.py
```

Under `importlib` mode, pytest discovers modules without adding anything to `sys.path`, so `pip install -e .` is still required for the package to be importable. Alternatively, set `pythonpath`:

```toml
[tool.pytest.ini_options]
pythonpath = ["."]
```

The `src/` layout is still preferred because it prevents accidentally importing an un-installed version of the package from the working directory.
