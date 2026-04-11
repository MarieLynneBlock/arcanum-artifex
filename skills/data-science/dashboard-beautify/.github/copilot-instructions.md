# Dashboard Beautify — Dash + Plotly Coding Standards

> **Usage**: This file is a reusable skill asset. Copy it to `.github/copilot-instructions.md`
> at the root of a project repo to activate it as repo-wide Copilot workspace instructions.
> As shipped, it lives inside the skill folder and is not auto-enforced.

**Philosophy**: form follows function, colour communicates, every design decision earns its place.
**Default mode**: production-grade delivery — correctness and accessibility first, aesthetics second.

---

## Project structure

```
project/
├── app.py              # Dash init, theme registration, server
├── layout.py           # Full app layout
├── callbacks.py        # All @callback functions
├── colours.py           # register_theme() + palette/colour constants
├── formatting.py       # Date, currency, number formatters
├── components/
│   ├── charts.py       # Pure figure-building functions (DataFrame in, Figure out)
│   └── cards.py        # KPI cards and reusable UI components
├── data/
│   └── loader.py       # Data loading, preprocessing, caching
└── assets/
    └── custom.css      # Minimal overrides only
```

---

## Theme system — `colours.py`

The project is theme-agnostic. `register_theme()` accepts any palette and surface colours.
Call it once in `app.py` before importing layout, then set `pio.templates.default`.

```python
# colours.py
import plotly.graph_objects as go
import plotly.io as pio

def register_theme(palette: list[str], theme_name: str = "atelier",
                   bg_plot: str = "#ECEFF4", bg_paper: str = "rgba(0,0,0,0)",
                   text_colour: str = "#2E3440", grid_colour: str = "#D8DEE9",
                   muted_colour: str = "#4C566A") -> None:
    """Register a named Plotly template. Call once at app startup."""
    pio.templates[theme_name] = go.layout.Template(
        layout=go.Layout(
            font=dict(family="Inter, system-ui, sans-serif", size=13, color=text_colour),
            paper_bgcolor=bg_paper,
            plot_bgcolor=bg_plot,
            colorway=palette,
            margin=dict(l=40, r=20, t=55, b=40),
            title=dict(
                # Bold via <b> tags in title string — font dict has no 'weight' property
                font=dict(size=16, color=text_colour),
                x=0.0, xanchor="left",
            ),
            xaxis=dict(gridcolor=grid_colour, linecolor=grid_colour,
                       tickfont=dict(size=11, color=muted_colour), zeroline=False),
            yaxis=dict(gridcolor=grid_colour, linecolor=grid_colour,
                       tickfont=dict(size=11, color=muted_colour), zeroline=False),
            legend=dict(orientation="h", y=1.02, x=0,
                        bgcolor="rgba(0,0,0,0)", borderwidth=0),
            hoverlabel=dict(bgcolor=bg_plot, bordercolor=grid_colour,
                            font=dict(size=12, color=text_colour)),
        )
    )
```

### Nord light (default)
```python
NORD_CATEGORICAL = ["#88C0D0","#A3BE8C","#81A1C1","#EBCB8B","#B48EAD","#BF616A","#8FBCBB"]

NORD_SIGNAL = {
    "good":    "#A3BE8C",   # ⚠️ CVD: never sole pairing with bad — add redundant encoding
    "warning": "#EBCB8B",   # ⚠️ low contrast as text on light bg — use fills only
    "caution": "#D08770",
    "bad":     "#BF616A",   # ⚠️ CVD: never sole pairing with good
    "neutral": "#4C566A",
}

NORD_LIGHT_CONFIG = dict(
    palette=NORD_CATEGORICAL, theme_name="nord_light",
    bg_plot="#ECEFF4", text_colour="#2E3440",
    grid_colour="#D8DEE9", muted_colour="#4C566A",
)

NORD_DARK_CONFIG = dict(
    palette=NORD_CATEGORICAL, theme_name="nord_dark",
    bg_plot="#3B4252", text_colour="#ECEFF4",
    grid_colour="#434C5E", muted_colour="#D8DEE9",
)
```

### App initialisation — `app.py`
```python
import dash
import dash_bootstrap_components as dbc
import plotly.io as pio
from colours import register_theme, NORD_LIGHT_CONFIG
import callbacks  # noqa: F401

register_theme(**NORD_LIGHT_CONFIG)
pio.templates.default = "nord_light"

from layout import layout  # import after theme is registered

app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.FLATLY],
    suppress_callback_exceptions=True,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)
server = app.server
app.layout = layout

if __name__ == "__main__":
    app.run(debug=True)
```

---

## Chart functions — `components/charts.py`

Every function must be **pure**: DataFrame in, `go.Figure` out. No side effects, no globals.

```python
from colours import NORD_SIGNAL, TEXT_MUTED  # or your theme's equivalents
import pandas as pd
import plotly.graph_objects as go

def make_trend_chart(df: pd.DataFrame, metric: str, title: str) -> go.Figure:
    if df.empty:
        return _empty_chart(title)
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["date"], y=df[metric],
        mode="lines",
        line=dict(width=2.5),           # colour from theme colorway — don't specify inline
        hovertemplate="<b>%{x|%d %b %Y}</b><br>Value: %{y:,.1f}<extra></extra>",
    ))
    fig.update_layout(title=f"<b>{title}</b>")
    return fig

def _empty_chart(title: str) -> go.Figure:
    """Standard empty state — always handle missing data explicitly."""
    fig = go.Figure()
    fig.update_layout(
        title=f"<b>{title}</b>",
        annotations=[dict(
            text="No data for this selection.",
            xref="paper", yref="paper", x=0.5, y=0.5,
            showarrow=False, font=dict(size=14, color=TEXT_MUTED),  # from colours.py
        )],
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
    )
    return fig

def make_status_bars(df: pd.DataFrame, category_col: str,
                     value_col: str, target: float, title: str) -> go.Figure:
    if df.empty:
        return _empty_chart(title)
    colours = [NORD_SIGNAL["good"] if v >= target else NORD_SIGNAL["bad"]
               for v in df[value_col]]
    fig = go.Figure(go.Bar(
        x=df[category_col], y=df[value_col],
        marker_color=colours,
        # Redundant encoding: text label so status is not colour-only
        text=[f"{'✓' if v >= target else '✗'} {v:.1f}" for v in df[value_col]],
        textposition="outside",
        hovertemplate="<b>%{x}</b><br>%{y:.1f} (target: " + str(target) + ")<extra></extra>",
    ))
    fig.add_hline(y=target, line_dash="dash", line_color=NORD_SIGNAL["neutral"],
                  annotation_text=f"Target: {target}", annotation_position="top right")
    fig.update_layout(title=f"<b>{title}</b>")
    return fig
```

---

## KPI cards — `components/cards.py`

```python
from dash import html
import dash_bootstrap_components as dbc
from colours import NORD_SIGNAL

def kpi_card(label: str, value: str, delta: str | None = None,
             delta_positive: bool = True) -> dbc.Card:
    delta_colour = NORD_SIGNAL["good"] if delta_positive else NORD_SIGNAL["bad"]
    return dbc.Card(
        dbc.CardBody([
            html.P(label, className="text-muted small mb-1 text-uppercase",
                   style={"letterSpacing": "0.05em"}),
            html.H3(value, className="fw-bold mb-0"),
            html.P(delta, style={"color": delta_colour, "fontSize": "0.85rem"}) if delta else None,
        ]),
        className="shadow-sm border-0 h-100",
    )
```

---

## Standard layout — `layout.py`

```python
layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H2("Insight-led dashboard title", className="fw-bold"), width=8),
        dbc.Col(dbc.Select(id="filter", options=[]), width=4,
                className="d-flex align-items-end justify-content-end"),
    ], className="mb-4 mt-3"),

    dbc.Row([                    # KPI cards — always first row
        dbc.Col(kpi_card("Label", "Value", "+X%", True), width=3),
        dbc.Col(kpi_card("Label", "Value", "-X%", False), width=3),
        dbc.Col(kpi_card("Label", "Value"), width=3),
        dbc.Col(kpi_card("Label", "Value"), width=3),
    ], className="mb-4"),

    dbc.Row([                    # Primary chart — full width
        dbc.Col(dbc.Card(
            dcc.Loading(dcc.Graph(id="primary-chart", config={"responsive": True})),
            className="shadow-sm border-0 p-3",
        ), width=12),
    ], className="mb-4"),

    dbc.Row([                    # Secondary charts side by side
        dbc.Col(dbc.Card(
            dcc.Loading(dcc.Graph(id="chart-left", config={"responsive": True})),
            className="shadow-sm border-0 p-3",
        ), width=6),
        dbc.Col(dbc.Card(
            dcc.Loading(dcc.Graph(id="chart-right", config={"responsive": True})),
            className="shadow-sm border-0 p-3",
        ), width=6),
    ], className="mb-4"),
], fluid=True, className="px-4 py-2")
```

---

## Callbacks — `callbacks.py`

```python
from dash import Input, Output, callback, no_update

@callback(
    Output("primary-chart", "figure"),
    Input("filter", "value"),
    prevent_initial_call=True,
)
def update_primary(filter_value: str):
    if not filter_value:
        return no_update
    df = load_filtered_data(filter_value)   # cached in loader.py
    return make_trend_chart(df, "value", "Insight-led title")
```

Rules:
- One callback per logical interaction.
- `prevent_initial_call=True` where the layout default covers the initial state.
- `no_update` for outputs that have not changed.
- `dcc.Store` for shared state — never module-level globals.

---

## Formatting — `formatting.py`

```python
DATE_FORMAT    = "%d %b %Y"      # 04 Apr 2024
DATE_SHORT     = "%b %Y"
TIMEZONE_LABEL = "Europe/London" # named IANA zone — never "UTC+1"
PCT_PRECISION  = 1
CCY_SYMBOL     = "£"

def fmt_pct(v: float) -> str:            return f"{v:.{PCT_PRECISION}f}%"
def fmt_currency(v: float, u="M") -> str: return f"{CCY_SYMBOL}{v:.1f}{u}"
def fmt_delta(v: float) -> str:          return f"{'+' if v>=0 else ''}{v:.{PCT_PRECISION}f}%"
def fmt_pp(v: float) -> str:             return f"{'+' if v>=0 else ''}{v:.{PCT_PRECISION}f}pp"

def fmt_large(v: float) -> str:
    for t, s in [(1e9,"B"),(1e6,"M"),(1e3,"K")]:
        if abs(v) >= t: return f"{v/t:.1f}{s}"
    return f"{v:,.0f}"
```

Apply in `hovertemplate` and `tickformat` — never format ad hoc inline.
Use `pp` (percentage points) for absolute changes between percentage values.

---

## Chart selection — quick reference

| Intent | Use | Never |
|---|---|---|
| Change over time | Line, area | Bar (discrete periods only) |
| Compare categories | Horizontal bar (many), column (few) | Line |
| Part of a whole | Stacked bar, treemap | Pie > 4 slices |
| Distribution | Histogram, violin, box | Bar of means |
| Correlation | Scatter, bubble | Line |
| Flow | Sankey | — |
| Single KPI | Styled `html.Div` card | Any chart |
| Multiple series, different scales | Small multiples | Dual-axis |

---

## Colourblindness — non-negotiable rules

1. Red and green (`NORD_SIGNAL["bad"]` + `NORD_SIGNAL["good"]`) must always have a redundant encoding alongside colour: shape, line dash, hatch pattern, or direct text label.
2. `NORD13` (aurora yellow — `SIGNAL["warning"]`) must not be used as text on light backgrounds — fills only.
3. Sequential continuous data: `"Viridis"`, `"Cividis"`, or `"Magma"` — never `"Jet"` or `"Rainbow"`.
4. Tooltips must include series name as text — colour alone is not sufficient.
5. All multi-series charts: use shape or dash redundancy alongside colour.

```python
# Scatter — colour + shape
marker=dict(color=NORD_CATEGORICAL[0], symbol="circle")   # series A
marker=dict(color=NORD_CATEGORICAL[1], symbol="square")   # series B

# Line — colour + dash
line=dict(color=NORD_CATEGORICAL[0], dash="solid")
line=dict(color=NORD_CATEGORICAL[1], dash="dash")

# Bar — colour + hatch
marker=dict(color=NORD_SIGNAL["good"],
            pattern=dict(shape="/", fgcolor=TEXT_PRIMARY, size=6))  # TEXT_PRIMARY from colours.py
```

---

## Pre-commit checklist

```
□ hovertemplate set on all traces (value, label, unit, context)
□ _empty_chart() returned for all empty-data cases
□ Chart title states the insight — not the chart type
□ No inline hex literals — all colours from colours.py
□ config={"responsive": True} on all dcc.Graph
□ dcc.Loading wrapper on charts with non-trivial data fetch
□ Red/green pairs have redundant encoding
□ Sequential data uses Viridis / Cividis / Magma
□ Timezone shown explicitly on all time series
□ fmt_* formatters used — no ad hoc f-string formatting
```
