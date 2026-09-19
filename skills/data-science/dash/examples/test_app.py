"""Unit tests for the callback functions in app.py (no browser/Selenium required).

From this examples/ directory, run:
pip install "dash>=2.9,<5" "pandas>=2.1" "plotly>=5" pytest
pytest test_app.py
"""

from contextvars import copy_context
import io

import pandas as pd
from dash._callback_context import context_value
from dash._utils import AttributeDict

from app import (
    add_region_filter,
    compute_category_aggregate,
    render_sales_graph,
    set_chart_mode,
    summarize_filters,
)


def test_compute_category_aggregate_returns_json_per_region():
    aggregate_json = compute_category_aggregate("Widgets")
    dff = pd.read_json(io.StringIO(aggregate_json), orient="split")
    assert set(dff["region"]) == {"North", "South", "East", "West"}
    assert dff["amount"].sum() > 0


def _run_with_triggered_id(triggered_id, fn, *args):
    def run_callback():
        context_value.set(
            AttributeDict(triggered_inputs=[{"prop_id": f"{triggered_id}.n_clicks"}])
        )
        return fn(*args)

    return copy_context().run(run_callback)


def test_set_chart_mode_branches_on_triggered_id():
    assert _run_with_triggered_id("show-bar-btn", set_chart_mode, 1, 0) == "bar"
    assert _run_with_triggered_id("show-line-btn", set_chart_mode, 1, 1) == "line"


def test_render_sales_graph_uses_stored_mode_not_last_trigger():
    """The chart mode must survive a re-render triggered by the category or a region
    filter, not just by the chart-type buttons — regression coverage for a bug where the
    chart silently reverted to bar on any non-button trigger."""
    aggregate_json = compute_category_aggregate("Widgets")

    bar_figure = render_sales_graph("bar", aggregate_json, [])
    line_figure = render_sales_graph("line", aggregate_json, [])
    # Simulates a region-filter change while "line" mode is already selected: the mode
    # is read from chart-mode-store, not derived from which input just fired.
    filtered_line_figure = render_sales_graph("line", aggregate_json, ["North"])

    assert bar_figure.data[0].type == "bar"
    assert line_figure.data[0].type == "scatter"  # px.line renders as a scatter trace
    assert filtered_line_figure.data[0].type == "scatter"
    assert list(filtered_line_figure.data[0].x) == ["North"]


def test_render_sales_graph_rejects_malformed_store_payload():
    """A dcc.Store payload is client-controlled input; a value missing the expected
    columns must not raise, it should fall back to an empty chart."""
    malformed_json = pd.DataFrame({"unexpected": [1, 2, 3]}).to_json(orient="split")

    figure = render_sales_graph("bar", malformed_json, [])

    assert figure.data[0].x is None
    assert figure.data[0].y is None


def test_add_region_filter_appends_one_dropdown():
    patch = add_region_filter(1)
    # Patch() records operations rather than a plain list; converting to a dict-like
    # operation list confirms exactly one append was queued.
    assert patch.to_plotly_json()["operations"][0]["operation"] == "Append"


def test_summarize_filters_reports_selection():
    assert summarize_filters([None, "North", "South"]) == "Filtering on: North, South"
    assert summarize_filters([None, None]) == "No region filters selected."
