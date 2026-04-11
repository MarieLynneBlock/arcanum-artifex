# Observability — Logging, Timing, and Error Reporting

A production dashboard without observability is a black box. You need to know when callbacks are slow,
when data loads fail silently, and which filters users actually use. Add these patterns from the start —
retrofitting logging into a Dash app is painful.

---

## Structured logging

Use Python's `logging` module with structured output — not `print()`.

```python
# In app.py — configure once, import logger everywhere
import logging
import json

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)
logger = logging.getLogger("dashboard")

# For production: switch to JSON logging for ingestion by CloudWatch / Datadog / ELK
class JsonFormatter(logging.Formatter):
    def format(self, record):
        return json.dumps({
            "time":    self.formatTime(record),
            "level":   record.levelname,
            "logger":  record.name,
            "message": record.getMessage(),
            **getattr(record, "extra", {}),
        })

handler = logging.StreamHandler()
handler.setFormatter(JsonFormatter())
logger.handlers = [handler]
```

Log at the right level:
- `DEBUG` — detailed trace, dev only
- `INFO` — data loaded, cache hit/miss, callback triggered
- `WARNING` — data quality issues flagged, fallback used
- `ERROR` — query failed, unhandled exception in callback

---

## Callback timing

Slow callbacks are the most common Dash performance complaint. Measure them:

```python
import time
import functools
from app import logger

def timed(func):
    """Decorator — logs callback execution time and input summary."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = (time.perf_counter() - start) * 1000  # ms
        logger.info(
            f"callback:{func.__name__} elapsed={elapsed:.1f}ms inputs={args!r:.200}"
        )
        if elapsed > 2000:
            logger.warning(f"callback:{func.__name__} SLOW — {elapsed:.0f}ms exceeds 2s threshold")
        return result
    return wrapper

# Usage in callbacks.py
@callback(Output("chart", "figure"), Input("filter", "value"))
@timed
def update_chart(filter_value):
    ...
```

Set a threshold appropriate to your audience — 500ms for internal analytical tools, 200ms for operational dashboards.

---

## Data loader logging

Log every data fetch — source, shape, and timing:

```python
# In data/loader.py
from app import logger

def load_monthly_revenue(region: str, year: int) -> pd.DataFrame:
    start = time.perf_counter()
    try:
        df = _query_database(region=region, year=year)
        elapsed = (time.perf_counter() - start) * 1000
        logger.info(
            f"loader:monthly_revenue rows={len(df)} region={region} year={year} elapsed={elapsed:.1f}ms"
        )
        return df
    except Exception as e:
        logger.error(f"loader:monthly_revenue FAILED region={region} year={year} error={e!r}")
        raise
```

Log cache hits distinctly from actual fetches — a hit at 1ms vs a miss at 800ms tells you whether
your caching strategy is working:

```python
@cache.memoize(timeout=300)
def load_monthly_revenue(region: str, year: int) -> pd.DataFrame:
    logger.info(f"loader:monthly_revenue CACHE_MISS region={region} year={year}")
    ...

# Wrap the cached call to detect hits
def get_revenue(region, year):
    before = time.perf_counter()
    df = load_monthly_revenue(region, year)
    elapsed = (time.perf_counter() - before) * 1000
    if elapsed < 5:
        logger.debug(f"loader:monthly_revenue CACHE_HIT elapsed={elapsed:.1f}ms")
    return df
```

---

## Error handling in callbacks

Never let an unhandled exception return a blank chart with no user feedback.

```python
from dash import callback, Output, Input, html
import traceback
from components.charts import make_chart_or_empty
from app import logger

@callback(Output("revenue-chart", "figure"), Input("region", "value"))
def update_revenue(region):
    try:
        df = get_revenue(region=region)
        return make_chart_or_empty(df, "Revenue by month")
    except Exception as e:
        logger.error(f"callback:update_revenue FAILED region={region}\n{traceback.format_exc()}")
        # Return an empty chart with an error message — never a blank figure
        return _error_chart("Revenue by month", str(e))

def _error_chart(title: str, error_msg: str) -> go.Figure:
    """Visible error state — do not show raw exception to end users in production."""
    import os
    msg = f"Error: {error_msg}" if os.getenv("DASH_DEBUG") else "Could not load data. Please try again."
    fig = go.Figure()
    fig.update_layout(
        title=title,
        annotations=[dict(
            text=msg, x=0.5, y=0.5,
            xref="paper", yref="paper",
            showarrow=False, font=dict(size=13, color=NORD_SIGNAL["bad"]),
        )],
        xaxis_visible=False, yaxis_visible=False,
    )
    return fig
```

Show technical error detail only in debug mode. End users see a clean message; developers see the traceback in logs.

---

## Data quality logging

Surface data quality findings as structured log events — not just console prints:

```python
def log_data_quality(df: pd.DataFrame, source: str) -> None:
    null_rates = df.isnull().mean()
    flagged = null_rates[null_rates > 0.05]
    for col, rate in flagged.items():
        logger.warning(f"data_quality source={source} col={col} null_rate={rate:.2%}")

    n_dupes = df.duplicated().sum()
    if n_dupes > 0:
        logger.warning(f"data_quality source={source} duplicates={n_dupes}")

    logger.info(f"data_quality source={source} rows={len(df)} cols={len(df.columns)} ok")
```

---

## Usage analytics (optional but useful)

Track which filters users actually engage with — this informs future dashboard design:

```python
@callback(Output("filter-store", "data"), Input("region-filter", "value"))
def track_filter_usage(region):
    logger.info(f"user_action filter=region value={region}")
    return {"region": region}
```

In production, pipe these events to your analytics platform (Amplitude, Mixpanel, or a simple
DynamoDB table) rather than just logs. The patterns reveal which parts of the dashboard are used,
which filters are never touched, and which views are abandoned immediately.

---

## Observability checklist

```
□ Structured logging configured in app.py — JSON format in production
□ @timed decorator on all callbacks — slow threshold logged as WARNING
□ All data loader functions log: source, rows, elapsed time
□ Cache hits logged distinctly from misses
□ All callbacks have try/except — unhandled exceptions never reach the user as blank charts
□ Error chart returns user-friendly message; raw errors only in DEBUG mode
□ Data quality log_data_quality() called on every loader return
□ Log level appropriate per environment: DEBUG in dev, INFO in staging/prod
```
