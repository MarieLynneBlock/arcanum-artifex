# Colourblindness Support — Reference

Approximately 8% of men and 0.5% of women have some form of colour vision deficiency (CVD). In a dashboard 
used by a team of 50, that's likely 3–4 people for whom your colour choices may actively mislead. This is 
not a corner case — it is a baseline accessibility requirement.

---

## Types of Colour Vision Deficiency

| Type | Prevalence | What's affected |
|---|---|---|
| **Deuteranomaly** | ~5% men | Reduced green sensitivity (most common) |
| **Deuteranopia** | ~1% men | No green receptors |
| **Protanomaly** | ~1% men | Reduced red sensitivity |
| **Protanopia** | ~1% men | No red receptors |
| **Tritanomaly** | Rare | Reduced blue sensitivity |
| **Tritanopia** | Very rare | No blue receptors |
| **Achromatopsia** | Very rare | No colour vision at all |

The red-green deficiencies (deuteranopia + protanopia) are by far the most prevalent and the ones most 
commonly violated by default chart palettes. **Never use red and green as the primary distinguishing colours.**

---

## Simulation — Check Before Shipping

Always simulate your charts before sharing. Tools:

### Browser-based (no install)
- **Coblis** — https://www.colour-blindness.com/coblis-colour-blindness-simulator/ (upload screenshot)
- **Adobe Colour** — https://colour.adobe.com/create/colour-accessibility (checks palette conflicts)
- **Chromatic Vision Simulator** — browser extension, real-time page simulation

### Python — programmatic simulation
```python
# Using the `daltonize` library
pip install daltonize

from daltonize import daltonize
import numpy as np
from PIL import Image
import plotly.io as pio

# Export your figure as image first
img_bytes = pio.to_image(fig, format="png")

# Simulate deuteranopia
img = Image.open(io.BytesIO(img_bytes))
img_array = np.array(img)
simulated = daltonize.simulate(img_array, mode='d')  # 'd'=deuteranopia, 'p'=protanopia, 't'=tritanopia
Image.fromarray(simulated).save("simulated_deuteranopia.png")
```

Modes: `'d'` deuteranopia, `'p'` protanopia, `'t'` tritanopia, `'da'` deuteranomaly, `'pa'` protanomaly.

### Plotly-native: colour simulation in browser
```python
# No library needed — use CSS filter in the Dash layout for quick visual check
# Add temporarily to dbc.Container style, remove before shipping
app.layout = dbc.Container(
    [...],
    style={"filter": "url(#deuteranopia)"},  # see SVG filter below
)
```

SVG filters for in-browser simulation (add to `assets/cvd_filters.svg`, reference in `index.html`):
```xml
<svg xmlns="http://www.w3.org/2000/svg" style="display:none">
  <!-- Deuteranopia -->
  <filter id="deuteranopia">
    <feColorMatrix type="matrix" values="
      0.367  0.861 -0.228  0  0
      0.280  0.673  0.047  0  0
     -0.012  0.043  0.969  0  0
      0      0      0      1  0"/>
  </filter>
  <!-- Protanopia -->
  <filter id="protanopia">
    <feColorMatrix type="matrix" values="
      0.152  1.053 -0.205  0  0
      0.115  0.786  0.099  0  0
     -0.004 -0.048  1.052  0  0
      0      0      0      1  0"/>
  </filter>
  <!-- Tritanopia -->
  <filter id="tritanopia">
    <feColorMatrix type="matrix" values="
      1.256 -0.077 -0.179  0  0
     -0.078  0.931  0.148  0  0
      0.005  0.691  0.304  0  0
      0      0      0      1  0"/>
  </filter>
</svg>
```

---

## Compliant Palette Choices

### Okabe-Ito — verified colourblind-safe (categorical, up to 7 series)
```python
OKABE_ITO = [
    "#E69F00",  # orange     — safe across all CVD types
    "#56B4E9",  # sky blue   — safe
    "#009E73",  # teal green — safe (distinct from red even in protanopia)
    "#F0E442",  # yellow     — safe, but low contrast on white — avoid as text
    "#0072B2",  # blue       — safe
    "#D55E00",  # vermillion — safe (reads as distinct from green in deuteranopia)
    "#CC79A7",  # pink/mauve — safe
]
```
Reference: Okabe M, Ito K (2002). "Colour Universal Design". *J-stage.*

### Nord categorical — colourblind-aware ordering
Nord's Frost + Aurora colours are softer than Okabe-Ito but still performant for CVD if ordered correctly.
The key is ensuring the first 3–4 colours are distinguishable under deuteranopia:

```python
NORD_CVD_ORDERED = [
    "#88C0D0",  # frost light blue — safe primary
    "#A3BE8C",  # aurora green     — avoid pairing directly with #BF616A in same chart
    "#81A1C1",  # frost slate      — safe
    "#EBCB8B",  # aurora yellow    — safe, low contrast on light bg
    "#B48EAD",  # aurora purple    — safe
    "#BF616A",  # aurora red       — avoid pairing with #A3BE8C (red-green risk)
    "#8FBCBB",  # frost teal       — safe
]
```

**Nord-specific warning**: `#A3BE8C` (green) and `#BF616A` (red) look similar under deuteranopia/protanopia. 
If you're using both in the same chart to mean different things — don't. Use shape or pattern redundantly, 
or replace one with `#88C0D0` (blue) or `#B48EAD` (purple).

### Sequential palettes — all safe choices
These are perceptually uniform and CVD-safe:
- `"Viridis"` — yellow→green→blue. Safe under all deficiency types.
- `"Cividis"` — explicitly designed for CVD. Blue→yellow, distinguishable in all conditions.
- `"Magma"` — black→purple→yellow. Safe.
- `"Blues"` / `"Purples"` — single-hue, always safe.

**Avoid**: `"Jet"`, `"Rainbow"`, `"Spectral"` — all fail under deuteranopia.

---

## Redundant Encoding — The Most Reliable Strategy

Colour should **never be the only encoding** for critical information. Always pair with at least one other channel:

### Shape + colour (scatter plots)
```python
symbol_map = {
    "Group A": "circle",
    "Group B": "square",
    "Group C": "diamond",
    "Group D": "cross",
}
colour_map = {
    "Group A": "#88C0D0",
    "Group B": "#A3BE8C",
    "Group C": "#BF616A",
    "Group D": "#EBCB8B",
}

for group, df_group in df.groupby("group"):
    fig.add_trace(go.Scatter(
        x=df_group["x"], y=df_group["y"],
        mode="markers",
        name=group,
        marker=dict(
            color=colour_map[group],
            symbol=symbol_map[group],
            size=9,
            line=dict(width=1, color="#2E3440"),  # border improves contrast
        ),
    ))
```

### Line dash + colour (line charts)
```python
dash_map = {
    "Series A": "solid",
    "Series B": "dash",
    "Series C": "dot",
    "Series D": "dashdot",
}
for name, group in df.groupby("series"):
    fig.add_trace(go.Scatter(
        x=group["date"], y=group["value"],
        mode="lines",
        name=name,
        line=dict(
            color=colour_map[name],
            dash=dash_map[name],
            width=2.5,
        ),
    ))
```

### Pattern fill + colour (bar charts)
```python
# Plotly supports hatching via marker.pattern
fig.add_trace(go.Bar(
    x=categories,
    y=values,
    marker=dict(
        color="#A3BE8C",
        pattern=dict(shape="/", fgcolor="#2E3440", size=6),
    ),
    name="Group B",
))
```
Available patterns: `""` (solid), `"/"`, `"\\"`, `"x"`, `"-"`, `"|"`, `"+"`, `"."`.

### Direct annotation (avoid legend dependency)
When you have 2–3 series, label them directly rather than relying on a legend:
```python
# Add text at end of each line
fig.add_annotation(
    x=df[df["series"]=="A"]["date"].iloc[-1],
    y=df[df["series"]=="A"]["value"].iloc[-1],
    text="<b>Series A</b>",
    showarrow=False,
    xanchor="left",
    font=dict(color=colour_map["A"], size=12),
)
```
This eliminates the colour-matching cognitive task entirely.

---

## Text and Contrast

Data labels, axis ticks, and annotations on coloured backgrounds are a frequent accessibility failure point.

### Minimum contrast ratios (WCAG 2.1)
- Normal text (< 18px): **4.5:1**
- Large text (≥ 18px, bold): **3:1**
- UI components and chart borders: **3:1**

### Checking contrast programmatically
```python
def contrast_ratio(hex1: str, hex2: str) -> float:
    """WCAG contrast ratio between two hex colours."""
    def relative_luminance(hex_colour: str) -> float:
        rgb = tuple(int(hex_colour.lstrip("#")[i:i+2], 16) / 255 for i in (0, 2, 4))
        def linearise(c):
            return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
        r, g, b = [linearise(c) for c in rgb]
        return 0.2126 * r + 0.7152 * g + 0.0722 * b

    l1 = relative_luminance(hex1)
    l2 = relative_luminance(hex2)
    lighter, darker = max(l1, l2), min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)

# Example: check Nord text on card background
print(contrast_ratio("#2E3440", "#E5E9F0"))  # → ~10.5:1 ✅ passes AA and AAA
print(contrast_ratio("#EBCB8B", "#ECEFF4"))  # → ~1.8:1  ❌ fails — don't use yellow text on light
```

### Nord contrast pairs (pre-checked)
| Foreground | Background | Ratio | WCAG |
|---|---|---|---|
| `#2E3440` (nord0) | `#ECEFF4` (nord6) | ~10.5:1 | ✅ AAA |
| `#2E3440` (nord0) | `#88C0D0` (frost) | ~5.1:1 | ✅ AA |
| `#ECEFF4` (nord6) | `#2E3440` (nord0) | ~10.5:1 | ✅ AAA |
| `#ECEFF4` (nord6) | `#5E81AC` (nord10) | ~4.6:1 | ✅ AA |
| `#EBCB8B` (nord13) | `#ECEFF4` (nord6) | ~1.8:1 | ❌ Fail |
| `#A3BE8C` (nord14) | `#ECEFF4` (nord6) | ~3.1:1 | ⚠️ Large text only |

---

## Checklist Before Shipping

```
□ Simulated under deuteranopia — no information is lost
□ Simulated under protanopia — no information is lost  
□ Red and green are not the sole distinguishing pair in any chart
□ All coloured series use at least one redundant encoding (shape, dash, pattern, or label)
□ All text on coloured backgrounds passes 4.5:1 contrast (3:1 for large/bold)
□ Nord yellow (#EBCB8B) is not used as standalone text on light backgrounds
□ Legend is not the only way to identify series — direct labels used where possible
□ Sequential/continuous data uses Viridis, Cividis, or Magma — not Rainbow/Jet
□ Tooltips include the series name as text — not only implied by colour
```

---

## Keyboard and screen reader accessibility

Colour and CVD are not the only accessibility concerns. Dashboards also need to be navigable without
a mouse and interpretable without a screen — for users of assistive technology, and for anyone reviewing
a dashboard in a context where hover is unavailable (e.g. a printed export, a meeting slide).

### Keyboard navigation in Dash

Dash renders HTML — tab order follows DOM order by default. Ensure:

1. **Filters before charts in the DOM** — filters should appear before `dcc.Graph` components in `layout.py`,
   so tab order reaches them first.
2. **Interactive controls have visible focus indicators** — Bootstrap components handle this; do not
   suppress CSS `outline` styles.
3. **Dropdowns and date pickers are keyboard-operable** — `dcc.Dropdown` and `dcc.DatePickerRange`
   support keyboard navigation natively; test with Tab + arrow keys before shipping.

```python
# Correct DOM order — filter before chart
dbc.Row([
    dbc.Col(dbc.Select(id="region-filter", ...), width=3),   # reaches tab focus first
]),
dbc.Row([
    dbc.Col(dcc.Graph(id="main-chart"), width=12),
]),
```

### Minimum font sizes

Small text on charts is a frequent accessibility failure — particularly on dashboards viewed on
high-DPI displays where the rendered size can be smaller than the CSS pixel size suggests.

| Element | Minimum size |
|---|---|
| Axis tick labels | 11px |
| Axis titles | 12px |
| Chart annotations | 11px |
| Legend text | 12px |
| Chart title | 15px |
| KPI card value | 24px |
| KPI card label | 12px |

```python
fig.update_layout(
    font=dict(size=13),          # base — inherited by most elements
    title=dict(font=dict(size=16)),
)
fig.update_xaxes(tickfont=dict(size=11))
fig.update_yaxes(tickfont=dict(size=11))
```

Test at 375px mobile width — tick labels are the most common failure point on small screens.

### Text summaries for key charts

Screen readers cannot interpret SVG charts. For every primary chart, provide a visible text summary
adjacent to the chart — not in hover, not hidden behind an accessible description attribute:

```python
def chart_with_summary(fig: go.Figure, chart_id: str, summary: str) -> dbc.Card:
    """Wrap a chart with a visible text insight summary."""
    return dbc.Card([
        dcc.Graph(id=chart_id, figure=fig, config={"responsive": True}),
        html.P(
            summary,
            className="text-muted small px-3 pb-2 mb-0",
            # Example: "Revenue grew 34% between Q1 and Q3 2023, peaking at £4.2M in August."
        ),
    ], className="shadow-sm border-0")
```

This also benefits non-AT users — a one-sentence plain-language summary anchors the chart's meaning
and reduces time-to-insight.

### Hover-only information — avoid for critical values

Never encode critical information only in hover tooltips. Hover is unavailable on:
- Touch screens (tap reveals tooltip, but it disappears on next interaction)
- Keyboard-only navigation
- Printed or exported views
- Screen readers

For values that are critical to the primary question, annotate them directly on the chart:
```python
fig.add_annotation(
    x=peak_date,
    y=peak_value,
    text=f"Peak: £{peak_value/1e6:.1f}M",
    showarrow=True,
    arrowhead=2,
    font=dict(size=11),
    bgcolor="white",
    bordercolor="#D8DEE9",
    borderpad=4,
)
```

### ARIA and semantic HTML in Dash layout

Dash's `html.*` components accept standard HTML attributes including `aria-*`:

```python
html.H2("Dashboard Title", **{"aria-label": "NHS A&E Performance Dashboard — 2023 to 2024"})

# For icon-only buttons, always add aria-label
html.Button("⬇", id="download-btn", **{"aria-label": "Download data as CSV"})

# Wrap decorative elements so screen readers skip them
html.Span("📊", **{"aria-hidden": "true"})
```

### Pre-ship keyboard and screen reader checklist

```
□ Tab through the entire dashboard — reaches all interactive controls in logical order
□ All dropdowns, date pickers, and buttons operable with keyboard alone
□ No interactive element relies solely on hover to reveal its function
□ Critical chart values annotated directly (not hover-only)
□ Every primary chart has a visible plain-language summary sentence
□ All axis tick labels are ≥ 11px — check at 375px mobile width
□ Icon-only buttons have aria-label set
□ Dashboard reviewed with browser screen reader (NVDA / VoiceOver) — filters and KPI values are read correctly
```

---

## Further Reading

- Okabe M, Ito K (2002). *Colour Universal Design (CUD)*. https://jfly.uni-koeln.de/colour/
- WCAG 2.1 Success Criteria 1.4.3 (Contrast, Minimum): https://www.w3.org/WAI/WCAG21/quickref/#contrast-minimum
- WCAG 2.1 Success Criteria 2.1.1 (Keyboard): https://www.w3.org/WAI/WCAG21/quickref/#keyboard
- Crameri F et al. (2020). "The misuse of colour in science communication." *Nature Communications* 11, 5444.
- Rougier NP et al. (2014). "Ten Simple Rules for Better Figures." *PLOS Computational Biology*.
