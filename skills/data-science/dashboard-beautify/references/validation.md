# Validation — Pre-Ship QA, Data Quality, and Localisation

---

## Data quality gate — detail

Run before any design or build work begins. Document findings in a brief that the data owner signs off.

### Missingness
```python
def audit_missingness(df: pd.DataFrame) -> pd.DataFrame:
    """Returns a summary of null counts and proportions per column."""
    total = len(df)
    summary = (
        df.isnull()
          .sum()
          .rename("null_count")
          .to_frame()
    )
    summary["null_pct"] = (summary["null_count"] / total * 100).round(2)
    summary["non_null_count"] = total - summary["null_count"]
    return summary[summary["null_count"] > 0].sort_values("null_pct", ascending=False)
```

For each column with nulls, answer:
- Is this null expected (e.g. optional field) or a data pipeline issue?
- What does the dashboard show for a null? (Handle explicitly — no silent drops.)
- Does nulls-in = nulls-out break any aggregation?

### Duplicates
```python
def audit_duplicates(df: pd.DataFrame, grain_cols: list[str]) -> dict:
    """Check uniqueness at the intended grain."""
    total = len(df)
    unique = df.drop_duplicates(subset=grain_cols)
    duplicated = total - len(unique)
    return {
        "total_rows": total,
        "unique_at_grain": len(unique),
        "duplicate_rows": duplicated,
        "duplicate_pct": round(duplicated / total * 100, 2),
        "example_duplicates": df[df.duplicated(subset=grain_cols, keep=False)].head(10),
    }
```

### Outliers — flag, don't silently drop
```python
def flag_outliers(series: pd.Series, method: str = "iqr") -> pd.Series:
    """
    Returns a boolean mask of outlier rows.
    method: 'iqr' (1.5×IQR rule) or 'zscore' (|z| > 3)
    """
    if method == "iqr":
        q1, q3 = series.quantile([0.25, 0.75])
        iqr = q3 - q1
        return (series < q1 - 1.5 * iqr) | (series > q3 + 1.5 * iqr)
    elif method == "zscore":
        z = (series - series.mean()) / series.std()
        return z.abs() > 3
```

If outliers are real, annotate them on the chart. If they are data quality issues, exclude them and document the decision visibly (e.g. a footnote on the dashboard).

### Unit consistency check
Before any aggregation involving units, assert consistency:
```python
assert df["currency"].nunique() == 1, \
    f"Mixed currencies in data: {df['currency'].unique()}. Normalise before aggregating."
```

### Timezone normalisation
```python
import pytz
from datetime import timezone

def normalise_to_utc(df: pd.DataFrame, ts_col: str, source_tz: str) -> pd.DataFrame:
    """Convert naive or local timestamps to UTC. Call at ingestion."""
    tz = pytz.timezone(source_tz)
    df[ts_col] = (
        pd.to_datetime(df[ts_col])
          .dt.tz_localize(tz, ambiguous="infer", nonexistent="shift_forward")
          .dt.tz_convert("UTC")
    )
    return df
```

Display timezone must be explicit in the UI — never show a time without naming the zone.

---

## Pre-ship QA — full checklist

### Data correctness
```
□ Spot-check ≥ 3 data points against the source system (database, report, or source file)
□ Total/aggregate values reconciled — sum of parts equals the whole where applicable
□ Date boundaries correct — "last 30 days" actually includes 30 days, not 29 or 31
□ Filter logic verified — applying two filters simultaneously gives the correct intersection
□ Metric definitions confirmed with data owner and documented in the dashboard
```

### Edge cases and error states
```
□ Empty filter result: no blank chart — show "No data for this selection" message
□ Single data point: no line chart with one point and no context — handle gracefully
□ Maximum date range: performance acceptable, no timeout
□ All-null column: does not crash — handle in chart function with early return
□ Future dates in data (if relevant): handled or excluded
```

Empty state pattern:
```python
def make_chart(df: pd.DataFrame) -> go.Figure:
    if df.empty:
        fig = go.Figure()
        fig.update_layout(
            title="No data for this selection",
            annotations=[dict(
                text="Adjust the filters above to see data.",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False,
                font=dict(size=14, color="#718096"),
            )],
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
        )
        return fig
    # ... normal chart build
```

### Visual and layout
```
□ All chart titles state an insight — not "Revenue" but "Revenue up 34% after Q2"
□ Axis units labelled or unambiguous from context
□ Date range and timezone displayed on all time series charts
□ Legend entries match series names in the data (no "trace 0", "trace 1")
□ hovertemplate set on all traces — includes value, label, unit, and context
□ No inline hex literals — all colours from colours.py
□ Consistent chart heights within each row
□ KPI card deltas show direction and reference period ("+12% vs last month")
```

### Responsiveness and accessibility
```
□ Mobile viewport tested at 768px minimum width — no horizontal scroll, no clipped labels
□ Tablet viewport tested at 1024px
□ config={"responsive": True} on all dcc.Graph components
□ Keyboard navigation: Tab through all interactive controls in logical order
□ All dcc.Loading wrappers in place for any chart with non-trivial data fetch
□ Screen reader test: every chart has a title; complex charts have a plain-language summary
□ Colourblindness checklist complete (colourblindness.md)
```

### Performance
```
□ Initial page load < 3s on target connection (test with browser DevTools throttling)
□ Filter callback response < 1s for typical selections
□ No n+1 queries in callbacks — verify with query logging
□ Cache hit rate acceptable under realistic concurrent load
```

---

## Localisation standards

Define all formatting conventions in `formatting.py` at project start. Never format inline.

### Dates
```python
DATE_FORMAT      = "%d %b %Y"   # 04 Apr 2024 — unambiguous, no leading zero confusion
DATE_SHORT       = "%b %Y"      # Apr 2024
DATETIME_FORMAT  = "%d %b %Y %H:%M"
TIMEZONE_LABEL   = "Europe/London"  # always a named IANA zone — never "UTC+1" or "BST"
```

Always display the timezone on time series charts:
```python
fig.update_layout(
    xaxis_title=f"Date ({TIMEZONE_LABEL})",
    # or via subtitle:
    title=f"<b>Chart title</b><br><sup>All times shown in {TIMEZONE_LABEL}</sup>",
)
```

### Numbers
```python
PCT_PRECISION  = 1   # 68.4% — one decimal place; 68.3912% adds false precision
CCY_PRECISION  = 1   # £4.2M

def fmt_pct(v: float) -> str:
    return f"{v:.{PCT_PRECISION}f}%"

def fmt_currency(v: float, unit: str = "M") -> str:
    return f"£{v:.{CCY_PRECISION}f}{unit}"

def fmt_large(v: float) -> str:
    """Auto-abbreviate for KPI cards: 1.2K, 4.3M, 2.1B."""
    for threshold, suffix in [(1e9, "B"), (1e6, "M"), (1e3, "K")]:
        if abs(v) >= threshold:
            return f"{v / threshold:.1f}{suffix}"
    return f"{v:,.0f}"

def fmt_delta(v: float, unit: str = "%") -> str:
    """Always show sign for deltas: +12.4% or -3.1%."""
    sign = "+" if v >= 0 else ""
    return f"{sign}{v:.{PCT_PRECISION}f}{unit}"
```

Apply in `hovertemplate`:
```python
hovertemplate="<b>%{x|%d %b %Y}</b><br>Revenue: £%{y:.1f}M<extra></extra>"
```

Apply in axis tick format:
```python
fig.update_yaxes(tickformat=".1f", ticksuffix="M", tickprefix="£")
fig.update_xaxes(tickformat="%b %Y")
```

### Percentage points vs percentages
When a metric changes from 68% to 72%, that is a **4 percentage point (pp)** increase, not a 4% increase.
Use "pp" for absolute changes between percentage values:
```python
def fmt_pp_delta(v: float) -> str:
    sign = "+" if v >= 0 else ""
    return f"{sign}{v:.{PCT_PRECISION}f}pp"
```

### Locale-specific considerations
If the dashboard will be used across multiple locales:
- Use `babel` for locale-aware number and date formatting rather than manual f-strings.
- Test decimal separators: `1,234.56` (en-GB) vs `1.234,56` (de-DE).
- Currency: always include the symbol — do not assume context makes it obvious.
- Week numbering: ISO week (Mon start) vs US week (Sun start) — specify in any week-based grouping.
