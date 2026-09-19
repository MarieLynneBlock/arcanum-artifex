"""Local-development Dash example: shared aggregate store, dynamic pattern-matching filters,
and a single callback that branches on ctx.triggered_id instead of duplicating an output.

Production entry points and server configuration are intentionally project-specific.

From this examples/ directory, run:
pip install "dash>=2.9,<5" "pandas>=2.1" "plotly>=5"
python app.py
Then open http://127.0.0.1:8050/
"""

from __future__ import annotations

import io

import pandas as pd
import plotly.express as px
from dash import ALL, Dash, Input, Output, Patch, callback, ctx, dcc, html

# Synthetic dataset (no external fetch, no I/O) so the example runs offline.
SALES = pd.DataFrame(
    {
        "region": ["North", "North", "South", "South", "East", "East", "West", "West"] * 3,
        "category": (["Widgets"] * 8 + ["Gadgets"] * 8 + ["Gizmos"] * 8),
        "amount": [120, 90, 150, 80, 60, 110, 95, 70, 200, 60, 40, 90, 130, 55, 30, 45,
                   80, 65, 100, 75, 50, 85, 40, 60],
    }
)

app = Dash(__name__)

app.layout = html.Div(
    [
        html.H2("Regional sales explorer"),
        # --- Shared aggregate, computed once per category and reused by both chart buttons ---
        dcc.Dropdown(
            options=sorted(SALES["category"].unique()),
            value="Widgets",
            id="category-dropdown",
        ),
        dcc.Store(id="category-aggregate-store"),
        # Persists the user's chart-type choice so it survives unrelated re-renders
        # (category change, filter change) instead of resetting to bar every time.
        dcc.Store(id="chart-mode-store", data="bar"),
        html.Button("Show as bar chart", id="show-bar-btn", n_clicks=0),
        html.Button("Show as line chart", id="show-line-btn", n_clicks=0),
        dcc.Graph(id="sales-graph"),
        html.Hr(),
        # --- Dynamic, pattern-matching region filters ---
        html.Button("Add region filter", id="add-filter-btn", n_clicks=0),
        html.Div(id="filter-container-div", children=[]),
        html.Div(id="filter-summary-div"),
    ]
)


@callback(
    Output("category-aggregate-store", "data"),
    Input("category-dropdown", "value"),
)
def compute_category_aggregate(category):
    """Compute the (here, cheap; in practice expensive) aggregate once per category change."""
    aggregate = (
        SALES[SALES["category"] == category]
        .groupby("region", as_index=False)["amount"]
        .sum()
    )
    return aggregate.to_json(orient="split")


@callback(
    Output("chart-mode-store", "data"),
    Input("show-bar-btn", "n_clicks"),
    Input("show-line-btn", "n_clicks"),
    prevent_initial_call=True,
)
def set_chart_mode(_bar_clicks, _line_clicks):
    """Record which chart type the user last asked for, separately from rendering it.

    Keeping this choice in its own store (rather than reading ctx.triggered_id inside
    render_sales_graph) means the mode survives re-renders triggered by something else,
    e.g. a category or region-filter change, instead of silently reverting to bar.
    """
    return "line" if ctx.triggered_id == "show-line-btn" else "bar"


@callback(
    Output("sales-graph", "figure"),
    Input("chart-mode-store", "data"),
    Input("category-aggregate-store", "data"),
    Input({"type": "region-filter", "index": ALL}, "value"),
)
def render_sales_graph(chart_mode, aggregate_json, selected_regions):
    """One callback, one output: read the stored chart mode instead of registering the
    same Output on two separate callbacks (see duplicate-outputs).

    Region filters consume the aggregate in dcc.Store, rather than recomputing it.
    """
    if aggregate_json is None:
        return px.bar()

    dff = pd.read_json(io.StringIO(aggregate_json), orient="split")
    # dcc.Store round-trips through the browser and is client-controlled input — validate
    # its shape before indexing into it, the same as any other external input.
    if not {"region", "amount"}.issubset(dff.columns):
        return px.bar()

    selected_regions = [region for region in selected_regions if region]
    if selected_regions:
        dff = dff[dff["region"].isin(selected_regions)]

    if chart_mode == "line":
        return px.line(dff, x="region", y="amount", markers=True)
    return px.bar(dff, x="region", y="amount")


@callback(
    Output("filter-container-div", "children"),
    Input("add-filter-btn", "n_clicks"),
    prevent_initial_call=True,
)
def add_region_filter(n_clicks):
    """Append one more pattern-matching dropdown each time the button is clicked."""
    patched_children = Patch()
    patched_children.append(
        dcc.Dropdown(
            options=sorted(SALES["region"].unique()),
            id={"type": "region-filter", "index": n_clicks},
            style={"maxWidth": 240},
        )
    )
    return patched_children


@callback(
    Output("filter-summary-div", "children"),
    Input({"type": "region-filter", "index": ALL}, "value"),
)
def summarize_filters(values):
    """Summarize the filters that also drive the aggregate-backed graph."""
    selected = [v for v in values if v]
    if not selected:
        return "No region filters selected."
    return f"Filtering on: {', '.join(selected)}"


if __name__ == "__main__":
    # debug=True is for local development only — never enable it in a deployed app.
    app.run(debug=True)
