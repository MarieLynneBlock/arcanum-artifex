# Slide patterns

Each pattern maps to helpers in `scripts/theme.js`. Coordinates in inches on the 13.333 × 7.5 canvas. Vary the patterns across a deck; never produce a run of identical card slides. Generated deck projects copy this helper to their own `scripts/theme.js` and require it locally.

All patterns work in both themes — get the light theme via `getTheme({ mode: "light", accent })`; the helpers swap surface and text colours themselves. Colour names below (`frost`, `heading`, `body`, ...) mean the theme's role colour, not a fixed hex, unless a hex is given. Pattern 12 is light-theme only.

## 1. Title slide

Left-aligned block, generous whitespace, optional image right.

- Kicker `ONBOARDING · <TEAM>` — 14pt bold `frost`, charSpacing 3, at (0.7, 2.05).
- Title line 1 (product/topic) 54pt bold `heading` at (0.66, 2.45).
- Title line 2 (session name) 54pt bold `frost` at (0.66, 3.45).
- Subtitle: one sentence, 15pt `body`, y 4.55.
- Thin `steel` rule: line from (0.72, 5.5), w 3.4.
- Credit line 12pt `muted`: presenter or team credit (e.g. `<team> · <role>`), y 5.62.
- Optional illustration/photo on the right half; keep it clear of the text block.
- No footer on the title slide.

## 2. Numbered agenda

Title zone as standard, then one row per item:

- Big Consolas digit (22–28pt, `frost`) at x 0.7.
- Item title 14pt bold `heading` + one-line description 12pt `body` to its right.
- 6–7 items max; for timed sessions put the clock time (mono, `frost`) instead of the digit and mark breaks with ☕ and the `yellow` accent.
- Use `agendaRows(slide, rows)`.

## 3. Card row (2–4 cards)

The workhorse. `cardRow` helper: title zone, then N cards side by side in the body zone, each with accent bar, label, headline, body. Assign accent colours semantically (e.g. AI HANDLES `frost` / YOU OWN `yellow` / YOU OWN `green`). Follow with a takeaway strip or stat line.

## 4. Two-column contrast (TODAY / WHAT FOLLOWS, DO / DON'T)

Two half-width columns, each with a mono uppercase header in its accent colour and `▸`-led lines (12pt `body`). DO/DON'T uses `green` vs `red`. No card fill needed; a hairline (`muted`) between columns is enough.
Use `twoColumnContrast(slide, left, right)`.

## 5. Spectrum / trajectory

Horizontal line (`steel`, 1.5pt) across the body zone with 4–5 stops: dot or small roundRect per stop, mono label above, 2-line description below (10.5pt `body`). Mark position with labels like `YOU START HERE` / `WHERE YOU'RE HEADING` in `green`/`frost`. Below, two half-width cards can contrast NOW vs NEXT.

## 6. Mode/tool comparison (3 columns)

Three equal cards, each: mono uppercase name (14pt, accent per column), one-line role (bold `heading`), 3–4 short lines (`body`), and a bottom mono example in a nested `cardAlt` code block (Consolas 10.5pt). Close with a `CONTEXT IS THE LEVER`-style green banner carrying a vague → anchored example in Consolas.

## 7. Layer stack

Stacked full-width rounded rects (one per layer), each slightly indented or colour-stepped, mono label left + description right. Max 5 layers. Good for instruction hierarchies, governance layers.
Use `layerStack(slide, layers)`.

## 8. Stat + argument

One oversized mono figure (Consolas 44–60pt, accent colour) with source attribution (9pt `muted`), a caveat pill if derived or estimated, and a takeaway strip that interprets it. Use `sourcePill` for a directly sourced figure; use `DERIVED` or `EST.` for calculated or estimated values. `statArgument(slide, figure, attribution, options)` lays out the figure, attribution, caveat, and optional takeaway. Whitespace is the design.

## 9. Section divider

Background `bg`, oversized section number in Consolas (`card` colour, huge, as a background numeral), section title 36–40pt bold `heading`, one-line framing sentence `body`. No footer clutter beyond page number.

## 10. Ethics / cost slide

Card row or two-column with `red`/`yellow` semantics; always ends with a green banner stating the responsible default. Include billing/consumption figures with their source or a `DERIVED` pill.

## 11. Closing / next steps

Title `What's next` style, numbered mono steps or short card row (your track, your repo, first task), coach contact line, and a green banner with the single call to action.

## 12. Banner-title header (light theme)

`bannerTitle` helper: full-content-width accent `roundRect` (x 0.6, y 0.39, w 12.133, h 0.73) carrying the slide title at 24pt bold, footer as standard. Title text is `ECEFF4` on dark-enough accents (`steel`, `red`) and `2E3440` on light tones — the helper picks automatically by luminance. This is an **alternative** to kicker + title + standfirst: choose one header anatomy per deck, never mix within a deck. On banner-title slides the body zone may start at y 1.5 instead of 2.2.

## Slido / poll placeholder

Dark slide, poll question as title, `scan to join · slido.com · #<code>` in mono `frost`, note in `muted`: `SLIDO PLACEHOLDER · replace via add-in`.
