# Formatting and Localisation — Reference

Inconsistent formatting is a credibility problem. A dashboard that shows "3/4/24" in one place and
"04 March 2024" in another signals that no one checked the output. Define conventions once in
`colours.py` and enforce them everywhere.

---

## Dates

**Default format: `DD Mon YYYY`** — e.g. `15 Jan 2024`

This is unambiguous across all locales. `MM/DD/YY` is ambiguous (US vs EU), `YYYY-MM-DD` reads as technical/raw.

```python
# colours.py
DATE_FORMAT         = "%d %b %Y"    # 15 Jan 2024
DATE_FORMAT_SHORT   = "%d %b"       # 15 Jan  (for axis ticks with known year)
DATE_FORMAT_MONTH   = "%b %Y"       # Jan 2024 (for monthly aggregations)
DATE_FORMAT_QUARTER = "Q{q} {year}" # Q1 2024 (see format_quarter() below)
DATE_FORMAT_ISO     = "%Y-%m-%d"    # for data operations only — never display

def format_date(dt: pd.Timestamp | str) -> str:
    return pd.Timestamp(dt).strftime(DATE_FORMAT)

def format_quarter(dt: pd.Timestamp) -> str:
    q = (dt.month - 1) // 3 + 1
    return f"Q{q} {dt.year}"
```

### Axis tick formats in Plotly
```python
fig.update_xaxes(tickformat="%d %b %Y")     # 15 Jan 2024
fig.update_xaxes(tickformat="%b %Y")        # Jan 2024 — for monthly data
fig.update_xaxes(tickformat="%b '%y")       # Jan '24 — compact, for many ticks
```

### In hover templates
```python
hovertemplate="<b>%{x|%d %b %Y}</b><br>Value: %{y}<extra></extra>"
```

---

## Timezones

**Rule: all timestamps in a single named timezone throughout a dashboard.**

Never mix timezone-aware and timezone-naive values. Never display UTC to end users without a label.

```python
# colours.py
DISPLAY_TIMEZONE = "Europe/London"   # change per deployment region

# In loader.py
import pytz

def normalise_tz(df: pd.DataFrame, col: str) -> pd.DataFrame:
    tz = pytz.timezone(DISPLAY_TIMEZONE)
    df[col] = pd.to_datetime(df[col], utc=True).dt.tz_convert(tz)
    return df
```

Always label the timezone in the chart subtitle or axis title:
```python
fig.update_layout(
    title="<b>Request volume</b><br><sup>All times in Europe/London (GMT/BST)</sup>"
)
# or
fig.update_xaxes(title_text="Time (GMT)")
```

---

## Numbers and currency

### General number formatting

```python
def format_number(value: float, precision: int = 1) -> str:
    """
    Abbreviate large numbers with K/M/B suffix.
    4_213_500 → '4.2M'
    12_400    → '12.4K'
    842       → '842'
    """
    if abs(value) >= 1_000_000_000:
        return f"{value / 1_000_000_000:.{precision}f}B"
    if abs(value) >= 1_000_000:
        return f"{value / 1_000_000:.{precision}f}M"
    if abs(value) >= 1_000:
        return f"{value / 1_000:.{precision}f}K"
    return f"{value:,.{precision}f}"
```

**Precision rules:**
- Raw counts (users, transactions): 0 decimal places — `18,432` not `18,432.0`
- Aggregated totals (revenue, cost): 1dp at M scale — `£4.2M`, 0dp at B scale — `£1B`
- Rates and averages: 1dp — `3.4` not `3.43721`
- Financial transactions: always 2dp — `£1,234.56`

### Currency

```python
# colours.py
CURRENCY_SYMBOL = "£"   # change per deployment: "$", "€", "¥"
CURRENCY_CODE   = "GBP"

def format_currency(value: float, abbreviated: bool = True) -> str:
    if abbreviated:
        return f"{CURRENCY_SYMBOL}{format_number(value)}"
    return f"{CURRENCY_SYMBOL}{value:,.2f}"
```

**Rules:**
- Symbol before value: `£4.2M` not `4.2M £`
- Thousands separator: `£1,234` not `£1234`
- Abbreviate at 1K for dashboard displays; use full precision in exported tables
- When showing multiple currencies, always include the currency code — `£4.2M GBP` — to avoid ambiguity

### Plotly tick formatting
```python
fig.update_yaxes(tickprefix="£", tickformat=",.1f")    # £4.2
fig.update_yaxes(tickprefix="£", ticksuffix="M")        # £4.2M  (if data already in millions)
fig.update_yaxes(tickformat="$,.0f")                    # $18,432
```

---

## Percentages

**Rule: 1 decimal place, `%` suffix, always.**

```python
def format_pct(value: float, is_fraction: bool = False, precision: int = 1) -> str:
    """
    Format a percentage value.
    is_fraction=True: input is 0–1 scale (0.683 → '68.3%')
    is_fraction=False: input is 0–100 scale (68.3 → '68.3%')
    """
    v = value * 100 if is_fraction else value
    return f"{v:.{precision}f}%"
```

**Confirm the scale of every percentage column before building.** `0.683` and `68.3` are both plausible
values for the same metric — check which your data source uses and document it in `validate_units()`.

In Plotly:
```python
fig.update_yaxes(tickformat=".1%")    # if data is 0–1 scale (Plotly multiplies by 100)
fig.update_yaxes(ticksuffix="%", tickformat=".1f")    # if data is 0–100 scale
```

---

## Percentage points vs percentages

When showing change in a rate metric, distinguish clearly:

- **Percentage change**: `+12.5%` — means the value increased by 12.5% of its previous value
- **Percentage point change**: `+2.3pp` — means the rate moved from e.g. 68.0% to 70.3%

Use `pp` suffix explicitly in chart labels and tooltips when reporting change in a rate.

```python
def format_delta_pct(before: float, after: float) -> str:
    """Returns e.g. '+2.3pp' for a rate that moved from 68.0 to 70.3."""
    delta = after - before
    sign = "+" if delta >= 0 else ""
    return f"{sign}{delta:.1f}pp"
```

---

## Large numbers — display conventions

| Value | Display | Never |
|---|---|---|
| 842 | `842` | `842.0` |
| 12,400 | `12.4K` | `12400` or `12,400.0` |
| 4,213,500 | `£4.2M` | `£4,213,500` or `4213500` |
| 1,100,000,000 | `£1.1B` | `£1,100,000,000` |

Define K/M/B breakpoints in `colours.py`:
```python
K_THRESHOLD = 1_000
M_THRESHOLD = 1_000_000
B_THRESHOLD = 1_000_000_000
```

---

## Null / missing value display

Never show `NaN`, `None`, `null`, or blank space to end users. Define display substitutes:

```python
NULL_DISPLAY = {
    "numeric":     "—",      # en-dash — visually distinct from zero
    "text":        "Unknown",
    "percentage":  "N/A",
    "date":        "No date",
}
```

In Plotly, gaps in time series are handled by:
```python
fig.update_traces(connectgaps=False)   # show gap as break in line — honest
# OR
fig.update_traces(connectgaps=True)    # interpolate — only if interpolation is meaningful
```

Default to `connectgaps=False` — do not imply continuity where data is absent.

---

## Axis label conventions

- Include units in the axis title if not obvious from context: `Revenue (£M)`, `Response time (ms)`, `Temperature (°C)`
- Omit axis titles when the chart title or subtitle makes them redundant
- Y-axis: vertical label is readable — Plotly defaults are fine; do not rotate to horizontal
- X-axis for time: let Plotly choose tick density; override only if ticks overlap

```python
fig.update_layout(
    xaxis_title=None,           # date is obvious from tick format
    yaxis_title="Revenue (£M)", # unit is not obvious
)
```

---

## Locale-specific formatting — reference

| Locale | Date format | Thousands sep | Decimal sep | Currency |
|---|---|---|---|---|
| UK (default) | `15 Jan 2024` | `,` | `.` | `£` prefix |
| EU (generic) | `15 Jan 2024` | `.` | `,` | `€` prefix |
| US | `Jan 15, 2024` | `,` | `.` | `$` prefix |
| DE | `15. Jan. 2024` | `.` | `,` | `€` suffix |

For multi-locale deployments, use Python's `locale` module or the `babel` library:
```python
from babel.numbers import format_currency
format_currency(4_213_500, "GBP", locale="en_GB")   # → '£4,213,500.00'
```
