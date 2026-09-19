---
name: dash
description: >-
  Use when building, reviewing, or debugging Plotly Dash apps: laying out pages with
  dash.html/dash.dcc, wiring callbacks (Input/Output/State, chained callbacks, pattern-matching
  ALL/MATCH, duplicate outputs), sharing data safely between callbacks, structuring multi-page
  apps with Dash Pages, or diagnosing slow, stuck, or inconsistent callback behaviour. Produces a
  stateless callback graph, a data-sharing strategy appropriate to payload size and concurrency,
  and a test/deployment plan. Dash app development only, not general Plotly chart authoring or
  non-Dash web frameworks.
compatibility: Supports Dash 2.9 through 4.x; the bundled example is verified on Dash 4.4.1. Version-gate features added after 2.9 as noted in the references.
metadata:
  skill-author: 'Marie-Lynne Block'
  version: '1.0.2'
---

# Dash App Development

Build interactive, reactive web apps with Dash. Dash apps are stateless: every callback
must be safe to run on any worker, in any order, without depending on state left behind
by another callback or another user's session. Most Dash bugs — inconsistent output,
data leaking between users, apps that stop scaling — trace back to breaking this rule.

## When to use it

- Structuring a new Dash app's layout and callback graph
- Wiring interactivity: `Input`/`Output`/`State`, chained callbacks, multiple inputs/outputs
- Handling a variable/dynamic number of components with pattern-matching callbacks (`ALL`, `MATCH`, `ALLSMALLER`)
- Sharing data between callbacks without global variables (`dcc.Store`, server-side caching)
- Building or restructuring a multi-page app with Dash Pages
- Diagnosing "duplicate callback outputs", circular imports, callbacks firing in the wrong order, or data from one user showing up for another
- Deciding between a normal callback, a clientside callback, and a background callback
- Adding tests for callbacks before shipping

Not for: authoring the underlying Plotly figures themselves (see Plotly Express/graph_objects
docs), non-Dash Flask/FastAPI apps, or Dash Enterprise-only features beyond what is documented
on the public Dash Python User Guide. This skill also does not cover the visual or accessibility
design of the dashboard (layout strategy, colour semantics, KPI panel critique) — only the
callback wiring and data architecture underneath.

## Workflow

1. **Establish the interaction contract.** Before writing code, decide: what does the user
   see and change (layout/components), what triggers a re-render vs. what's read only on
   submit (`Input` vs `State`), what data must survive between callbacks or page loads
   (browser session vs. server-side), and whether this is a single page or needs routing.
   Ask about concurrency (single analyst vs. many simultaneous users) — it decides whether
   global variables are merely bad practice or an active data-leak risk.

2. **Structure the layout.** Compose `dash.html` (HTML tags) and `dash.dcc` (interactive
   components) into a tree assigned to `app.layout`. Give every component that a callback
   references a stable `id`. Extract repeated markup into small functions that return
   components rather than copy-pasting blocks. See [layout and reusable components](./references/architecture.md#layout).

3. **Wire callbacks with the right shape.** For each reactive relationship, decide:
   - `Input` (fires the callback) vs. `State` (read but doesn't fire it) — see
     [State vs Input](./references/callbacks.md#state-vs-input).
   - One callback with multiple outputs (only when they share an expensive computation and
     should always update together) vs. separate callbacks (when inputs differ, or outputs
     should update independently/in parallel) — see [combining outputs](./references/callbacks.md#multiple-inputsoutputs).
   - Chained callbacks when one component's options depend on another's value — see
     [chained callbacks](./references/callbacks.md#chained-callbacks).
   - `ctx.triggered_id` when several inputs feed one output and you need to branch on which
     one fired, instead of guessing from values — see [determining the trigger](./references/callbacks.md#which-input-triggered).
   - A dict `id` plus `ALL`/`MATCH`/`ALLSMALLER` when the number of components is dynamic
     (added/removed at runtime) — see [pattern-matching callbacks](./references/callbacks.md#pattern-matching-callbacks).

4. **Never mutate state outside a callback's scope.** Callbacks must not modify module-level
   variables, dataframes, or caches that other sessions/workers read — Dash runs across
   multiple processes/threads with no shared memory by default, so this silently corrupts
   results for other users. Reassign to a new local variable instead. For anything that must
   persist across callbacks, pick a sharing strategy sized to the data:
   - Small, session-scoped values → `dcc.Store` (browser-side, JSON-serialized).
   - Expensive results reused by several callbacks → compute once and store the
     precomputed/aggregated result, not the full raw dataset.
   - Large or genuinely shared state → a server-side cache (e.g. Flask-Caching with Redis or
     filesystem), keyed by a session id stored in `dcc.Store` if it must stay per-user.
   Full trade-offs and code: [sharing data between callbacks](./references/architecture.md#sharing-data-between-callbacks).

5. **Pick the execution model for cost and scale.** Default to a normal server-side callback.
   Move to a **clientside callback** only for cheap, pure transforms where round-trip latency
   or payload size dominates (it blocks the browser's main thread and can't touch server
   state/DB connections). Move to a **background callback** (`background=True` with a
   `DiskcacheManager` locally, `CeleryManager`+Redis in production) for anything that risks a
   ~30s timeout or would tie up a web worker. See
   [performance and execution models](./references/architecture.md#performance).

6. **Add routing only when the app needs more than one page.** Prefer Dash Pages
   (`use_pages=True`, `dash.register_page`, `dash.page_container`) over hand-rolled
   `dcc.Location` routing unless you're constrained to an older Dash version. Watch for the
   circular-import trap when a page needs the `app` object. See
   [multi-page apps](./references/architecture.md#multi-page-apps).

7. **Test before shipping.** Unit-test callback functions directly by importing and calling
   them (mock `ctx.triggered_id` via `contextvars` when the logic depends on it). Add
   `dash.testing` end-to-end tests only where interaction order or real DOM state matters.
   See [testing](./references/architecture.md#testing).

8. **State the deployment model explicitly.** Production topology is project-specific: identify
  the actual server backend, entry point, worker model, and hosting platform instead of deriving
  them from a local example. Any callback may execute on any available worker, so confirm the app
  has no assumptions that break under that model before calling it done. See
  [deployment](./references/architecture.md#deployment).

## Output format

- A short interaction contract: what triggers what, what State only reads, what must persist and where
- The layout tree and callback definitions (or a diff against the existing app)
- The data-sharing/execution-model choice made, with the reason (payload size, concurrency, latency)
- Tests added or run, and what remains unverified (e.g. "unit-tested the callback logic; did not run browser e2e")

## Examples

### Example 1 — dynamic filter list with shared aggregate

**Input:** "Users can add any number of city filters; each should read from a dataset that's
expensive to compute once, cheap to reuse. Multiple users will use this at once."
**Expected output:** A layout with an "Add filter" button producing pattern-matching
(`ALL`) dropdowns, a `dcc.Store` holding the precomputed aggregate keyed off the shared inputs,
and a graph callback that filters that aggregate without recomputing it. See the runnable version
in [examples/app.py](./examples/app.py).

### Example 2 — "why did my second callback overwrite the first?"

**Input:** "I have two buttons that both need to update the same graph, and Dash complains
about duplicate callback outputs."
**Expected output:** A recommendation to combine the callback and branch on
`ctx.triggered_id` (preferred when only one should ever be "live"), or use
`allow_duplicate=True` with `prevent_initial_call=True` when the callbacks must stay separate
— with an explicit note that update order between duplicate outputs isn't guaranteed. See
[duplicate outputs](./references/callbacks.md#duplicate-outputs).

## Notes

- Prefer the documented `dash`, `dash.html`, `dash.dcc` APIs; don't invent component props or
  callback arguments that aren't in the current Dash User Guide.
- A `dcc.Store` payload is still transported over the network on every callback that reads
  it — for large data, store aggregates/subsets, not the full frame. Treat it as untrusted
  input on the way back in: validate shape before indexing into it.
- `allow_duplicate=True` requires `prevent_initial_call=True` on that callback, or
  `Dash(prevent_initial_callbacks="initial_duplicate")` on the app.
- The bundled [example app](./examples/app.py) is for local development; production entry points,
  process managers, and hosting configuration belong to the consuming project.
- Reference files: [callbacks](./references/callbacks.md) (callback wiring patterns) and
  [architecture](./references/architecture.md) (layout, data sharing, multi-page, performance,
  testing, deployment). Runnable example: [examples/app.py](./examples/app.py) with tests in
  [examples/test_app.py](./examples/test_app.py).
