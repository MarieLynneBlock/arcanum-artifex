# Layout and Composition — Reference

## Dashboard Composition Principles

### The Hierarchy Rule
Every dashboard has one primary question it answers. That answer should be visible in < 3 seconds. Everything else is supporting evidence. If you can't identify the primary question, the dashboard isn't ready to build yet.

### Reading patterns
- **F-pattern** (most common): Eyes scan top-left to right, then down-left, repeat. Most important = top-left.
- **Z-pattern** (for lighter content, landing pages): Top-left → top-right → bottom-left → bottom-right.
- For dashboards: use F-pattern. KPIs top row, primary chart second, supporting charts below.

### Visual hierarchy tools
1. **Size**: Larger = more important. Make the primary chart visually dominant.
2. **Position**: Top and left = priority. Bottom-right = least attention.
3. **Colour weight**: Bold colours draw eye before muted ones.
4. **White space**: Generous margin signals "this element is important". Cramped = noise.

---

## Grid Recipes (Dash Bootstrap Components)

### KPI row + 2-chart layout (most common)
```python
layout = dbc.Container([
    # Header
    dbc.Row([
        dbc.Col(html.H2("Dashboard Title", className="text-primary fw-bold"), width=8),
        dbc.Col(dbc.Select(id="time-filter", options=[...]), width=4, className="d-flex align-items-center"),
    ], className="mb-4 mt-3"),

    # KPI cards
    dbc.Row([
        dbc.Col(kpi_card("Total Revenue", "£4.2M", "+12% vs last month", True), width=3),
        dbc.Col(kpi_card("Active Users", "18,432", "+5.3%", True), width=3),
        dbc.Col(kpi_card("Churn Rate", "3.1%", "+0.4pp", False), width=3),
        dbc.Col(kpi_card("NPS Score", "62", "-2pts", False), width=3),
    ], className="mb-4"),

    # Primary chart (full width)
    dbc.Row([
        dbc.Col(
            dbc.Card(dcc.Graph(id="primary-chart", config={"responsive": True}),
                     className="shadow-sm border-0 p-3"),
            width=12
        ),
    ], className="mb-4"),

    # Secondary charts (side by side)
    dbc.Row([
        dbc.Col(
            dbc.Card(dcc.Graph(id="chart-left", config={"responsive": True}),
                     className="shadow-sm border-0 p-3"),
            width=6
        ),
        dbc.Col(
            dbc.Card(dcc.Graph(id="chart-right", config={"responsive": True}),
                     className="shadow-sm border-0 p-3"),
            width=6
        ),
    ], className="mb-4"),

], fluid=True, className="px-4 py-2")
```

### Three-column analytical layout
```python
dbc.Row([
    dbc.Col([sidebar_controls], width=2),
    dbc.Col([primary_chart], width=7),
    dbc.Col([detail_panel], width=3),
])
```
Use when: The dashboard has complex filter controls, or needs a detail/drill-down panel.

### Tabbed multi-topic dashboard
```python
dbc.Tabs([
    dbc.Tab(label="Overview", tab_id="overview", children=[overview_layout]),
    dbc.Tab(label="Revenue", tab_id="revenue", children=[revenue_layout]),
    dbc.Tab(label="Engagement", tab_id="engagement", children=[engagement_layout]),
], id="main-tabs", active_tab="overview")
```
Use when: Topics are distinct and users won't need to compare across them.

---

## Typography Scale

Consistency is everything. Define once, use everywhere:

```python
# Define as constants or CSS variables
TYPOGRAPHY = {
    "h1": dict(fontSize="1.8rem", fontWeight="700", color="#1a202c"),
    "h2": dict(fontSize="1.4rem", fontWeight="600", color="#1a202c"),
    "h3": dict(fontSize="1.1rem", fontWeight="600", color="#2d3748"),
    "body": dict(fontSize="0.95rem", color="#4a5568"),
    "muted": dict(fontSize="0.85rem", color="#718096"),
    "kpi_value": dict(fontSize="2rem", fontWeight="700", color="#1a202c"),
    "kpi_label": dict(fontSize="0.8rem", color="#718096", textTransform="uppercase", letterSpacing="0.05em"),
}
```

Chart titles should use H3 scale. Dashboard title should use H1/H2.

---

## Spacing System

Use a 4px base unit. Multiples: 4, 8, 12, 16, 24, 32, 48, 64px.

In Bootstrap terms: `mb-1` = 4px, `mb-2` = 8px, `mb-3` = 16px, `mb-4` = 24px, `mb-5` = 48px.

Card internal padding: `p-3` (16px) for charts. `p-4` (24px) for KPI cards with more white space.

---

## Infographic Layout (Single Chart)

For a single polished chart intended as a standalone visual:

### Anatomy
```
[TITLE — states the insight, not the chart type]
[SUBTITLE — provides context: timeframe, source, caveats]
[CHART]
[ANNOTATION(s) — call out the most important data point(s)]
[FOOTER — source citation, date, author/brand]
```

### Plotly infographic template
```python
fig.update_layout(
    title=dict(
        text="<b>Revenue grew 34% after Q2 2023</b><br><sup style='color:#718096'>Monthly revenue, Jan 2022 – Dec 2023 | Source: Finance system</sup>",
        x=0.0,
        xanchor="left",
        font=dict(size=18),
    ),
    margin=dict(l=60, r=40, t=80, b=60),
    annotations=[
        dict(
            x="2023-07-01",
            y=peak_value,
            text="New pricing model<br>introduced",
            showarrow=True,
            arrowhead=2,
            arrowcolor="#0072B2",
            font=dict(size=11, color="#2d3748"),
            bgcolor="white",
            bordercolor="#e2e8f0",
            borderwidth=1,
            borderpad=4,
        )
    ],
)
```

### Removing chart furniture
```python
fig.update_layout(
    xaxis=dict(showgrid=False, showline=True, linecolor="#cbd5e0"),
    yaxis=dict(showgrid=True, gridcolor="#f0f4f8", showline=False, zeroline=False),
    showlegend=False,  # if series is obvious from title/subtitle
)
```

---

## Custom CSS — `assets/custom.css`

Keep this minimal. Bootstrap handles 90% of layout. Override only for brand-specific polish:

```css
/* Smooth card hover */
.card {
    transition: box-shadow 0.2s ease;
}
.card:hover {
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08) !important;
}

/* KPI value emphasis */
.kpi-value {
    font-size: 2rem;
    font-weight: 700;
    line-height: 1.1;
    letter-spacing: -0.02em;
}

/* Loading overlay — matches card background */
._dash-loading {
    background-color: rgba(255, 255, 255, 0.7);
}

/* Tab styling */
.nav-tabs .nav-link.active {
    font-weight: 600;
    border-bottom: 2px solid #0072B2;
}
```

---

## Common Anti-Patterns to Avoid

| Anti-pattern | Why it fails | Better alternative |
|---|---|---|
| Chart every column of data | No editorial curation — overwhelms user | Choose 3–5 metrics that tell the story |
| Cramped charts no padding | Signals lack of confidence; harder to read | `p-3` minimum in every card |
| Legend only (no direct labels) | Forces eye travel, disrupts reading flow | Use `fig.add_annotation()` for direct labelling where possible |
| Inconsistent chart heights in a row | Breaks visual rhythm, looks amateur | Set explicit `height` in `dcc.Graph` or use CSS |
| Default Plotly blue everywhere | Means nothing, communicates nothing | Intentional palette with primary + supporting |
| Dashboard title = "Dashboard" | Wastes prime real estate | State what this dashboard is *for* |
| Filters at the bottom | Nobody finds them | Filters always above the charts they affect |
