# Chart Selection — Extended Reference

Drawn from Abela's Chart Chooser framework and the ActiveWizards variable-count decision tree.

## Primary Decision: How many variables?

### Single variable
Ask: Is it ordered (has a natural sequence — time, rank, rating)?

- **Yes, ordered**: Line chart (time), area chart (cumulative), box/violin (distribution across ordered groups)
- **No, not ordered**: 
  - Distribution of values → Histogram or density plot
  - Spread and outliers → Box plot
  - Central tendency comparison → Bar chart

### Two or more variables

Ask: Are the variables of the *same type* (similar scale, measuring related things)?

#### No — different variables (e.g. price vs volume, sales vs satisfaction)
- **Both unordered** → Scatter plot
- **One ordered (time)** → Line chart or area chart; connected scatter plot if trajectory matters
- **Showing flow/transfer between states** → Sankey diagram

#### Yes — similar variables (e.g. multiple metrics, multiple categories)

Ask: Is there a hierarchy (parent → child relationships)?

- **Has hierarchy**: Venn diagram (overlap/membership), Sunburst or Treemap (part-of-whole with nesting)
- **No hierarchy**: 
  - Not ordered → Heatmap (dense), Stacked bars, Treemap, Pie (≤4 slices only)
  - Ordered → Stacked area chart, Stacked line chart

---

## Decision by Intent

### Comparison
"How does A compare to B?"

| Scenario | Chart |
|---|---|
| Few items, few categories | Bar chart (horizontal if long labels) |
| Many items | Dot plot or ranked table |
| Over time, few periods | Column chart |
| Over time, many periods | Line chart |
| Multiple metrics per item | Radar/spider chart (use cautiously — angle distorts) |
| Two variables per item | Scatter plot, bubble chart |

### Distribution
"What's the spread of this variable?"

| Scenario | Chart |
|---|---|
| Few data points | Strip plot or dot plot |
| Many data points | Histogram |
| Comparing distributions across groups | Violin plot (shows shape) or box plot (shows quartiles) |
| Two variables | 2D histogram, density contour |

### Composition (part-of-whole)
"What makes up the total?"

| Scenario | Chart |
|---|---|
| Simple share of total, static | Pie chart (≤4 slices) or donut. Use a bar chart for > 4. |
| Static, many components | Stacked 100% bar or treemap |
| Changing over time | Stacked area (relative); stacked bar (absolute) |
| Accumulation / waterfall | Waterfall chart |
| Nested hierarchy | Sunburst or treemap |
| Components of components | Stacked 100% column with subcomponents |

### Relationship
"Is there a correlation or pattern between variables?"

| Scenario | Chart |
|---|---|
| Two variables | Scatter plot |
| Three variables | Bubble chart (size = 3rd var) or scatter with colour encoding |
| Many variables | Heatmap (correlation matrix), parallel coordinates |
| Network structure | Network graph (use sparingly — complexity hides insight) |

### Over Time
"How does this change?"

| Scenario | Chart |
|---|---|
| Single metric, continuous | Line chart |
| Single metric, discrete periods | Column chart |
| Cumulative | Area chart |
| Cyclical data | Circular/polar area chart, or line chart with cycle annotations |
| Multiple series, similar scale | Multi-line chart |
| Multiple series, different scales | Small multiples (NOT dual axis) |
| Showing individual data points and trend | Connected scatter plot |

---

## Edge Cases and Gotchas

**When NOT to use a line chart**: Categorical x-axis with no order (e.g. cities). Use bar chart. Lines imply continuity.

**When a pie chart is acceptable**: Exactly 2–4 slices, difference between slices is visually obvious, percentages sum to 100. Add direct labels — never rely on a legend alone for pie.

**Heatmaps require careful ordering**: Always cluster rows/columns meaningfully (hierarchical clustering, or sort by a key variable). A random-order heatmap is noise.

**Box plots vs violin plots**: Box plots communicate quartile statistics efficiently. Violin plots show distributional shape — prefer violin when the shape (bimodal, skewed) is the story.

**Scatter plots with many points**: At > ~5,000 points, use hexbin or 2D density plot. Overplotted scatter reads as a blob.

**Treemaps**: Good for hierarchical proportions. Poor for comparing sizes across different hierarchy levels. Label only the largest cells.

**Sankey diagrams**: Reserve for genuine flow data (money, energy, users through a funnel). Don't force non-flow data into one.

**Tables are valid**: When the user needs to look up exact values, or when there are many categories with small differences, a well-designed table beats any chart. Use `dash_table.DataTable` with conditional formatting.

---

## Small Multiples Pattern

When you have multiple series that would create a cluttered single chart — use small multiples (trellis/facet):

```python
import plotly.express as px

fig = px.line(
    df,
    x="date",
    y="value",
    facet_col="category",
    facet_col_wrap=3,
)
fig.update_yaxes(matches=None)  # independent y-axes if scales differ
fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
```

Small multiples are almost always better than dual-axis charts for multi-series comparison.
