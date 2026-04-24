# Coverage measurement, quality linting, and tox

## pytest-cov

Install:

```sh
pip install pytest-cov
```

Run with coverage:

```sh
pytest --cov=src/ --cov-report=term-missing
```

`term-missing` shows which lines were not executed. Other report formats:

- `html` — writes an interactive report to `htmlcov/`
- `xml` — for CI upload (Codecov, SonarQube)
- `lcov` — for editors that show inline coverage

## Configuration in pyproject.toml

```toml
[tool.coverage.run]
source = ["src"]
branch = true              # measure branch coverage, not just line coverage

[tool.coverage.report]
fail_under = 80            # fail if total coverage is below 80%
show_missing = true
skip_covered = false

[tool.coverage.html]
directory = "htmlcov"
```

## Line coverage vs branch coverage

| Metric | What it measures | Risk if missing |
| --- | --- | --- |
| Line coverage | Whether a line was executed at all | Misses untested decision branches |
| Branch coverage | Whether each true/false decision was exercised | More complete — use `branch = true` |

Enable branch coverage (`branch = true`) for any code with conditionals. It is the more informative metric.

## The 80% target — what it means

80% is a floor, not a ceiling. Prioritise coverage in this order:

1. All public functions and methods — aim for 100% of these.
2. All error branches and exception paths.
3. Boundary values and edge cases.

The remaining 20% gap typically comes from:

- Private helpers tested indirectly through their public callers.
- CLI entrypoints (`if __name__ == "__main__":`).
- Dead code paths that cannot be exercised in unit tests.
- Integration-only code paths (live database, network calls).

A suite with 80% coverage and confidence in every covered line is better than one with 95% coverage full of assertion-free or mocked tests.

## Excluding from coverage

Use `# pragma: no cover` for lines that should never be counted:

```python
if __name__ == "__main__":  # pragma: no cover
    app.run()
```

Or exclude by pattern in config:

```toml
[tool.coverage.report]
exclude_lines = [
  "pragma: no cover",
  "if TYPE_CHECKING:",
  "@(abc\\.)?abstractmethod",
  "raise NotImplementedError",
]
```

## flake8-pytest-style

Catches common pytest coding mistakes at lint time:

```sh
pip install flake8-pytest-style
flake8 tests/
```

Key rules:

| Rule | What it catches |
| --- | --- |
| PT001 | `@pytest.fixture()` called without parentheses when they are not needed (configurable style choice) |
| PT006 | Wrong type for `@pytest.mark.parametrize` names — should be a string or tuple of strings |
| PT011 | `pytest.raises(Exception)` without `match=` — test passes even if the wrong exception type is raised |
| PT012 | `pytest.raises` block contains more than one statement — extra statements are not checked for exceptions |
| PT023 | Marks applied without `@` prefix or incorrectly without parentheses |

Configure in `pyproject.toml` (requires `flake8` plugin support via `Flake8-pyproject`):

```toml
[tool.flake8]
max-line-length = 120
```

Or in `setup.cfg`:

```ini
[flake8]
max-line-length = 120
```

## tox

tox creates isolated virtualenvs for each Python version and runs the test suite inside them — essential for verifying compatibility before a release.

Minimal `tox.ini`:

```ini
[tox]
envlist = py311, py312, py313

[testenv]
deps = .[dev]
commands = pytest {posargs}
```

Or in `pyproject.toml` using the inline config approach:

```toml
[tool.tox]
legacy_tox_ini = """
[tox]
envlist = py311, py312, py313

[testenv]
deps = .[dev]
commands = pytest {posargs}
"""
```

Run:

```sh
tox              # all environments
tox -e py312     # single environment
```

## CI — minimal GitHub Actions snippet

```yaml
name: Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.11", "3.12", "3.13"]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
      - run: pip install -e ".[dev]"
      - run: pytest --cov=src/ --cov-report=xml -m "not integration"
      - uses: codecov/codecov-action@v4
```
