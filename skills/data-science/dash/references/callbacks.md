# Callback Patterns

All examples assume `from dash import Dash, dcc, html, Input, Output, State, ctx, callback`
unless noted. `@callback` (module-level, since Dash 2.0) is used instead of `@app.callback` so
callbacks can live in separate files without importing the `app` object.

## Anatomy and initial call

```python
@callback(
    Output('my-output', 'children'),
    Input('my-input', 'value'),
)
def update_output_div(input_value):
    return f'Output: {input_value}'
```

- Inputs/outputs are `(component_id, component_property)` pairs, not the components themselves.
- On app start, Dash calls every callback once with the initial values of its `Input`s to
  populate outputs. Don't set a conflicting initial value on the output component in the
  layout — it will be immediately overwritten.
- Set `prevent_initial_call=True` on the `@callback` decorator to skip that first firing
  (required alongside `allow_duplicate=True`, see [Duplicate outputs](#duplicate-outputs)).

## State vs Input

`Input` fires the callback on every change. `State` is passed into the callback but never
triggers it — use it for "read the form, but only on submit" patterns:

```python
@callback(
    Output('output-state', 'children'),
    Input('submit-button-state', 'n_clicks'),
    State('input-1-state', 'value'),
    State('input-2-state', 'value'),
)
def update_output(n_clicks, input1, input2):
    return f'Button pressed {n_clicks} times, Input 1 is "{input1}", Input 2 is "{input2}"'
```

Typing in the two `dcc.Input`s above does not fire the callback; clicking the button does, and
the current input values are still available as arguments.

## Multiple Inputs/Outputs

Any output can depend on several inputs; Dash passes the current value of every listed
`Input` in declaration order, even though only one changed:

```python
@callback(
    Output('indicator-graphic', 'figure'),
    Input('xaxis-column', 'value'),
    Input('yaxis-column', 'value'),
    Input('year--slider', 'value'),
)
def update_graph(xaxis_column_name, yaxis_column_name, year_value):
    ...
```

A single callback can also return several outputs — list every `Output`, return that many
values, in order:

```python
@callback(
    Output('square', 'children'),
    Output('cube', 'children'),
    Input('num-multi', 'value'),
)
def callback_a(x):
    if x is None:
        return "", ""
    return x ** 2, x ** 3
```

Combine outputs only when they share the same expensive intermediate result (e.g. one slow
query feeding both a graph and a table). Otherwise keep callbacks separate:
- If outputs depend on only *some* of the same inputs, separate callbacks avoid recomputing
  everything when an unrelated input changes.
- If outputs need very different computation from the same inputs, separate callbacks can run
  in parallel.

## Chained callbacks

The output of one callback can be the input of another — useful for dependent option sets:

```python
@callback(Output('cities-radio', 'options'), Input('countries-radio', 'value'))
def set_cities_options(selected_country):
    return [{'label': i, 'value': i} for i in all_options[selected_country]]

@callback(Output('cities-radio', 'value'), Input('cities-radio', 'options'))
def set_cities_value(available_options):
    return available_options[0]['value']

@callback(
    Output('display-selected-values', 'children'),
    Input('countries-radio', 'value'),
    Input('cities-radio', 'value'),
)
def set_display_children(selected_country, selected_city):
    return f'{selected_city} is a city in {selected_country}'
```

Dash waits for `cities-radio`'s `value` to update before calling `set_display_children`, so it
never runs with a mismatched pair like `("America", "Montréal")`.

## Which input triggered

When several `Input`s feed one callback and the response depends on *which one* changed, use
`ctx.triggered_id` (import `ctx` from `dash`) instead of inferring it from values:

```python
from dash import ctx, no_update

@callback(
    Output('graph', 'figure'),
    Input('reset', 'n_clicks'),
    Input('draw', 'n_clicks'),
    prevent_initial_call=True,
)
def update_graph(_reset_clicks, _draw_clicks):
    if ctx.triggered_id == 'reset':
        return reset_graph()
    if ctx.triggered_id == 'draw':
        return draw_graph()
    return no_update
```

`ctx.triggered_prop_ids`, `ctx.triggered`, `ctx.inputs`, `ctx.inputs_list`, and
`ctx.outputs_list` expose more detail (useful with pattern-matching, see below).

## Duplicate outputs

By default, a given `(component_id, property)` pair can be the `Output` of only one callback —
adding it to two callbacks raises "Duplicate callback outputs" in debug mode.

- **Preferred:** combine the callback and branch on `ctx.triggered_id` (see above). This also
  makes update order deterministic.
- **When callbacks must stay separate:** set `allow_duplicate=True` on every extra `Output`
  targeting that pair, and set `prevent_initial_call=True` on that callback (or
  `Dash(prevent_initial_callbacks="initial_duplicate")` on the app). If two such callbacks can
  fire at the same time, the order they apply is **not guaranteed** — avoid this for outputs
  where partial/racing updates would corrupt state (e.g. two callbacks each patching a
  different part of the same figure).

## Pattern-matching callbacks

Use a **dict `id`** (e.g. `{'type': 'filter-dropdown', 'index': n}`) instead of a string when
the number of matching components is dynamic, then match with `ALL`, `MATCH`, or `ALLSMALLER`
in the callback:

- **`ALL`** — fires whenever any matching component changes; the callback receives a *list* of
  all current values, in DOM order.
  ```python
  @callback(
      Output('dropdown-container-output-div', 'children'),
      Input({'type': 'city-filter-dropdown', 'index': ALL}, 'value'),
  )
  def display_output(values):
      return html.Div([html.Div(f'Dropdown {i + 1} = {v}') for i, v in enumerate(values)])
  ```
- **`MATCH`** — fires per matching component and updates only the one output with the same
  dynamic id part; the callback receives a single value (not a list). Before Dash 4.2, every
  `MATCH` key used in an `Input`/`State` must also appear as `MATCH` in the `Output`. Dash 4.2+
  also permits a fixed-id output, an `ALL`-only output pattern, or no output.
  ```python
  @callback(
      Output({'type': 'city-dynamic-output', 'index': MATCH}, 'children'),
      Input({'type': 'city-dynamic-dropdown', 'index': MATCH}, 'value'),
      State({'type': 'city-dynamic-dropdown', 'index': MATCH}, 'id'),
  )
  def display_output(value, id_):
      return html.Div(f"Dropdown {id_['index']} = {value}")
  ```
- **`ALLSMALLER`** — used with `Input`/`State` alongside `MATCH` in `Output`; passes the values
  of all matching components with a smaller `index` than the one being matched. Useful for
  "filters that narrow progressively" UIs; usually replaceable by `ALL` plus manual filtering,
  but `ALLSMALLER` keeps that logic out of the callback body.

Only the `id` can carry a pattern — component properties (e.g. `value`) can't. Component keys
in the id dict are arbitrary; `type`/`index` is a common, readable convention. On Dash 2.9+, use
`dash.Patch()` to append/patch children in place instead of rebuilding the whole children list
(see [partial property updates](https://dash.plotly.com/partial-properties)).

## Clientside callbacks

Run a callback's logic as JavaScript in the browser instead of a Python round trip. Use this
only when normal callback overhead is the actual bottleneck — large payloads, high call
frequency, or a callback chain requiring multiple round trips — and the logic doesn't need
server state, a database, or global variables (those aren't reachable from the browser):

```python
from dash import clientside_callback

clientside_callback(
    """
    function(largeValue1, largeValue2) {
        return someTransform(largeValue1, largeValue2);
    }
    """,
    Output('out-component', 'value'),
    Input('in-component1', 'value'),
    Input('in-component2', 'value'),
)
```

For larger scripts, define a named function in `assets/*.js` under
`window.dash_clientside.<namespace>.<function_name>` and reference it with
`ClientsideFunction(namespace=..., function_name=...)` instead of an inline string.
`dash_clientside.callback_context.triggered_id` mirrors server-side `ctx.triggered_id`.
Clientside callbacks block the browser's main thread while running and cannot return a
`Promise` before Dash 2.4.

## Background callbacks

For callbacks that risk the ~30s default server timeout, or that would otherwise tie up a web
worker while running, set `background=True` and provide a manager. Install the backend that the
environment uses: `python -m pip install "dash[diskcache]"` for local development, or
`python -m pip install "dash[celery]"` plus a Redis service for production:

```python
import os

from dash import CeleryManager, DiskcacheManager

if 'REDIS_URL' in os.environ:
    from celery import Celery

    celery_app = Celery(__name__, broker=os.environ['REDIS_URL'], backend=os.environ['REDIS_URL'])
    background_callback_manager = CeleryManager(celery_app)
else:
    import diskcache

    background_callback_manager = DiskcacheManager(diskcache.Cache('./cache'))

@callback(
    output=Output('paragraph_id', 'children'),
    inputs=Input('button_id', 'n_clicks'),
    background=True,
    manager=background_callback_manager,
)
def update_clicks(n_clicks):
    ...
```

- `DiskcacheManager` is a simple local-development backend; it is not a queue and is not
  recommended for production.
- `CeleryManager` + Redis queues callbacks and runs them one at a time on dedicated workers —
  the recommended production setup. Start at least one worker separately, for example
  `celery -A app:celery_app worker --loglevel=INFO --concurrency=2`; production deployment must
  run that worker alongside the Dash web process.
- `running=[(Output(...), during_value, after_value), ...]` (Dash ≥2.16) disables/re-enables UI
  elements while the callback runs (e.g. disable the trigger button).
- `cancel=[Input(...)]` cancels an in-flight callback when the given input changes.
- `progress=[Output(...), ...]` plus a `set_progress` first argument reports incremental
  progress (e.g. a progress bar).
- `set_props(component_id, {prop: value})` (Dash ≥2.17) updates a component property from inside
  a background or normal callback without declaring it as an `Output` — but it isn't validated,
  doesn't appear in the callback graph, and doesn't interact with `dcc.Loading`, so it trades
  debuggability for flexibility.
- `progress` and `set_props` report updates only; neither enables result caching. To cache a
  background callback, configure its manager with `cache_by=[...]` and optionally `expire=...`.
  Choose cache-key values that include any user/session discriminator needed to prevent one
  user's result being served to another.
