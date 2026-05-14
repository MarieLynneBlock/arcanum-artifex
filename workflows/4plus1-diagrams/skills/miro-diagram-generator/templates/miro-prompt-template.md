# Miro prompt — [System name] — [View name]

Paste the block below into Miro AI Sidekick. Edit the bracketed placeholders first. Attach any reference context from your board (sticky notes, docs, images) before running.

---

## Role

You are a senior [solutions architect / systems analyst / business architect] working in Miro AI. Your job is to create a **[view name] view** for the system **[system name]** on a clean Miro frame. The diagram will be reviewed by **[audience — developers / cross-functional product team / executive steering committee]**.

## Input

**System under documentation:** [System name] — [one-line description].

**Scope of this view:** [what this specific view covers; what it does NOT cover].

**Key elements to include (exact list):**
- [Element 1 — name, type, role]
- [Element 2 — name, type, role]
- [Element 3 — ...]
- [...continue for every element]

**Key relationships to depict (exact list):**
- [Source] → [target] : [relationship type] : [label]
- [Source] → [target] : [relationship type] : [label]
- [...continue for every relationship]

**Context already on the board:** [describe sticky notes, docs, or images the user has placed as reference — or "none"].

## Steps

Perform these steps in order. Do not skip or reorder.

1. Create a new frame titled **"[View name] view — [System name]"**, sized approximately [width × height].
2. [Specific step — e.g. "Place a legend in the top-right corner listing the shape and colour codes used in this diagram."]
3. [Specific step — e.g. "Create [N] swimlanes as horizontal rectangles, labelled top-to-bottom: [lane 1], [lane 2], [lane 3]."]
4. [Specific step — e.g. "In swimlane 1, place [N] rounded rectangles labelled [list] — space them evenly left-to-right."]
5. [Continue with exact counts, positions, labels, and colours for every element.]
6. Draw arrows connecting the elements as listed in "Key relationships" above. Use:
   - **Solid arrow** for [meaning — e.g. synchronous call]
   - **Dashed arrow** for [meaning — e.g. asynchronous event]
   - **Dotted arrow** for [meaning — e.g. data reference]
7. [Apply colour semantics.]
8. [Any final step — e.g. "Align all elements to the Miro grid and ensure no arrows cross unnecessarily."]

## Expectation

The final Miro frame must contain exactly:
- **1 frame** titled "[View name] view — [System name]"
- **1 legend** in the top-right
- **[N] swimlanes / subgraphs / groups** (name each)
- **[N] sticky notes** of colour [X] representing [meaning]
- **[N] rectangles / rounded rectangles / other shape** representing [meaning]
- **[N] arrows**: [X] solid (for [meaning]), [Y] dashed (for [meaning]), [Z] dotted (for [meaning])
- No orphan shapes (every shape must participate in at least one labelled arrow, unless it's a legend element).
- All text is readable at the default Miro zoom level.

## Narrowing

Do **NOT** include:
- [Content belonging to a different view — e.g. "deployment details — that's in the physical view"]
- [Content belonging to a different view — e.g. "code structure — that's in the development view"]
- Decorative elements unrelated to the architecture.
- Unlabelled arrows.
- Shapes without clear semantic meaning.
- Brand colours or marketing imagery.

Do **NOT** use a shape, colour, or arrow style not listed in the Expectation section.
