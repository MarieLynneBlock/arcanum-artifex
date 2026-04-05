# Copilot Instructions

<!--
  Deploy to: .github/copilot-instructions.md
  Stack: Python / Jupyter Notebooks
-->

## Project

[One sentence describing the analysis or reporting purpose of this notebook project.]

## Stack

- Language: Python 3.12+
- Environment: Jupyter Notebook / JupyterLab
- Data: [pandas / polars]
- Visualisation: [matplotlib / seaborn / plotly]
- Package manager: [uv / pip + requirements.txt]

## Notebook conventions

- Notebooks are for exploration, analysis, and presentation — not for production logic.
- Production-ready functions are extracted to `.py` modules and imported into notebooks.
- Cell order:
  1. Imports
  2. Configuration and constants
  3. Data loading
  4. Analysis / transformation
  5. Visualisation / output
- Use Markdown cells to explain intent, methodology, and findings before code cells.
- Keep cells small and focused — one logical step per cell.
- Name notebooks descriptively: `[date]-[topic].ipynb` (e.g. `2025-04-revenue-analysis.ipynb`).

## Code quality in notebooks

- Type hints on extracted functions (in `.py` modules). Optional in notebook cells.
- `snake_case` for variables and functions. `PascalCase` for classes. `UPPER_SNAKE_CASE` for constants.
- Use `pathlib.Path` for file paths — not string concatenation.
- Load credentials and config from environment variables or `.env` — never hardcode in notebooks.

## Version control

- Clear all cell outputs before committing: **Kernel → Restart & Clear Output**.
- Do not commit notebooks with outputs containing sensitive data, PII, or large binary content.
- Use `.gitignore` to exclude heavyweight output directories (e.g. `outputs/`, `data/raw/`).
- Consider `nbstripout` as a pre-commit hook to automatically strip outputs.

## What not to do

- Do not write production logic in notebook cells — extract to `.py` modules.
- Do not hardcode file paths — use `pathlib.Path` relative to the project root.
- Do not commit notebooks with sensitive output.
- Do not use `except Exception` — catch specific exceptions.
- Do not load large datasets without a sample/filter for development — keep notebooks fast to re-run.
