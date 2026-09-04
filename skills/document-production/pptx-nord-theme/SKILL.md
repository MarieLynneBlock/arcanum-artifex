---
name: pptx-nord-theme
description: Build PowerPoint (.pptx) slide decks in a Nord-themed house style — Nord palette with a dark theme (default) and a light theme, Consolas mono figures, kicker + title + standfirst anatomy, white-on-dark cards with coloured accent bars, green takeaway banners, facilitation-grade speaker notes. Use this skill whenever the user asks for a deck, slides, a presentation, an onboarding session, an inspiration session, a workshop deck, a kickoff deck, or any .pptx output.
---

# Nord Theme Deck

Generates coaching and enablement decks in a consistent Nord-themed house style. Output is always a real `.pptx` built with `pptxgenjs` (Node).

## Workflow

1. **Ask before starting when scope is materially ambiguous.** Use details supplied by the user. Before reading references or writing code, ask focused questions when an unknown audience, duration, required outcome, source authority, or footer identity would materially change the deck's content, timing, or audience fit. Do not ask for low-impact preferences alone. When source material is provided without presentation parameters and no material ambiguity remains, proceed and state these assumptions in one sentence: English, a mixed technical audience, dark theme, `green` accent, single-track, kicker + title + standfirst header, and a concise deck sized to the source. For a known duration, budget roughly one content slide per 1–2 minutes; keep short decks high-level and reserve detailed sections and exercises for longer sessions. Footer left carries `<organisation or programme> · <topic> · <session>` and footer right carries the page number.
2. **Run the environment preflight.** Before writing the generator, check `node --version`, `npm --version`, `soffice --version`, `pdftoppm -v`, `magick -version`, and `gs --version`; missing optional QA tools select the fallback in `references/pptxgenjs-notes.md`. If Node or npm is unavailable, stop and request permission before any machine-wide installation. Do not assume Homebrew, Chocolatey, apt, or another package manager is present; explain that such installation can make system-wide changes and may prompt for confirmation.
3. **Read the references.** Before writing the generator script, read:
   - `references/design-tokens.md` — palette semantics, type scale, layout grid. Non-negotiable values.
   - `references/slide-patterns.md` — recipes for every slide layout with coordinates.
   - `references/pptxgenjs-notes.md` — API footguns that corrupt files, plus the QA loop.
4. **Create a portable deck project.** Use this structure: `deck.js`, `package.json`, `package-lock.json`, `.gitignore`, `scripts/theme.js`, `dist/`, and `qa-render/`. Copy this skill's `scripts/theme.js` to the project's `scripts/theme.js`; `deck.js` must require that local copy, never an absolute skill path. Add local `pptxgenjs` as a pinned dependency and scripts for build and QA. Keep generated PPTX/PDF files in `dist/` and rendered images in `qa-render/`; ignore `node_modules/`, `dist/`, and `qa-render/` by default.
5. **Write one generator script** (`deck.js`) that builds every slide through the local `scripts/theme.js` helpers. The top-level exports are the dark theme; for light decks get the helpers via `getTheme({ mode: "light", accent: "..." })`. Use the pattern helpers (`agendaRows`, `twoColumnContrast`, `layerStack`, `decisionFlow`, `statArgument`) rather than bespoke layout code where they fit. Never hand-place kickers, titles, footers, or cards with raw coordinates — the helpers hold the grid.
6. **Add speaker notes to every content slide** (see Speaker notes below).
7. **Run QA** per `references/pptxgenjs-notes.md`: run the automated text check, render to images via the first available documented path, inspect the contact sheet plus all dense or suspicious slides at full size, fix, and re-render. On light backgrounds, additionally check every text element against the text-safe accent rule in `references/design-tokens.md` (light tones are fill-only on light surfaces).

## House rules (content and voice)

- **Language split:** the control plane (script, helper names, comments, this skill) stays in English. Slide content follows the user's requested language; default English.
- **British English** in English-language content.
- **Plain developer language, never marketing copy.** "Assign a GitHub issue; it works on a branch, runs tests, opens a PR" — not "unlock the power of autonomous agents".
- **No em dashes in slide text.** Use the middot ` · `, a colon, or a comma. Middots also separate footer segments and kicker parts.
- **Sentence-length discipline:** titles are claims, not labels ("The work changes shape, it doesn't disappear"). Standfirsts are one or two short sentences that earn the slide.
- **Figures and sources:** use `sourcePill` for a figure taken directly from a named source. Any computed figure gets a `DERIVED` pill; any estimate gets an `EST.` pill. Keep the source/attribution visible beside or beneath the figure.
- **Ethics and cost are standard sections** in onboarding/enablement decks: risk, responsibility, billing implications, sensitive-data handling. Include them unless the user explicitly drops them.
- **Sensitive domains (healthcare/public sector):** examples use synthetic or clearly hypothetical data only. Never real patient/citizen data, even as filler.
- **Numbering:** kicker carries the section number (`02 · YOUR TRAJECTORY`). Footer right shows the page number (`4` or `4 / 43`). Footer left shows the deck identity in the form `<organisation or programme> · <topic> · <session>` (e.g. `ORG · GitHub Copilot · Agentic Kickoff`).

## Speaker notes

Every content slide gets facilitation-grade notes via `slide.addNotes()` — plain text, once per slide. Convention:

```
SECTION LABEL · DURATION: N min

What to do before/while presenting (logistics, hybrid setup, Slido, demos).

Verbatim opener in quotes where the phrasing matters:
"Welcome everyone. Over the next 2.5 hours we'll cover..."

Transition cue to the next slide.
```

Notes are for the presenter running the session, not a prose summary of the slide.

## Dual-track decks

Mixed-audience decks may use EXPLORER / BUILDER track markers: small bordered pills, EXPLORER in `yellow`, BUILDER in `green`, mono uppercase. Each marked block tells one track what to focus on. Only use when the user confirms a mixed audience.

## Interactive placeholders

Slido (or similar) slides are placeholders inserted by the plugin later. Generate a simple dark slide with the poll question and a note `SLIDO PLACEHOLDER · replace via add-in`, and say so in the speaker notes.

## Definition of done

- `deck.js` runs clean and writes the `.pptx` into `dist/`; its only project dependencies are local files and the lockfile-resolved npm packages.
- The automated text QA has no unexpected matches; slide and note counts are checked.
- A contact sheet and every dense or suspicious slide are visually inspected at full size; no text overflow, no overlaps, footer on every content slide. For high-stakes decks, inspect every slide at full size.
- Speaker notes present on every content slide.
- No em dashes in slide text; no marketing phrasing; derived figures carry their pill.
