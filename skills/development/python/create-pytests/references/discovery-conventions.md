# Pytest discovery rules and naming conventions

## How pytest finds tests

1. Start from `testpaths` (or the current directory if not set).
2. Recurse into subdirectories unless they match `norecursedirs` (default: `.git`, `.venv`, `node_modules`, `dist`, `build`).
3. In each directory, collect files matching `python_files` (default: `test_*.py` and `*_test.py`).
4. From those files, collect:
   - Functions matching `python_functions` (default: `test_*`) at module scope.
   - Methods matching `python_functions` inside classes matching `python_classes` (default: `Test*`), excluding classes that have an `__init__` method.

## File naming

| Pattern | Collected? | Convention |
| --- | --- | --- |
| `test_models.py` | Yes | preferred |
| `models_test.py` | Yes | acceptable |
| `models.py` | No | source code |
| `test_models.spec.py` | No | wrong extension style |

Use `test_<module>.py` as the default. Reserve `<module>_test.py` for codebases that already use it consistently.

## Function and class naming

```python
# Collected
def test_create_item(): ...

class TestItem:
    def test_to_dict(self): ...
    def test_from_dict(self): ...

# Not collected
def create_item_test(): ...   # no test_ prefix

class ItemTests:              # no Test prefix
    ...

class TestItem:
    def __init__(self): ...   # has __init__ — pytest skips this class
    def test_to_dict(self): ...
```

## Customising patterns

Change patterns in `[tool.pytest.ini_options]` only when migrating a legacy suite:

```toml
python_files = ["test_*.py", "check_*.py"]
python_functions = ["test_*", "check_*"]
python_classes = ["Test*", "Check*"]
```

Changing these is rarely the right answer for new projects.

## Deselecting tests

By keyword expression:

```sh
pytest -k "item and not slow"        # matches test names containing "item" but not "slow"
pytest -k "TestItem or TestModel"    # matches by class name
pytest -k "not integration"          # exclude by name substring
```

By marker expression:

```sh
pytest -m "not integration"          # skip all integration-marked tests
pytest -m "smoke or not slow"        # combine markers
```

By path:

```sh
pytest tests/test_models.py                               # single file
pytest tests/test_models.py::TestItem::test_to_dict      # single test
```

## conftest.py discovery

pytest walks up the directory tree from the test file to the rootdir, loading `conftest.py` files at each level. Fixtures in a conftest are available to all tests in the same directory and below.

```text
tests/
    conftest.py         fixtures available to all tests
    models/
        conftest.py     fixtures available only to tests/models/ tests
        test_item.py
    api/
        conftest.py     fixtures available only to tests/api/ tests
        test_routes.py
```

## Common collection errors

### ImportError during collection

Usually caused by a missing editable install. Fix:

```sh
pip install -e .
```

Or verify the package is on the path by running `python -c "import mypkg"` inside the virtualenv.

### Duplicate module names in prepend mode

Two test files with the same name in different directories will conflict under `prepend` mode. Fix: switch to `importlib` mode — no init file required, duplicate names work correctly.

### PytestUnknownMarkWarning

A marker is used in a test but not declared. Fix: add it to the `markers` list in `pyproject.toml` and enable `--strict-markers`.

### Tests not collected at all

Run `pytest --collect-only` to see what pytest finds without running anything. Common causes:

- File does not match `python_files` pattern.
- Function does not match `python_functions` pattern.
- Class has an `__init__` method.
- `testpaths` is set but points to the wrong directory.
