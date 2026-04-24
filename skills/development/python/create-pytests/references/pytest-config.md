# pytest configuration — [tool.pytest.ini_options] and strict mode

## Where config lives

Prefer `pyproject.toml` as the single source of truth:

```toml
[tool.pytest.ini_options]
# options here
```

Alternatives (legacy, avoid for new projects):

- `pytest.ini` — pytest-only file, highest priority, but separate from packaging config
- `setup.cfg` — deprecated by setuptools; avoid
- `tox.ini` — acceptable when tox is already the test runner

## Core options

| Option | Type | What it does |
| --- | --- | --- |
| `addopts` | list | Extra CLI flags always passed to pytest |
| `testpaths` | list | Directories to search for tests |
| `pythonpath` | list | Paths added to `sys.path` (for non-src layouts without editable install) |
| `markers` | list | Custom marker declarations (prevents `PytestUnknownMarkWarning`) |
| `filterwarnings` | list | Warning filters (e.g. `"error"` to fail on any warning) |
| `minversion` | str | Minimum pytest version required |

## importlib mode

Add to `addopts` for all new projects:

```toml
addopts = ["--import-mode=importlib"]
```

This mode does not modify `sys.path` during test collection. It is the recommended mode for new projects and will become the default in a future major version.

## Markers

Declare all custom markers to prevent warnings:

```toml
markers = [
  "integration: tests that require live external services",
  "slow: marks tests as slow (deselect with '-m not slow')",
  "smoke: fast sanity checks for CI gate",
]
```

## Strict mode (pytest 9.0+)

Enable all strictness options at once:

```toml
strict = true
```

Or enable individually (safer if pinning to an older pytest):

```toml
strict_config = true       # error on unrecognised config keys
strict_markers = true      # error on undeclared markers
xfail_strict = true        # xfail tests that unexpectedly pass become failures
```

If strict mode conflicts with a specific option, disable it selectively:

```toml
strict = true
strict_parametrize_ids = false
```

Only enable `strict = true` with a pinned or locked version of pytest, or accept that new strictness options added in future releases will take effect automatically.

## Warnings as errors

```toml
filterwarnings = ["error"]
```

To allow specific known deprecation warnings from third-party libraries:

```toml
filterwarnings = [
  "error",
  "ignore::DeprecationWarning:some_third_party_library",
]
```

## Complete annotated reference block

```toml
[tool.pytest.ini_options]
addopts = [
  "--import-mode=importlib",    # clean import mode — no sys.path changes
  "-ra",                        # show short summary for all non-passing tests
  "--strict-markers",           # error on undeclared markers
  "--strict-config",            # error on unrecognised config keys
]
testpaths = ["tests"]
minversion = "8.0"
markers = [
  "integration: tests that require live external services (deselect with '-m not integration')",
  "slow: tests that take more than 1 second to run",
]
filterwarnings = ["error"]
xfail_strict = true
```
