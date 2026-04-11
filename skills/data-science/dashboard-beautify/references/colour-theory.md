# Colour Theory — Data Visualisation Reference

## Core principle
Colour in data visualisation is not decoration. Every colour choice must carry a semantic load.
The question is never "does this look nice?" — it's "does this colour communicate something true about the data?"

See also: `colourblindness.md` — simulation tools, CVD-safe palettes, and the pre-ship checklist.

---

## Theme architecture

All colour values live in `colours.py`. The `register_theme()` function in SKILL.md Step 5 accepts any palette and surface colours — this file provides pre-built configurations for common contexts.

**How to use**: copy the relevant block into `colours.py`, call `register_theme(**config)` in `app.py` before importing layout, then set `pio.templates.default = theme_name`.

---

## Pre-built themes

### Nord light — default recommendation

Soft, cool-toned, perceptually restful. Well-suited to dashboards viewed for extended periods.
Passes WCAG AA across all surface/text pairings listed below.

```python
# Nord colour constants
NORD0  = "#2E3440"  # darkest — main bg (dark)
NORD1  = "#3B4252"  # card bg (dark)
NORD2  = "#434C5E"  # active / selected
NORD3  = "#4C566A"  # muted text, gridlines
NORD4  = "#D8DEE9"  # muted text on dark / gridlines (light)
NORD5  = "#E5E9F0"  # card bg (light)
NORD6  = "#ECEFF4"  # page bg (light) / primary text on dark
NORD7  = "#8FBCBB"  # frost teal
NORD8  = "#88C0D0"  # frost light blue  — PRIMARY series colour
NORD9  = "#81A1C1"  # frost slate
NORD10 = "#5E81AC"  # frost deep blue
NORD11 = "#BF616A"  # aurora red    — status: bad    ⚠️ CVD: never sole pairing with NORD14
NORD12 = "#D08770"  # aurora orange — status: caution
NORD13 = "#EBCB8B"  # aurora yellow — status: warning ⚠️ fails contrast on light bg as text
NORD14 = "#A3BE8C"  # aurora green  — status: good   ⚠️ CVD: never sole pairing with NORD11
NORD15 = "#B48EAD"  # aurora purple

NORD_CATEGORICAL = [NORD8, NORD14, NORD9, NORD13, NORD15, NORD11, NORD7]  # CVD-aware order

NORD_SIGNAL = {
    "good":    NORD14,
    "warning": NORD13,
    "caution": NORD12,
    "bad":     NORD11,
    "neutral": NORD3,
}

NORD_LIGHT_CONFIG = dict(
    palette=NORD_CATEGORICAL,
    theme_name="nord_light",
    bg_plot=NORD6,
    bg_paper="rgba(0,0,0,0)",
    text_colour=NORD0,
    grid_colour=NORD4,
    muted_colour=NORD3,
)

NORD_DARK_CONFIG = dict(
    palette=NORD_CATEGORICAL,
    theme_name="nord_dark",
    bg_plot=NORD1,
    bg_paper="rgba(0,0,0,0)",
    text_colour=NORD6,
    grid_colour=NORD2,
    muted_colour=NORD4,
)
```

**Nord contrast pairs (pre-checked):**

| Foreground | Background | Ratio | WCAG |
|---|---|---|---|
| NORD0 `#2E3440` | NORD6 `#ECEFF4` | ~10.5:1 | ✅ AAA |
| NORD0 `#2E3440` | NORD8 `#88C0D0` | ~5.1:1 | ✅ AA |
| NORD6 `#ECEFF4` | NORD0 `#2E3440` | ~10.5:1 | ✅ AAA |
| NORD6 `#ECEFF4` | NORD10 `#5E81AC` | ~4.6:1 | ✅ AA |
| NORD13 `#EBCB8B` | NORD6 `#ECEFF4` | ~1.8:1 | ❌ Fail — never use as text on light |
| NORD14 `#A3BE8C` | NORD6 `#ECEFF4` | ~3.1:1 | ⚠️ Large text only |

---

### High-contrast light — clinical / public sector

For environments where accessibility standards are stricter (e.g. NHS Digital, GOV.UK).
All text pairs meet WCAG AAA (7:1+).

```python
HC_CATEGORICAL = [
    "#005EB8",  # NHS blue — primary
    "#007F3B",  # NHS green
    "#AE2573",  # NHS pink
    "#330072",  # NHS purple
    "#ED8B00",  # NHS warm yellow
    "#00A9CE",  # NHS light blue
]

HC_SIGNAL = {
    "good":    "#007F3B",
    "warning": "#ED8B00",
    "bad":     "#DA291C",
    "neutral": "#425563",
}

HC_LIGHT_CONFIG = dict(
    palette=HC_CATEGORICAL,
    theme_name="hc_light",
    bg_plot="#FFFFFF",
    bg_paper="rgba(0,0,0,0)",
    text_colour="#212B32",
    grid_colour="#D8DDE0",
    muted_colour="#425563",
)
```

---

### Okabe-Ito — maximum CVD safety for categorical data

When colourblindness safety is the primary constraint and brand/aesthetics are secondary.
Verified safe across deuteranopia, protanopia, and tritanopia.

```python
OKABE_ITO = [
    "#E69F00",  # orange
    "#56B4E9",  # sky blue
    "#009E73",  # teal green
    "#F0E442",  # yellow      ⚠️ low contrast on white — do not use as text
    "#0072B2",  # blue
    "#D55E00",  # vermillion
    "#CC79A7",  # pink/mauve
]

OKABE_CONFIG = dict(
    palette=OKABE_ITO,
    theme_name="okabe",
    bg_plot="#F8F9FA",
    bg_paper="rgba(0,0,0,0)",
    text_colour="#1A202C",
    grid_colour="#E2E8F0",
    muted_colour="#718096",
)
```

---

### Custom brand theme — pattern

If the project has a brand palette, derive the theme colours from it:

```python
BRAND_PRIMARY   = "#______"   # main series / hero colour
BRAND_SECONDARY = "#______"   # supporting series
BRAND_ACCENT    = "#______"   # emphasis / highlight
BRAND_SURFACE   = "#______"   # card surface
BRAND_TEXT      = "#______"   # primary text
BRAND_MUTED     = "#______"   # secondary text / tick labels
BRAND_GRID      = "#______"   # gridlines

BRAND_CATEGORICAL = [BRAND_PRIMARY, BRAND_SECONDARY, BRAND_ACCENT]

BRAND_CONFIG = dict(
    palette=BRAND_CATEGORICAL,
    theme_name="brand",
    bg_plot=BRAND_SURFACE,
    bg_paper="rgba(0,0,0,0)",
    text_colour=BRAND_TEXT,
    grid_colour=BRAND_GRID,
    muted_colour=BRAND_MUTED,
)
```

Before using: verify all text/background pairs meet WCAG AA (4.5:1 normal text, 3:1 large).
Use the contrast checker in `colourblindness.md`.

---

## Semantic colour roles

These apply regardless of theme. Signal colours must not be reused for category decoration.

| Role | Use for | Do not use for |
|---|---|---|
| Primary series | Hero data line / bar | Status indication |
| Signal: good | Target met, positive delta | Category labels |
| Signal: warning | Near threshold, caution | Category labels |
| Signal: bad | Threshold breached, alert | Category labels |
| Signal: neutral | Reference lines, "other" | Primary data |
| Muted | Gridlines, tick labels, de-emphasised series | Primary data |

---

## Sequential palettes — continuous / ordered data

Use Plotly's built-in perceptually uniform options:

| Palette | Best for |
|---|---|
| `"Viridis"` | General use — yellow→green→blue |
| `"Cividis"` | Maximum CVD safety — explicitly designed for colour vision deficiency |
| `"Magma"` | Dark backgrounds — black→purple→yellow |
| `"Blues"` / `"Greens"` | Single-hue when one colour family fits the theme |

**Never use**: `"Jet"`, `"Rainbow"`, `"Spectral"` — perceptually non-uniform, create false features.

```python
fig.update_traces(marker_colorscale="Viridis")
```

---

## Diverging palettes — data with a meaningful midpoint

Use when visualising deviation from zero, over/under target, or positive/negative values.

| Palette | Character |
|---|---|
| `"RdBu"` | Red (low) → white (mid) → blue (high) |
| `"PiYG"` | Pink → white → green — more CVD-safe than RdBu |
| `"RdYlGn"` | Traffic light — only when semantics genuinely match good/neutral/bad |

Always set the midpoint explicitly:
```python
fig.update_traces(marker_colorscale="RdBu", marker_cmid=0)
```

---

## Highlight / focus pattern

```python
HIGHLIGHT = NORD8     # swap for your theme's primary
MUTED     = "#D3D3D3"

for name, group in df.groupby("category"):
    colour = HIGHLIGHT if name == focus_category else MUTED
    fig.add_trace(go.Bar(x=group["x"], y=group["y"],
                         name=name, marker_color=colour))
```

---

## Conditional colouring against a threshold

```python
from colours import SIGNAL  # your theme's signal dict

df["colour"] = df["value"].apply(
    lambda v: SIGNAL["good"] if v >= target else SIGNAL["bad"]
)
fig = go.Figure(go.Bar(x=df["category"], y=df["value"], marker_color=df["colour"]))
fig.add_hline(
    y=target, line_dash="dash", line_color=SIGNAL["neutral"], line_width=1.5,
    annotation_text=f"Target: {target}", annotation_position="top right",
)
```
