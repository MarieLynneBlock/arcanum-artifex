# Layout, Data Sharing, Multi-Page, Performance, Testing, Deployment

## Layout

A Dash app has two parts: `app.layout` (what it looks like) and callbacks (its interactivity).
`app.layout` is a tree of components — `dash.html` provides a class per HTML tag; `dash.dcc`
provides higher-level interactive components (dropdowns, graphs, stores, ...).

```python
from dash import Dash, html, dcc
import plotly.express as px

app = Dash()
app.layout = html.Div([
    html.H1('Hello Dash'),
    dcc.Graph(id='example-graph', figure=fig),
])
```

- `style` takes a dict with camelCase keys (`textAlign`, not `text-align`); HTML `class`
  becomes `className`.
- `children` is conventionally the first argument and can be omitted:
  `html.H1('Hello Dash')` is the same as `html.H1(children='Hello Dash')`.
- Extract repeated markup (e.g. a table generator, a sidebar) into a plain Python function that
  returns a component tree — this is "reusable components" in Dash, no special API needed.
- `help(dcc.Dropdown)` (or any component) lists every keyword argument/property at the
  installed Dash version; don't guess prop names.

## Sharing data between callbacks

Dash is intentionally **stateless**: callbacks should be safe to run in any available worker.
Separate worker processes do not share memory; threads in one process do share memory and can
race when callbacks mutate it. Design callbacks for both models so the app can scale and remains
robust if a worker process dies.

**Never mutate a global variable inside a callback.** It appears to work for a single session,
then breaks as soon as another user (or another worker) reads that "global" state:

```python
# Bad: mutates shared state; a second user (or worker) filters what's left
@callback(Output('output', 'children'), Input('score', 'value'))
def update_output(value):
    global df
    df = df[df['score'] == value]
    return len(df)

# Good: reassigns a local, leaves the source data untouched
@callback(Output('output', 'children'), Input('score', 'value'))
def update_output(value):
    filtered_df = df[df['score'] == value]
    return len(filtered_df)
```

Loading/querying data once at module scope (outside any callback) is fine and recommended for
expensive, read-only initialization — it happens once per worker startup, not per request.

Pick a sharing mechanism by payload size and who needs to see it:

1. **`dcc.Store`** (browser-side, JSON-serialized): the default choice for an intermediate
   value computed once and reused by several callbacks in the same session.
   ```python
   @callback(Output('intermediate-value', 'data'), Input('dropdown', 'value'))
   def clean_data(value):
       cleaned_df = slow_processing_step(value)
       # date_format='iso' only matters when the frame has datetime columns; omit it otherwise.
       return cleaned_df.to_json(date_format='iso', orient='split')

   @callback(Output('graph', 'figure'), Input('intermediate-value', 'data'))
   def update_graph(jsonified_cleaned_data):
       dff = pd.read_json(io.StringIO(jsonified_cleaned_data), orient='split')
       return create_figure(dff)
   ```
   Recent pandas versions require `io.StringIO(...)` around a JSON string passed to
   `pd.read_json` (a bare string is otherwise treated as a file path). Trade-off: no server
   memory cost, but the full payload transits the network on every
   callback that reads it, and a new browser session recomputes from scratch.

   **A `dcc.Store` value is client-controlled input, not trusted server state** — it round-trips
   through the browser and any callback that reads it can receive a payload the user edited,
   replayed, or forged. Validate shape (expected columns/keys, types, a size bound) before
   indexing into it, the same as you would for any other external input.
2. **Precomputed aggregates**: if the app only ever displays a subset/aggregation of the full
   result, compute and store that instead of the raw dataset — cuts both network and JSON
   (de)serialization cost.
3. **Server-side cache + signal** (e.g. Flask-Caching with Redis or a filesystem backend):
  for an expensive computation shared *across users*, cache the result keyed by its inputs and
  use a `dcc.Store` "signal" to tell dependent callbacks the result is ready. This keeps the
  expensive step to one process instead of duplicating it per callback. A filesystem backend
  must use a shared, persistent volume to work across replicas; use Redis or another shared
  cache service when replicas have isolated or ephemeral filesystems.
4. **Per-user server-side cache**: when data must stay isolated per user but is too large/slow
   to round-trip through the browser, cache it server-side keyed by a session id stored in
   `dcc.Store`. Faster than shipping the data to the browser and back, but the session id in
   `dcc.Store` is not encrypted — treat it like any other client-controlled value (see OWASP
   session-fixation concerns before relying on it for anything sensitive).

`storage_type` on `dcc.Store` controls browser persistence: `memory` (default, cleared on
refresh), `local` (until manually cleared), `session` (until the tab closes).

## Multi-page apps

**Dash Pages** (`use_pages=True`, Dash ≥2.5) is the default way to build multi-page apps:

```
app.py
pages/
    home.py
    analytics.py
```

```python
# pages/analytics.py
import dash
from dash import html, dcc, callback, Input, Output

dash.register_page(__name__)   # path inferred as /analytics

layout = html.Div([...])

@callback(Output('analytics-output', 'children'), Input('analytics-input', 'value'))
def update_city_selected(input_value):
    return f'You selected: {input_value}'
```

```python
# app.py
import dash
from dash import Dash, html

app = Dash(__name__, use_pages=True)
app.layout = html.Div([dash.page_container])

if __name__ == '__main__':
    app.run(debug=True)
```

- `layout` can be a variable or a function (receives query-string/path variables as kwargs;
  include `**kwargs` defensively). Only `app.py` should set `app.layout`.
- `dash.page_registry` lists every registered page (path, title, name, order, meta image); use
  it to build nav links.
- `path_template="/report/<report_id>"` captures URL segments as layout kwargs (always `str`).
  Query-string parameters are captured the same way.
- `redirect_from=[...]` on `register_page` keeps old links working after a path change.
- A `pages/not_found_404.py` with `dash.register_page(__name__)` overrides the default 404.
- **Circular imports**: a page that does `from app import app` to get the `app` object will
  fail because `app.py` imports the pages package first. Use `callback` (module-level import
  from `dash`) instead of `app.callback`, and `dash.get_app()`/`dash.get_asset_url()` instead of
  importing `app` directly.
- `suppress_callback_exceptions=True` skips Dash's layout validation for components declared
  outside the initial layout — needed for larger apps where validating cost matters, but it
  also hides genuine ID/typo errors, so don't set it by default.

For apps still on an older Dash without Pages, `dcc.Location` + `dcc.Link` plus a callback that
swaps `page-content` based on `pathname` gives the same routing manually; `app.validation_layout`
can hold the full set of components across pages for validation without eagerly rendering them.

## Performance

- **Memoization**: `functools.lru_cache` is thread-safe, but is local to each Python process.
  It can be appropriate for a pure function in one process, or when duplicate computation across
  workers is acceptable. For cache reuse across workers, replicas, or sessions, use a shared
  cache (Flask-Caching with Redis or filesystem, `@cache.memoize`) instead, and prefer caching
  the underlying data-fetching function over the callback itself for finer control.
- **Graphs**: Plotly's SVG rendering gets slow above roughly 15k points; use `scattergl` for
  large scatter plots and benchmark aggregation or downsampling for the remaining chart types.
  Plotly 6 removed `pointcloud` and `heatmapgl`; use `heatmap` for matrix data instead.
- **Clientside callbacks** cut server round trips for cheap, pure transforms (see
  [callbacks reference](./callbacks.md#clientside-callbacks)).
- **Background callbacks** move slow work off the request/response path entirely (see
  [callbacks reference](./callbacks.md#background-callbacks)). `progress` and `set_props`
  report status; they do not cache results. To reuse background-callback results, configure the
  manager with `cache_by` and an appropriate expiry, including user identity in the cache key
  when results must remain private.
- **Partial property updates**: Python `dash.Patch()` (Dash ≥2.9) and clientside
  `new dash_clientside.Patch` (Dash ≥3.3) update only the changed part of a large property
  (e.g. one field of a figure) instead of re-sending the whole thing.
- **`orjson`**, if installed, is used automatically by Dash to speed up JSON (de)serialization
  for callback payloads — no code change needed beyond `pip install orjson`.

## Testing

**Unit tests** (Dash ≥2.6, `pip install pytest`) call the callback function directly — no browser
needed:

```python
# app.py
@callback(Output('container-no-ctx', 'children'), Input('btn-1', 'n_clicks'), Input('btn-2', 'n_clicks'))
def update(btn1, btn2):
    return f'button 1: {btn1} & button 2: {btn2}'
```

```python
# test_app_callbacks.py
from app import update

def test_update_callback():
    assert update(1, 0) == 'button 1: 1 & button 2: 0'
```

If the callback reads `ctx.triggered_id`, mock it with `contextvars`:

```python
from contextvars import copy_context
from dash._callback_context import context_value
from dash._utils import AttributeDict
from app import display

def test_display_callback():
    def run_callback():
        context_value.set(AttributeDict(triggered_inputs=[{"prop_id": "btn-1.n_clicks"}]))
        return display(1, 0, 0)

    output = copy_context().run(run_callback)
    assert output == 'You last clicked button with ID btn-1'
```

**End-to-end tests** (`pip install "dash[testing]>=2.6"` plus a WebDriver, e.g. ChromeDriver) use
the `dash_duo` pytest fixture (Selenium + a real browser) for cases where interaction order or
actual DOM state matters — slower and more setup but closer to what the user experiences:

```python
def test_001_child_with_0(dash_duo):
    app = dash.Dash()
    app.layout = html.Div(id="nully-wrapper", children=0)
    dash_duo.start_server(app)
    dash_duo.wait_for_text_to_equal("#nully-wrapper", "0", timeout=4)
    assert dash_duo.get_logs() == [], "browser console should contain no error"
```

Run with `pytest`; add `--headless` to avoid opening a visible browser, `-k <id>` to select one
test.

## Deployment

The examples bundled with this skill are local-development examples. They intentionally do not
define a production entry point because server backends, process managers, container layouts,
and managed hosting configuration vary by project.

Dash apps are stateless by design so they can scale horizontally. For a Flask-backed project
that chooses Gunicorn, expose `server = app.server` in the actual application module and target
that module and variable, for example `gunicorn app:server --workers 8`. Other backends and
hosting platforms require different entry points and process models. In every case, assume any
callback can run on any available worker; global mutable state remains unsafe (see
[sharing data between callbacks](#sharing-data-between-callbacks)).

Plotly documents two managed hosting options for publishing an app beyond `localhost` — Plotly
Cloud and Dash Enterprise — both handling access control, logs, and scaling; consult the
current [Dash deployment guide](https://dash.plotly.com/deployment) for their setup steps and
current feature set rather than assuming capabilities not confirmed there.
