---
name: dashboard-beautify
description: >-
  Design and build production-grade dashboards and infographics with Dash and Plotly Python:
  layout strategy, colour semantics, accessibility, and pre-ship validation. Use when creating
  or beautifying a dashboard, KPI panel, or data infographic.
metadata:
  skill-author: 'Marie-Lynne Block'
  version: 0.0.4
---

# Data Atelier

Production-grade dashboards and infographics with Dash and Plotly Python.

**Philosophy**: form follows function, colour communicates, every design decision earns its place.
A dashboard is a curated argument made from data — not a chart dump.

**Default target**: production delivery. Optimise for correctness, maintainability, and accessibility
from the start — not as an afterthought.

---

## Before writing any code — establish the brief

1. **What is the primary question this dashboard answers?** The answer must be visible in < 3 seconds.
2. **Who is the audience?** Executive / analyst / operational — determines density, annotation level, interactivity depth.
3. **Single infographic or multi-panel dashboard?** Different layout and scope strategies apply.
4. **What is the data shape?** Time series / categories / relationships / distributions / compositions.
5. **What is the data source and refresh cadence?** Determines caching strategy and performance approach.

If any of these are unanswered, ask before writing code.

---

## Step 1 — Data quality gate

Run this before any design work. A beautiful dashboard built on bad data is worse than no dashboard.

Read `references/data-quality.md` for full checks. Minimum required:

- **Missingness**: identify null rates per column — flag anything > 5% to the user before proceeding
- **Duplicates**: check for duplicate rows on the natural key; deduplicate or explain why not
- **Outliers**: surface extreme values — confirm they are real, not ingestion errors
- **Unit consistency**: confirm all numeric columns use consistent units (£ vs $, thousands vs millions)
- **Metric definitions**: confirm calculated fields (rates, ratios, aggregations) match the agreed definition
- **Timezone normalisation**: all timestamps must be in a single consistent timezone before display

---

## Step 2 — Choose the right chart

| Data intent | Recommended | Never |
|---|---|---|
| Change over time | Line, area, connected scatter | Bar (unless discrete periods only) |
| Compare categories | Horizontal bar (many labels), column (few) | Line (implies continuity between categories) |
| Part of a whole | Stacked bar, treemap, sunburst | Pie with > 4 slices |
| Distribution | Histogram, violin, box plot | Bar chart of means (hides spread) |
| Correlation / relationship | Scatter, bubble (3rd variable as size) | Line |
| Flow / transfer | Sankey | — |
| Multi-variable dense | Heatmap, parallel coordinates | Radar/spider (angle distorts magnitude) |
| Single KPI | Styled `html.Div` card — no chart | Any chart type |
| Multiple series, different scales | Small multiples (facets) | Dual-axis (almost always misleading) |

**Hard anti-patterns — flag to user unless explicitly overridden:**
- 3D charts (perspective distortion destroys accuracy)
- Rainbow / Jet colormaps on continuous data (use Viridis, Cividis, Magma)
- Pie charts with > 4 slices
- Dual-axis charts

Read `references/chart-selection.md` for edge cases and the full decision framework.

---

## Step 3 — Colour strategy

Read `references/colour-theory.md` for the full palette library and per-theme Plotly template code.

This skill is **theme-agnostic**. Select the appropriate theme for the project and apply it consistently — do not mix themes within a project. Available themes documented in the reference:

- **Nord** — soft, cool-toned, professional; well-suited to extended use and healthcare/public sector
- **Okabe-Ito** — colourblind-safe, vivid; good default when no brand constraint applies
- **Muted Professional** — desaturated enterprise palette; suits financial and government contexts

**Colour rules — apply regardless of theme:**
1. Maximum 6–7 distinct colours per chart — beyond that, use grouping or small multiples.
2. Signal colours (red = bad, green = good, amber = warning) are reserved for status encoding only.
3. Colour is **never the only encoding** for critical distinctions — always pair with shape, dash, or pattern. See `references/colourblindness.md`.
4. Sequential palettes for ordered/continuous data; diverging palettes for data with a meaningful midpoint.
5. Never hard-code hex values inline — import from a central `colours.py` module.

---

## Step 4 — Layout and composition

Read `references/layout-principles.md` for grid recipes and typography scale.

- Use `dbc.Container` / `dbc.Row` / `dbc.Col` from `dash-bootstrap-components` for all grid work.
- **F-pattern reading order**: most important content top-left. KPI cards → primary chart → supporting charts.
- Wrap every chart in `dbc.Card` with consistent internal padding (`p-3`).
- Consistent chart heights within a row — mixed heights break visual rhythm.
- White space is structural, not waste.
- Infographic titles state the insight, not the chart type: `"Revenue grew 34% after the Q2 pricing change"` not `"Revenue over time"`.

---

## Step 5 — Plotly template

Register a named template once in `app.py` before the layout import. Every figure inherits it automatically.

Fill palette values from `colours.py` for the selected theme. Full per-theme template code is in `references/colour-theory.md`.

```python
import plotly.graph_objects as go
import plotly.io as pio
from colours import PALETTE, SURFACE, TEXT_PRIMARY, TEXT_MUTED, GRID, HOVER_BG, HOVER_BORDER

pio.templates["project_theme"] = go.layout.Template(
    layout=go.Layout(
        font=dict(family="Inter, system-ui, sans-serif", size=13, color=TEXT_PRIMARY),
        paper_bgcolor="rgba(0,0,0,0)",   # transparent — card handles background
        plot_bgcolor=SURFACE,
        colorway=PALETTE,
        margin=dict(l=40, r=20, t=55, b=40),
        title=dict(
            font=dict(size=16),          # use html.B() in title string for bold — weight is not a valid Plotly font property
            x=0.0,
            xanchor="left",
        ),
        xaxis=dict(gridcolor=GRID, linecolor=GRID,
                   tickfont=dict(size=11, color=TEXT_MUTED), zeroline=False),
        yaxis=dict(gridcolor=GRID, linecolor=GRID,
                   tickfont=dict(size=11, color=TEXT_MUTED), zeroline=False),
        legend=dict(orientation="h", y=1.02, x=0,
                    bgcolor="rgba(0,0,0,0)", borderwidth=0),
        hoverlabel=dict(bgcolor=HOVER_BG, bordercolor=HOVER_BORDER,
                        font=dict(size=12, color=TEXT_PRIMARY)),
    )
)

pio.templates.default = "project_theme"
```

Chart functions live in `components/charts.py` and are **pure**: DataFrame in, `go.Figure` out — no side effects, no globals, no Dash logic inside figure functions.

---

## Step 6 — Project structure

```
project/
├── app.py              # Dash init, template registration, server export
├── layout.py           # Full app layout
├── callbacks.py        # All @callback functions
├── colours.py          # Single source of truth for all colour constants
├── components/
│   ├── charts.py       # Pure figure-building functions
│   └── cards.py        # KPI cards and reusable UI components
├── data/
│   └── loader.py       # Data loading, preprocessing, caching
└── assets/
    └── custom.css      # Minimal overrides only
```

---

## Step 7 — Performance

Read `references/performance.md` before building against real data at scale. Minimum requirements:

- Server-side aggregation — never send row-level data to the browser when aggregated data suffices
- Cache expensive loader functions (Flask-Caching or `functools.lru_cache`)
- WebGL traces (`go.Scattergl`, `go.Heatmapgl`) for > 10k data points
- `dcc.Loading` wrapper on every chart that involves a data fetch callback
- Empty-state handling in every callback — never return a blank figure without a user-facing message

---

## Step 8 — Interaction design

Read `references/interaction-design.md` for full rules. Core principles:

- The **default view** must answer the primary question with zero interaction.
- Filters go **above** the charts they affect — never below.
- Maximum **3 filter controls** on a single view before reconsidering the dashboard scope.
- Use **drill-down** when detail replaces the summary; **cross-filter** when users compare sub-populations.
- `dcc.Store` for shared state — never global Python variables in callbacks.
- One callback per logical interaction; return `dash.no_update` for unchanged outputs.

---

## Step 9 — Formatting and localisation

Read `references/formatting.md` for full conventions. Non-negotiable defaults:

- Dates: `DD Mon YYYY` (e.g. `15 Jan 2024`) — never ambiguous `MM/DD/YY`
- Timestamps: single named timezone throughout; label it in the axis title or chart subtitle
- Currency: symbol prefix, thousands separator, 2dp for transactions, 0–1dp for aggregated totals (`£4.2M`)
- Percentages: 1 decimal place (`68.3%`)
- Large numbers: abbreviate at 1K / 1M / 1B thresholds — define the breakpoints in `formatting.py`

---

## Step 10 — Pre-ship checklist

All boxes must be checked before release.

**Data correctness**
```
□ Key metrics reconciled against source of truth
□ Filters tested for empty results — empty state handled gracefully
□ Date range edge cases tested (first day, last day, single day)
□ Aggregations spot-checked against raw data for a known sample
```

**Visual and UX**
```
□ Primary question answered in < 3 seconds on default view
□ Chart titles state the insight, not the chart type
□ Axis labels include units where not obvious from context
□ hovertemplate set on all traces (value + label + unit)
□ Consistent chart heights within each row
□ Filters positioned above the charts they affect
□ Empty-state message shown when a filter returns no data
□ Layout checked at 375px mobile viewport width
```

**Accessibility**
```
□ Colour is not the only encoding for any critical distinction
□ Red/green signal pairs have redundant encoding (shape / dash / pattern)
□ WCAG AA contrast met for all text (4.5:1 normal, 3:1 large/bold)
□ config={"responsive": True} on all dcc.Graph components
□ Tab order is logical — filters before charts, charts in reading order
□ Key chart insights have a visible text summary (not hover-only)
□ Simulated under deuteranopia — no information is lost
```

**Code quality**
```
□ No hex colour literals inline — all colours imported from colours.py
□ All chart functions are pure (DataFrame in, Figure out)
□ No global mutable state in callbacks
□ dcc.Loading on all data-fetch callbacks
□ weight not used in any Plotly font dict
```

---

## Reference files

| File | When to read |
|---|---|
| `references/chart-selection.md` | Choosing chart type, edge cases, anti-patterns |
| `references/colour-theory.md` | Theme selection, full palette library, per-theme template code |
| `references/colourblindness.md` | CVD simulation, redundant encoding, contrast checking, keyboard/screen-reader |
| `references/layout-principles.md` | Grid recipes, typography scale, infographic anatomy |
| `references/data-quality.md` | Pre-design data checks, missingness, outliers, metric definitions |
| `references/performance.md` | Large data, WebGL, caching, callback memoization |
| `references/interaction-design.md` | Filter rules, drill-down vs cross-filter, control count limits |
| `references/formatting.md` | Dates, timezones, currency, number abbreviation conventions |
| `references/observability.md` | Structured logging, callback timing, error handling patterns |
| `references/testing.md` | Figure function tests, callback integration tests, snapshot regression |
| `references/validation.md` | Pre-ship QA checklist, value reconciliation, axis/unit sanity checks |
