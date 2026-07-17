// pptx-nord-theme helpers for pptxgenjs
// Usage (dark theme, the default — top-level exports are the dark theme):
//   const pptxgen = require("pptxgenjs");
//   const T = require("./scripts/theme.js");
//   const pres = T.setup(new pptxgen());
//   const s = T.contentSlide(pres, { kicker: "01 · CALIBRATION",
//     title: "The work changes shape, it doesn't disappear",
//     standfirst: "AI takes volume. You keep judgement and direction.",
//     deckId: "ORG · GitHub Copilot · Agentic Kickoff", pageNum: 4 });
//   T.cardRow(s, [ {label:"AI HANDLES", accent:T.C.frost, headline:"volume", body:"boilerplate, tests, docs"} , ... ]);
// Usage (light theme; accent is a Nord token name or 6-digit hex, default "green"):
//   const L = require("./theme.js").getTheme({ mode: "light", accent: "frostDeep" });
//   const pres = L.setup(new pptxgen());
//   L.bannerTitle(pres, { title: "Where agents fit", deckId: "...", pageNum: 2 });
// On light surfaces use L.textSafe(colour) for any text colour you place yourself;
// light tones are fill-only there (see references/design-tokens.md).
// All coordinates are inches on the 13.333 x 7.5 canvas. Colours: 6 hex digits, no '#'.

// Official Nord palette, verbatim: https://www.nordtheme.com/docs/colors-and-palettes
const C = {
  bg: "2E3440", card: "3B4252", cardAlt: "434C5E", muted: "4C566A",                      // Polar Night nord0-3
  body: "D8DEE9", bodyLight: "E5E9F0", heading: "ECEFF4",                                // Snow Storm nord4-6
  frost: "88C0D0", frostDeep: "81A1C1", steel: "5E81AC", teal: "8FBCBB",                 // Frost nord8, 9, 10, 7
  green: "A3BE8C", yellow: "EBCB8B", orange: "D08770", red: "BF616A", purple: "B48EAD", // Aurora nord14, 13, 12, 11, 15
};
const FONT = "Calibri";
const MONO = "Consolas";
const PAGE = { w: 13.333, h: 7.5, mx: 0.6, contentW: 12.133 };
const WHITE = "FFFFFF";

// Light tones never appear as text on light surfaces; substitute the darker sibling.
// green has no darker Nord sibling: its text fallback is neutral muted, the green
// itself stays in bars, banners and pills.
const TEXT_SAFE_ON_LIGHT = {
  [C.frost]: C.steel, [C.teal]: C.steel, [C.yellow]: C.orange, [C.green]: C.muted,
};

// WCAG relative luminance; drives text colour on accent-filled shapes.
function relLum(hex) {
  const [r, g, b] = [0, 2, 4].map((i) => {
    const v = parseInt(hex.slice(i, i + 2), 16) / 255;
    return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4);
  });
  return 0.2126 * r + 0.7152 * g + 0.0722 * b;
}

function makeTheme(mode, accentIn) {
  const light = mode === "light";
  const accent = C[accentIn] || accentIn;
  const textSafe = (hex) => (light ? TEXT_SAFE_ON_LIGHT[hex] || hex : hex);
  const onFill = (hex) => (relLum(hex) > 0.3 ? C.bg : C.heading);

  const th = light ? {
    bg: C.heading, heading: C.bg, body: C.card, secondary: C.cardAlt, muted: C.muted,
    kickerText: textSafe(accent), titleAccentText: textSafe(accent), rule: C.steel,
    dividerNumeral: C.body,
    cardFill: C.card, cardHeading: C.heading, cardBody: C.body, // dark card kept on light bg
    stripText: C.body,
    codeFill: C.bodyLight, codeText: textSafe(C.frost),
  } : {
    bg: C.bg, heading: C.heading, body: C.body, secondary: C.bodyLight, muted: C.muted,
    kickerText: C.frost, titleAccentText: C.frost, rule: C.steel,
    dividerNumeral: C.card,
    cardFill: C.card, cardHeading: C.heading, cardBody: C.body,
    stripText: C.bodyLight,
    codeFill: C.cardAlt, codeText: C.frost,
  };

  function setup(pres) {
    pres.defineLayout({ name: "NORD", width: PAGE.w, height: PAGE.h });
    pres.layout = "NORD";
    return pres;
  }

  // --- slide scaffolds ----------------------------------------------------

  function baseSlide(pres) {
    const s = pres.addSlide();
    s.background = { color: th.bg };
    return s;
  }

  function contentSlide(pres, { kicker, title, standfirst, deckId, pageNum, pageTotal }) {
    const s = baseSlide(pres);
    if (kicker) s.addText(kicker.toUpperCase(), {
      x: PAGE.mx, y: 0.42, w: PAGE.contentW, h: 0.3, margin: 0,
      fontFace: FONT, fontSize: 11, bold: true, charSpacing: 3, color: th.kickerText, valign: "middle",
    });
    if (title) s.addText(title, {
      x: PAGE.mx, y: 0.72, w: PAGE.contentW, h: 0.7, margin: 0,
      fontFace: FONT, fontSize: 28, bold: true, color: th.heading, valign: "middle",
    });
    if (standfirst) s.addText(standfirst, { // string OR pptxgenjs rich-text array for inline accents
      x: PAGE.mx, y: 1.42, w: PAGE.contentW, h: 0.5, margin: 0,
      fontFace: FONT, fontSize: 14, color: th.body, valign: "middle",
    });
    if (deckId) footer(s, deckId, pageNum, pageTotal);
    return s;
  }

  // Banner-title header: accent bar carrying the slide title. An alternative to
  // kicker + title + standfirst, chosen per deck, never mixed within one deck.
  function bannerTitle(pres, { title, accent: acc, deckId, pageNum, pageTotal }) {
    const fill = acc ? (C[acc] || acc) : accent;
    const s = baseSlide(pres);
    s.addShape("roundRect", { x: PAGE.mx, y: 0.39, w: PAGE.contentW, h: 0.73, rectRadius: 0.06,
      fill: { color: fill } });
    s.addText(title, { x: PAGE.mx + 0.35, y: 0.39, w: PAGE.contentW - 0.7, h: 0.73, margin: 0,
      fontFace: FONT, fontSize: 24, bold: true, color: onFill(fill), valign: "middle" });
    if (deckId) footer(s, deckId, pageNum, pageTotal);
    return s;
  }

  function footer(s, deckId, pageNum, pageTotal) {
    s.addText(deckId, { x: PAGE.mx, y: 7.08, w: 9.0, h: 0.3, margin: 0,
      fontFace: FONT, fontSize: 9, color: th.muted, valign: "middle" });
    if (pageNum != null) s.addText(pageTotal ? `${pageNum} / ${pageTotal}` : String(pageNum), {
      x: 11.7, y: 7.08, w: 1.03, h: 0.3, margin: 0, align: "right",
      fontFace: FONT, fontSize: 9, color: th.muted, valign: "middle" });
  }

  function titleSlide(pres, { kicker, titleMain, titleAccent, subtitle, credit }) {
    const s = baseSlide(pres);
    s.addText((kicker || "").toUpperCase(), { x: 0.7, y: 2.05, w: 8.0, h: 0.4, margin: 0,
      fontFace: FONT, fontSize: 14, bold: true, charSpacing: 3, color: th.kickerText });
    s.addText(titleMain, { x: 0.66, y: 2.45, w: 8.4, h: 1.0, margin: 0,
      fontFace: FONT, fontSize: 54, bold: true, color: th.heading });
    if (titleAccent) s.addText(titleAccent, { x: 0.66, y: 3.45, w: 8.4, h: 1.0, margin: 0,
      fontFace: FONT, fontSize: 54, bold: true, color: th.titleAccentText });
    if (subtitle) s.addText(subtitle, { x: 0.7, y: 4.55, w: 8.2, h: 0.5, margin: 0,
      fontFace: FONT, fontSize: 15, color: th.body });
    s.addShape("line", { x: 0.72, y: 5.5, w: 3.4, h: 0, line: { color: th.rule, width: 1.5 } });
    if (credit) s.addText(credit, { x: 0.7, y: 5.62, w: 8.0, h: 0.4, margin: 0,
      fontFace: FONT, fontSize: 12, color: th.muted });
    return s;
  }

  function sectionDivider(pres, { number, title, framing, deckId, pageNum, pageTotal }) {
    const s = baseSlide(pres);
    s.addText(number, { x: 7.6, y: 1.2, w: 5.2, h: 5.1, margin: 0, align: "right", valign: "middle",
      fontFace: MONO, fontSize: 260, bold: true, color: th.dividerNumeral });
    s.addText(title, { x: PAGE.mx, y: 3.0, w: 9.0, h: 1.0, margin: 0,
      fontFace: FONT, fontSize: 38, bold: true, color: th.heading });
    if (framing) s.addText(framing, { x: PAGE.mx, y: 4.05, w: 8.5, h: 0.6, margin: 0,
      fontFace: FONT, fontSize: 14, color: th.body });
    if (deckId) footer(s, deckId, pageNum, pageTotal);
    return s;
  }

  // --- components ---------------------------------------------------------

  // One card: rounded rect + accent bar + label + headline + body.
  // Light theme only: soft:true renders a white card with a hairline border and
  // dark text instead of the default dark card.
  function card(s, { x, y = 2.2, w = 3.97, h = 2.35, accent: acc = C.frost, label, headline, headlineSize = 36, body, mono = false, soft = false }) {
    const isSoft = soft && light;
    if (isSoft) s.addShape("roundRect", { x, y, w, h, rectRadius: 0.06,
      fill: { color: WHITE }, line: { color: C.body, width: 0.75 } });
    else s.addShape("roundRect", { x, y, w, h, rectRadius: 0.06, fill: { color: th.cardFill } });
    s.addShape("roundRect", { x: x + 0.12, y: y + 0.16, w: 0.07, h: h - 0.32, rectRadius: 0.03, fill: { color: acc } });
    const tx = x + 0.3, tw = w - 0.45;
    if (label) s.addText(label.toUpperCase(), { x: tx, y: y + 0.2, w: tw, h: 0.3, margin: 0,
      fontFace: FONT, fontSize: 10, bold: true, charSpacing: 2, color: isSoft ? textSafe(acc) : acc, valign: "middle" });
    if (headline) s.addText(headline, { x: tx - 0.02, y: y + 0.48, w: tw, h: 0.8, margin: 0,
      fontFace: mono ? MONO : FONT, fontSize: headlineSize, bold: true, color: isSoft ? C.bg : th.cardHeading, valign: "middle" });
    if (body) s.addText(body, { x: tx, y: y + 1.4, w: tw, h: h - 1.55, margin: 0,
      fontFace: FONT, fontSize: 12, color: isSoft ? C.card : th.cardBody, valign: "top" });
  }

  // Evenly spaced row of cards across the content width.
  function cardRow(s, cards, { y = 2.2, h = 2.35, gap = 0.35 } = {}) {
    const w = (PAGE.contentW - gap * (cards.length - 1)) / cards.length;
    cards.forEach((c, i) => card(s, { ...c, x: PAGE.mx + i * (w + gap), y, w, h }));
  }

  // Numbered or timed agenda rows in the standard content body zone.
  function agendaRows(s, rows, { x = PAGE.mx, y = 2.15, w = PAGE.contentW, rowH = 0.48, gap = 0.08 } = {}) {
    rows.slice(0, 7).forEach((row, index) => {
      const rowY = y + index * (rowH + gap);
      const marker = row.time || String(index + 1).padStart(2, "0");
      const markerColour = row.break ? C.yellow : (row.accent || C.frost);
      s.addText(marker, { x, y: rowY, w: 0.72, h: rowH, margin: 0,
        fontFace: MONO, fontSize: row.time ? 13 : 24, bold: true, color: markerColour, valign: "middle" });
      s.addText(row.title, { x: x + 0.84, y: rowY, w: w - 0.84, h: 0.22, margin: 0,
        fontFace: FONT, fontSize: 14, bold: true, color: th.heading });
      if (row.description) s.addText(row.description, { x: x + 0.84, y: rowY + 0.24, w: w - 0.84, h: 0.2, margin: 0,
        fontFace: FONT, fontSize: 11.5, color: th.body });
    });
  }

  // Paired, unframed columns for DO/DON'T or TODAY/WHAT FOLLOWS comparisons.
  function twoColumnContrast(s, left, right, { x = PAGE.mx, y = 2.2, w = PAGE.contentW, h = 3.15, gap = 0.5 } = {}) {
    const columnW = (w - gap) / 2;
    const renderColumn = (column, columnX) => {
      const accentColour = column.accent || C.frost;
      s.addText((column.title || "").toUpperCase(), { x: columnX, y, w: columnW, h: 0.28, margin: 0,
        fontFace: MONO, fontSize: 12, bold: true, charSpacing: 1.5, color: textSafe(accentColour) });
      (column.lines || []).slice(0, 6).forEach((line, index) => s.addText(`▸ ${line}`, {
        x: columnX, y: y + 0.5 + index * 0.42, w: columnW, h: 0.28, margin: 0,
        fontFace: FONT, fontSize: 12, color: th.body,
      }));
    };
    renderColumn(left, x);
    s.addShape("line", { x: x + columnW + gap / 2, y: y + 0.05, w: 0, h: h - 0.1, line: { color: th.muted, width: 0.75 } });
    renderColumn(right, x + columnW + gap);
  }

  // Full-width instruction, architecture, or governance layers.
  function layerStack(s, layers, { x = PAGE.mx, y = 2.15, w = PAGE.contentW, h = 0.52, gap = 0.11, indent = 0.16 } = {}) {
    layers.slice(0, 5).forEach((layer, index) => {
      const inset = index * indent;
      const layerY = y + index * (h + gap);
      const fill = layer.fill || [C.card, C.cardAlt, C.muted][index % 3];
      const accentColour = layer.accent || C.frost;
      s.addShape("roundRect", { x: x + inset, y: layerY, w: w - inset * 2, h, rectRadius: 0.05, fill: { color: fill } });
      s.addText((layer.label || "").toUpperCase(), { x: x + inset + 0.22, y: layerY, w: 2.35, h, margin: 0,
        fontFace: MONO, fontSize: 10.5, bold: true, charSpacing: 1, color: accentColour, valign: "middle" });
      s.addText(layer.description || "", { x: x + inset + 2.65, y: layerY, w: w - inset * 2 - 2.9, h, margin: 0,
        fontFace: FONT, fontSize: 12, color: th.cardBody, valign: "middle" });
    });
  }

  // Linear decision flow with labelled steps and connective arrows.
  function decisionFlow(s, nodes, { x = PAGE.mx, y = 3.0, w = PAGE.contentW, h = 1.05, gap = 0.28 } = {}) {
    const nodeW = (w - gap * (nodes.length - 1)) / nodes.length;
    nodes.forEach((node, index) => {
      const nodeX = x + index * (nodeW + gap);
      s.addShape("roundRect", { x: nodeX, y, w: nodeW, h, rectRadius: 0.06, fill: { color: th.cardFill } });
      s.addText((node.label || "").toUpperCase(), { x: nodeX + 0.16, y: y + 0.15, w: nodeW - 0.32, h: 0.22, margin: 0,
        fontFace: MONO, fontSize: 9, bold: true, charSpacing: 1, color: node.accent || C.frost, align: "center" });
      s.addText(node.text || "", { x: nodeX + 0.16, y: y + 0.43, w: nodeW - 0.32, h: 0.4, margin: 0,
        fontFace: FONT, fontSize: 11.5, color: th.cardBody, align: "center", valign: "middle" });
      if (index < nodes.length - 1) s.addText("→", { x: nodeX + nodeW, y: y + 0.33, w: gap, h: 0.35, margin: 0,
        fontFace: FONT, fontSize: 17, bold: true, color: th.rule, align: "center" });
    });
  }

  // Large sourced or estimated figure with a compact attribution and caveat pill.
  function statArgument(s, figure, attribution, { x = PAGE.mx, y = 2.25, w = 5.6, figureSize = 54, accent: acc = C.frost, caveat, caveatWidth, takeaway } = {}) {
    s.addText(figure, { x, y, w, h: 0.85, margin: 0, fontFace: MONO, fontSize: figureSize, bold: true, color: acc, valign: "middle" });
    if (attribution) s.addText(attribution, { x, y: y + 0.98, w, h: 0.28, margin: 0,
      fontFace: FONT, fontSize: 9, color: th.muted, valign: "middle" });
    if (caveat) pill(s, caveat, { x: x + w - (caveatWidth || 0.9), y: y + 0.25, w: caveatWidth || 0.9, accent: C.muted, filled: true });
    if (takeaway) banner(s, takeaway, { y: y + 1.55 });
  }

  // Attribution marker for figures taken directly from a named source.
  function sourcePill(s, text, { x, y, w = 1.0, h = 0.28 } = {}) {
    pill(s, text || "SOURCE", { x, y, w, h, accent: C.muted, filled: true });
  }

  function sectionTakeaway(s, textRuns, options = {}) {
    banner(s, textRuns, { variant: "green", ...options });
  }

  // Green banner (directive) or dark strip (nuance). textRuns: string or rich-text array.
  function banner(s, textRuns, { y = 5.75, h = 0.7, variant = "green" } = {}) {
    const green = variant === "green";
    s.addShape("roundRect", { x: PAGE.mx, y, w: PAGE.contentW, h, rectRadius: 0.06,
      fill: { color: green ? C.green : C.card } });
    s.addText(textRuns, { x: PAGE.mx + 0.35, y, w: PAGE.contentW - 0.7, h, margin: 0,
      fontFace: FONT, fontSize: 12.5, color: green ? C.bg : th.stripText, valign: "middle" });
  }

  // Small bordered pill, mono uppercase (EXPLORER / BUILDER / DERIVED / EST.)
  function pill(s, text, { x, y, w = 1.1, h = 0.28, accent: acc = C.frost, filled = false } = {}) {
    s.addShape("roundRect", { x, y, w, h, rectRadius: 0.14,
      fill: filled ? { color: acc } : { color: th.bg },
      line: { color: acc, width: 1 } });
    s.addText(text.toUpperCase(), { x, y, w, h, margin: 0, align: "center", valign: "middle",
      fontFace: MONO, fontSize: 9, bold: true, charSpacing: 1,
      color: filled ? (light ? onFill(acc) : C.bg) : textSafe(acc) });
  }

  // Nested code block inside a card or on its own: alt-surface fill, Consolas.
  function codeBlock(s, text, { x, y, w, h = 0.55, size = 10.5, color } = {}) {
    s.addShape("roundRect", { x, y, w, h, rectRadius: 0.04, fill: { color: th.codeFill } });
    s.addText(text, { x: x + 0.15, y, w: w - 0.3, h, margin: 0,
      fontFace: MONO, fontSize: size, color: color ? textSafe(color) : th.codeText, valign: "middle" });
  }

  return {
    mode, C, FONT, MONO, PAGE, ...th, accent, accentText: textSafe(accent), textSafe, onFill,
    setup, baseSlide, contentSlide, bannerTitle, titleSlide, sectionDivider, footer,
    card, cardRow, agendaRows, twoColumnContrast, layerStack, decisionFlow, statArgument,
    banner, sectionTakeaway, pill, sourcePill, codeBlock,
  };
}

// mode "dark" (default) or "light"; accent: Nord token name or 6-digit hex, default green.
function getTheme({ mode = "dark", accent = "green" } = {}) {
  return makeTheme(mode, accent);
}

// Top-level exports are the dark theme, so existing deck scripts keep working.
module.exports = { ...getTheme(), getTheme };
