# Project setup — pyproject.toml, venv, and editable install

## Why hatchling

hatchling is a lightweight, PEP 517/518 compliant build backend maintained by the PyPA. It:

- Requires no `setup.py` or `setup.cfg`
- Supports automatic version detection from VCS tags or a static string
- Produces valid wheel and sdist distributions
- Is the default backend recommended by the official Python packaging tutorial

Alternatives: `setuptools` (legacy), `flit` (simpler but less flexible), `pdm-backend` (PDM-specific).

## Minimal pyproject.toml

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "PACKAGENAME"
version = "PACKAGEVERSION"

[tool.pytest.ini_options]
addopts = ["--import-mode=importlib"]
```

Replace `PACKAGENAME` with your package name and `PACKAGEVERSION` with the version string (e.g. `"0.1.0"`).

## Creating the virtual environment

```sh
python -m venv .venv
source .venv/bin/activate        # macOS / Linux
.venv\Scripts\activate.bat       # Windows
```

Use `.venv` (with the dot) so it is hidden from directory listings and consistently ignored by most `.gitignore` templates.

## Editable install

```sh
pip install -e .
```

An editable install makes the package importable from any Python process in the virtualenv without re-installing after code changes. Under `importlib` import mode, this is the standard way to make your package available to pytest without manipulating `sys.path`.

To include dev dependencies:

```sh
pip install -e ".[dev]"
```

where `[dev]` is defined in `[project.optional-dependencies]`:

```toml
[project.optional-dependencies]
dev = ["pytest>=8.0", "pytest-cov", "flake8-pytest-style"]
```

## Running tests

```sh
pytest                        # run all tests
pytest -v                     # verbose output
pytest --cov=src/             # with line coverage report
pytest -m "not integration"   # skip integration tests
```

## What not to do

- **`setup.py test`** — deprecated since Python 3.12 and removed in setuptools 67+. Use `pytest` directly.
- **`pytest-runner`** — a setuptools plugin that runs pytest via `python setup.py test`. It relies on deprecated setuptools hooks and bypasses `pip --require-hashes` security checks. Do not add it to any new project.
- **`python setup.py develop`** — the legacy editable install mechanism. Use `pip install -e .` instead.
- **`setuptools` as the build backend without a compelling reason** — hatchling is simpler and has fewer sharp edges for new projects.
