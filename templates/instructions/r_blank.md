# Copilot Instructions

<!--
  Deploy to: .github/copilot-instructions.md
  Stack: R
-->

## Project

[One sentence describing what this project does — analysis, dashboard, API, report, etc.]

## Stack

- Language: R 4.x
- Core packages: tidyverse (dplyr, tidyr, ggplot2, purrr, readr)
- [Shiny — if building dashboards/apps]
- [Plumber — if building REST APIs]
- [R Markdown / Quarto — if producing reports or notebooks]
- Package management: renv
- Test: testthat

## Conventions

- Use `<-` for assignment. Reserve `=` for function arguments only.
- Follow the [tidyverse style guide](https://style.tidyverse.org/): `snake_case` for all names.
- Prefer tidyverse over base R for data manipulation (`dplyr`, `tidyr`, `purrr`).
- Use the pipe operator (`|>` native pipe, R 4.1+) over `%>%` for new code.
- Functions: small, single-purpose, named with a verb (e.g. `calculate_revenue()`, `filter_active_users()`).
- Use `here::here()` for file paths — never hardcode absolute paths or use `setwd()`.
- Load credentials from environment variables via `Sys.getenv()` or `.Renviron` — never hardcode.
- Package dependencies managed with `renv` — commit `renv.lock`, not the `renv/library/` folder.

## Project structure

```text
project/
├── R/                  ← reusable functions (.R files, one topic per file)
├── data/
│   ├── raw/            ← source data, never modified
│   └── processed/      ← cleaned/transformed outputs
├── reports/            ← R Markdown / Quarto documents
├── tests/
│   └── testthat/       ← testthat unit tests
├── renv.lock
└── [project].Rproj
```

## Testing

- Use `testthat` for unit tests on functions in `R/`.
- Test files: `test-[topic].R` in `tests/testthat/`.
- Run with `devtools::test()` or `testthat::test_dir("tests/testthat")`.
- Test pure functions — avoid testing side effects (file I/O, plots) directly.

## What not to do

- Do not use `setwd()` — use `here::here()` for portable paths.
- Do not use `=` for assignment at the top level — use `<-`.
- Do not use `attach()` — it pollutes the global namespace.
- Do not use `T` / `F` as shortcuts for `TRUE` / `FALSE` — they can be overwritten.
- Do not commit `renv/library/` or `.Rhistory` — add to `.gitignore`.
- Do not suppress warnings globally with `suppressWarnings()` — fix the root cause.
