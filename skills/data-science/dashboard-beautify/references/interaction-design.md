# Interaction Design — Reference

Interactivity should reduce cognitive load, not demonstrate technical capability.
Every interactive element must earn its place by answering a question the static view cannot.

---

## Core rule

**The default view must answer the primary question without any interaction.**

If a user has to change a filter or click a chart before the dashboard makes sense, the default state is wrong.
Set filter defaults, date ranges, and visible series to the most useful state for the primary audience —
not the most general state.

---

## When to add interactivity

| User need | Right interaction | Wrong interaction |
|---|---|---|
| Focus on a sub-population | Dropdown / radio filter | Nothing (force them to squint) |
| Compare two time periods | Date range picker | Separate static charts |
| Understand a data point | Rich hover tooltip | Click-through to a table |
| Investigate a category in depth | Drill-down (new view/page) | Cross-filter (clutters summary) |
| Compare sub-populations across multiple charts | Cross-filter | Drill-down (loses context) |
| Export for reporting | Download button | Screenshot instructions |

---

## Filter design rules

1. Filters go **above** the charts they affect — never below, never in a sidebar that's not visible by default.
2. **Maximum 3 filter controls** on a single view. More than 3 signals the dashboard is trying to do too much — split into tabs or separate pages.
3. Every filter must have a **sensible default** — never leave a filter blank and force the user to make the first selection to see any data.
4. If a filter affects only one chart on the page, place it inside that chart's card — not in the global header.
5. Show the active filter state clearly — use a summary string ("Showing: Q1 2024, London region") near the primary chart.

```python
# Filter with sensible default — never blank
dbc.Select(
    id="region-filter",
    options=[{"label": "All regions", "value": "all"},
             {"label": "London", "value": "london"},
             {"label": "Manchester", "value": "manchester"}],
    value="all",   # ← always set a default value
    className="mb-3",
)
```

---

## Drill-down vs cross-filter — decision guide

### Use drill-down when:
- The detail view replaces the summary (user navigates "into" the data)
- The detail has a different structure to the summary (e.g. summary = monthly, detail = daily transactions)
- The audience needs to action something at the detail level (e.g. review individual records)

```python
# Drill-down pattern — navigate to detail page on click
@callback(
    Output("url", "pathname"),
    Input("summary-chart", "clickData"),
    prevent_initial_call=True,
)
def drill_down(click_data):
    if not click_data:
        return no_update
    category = click_data["points"][0]["x"]
    return f"/detail/{category}"
```

### Use cross-filter when:
- The detail remains visible alongside the summary (user filters in context)
- The user is comparing sub-populations across multiple chart types simultaneously
- The audience is analytical and expects to explore without losing their place

```python
# Cross-filter pattern — shared state via dcc.Store
@callback(
    Output("filter-store", "data"),
    Input("summary-chart", "clickData"),
    prevent_initial_call=True,
)
def update_filter_store(click_data):
    if not click_data:
        return no_update
    return {"selected_category": click_data["points"][0]["x"]}

@callback(
    Output("detail-chart", "figure"),
    Input("filter-store", "data"),
)
def update_detail(filter_data):
    category = filter_data.get("selected_category") if filter_data else None
    df_filtered = df[df["category"] == category] if category else df
    return make_detail_chart(df_filtered)
```

### Never use both on the same dashboard
Mixing drill-down navigation and cross-filter on the same page creates disorientation.
Pick one interaction model per dashboard and apply it consistently.

---

## Tooltips — always; make them count

Every chart must have `hovertemplate` set. The default Plotly hover is almost never good enough.

A good tooltip answers: **what is this value, what does it belong to, and what should I conclude?**

```python
# Minimal — values and labels only
hovertemplate="<b>%{x}</b><br>Revenue: £%{y:,.1f}M<extra></extra>"

# Informative — add context
hovertemplate=(
    "<b>%{customdata[0]}</b><br>"         # entity name
    "Revenue: <b>£%{y:,.1f}M</b><br>"
    "vs target: %{customdata[1]:+.1f}%<br>"   # delta
    "<i>Click to drill down</i>"              # affordance hint if drillable
    "<extra></extra>"
)
```

`<extra></extra>` removes the default trace name box — always include it.

---

## Number of controls — complexity budget

| Controls on a single view | Assessment |
|---|---|
| 0 | Static — appropriate for infographics and reports |
| 1–2 | Clean — well-suited to operational dashboards |
| 3 | Acceptable maximum for most audiences |
| 4–5 | Requires justification — consider tabs or sub-pages |
| 6+ | Redesign — the dashboard scope is too broad |

When you find yourself adding a 4th filter, ask: "Is this dashboard trying to answer too many questions at once?"
The right answer is usually to split the dashboard, not add another control.

---

## Date range picker — best practice

```python
import dash_core_components as dcc
from datetime import date, timedelta

dcc.DatePickerRange(
    id="date-range",
    min_date_allowed=date(2020, 1, 1),
    max_date_allowed=date.today(),
    start_date=date.today() - timedelta(days=89),   # default: last 90 days
    end_date=date.today(),
    display_format="DD MMM YYYY",
    first_day_of_week=1,   # Monday — appropriate for UK/EU contexts
)
```

- Default to the most useful window, not "all time" — all-time defaults load slowly and hide the recent signal
- Always show the date format explicitly in `display_format` — avoid ambiguity
- Set `first_day_of_week=1` (Monday) for UK/EU audiences

---

## Animations — use sparingly

Animations are appropriate when **temporal progression is the insight itself** — e.g. showing how a distribution shifts across years.

They are inappropriate for: transitions between filter states, loading indicators on charts (use `dcc.Loading` instead), or decorative effect.

```python
# Animated time series — only when the progression IS the story
fig = px.scatter(
    df, x="gdp", y="life_expectancy",
    animation_frame="year",
    animation_group="country",
    size="population",
    color="continent",
    range_x=[0, 60000], range_y=[25, 90],
)
```

Always provide a static alternative or summary for users who can't follow animations (cognitive accessibility).

---

## Empty states — never leave a blank chart

Every callback that can return no data must handle the empty state explicitly:

```python
def make_chart_or_empty(df: pd.DataFrame, title: str) -> go.Figure:
    if df.empty:
        fig = go.Figure()
        fig.update_layout(
            title=title,
            annotations=[dict(
                text="No data for the selected filters",
                x=0.5, y=0.5,
                xref="paper", yref="paper",
                showarrow=False,
                font=dict(size=14, color=TEXT_MUTED),
            )],
            xaxis_visible=False,
            yaxis_visible=False,
        )
        return fig
    return make_real_chart(df, title)
```

A blank `go.Figure()` with no annotation looks like a broken dashboard. An explicit empty-state message is a design decision.
