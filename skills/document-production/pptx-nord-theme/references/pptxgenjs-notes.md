# pptxgenjs notes and QA

## Setup

Create a local, portable project; do not rely on a globally installed `pptxgenjs` or an absolute path to this skill.

```bash
npm init -y
npm install --save-exact pptxgenjs
npm run build
```

Use a minimal `package.json` with `"build": "node deck.js"`; optionally add `qa:pdf`, `qa:images`, and `qa:text` scripts for the available renderer. Copy `scripts/theme.js` and `scripts/qa-pptx-text.py` from the skill into the project. Add a `.gitignore` containing `node_modules/`, `dist/`, and `qa-render/`.

Before generating, run this preflight. The Node commands are required; the renderer commands are capability checks, so a non-zero result for one of them is expected when the associated fallback is used:

```bash
node --version
npm --version
soffice --version
pdftoppm -v
magick -version
gs --version
```

If Node or npm is unavailable, stop and ask before installing a runtime. Do not assume the machine's package manager or make a global installation silently. On corporate machines npm may resolve through an internal proxy; use the sanctioned registry or mirror if installation fails.

## Footguns (these corrupt files or silently break layout)

- **Set the layout before adding slides.** Default canvas is 10 × 5.625". Use `LAYOUT_WIDE` (13.333 × 7.5) — this skill's grid assumes it. Off-canvas coordinates are written, not clamped; the shape just doesn't appear.
- **Colours: 6 hex digits, no `#`, no alpha.** `"88C0D0"` — both `"#88C0D0"` and 8-digit hex corrupt the file. Translucency: `transparency: 0-100` on fills/images.
- **pptxgenjs mutates option objects in place.** Never share an options/shadow object between two `add*` calls; build fresh objects (the theme helpers do this).
- **Text boxes have built-in padding.** Set `margin: 0` whenever text must align to a shape edge, line, or another text box — the helpers do.
- **Bullets:** `bullet: true` per item, never a literal `•`; `breakLine: true` on every array item except the last; space paragraphs with `paraSpaceAfter`, not `lineSpacing`.
- **`rectRadius` only applies to `ROUNDED_RECTANGLE`**, not `RECTANGLE`.
- **Gradient fills are unsupported** — the house style doesn't use them anyway.
- **`letterSpacing` is ignored; the real option is `charSpacing`.**
- **Speaker notes:** `slide.addNotes("...")`, plain text, once per slide. Never a text box on the slide.
- **One `new pptxgen()` per output file.**
- **Charts:** use `addChart()` with `chartColors` from the palette, quiet axes (`catAxisLabelColor`/`valAxisLabelColor: "D8DEE9"`, `valGridLine: { color: "434C5E", size: 0.5 }`, `catGridLine: { style: "none" }`), `showLegend: false` for single series. On stacked charts `dataLabelPosition` must be `ctr`, `inEnd`, or `inBase` — `outEnd` corrupts the file.

## QA loop (mandatory)

First renders always contain a few real defects. Render, look, fix, re-render.

### 1. Automated text QA

Run the supplied checker against the generated deck before visual QA. It reports slide and notes counts and flags em dashes, placeholders, and filler text. On macOS/Linux use `python3`; on Windows use `py -3` if `python3` is not available.

```bash
python3 scripts/qa-pptx-text.py dist/deck.pptx
```

### 2. Render using the first available path

**Preferred path: LibreOffice + Poppler**. Works on macOS, Linux, and Windows when both tools are installed and on `PATH`.

```bash
soffice --headless --convert-to pdf --outdir dist dist/deck.pptx
pdftoppm -jpeg -r 144 dist/deck.pdf qa-render/slide
```

**macOS fallback: Keynote + ImageMagick/Ghostscript.** Keynote must be installed. The terminal or automation host may need macOS Automation permission to control Keynote; opening and exporting may take longer for a large deck.

```bash
osascript <<'APPLESCRIPT'
tell application "Keynote"
  activate
  open POSIX file "/absolute/path/dist/deck.pptx"
  delay 1
  export front document to POSIX file "/absolute/path/dist/deck.pdf" as PDF
  close front document saving no
end tell
APPLESCRIPT

magick -density 144 dist/deck.pdf -quality 92 qa-render/slide-%02d.jpg
```

**Windows fallback: PowerPoint + ImageMagick/Ghostscript.** Export the PPTX to PDF from PowerPoint's normal Export UI, then use the same `magick` command above in PowerShell or Command Prompt. Do not claim unattended PowerPoint export works in every Windows environment.

**ImageMagick contact sheet** (macOS, Linux, or Windows where ImageMagick is available):

```bash
magick montage qa-render/slide-*.jpg -tile 3x5 -geometry 480x270+16+16 -background '#2E3440' qa-render/contact-sheet.jpg
```

Use `#` in ImageMagick colour arguments. The no-`#` colour rule applies only to pptxgenjs colour values.

### 3. Inspect and repeat

Inspect the contact sheet, then inspect every dense or suspicious slide at full size. For high-stakes decks, inspect every slide at full size. Check, in priority order:

1. **Text overflow / cut-off** at box or slide edges (the most common defect).
2. Overlapping elements; footers colliding with content.
3. Cramped gaps (< 0.3") or one large empty region next to a crowded one.
4. Misaligned columns/cards; inconsistent card widths.
5. Low contrast (e.g. `muted` text on `card` fill for anything that matters).
6. Any automated QA match that is not intentional.

If neither rendering chain is available, run the automated text QA and inspect the deck manually in PowerPoint, Keynote, or LibreOffice before sharing. This is a last resort, not an equivalent substitute for image QA.

After any fix, regenerate the PDF and images — pdftoppm renders the old PDF otherwise.
