# Performance — Large Data and Production Optimisation

This reference covers patterns for Dash + Plotly when data volume, query time, or callback complexity
starts affecting user experience. Apply these progressively — don't optimise prematurely.

---

## When to start worrying

| Symptom | Likely cause | Start with |
|---|---|---|
| Chart renders slow on first load | No caching, full data fetch per session | Server-side caching |
| Callback takes > 1s on filter change | Heavy computation in callback | Memoisation / pre-aggregation |
| Chart with > 50k points is sluggish | SVG renderer limit | WebGL traces |
| Dashboard slow for concurrent users | No shared cache | Redis / server-side store |
| Page load > 3s | Too much data serialised to client | Downsample or paginate |

---

## Caching — Flask-Caching with Dash

The single highest-impact optimisation for most dashboards.

```python
# app.py
from flask_caching import Cache

cache = Cache(app.server, config={
    "CACHE_TYPE": "SimpleCache",      # in-memory, single process
    # "CACHE_TYPE": "RedisCache",     # use for multi-process / production
    # "CACHE_REDIS_URL": os.environ["REDIS_URL"],
    "CACHE_DEFAULT_TIMEOUT": 300,     # seconds
})
```

```python
# data/loader.py
from app import cache

@cache.memoize(timeout=300)
def load_filtered_data(start_date: str, end_date: str, category: str) -> pd.DataFrame:
    """Cache key is derived from arguments — must be hashable primitives."""
    return query_database(start_date, end_date, category)
```

**Rules:**
- Cache at the data-loading layer, not inside callbacks.
- Cache keys must be deterministic and derived from all filter parameters.
- Set timeouts based on data freshness requirements — not arbitrarily long.
- Use `cache.delete_memoized(load_filtered_data)` in a refresh endpoint if data updates on a schedule.

---

## Pre-aggregation — server-side before the callback

Never send raw row-level data to Plotly if an aggregation will do. Aggregate at query time.

```python
# data/loader.py
def load_monthly_revenue(filters: dict) -> pd.DataFrame:
    """Return one row per month — not one row per transaction."""
    df = fetch_raw(filters)
    return (
        df.groupby(pd.Grouper(key="date", freq="ME"))
          ["revenue"]
          .sum()
          .reset_index()
    )
```

For very large datasets, push aggregation to the database:
```sql
SELECT DATE_TRUNC('month', transaction_date) AS month,
       SUM(revenue)                          AS revenue
FROM   transactions
WHERE  category = %(category)s
GROUP  BY 1
ORDER  BY 1;
```

---

## Downsampling — when you must show point-level data

When the insight requires individual data points (e.g. scatter of events) but volume is too high:

```python
def downsample(df: pd.DataFrame, max_points: int = 5_000) -> pd.DataFrame:
    """
    Uniform random sample. For time series, use LTTB instead (see below).
    Always annotate the chart to indicate sampling.
    """
    if len(df) <= max_points:
        return df
    return df.sample(n=max_points, random_state=42)
```

For time series, Largest-Triangle-Three-Buckets (LTTB) preserves visual shape far better than random sampling:
```python
pip install datashader  # includes LTTB via ds.transfer_functions
# or
pip install lttb
from lttb import lttb
downsampled = lttb(df[["timestamp_ms", "value"]].to_numpy(), n_out=2000)
```

Always add an annotation when data is sampled:
```python
fig.add_annotation(
    text=f"Showing {max_points:,} of {len(df):,} points (sampled)",
    xref="paper", yref="paper", x=1, y=0,
    xanchor="right", yanchor="bottom",
    font=dict(size=10, color="#718096"),
    showarrow=False,
)
```

---

## WebGL traces — 50k+ data points

Plotly's default renderer is SVG — it degrades badly above ~50k points. Switch to WebGL:

| Standard trace | WebGL equivalent |
|---|---|
| `go.Scatter` | `go.Scattergl` |
| `go.Bar` | No WebGL — pre-aggregate instead |
| `go.Heatmap` | `go.Heatmapgl` (Plotly 5.17+) |

```python
# Drop-in replacement — same API, GPU-accelerated rendering
fig.add_trace(go.Scattergl(
    x=df["x"],
    y=df["y"],
    mode="markers",
    marker=dict(size=4, opacity=0.6),
))
```

WebGL traces do not support all SVG features (some marker symbols, some text modes). Test visually before committing.

---

## Callback optimisation

### Avoid recomputing what hasn't changed
```python
from dash import callback, Input, Output, State, no_update

@callback(
    Output("chart", "figure"),
    Input("date-range", "start_date"),
    Input("date-range", "end_date"),
    Input("category", "value"),
    State("chart", "figure"),   # current figure — return as-is if nothing relevant changed
    prevent_initial_call=True,
)
def update_chart(start, end, category, current_fig):
    if not any([start, end, category]):
        return no_update
    df = load_filtered_data(start, end, category)  # hits cache if args match
    return make_chart(df)
```

### Background callbacks for slow operations (Dash 2.6+)
```python
from dash import callback, Input, Output
from dash.long_callback import DiskcacheLongCallbackManager
import diskcache

cache_mgr = DiskcacheLongCallbackManager(diskcache.Cache("./cache"))

app = dash.Dash(__name__, long_callback_manager=cache_mgr)

@app.long_callback(
    Output("result-chart", "figure"),
    Input("run-btn", "n_clicks"),
    running=[(Output("run-btn", "disabled"), True, False)],
    prevent_initial_call=True,
)
def run_slow_analysis(n_clicks):
    # This runs in a background process — UI stays responsive
    df = expensive_computation()
    return make_chart(df)
```

### `dcc.Store` for shared derived data
Compute once, share across multiple callbacks:
```python
# One callback fetches and stores
@callback(Output("shared-store", "data"), Input("filter", "value"))
def fetch_data(filter_val):
    df = load_filtered_data(filter_val)
    return df.to_json(date_format="iso", orient="split")

# Multiple callbacks read from store — no redundant fetches
@callback(Output("chart-a", "figure"), Input("shared-store", "data"))
def update_chart_a(json_data):
    df = pd.read_json(json_data, orient="split")
    return make_chart_a(df)
```

---

## Production deployment checklist

```
□ debug=False in production (app.run(debug=False))
□ Caching configured (Redis for multi-worker, SimpleCache for single-worker)
□ Cache timeouts set according to data freshness SLA
□ WebGL used for any scatter/line with > 50k points
□ Pre-aggregation happens at query layer, not in callbacks
□ All slow callbacks (> 2s) wrapped in dcc.Loading
□ Background callbacks used for operations > 5s
□ gunicorn worker count set (typically: 2 * CPU cores + 1)
□ Memory profiled under realistic concurrent load
```
