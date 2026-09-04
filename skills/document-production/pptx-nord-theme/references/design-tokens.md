# Design tokens

These values are the house style; do not restyle.

## Themes

Two themes, one grid. **Dark is the default**; theme and accent are confirmed during deck scoping.

- `getTheme({ mode: "dark" | "light", accent })` in `scripts/theme.js` returns the full helper set bound to that theme. The module's top-level exports are the dark theme, so existing dark deck scripts need no changes.
- `accent` is a Nord token name (`"green"`, `"steel"`, `"frostDeep"`, ...) or a 6-digit hex; default `green` (`A3BE8C`). In the light theme it drives kickers, the title-slide accent line and the `bannerTitle` header. The dark theme's slide anatomy is unchanged by it (kickers stay `frost`); it only affects elements you pass it to explicitly.

## Canvas

- 16:9 wide: **13.333" × 7.5"** (`pres.defineLayout` or `LAYOUT_WIDE` in pptxgenjs).
- Slide background, set via `slide.background`: solid `2E3440` (nord0) in the dark theme, `ECEFF4` (nord6) in the light theme.

## Palette (Nord, hex without `#` for pptxgenjs)

The full official [Nord palette](https://www.nordtheme.com/docs/colors-and-palettes) — all 16 colours, hex values verbatim. Token names are this skill's semantic roles; the Nord column is the official identifier (Polar Night nord0–3, Snow Storm nord4–6, Frost nord7–10, Aurora nord11–15).

| Token | Nord | Hex | Role |
| --- | --- | --- | --- |
| `bg` | nord0 | `2E3440` | Slide background; dark text on light banners |
| `card` | nord1 | `3B4252` | Card fill, code-block fill |
| `cardAlt` | nord2 | `434C5E` | Nested/secondary card fill |
| `muted` | nord3 | `4C566A` | Footer text, hairlines, caveat pills, de-emphasis |
| `body` | nord4 | `D8DEE9` | Body text, standfirsts, card body copy |
| `bodyLight` | nord5 | `E5E9F0` | Emphasised body copy on dark |
| `heading` | nord6 | `ECEFF4` | Titles, card headline figures |
| `frost` | nord8 | `88C0D0` | Kickers, structure labels, primary accent bars, links |
| `frostDeep` | nord9 | `81A1C1` | Secondary frost accent |
| `steel` | nord10 | `5E81AC` | Rules/divider lines, tertiary accent |
| `teal` | nord7 | `8FBCBB` | Occasional fourth accent |
| `green` | nord14 | `A3BE8C` | Positive / recommended / BUILDER / takeaway banners |
| `yellow` | nord13 | `EBCB8B` | Caution / cost / EXPLORER |
| `orange` | nord12 | `D08770` | Warm warning (sparingly) |
| `red` | nord11 | `BF616A` | Risk / anti-pattern / "don't" |
| `purple` | nord15 | `B48EAD` | Special-case accent (e.g. a fifth category) |

Semantics are load-bearing: green means recommended, yellow means caution/cost, red means risk. Never use them decoratively against those meanings. (These map cleanly onto the official Nord semantics: nord14 success, nord13 warning, nord11 error, nord9 primary accent.)

## Light theme

Same grid, typography and type scale as dark; only surfaces and text colours change.

| Role | Nord | Hex |
| --- | --- | --- |
| Slide background | nord6 | `ECEFF4` |
| Alt surface / code-block fill | nord5 | `E5E9F0` |
| Headings on light surfaces | nord0 | `2E3440` |
| Body text on light surfaces | nord1 | `3B4252` |
| Secondary text on light surfaces | nord2 | `434C5E` |
| Muted / footer | nord3 | `4C566A` |

- **The default card stays dark** (fill `3B4252`, heading `ECEFF4`, body `D8DEE9`, same accent-bar anatomy) — the white-on-dark card is the house signature on both backgrounds. Accent-coloured text on dark cards stays allowed as-is.
- **Soft card variant** (`card(s, { soft: true, ... })`, light theme only): `FFFFFF` fill, hairline `D8DEE9` border (0.75pt), heading `2E3440`, body `3B4252`, label in the text-safe accent.
- **Banners:** the green takeaway banner is unchanged (`A3BE8C` fill, `2E3440` text). The dark strip variant stays `3B4252` with `D8DEE9` text.
- **Section divider numeral:** `D8DEE9`.

### Text-safe accents on light surfaces

Any Nord accent may appear as a **fill** (bars, pills, banner backgrounds, swatches) on the light background. Light tones are fill-only there — never text. The helpers substitute automatically; use `theme.textSafe(colour)` for any text you place yourself:

| Accent | As text on light surfaces becomes |
| --- | --- |
| `frost` `88C0D0` | `steel` `5E81AC` |
| `teal` `8FBCBB` | `steel` `5E81AC` |
| `yellow` `EBCB8B` | `orange` `D08770` |
| `green` `A3BE8C` | `muted` `4C566A` (Nord has no darker green; the green stays in bars, banners and pills) |

`frostDeep` `81A1C1` and `purple` `B48EAD` remain legal as text (Nord light-ambiance convention) but sit near the contrast floor — keep them bold, never below 10pt.

### Banner-title text colour

`bannerTitle` picks its title colour by accent luminance: `ECEFF4` on the dark accents (`steel` `5E81AC`, `red` `BF616A`), `2E3440` on every lighter accent (`frostDeep`, `frost`, `teal`, `green`, `yellow`, `orange`, `purple`).

## Typography

- **Body/headings: Calibri.** Bold for titles, kickers, card labels, inline labels.
- **Mono: Consolas** for numbers/figures, code, CLI commands, pill labels, track markers, section digits, caveat pills. (Courier New is the fallback if Consolas is unavailable in the rendering environment.)
- Kickers and mono labels are UPPERCASE with letter spacing (`charSpacing: 3` for kickers, `2` for small labels).

### Type scale (pt)

| Element | Size | Weight/colour |
| --- | --- | --- |
| Title-slide main title | 54 | bold, line 1 `heading`, line 2 accent (`frost` in dark, text-safe accent in light) |
| Content-slide title | 28 | bold `heading` |
| Banner-title header | 24 | bold, on-accent text (see Light theme) |
| Section-divider title | 36–40 | bold `heading` |
| Kicker | 11 | bold, charSpacing 3 — `frost` in dark, text-safe accent in light |
| Standfirst | 14 | `body`; accent words coloured inline |
| Card big figure | 36 | bold `heading` |
| Card label | 10 | bold, accent colour, uppercase, mono or Calibri caps |
| Card body | 12–12.5 | `body` |
| Takeaway strip text | 12.5 | `bodyLight` (dark variant) or `bg` (green banner) |
| Footer | 9 | `muted` |
| Speaker-verbatim, small print | 9–10 | `muted` |

## Layout grid

- **Margins:** 0.6" left/right. Content width 12.1".
- Kicker: x 0.6, y 0.42, h 0.3.
- Title: x 0.6, y 0.72, h 0.7.
- Standfirst: x 0.6, y 1.42, h 0.5.
- **Body zone: y 2.2 → 5.5** (cards, columns, diagrams).
- Takeaway strip: y ≈ 5.6–6.5, full content width.
- Footer: y 7.08, h 0.3 — deck identity left (x 0.6), page number right-aligned (x 12.2, w 0.6).
- Card gap: ~0.35" between cards in a row. Three cards across: 3.97" wide each. Four across: 2.9".

## Card anatomy

A card is a `roundRect` (`rectRadius` ~0.06), fill `card`, no border, containing:
1. A vertical **accent bar**: thin `roundRect` 0.07" wide, inset 0.12" from card left, 0.16" from top/bottom, in the card's semantic accent colour.
2. A **label** row (10pt bold accent colour, uppercase) at the top.
3. A **headline** (big figure or short phrase, `heading`).
4. **Body copy** (`body`, 12pt).
Text starts ~0.3" in from the card's left edge (clear of the accent bar). Always set `margin: 0` on the text boxes and position deliberately.

## Banner anatomy (takeaway)

- **Green banner:** full-content-width `roundRect`, fill `green`, text in `bg`, bold lead-in then regular. For the one thing the audience must retain.
- **Dark takeaway strip:** same geometry, fill `card`, text `bodyLight`, optional left accent bar. For a closing nuance rather than a directive.
Use at most one banner per slide.
