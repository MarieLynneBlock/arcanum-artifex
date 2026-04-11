# Testing — Figure Functions, Callbacks, and Snapshot Regression

Dash apps are notoriously undertested. The most effective strategy targets three layers:
pure figure functions (fast, high value), callback logic (medium complexity), and snapshot
regression (catches unintended visual changes). Cover all three.

---

## Layer 1 — Figure function unit tests

Figure functions are pure (`DataFrame` in, `go.Figure` out) — they are the easiest and highest-value
tests to write. No Dash server needed.

```python
# tests/test_charts.py
import pytest
import pandas as pd
import plotly.graph_objects as go
from components.charts import make_trend_chart, make_status_bars

# Minimal synthetic fixture — never use real data in tests
@pytest.fixture
def revenue_df():
    return pd.DataFrame({
        "date":    pd.date_range("2024-01-01", periods=6, freq="MS"),
        "revenue": [4.1, 4.3, 3.9, 4.5, 4.8, 5.1],
    })

class TestMakeTrendChart:
    def test_returns_figure(self, revenue_df):
        fig = make_trend_chart(revenue_df, "revenue", "Revenue trend")
        assert isinstance(fig, go.Figure)

    def test_has_one_trace(self, revenue_df):
        fig = make_trend_chart(revenue_df, "revenue", "Revenue trend")
        assert len(fig.data) == 1

    def test_title_is_set(self, revenue_df):
        fig = make_trend_chart(revenue_df, "revenue", "My insight title")
        # Title is wrapped in bold HTML tags — assert on the full string
        assert fig.layout.title.text == "<b>My insight title</b>"

    def test_hovertemplate_is_set(self, revenue_df):
        """Default hover is never good enough — verify it's been customised."""
        fig = make_trend_chart(revenue_df, "revenue", "Revenue trend")
        assert fig.data[0].hovertemplate is not None
        assert "<extra></extra>" in fig.data[0].hovertemplate

    def test_empty_dataframe_returns_figure(self):
        """Empty state must return a figure, not raise."""
        empty_df = pd.DataFrame(columns=["date", "revenue"])
        fig = make_trend_chart(empty_df, "revenue", "Revenue trend")
        assert isinstance(fig, go.Figure)

    def test_no_inline_hex_in_traces(self, revenue_df):
        """Colour must come from the template colorway — not be hardcoded per trace."""
        fig = make_trend_chart(revenue_df, "revenue", "Revenue trend")
        for trace in fig.data:
            colour = getattr(getattr(trace, "line", None), "color", None)
            if colour:
                assert not colour.startswith("#"), \
                    f"Inline hex found in trace: {colour}. Import from colours.py."


class TestMakeStatusBars:
    @pytest.fixture
    def status_df(self):
        return pd.DataFrame({
            "region":  ["London", "Manchester", "Bristol", "Leeds"],
            "pct":     [72.1, 65.4, 80.3, 58.9],
        })

    def test_reference_line_at_target(self, status_df):
        fig = make_status_bars(status_df, "region", "pct", target=75.0, title="Performance")
        hlines = [s for s in fig.layout.shapes if s.type == "line"]
        assert any(abs(s.y0 - 75.0) < 0.01 for s in hlines), "Target reference line not found"

    def test_conditional_colours_applied(self, status_df):
        """Bars below target must use the 'bad' signal colour."""
        from colours import NORD_SIGNAL
        fig = make_status_bars(status_df, "region", "pct", target=75.0, title="Performance")
        colours = fig.data[0].marker.color
        # Manchester (65.4) and Leeds (58.9) are below target
        assert colours[1] == NORD_SIGNAL["bad"]
        assert colours[3] == NORD_SIGNAL["bad"]
```

### Minimum test matrix per figure function

| Test | Required |
|---|---|
| Returns `go.Figure` | ✅ always |
| Correct number of traces | ✅ always |
| Title is set | ✅ always |
| `hovertemplate` is customised | ✅ always |
| Empty DataFrame returns figure (not exception) | ✅ always |
| No inline hex on traces | ✅ always |
| Reference lines at correct y-value | if chart uses `add_hline` |
| Correct conditional colours | if chart uses signal colouring |
| Correct number of annotations | if chart uses `add_annotation` |

---

## Layer 2 — Callback logic tests

Use `dash.testing` for integration tests. These require a browser driver (Playwright or Selenium)
and are slower — run in CI, not on every save.

```python
# tests/test_callbacks.py
import pytest
from dash.testing.application_runners import import_app
from dash.testing.composite import DashComposite

@pytest.fixture
def dash_app():
    app = import_app("app")
    return app

def test_filter_updates_chart(dash_duo, dash_app):
    """Changing region filter must update the chart."""
    dash_duo.start_server(dash_app)

    # Wait for initial load
    dash_duo.wait_for_element("#revenue-chart", timeout=10)

    # Change filter
    dash_duo.find_element("#region-filter").send_keys("London")
    dash_duo.wait_for_element_by_id("revenue-chart")   # re-render triggered

    # Verify no error state
    page_text = dash_duo.driver.page_source
    assert "Could not load data" not in page_text

def test_empty_filter_shows_empty_state(dash_duo, dash_app):
    """A filter with no results must show the empty state message, not a blank chart."""
    dash_duo.start_server(dash_app)
    # Trigger an empty result by selecting a filter with no data
    dash_duo.find_element("#region-filter").send_keys("NONEXISTENT_REGION")
    dash_duo.wait_for_text_to_equal("#revenue-chart .annotation-text",
                                    "No data for this selection.", timeout=5)
```

### Callback test matrix

| Scenario | Test |
|---|---|
| Default load | Chart renders, no error state |
| Valid filter selection | Chart updates |
| Filter with no results | Empty state shown, not blank |
| Filter reset | Returns to default view |
| Multiple rapid filter changes | Final state is correct (no race condition) |
| Data loader raises exception | Error chart shown, not unhandled 500 |

---

## Layer 3 — Snapshot / regression tests

Catch unintended visual changes — layout shifts, missing traces, colour regressions.

```python
# tests/test_snapshots.py
import pytest
import pandas as pd
import json
from components.charts import make_trend_chart

@pytest.fixture
def revenue_df():
    return pd.DataFrame({
        "date":    pd.date_range("2024-01-01", periods=6, freq="MS"),
        "revenue": [4.1, 4.3, 3.9, 4.5, 4.8, 5.1],
    })

SNAPSHOT_DIR = "tests/snapshots"

def test_trend_chart_snapshot(revenue_df, snapshot):
    """
    Requires pytest-snapshot: pip install pytest-snapshot
    First run: pytest --snapshot-update  (generates baseline)
    Subsequent runs: pytest  (compares against baseline)
    """
    fig = make_trend_chart(revenue_df, "revenue", "Revenue trend")
    # Snapshot the JSON spec — catches trace count, layout, colour changes
    fig_json = json.loads(fig.to_json())
    snapshot.assert_match(json.dumps(fig_json, sort_keys=True, indent=2),
                          "trend_chart.json")
```

Install: `pip install pytest-snapshot`
Generate baseline: `pytest tests/test_snapshots.py --snapshot-update`
Run comparisons: `pytest tests/test_snapshots.py`

**What snapshots catch**: added/removed traces, title changes, layout property changes, colour changes if
colours are hardcoded (another reason to import from `colours.py` — a single change updates all snapshots predictably).

**What snapshots don't catch**: rendering bugs, font rendering, pixel-level differences. For those,
use Playwright's visual comparison mode.

---

## CI configuration

Minimum test pipeline for a production Dash app:

```yaml
# .github/workflows/test.yml
name: Tests

on: [push, pull_request]

jobs:
  unit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: {python-version: "3.11"}
      - run: pip install -r requirements-dev.txt
      - run: pytest tests/test_charts.py tests/test_snapshots.py -v

  integration:
    runs-on: ubuntu-latest
    needs: unit     # only run if unit tests pass
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: {python-version: "3.11"}
      - run: pip install -r requirements-dev.txt
      - run: playwright install chromium
      - run: pytest tests/test_callbacks.py -v
```

```
# requirements-dev.txt (in addition to requirements.txt)
pytest>=7.0
pytest-snapshot
playwright
pytest-playwright
```

---

## Testing checklist

```
□ All figure functions have: returns-Figure, trace-count, title, hovertemplate, empty-state, no-inline-hex tests
□ Snapshot baselines generated and committed for all primary charts
□ Callback tests cover: default load, valid filter, empty filter, error state
□ CI runs unit tests on every push
□ CI runs integration tests before merge to main
□ Snapshot diffs reviewed in PRs — unintended visual changes blocked from merge
□ Test fixtures use synthetic data only — no production data in tests
```
