# Copilot Instructions

<!--
  Deploy to: .github/copilot-instructions.md
  Stack: Python / Dash (Plotly)
-->

## Project

[One sentence describing what this dashboard does.]

## Stack

- Language: Python 3.12+
- Framework: Dash (Plotly)
- Styling: [Dash Bootstrap Components / Mantine / plain CSS]
- Data: [pandas / polars]
- Test: pytest, dash[testing] (Selenium-based)
- Package manager: [uv / pip + requirements.txt]

## Conventions

- One app per dashboard. Define layout in a `layout()` function, not at module level.
- Callbacks must be pure: no side effects outside of their return values.
- Use `dcc.Store` for shared client-side state between callbacks — not global variables or module-level state.
- Component IDs: `kebab-case` strings (e.g. `"revenue-chart"`, `"date-picker"`). Be consistent — IDs are the contract between layout and callbacks.
- Long-running data fetches: use `@callback(..., background=True)` or load data from a separate API — never in a layout function or synchronous callback.
- Split large apps: `layouts/` for page layouts, `callbacks/` for callback definitions, `components/` for reusable UI elements.
- `snake_case` for functions and variables. `PascalCase` for classes. `UPPER_SNAKE_CASE` for constants.
- Type hints on all function signatures.

## Data loading

- Load static data at startup in a module-level variable — acceptable for read-only data.
- For dynamic or user-specific data: fetch inside callbacks, not at layout time.
- Use `pandas` or `polars` for tabular data. Do not pass DataFrames through `dcc.Store` — serialise to JSON (`df.to_json()`) first.

## Testing

- Use `dash[testing]` with pytest for integration tests (requires Chrome/Chromium).
- Test callback logic independently as plain Python functions where possible.
- Test files: `test_[module].py` in a `tests/` directory.

## What not to do

- Do not use global mutable variables for state — use `dcc.Store`.
- Do not put data fetching logic inside layout functions — layout must be fast.
- Do not use duplicate component IDs — Dash will raise a runtime error.
- Do not pass large DataFrames through `dcc.Store` unserialized.
- Do not use `except Exception` — catch specific exceptions.
