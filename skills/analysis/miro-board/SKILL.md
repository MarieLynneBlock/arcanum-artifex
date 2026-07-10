---
name: miro-board
description: >-
  Generates Miro board content in two modes:
version: 1.0.0
tags:
  - miro
  - visual
  - diagramming
  - collaboration
  - api
metadata:
  skill-author: 'Marie-Lynne Block'
---

## What this skill does

Generates Miro board content in two modes:

- **API mode** — Python code using the Miro REST API v2 to programmatically create a board with frames, sticky notes, shapes, connectors, and text.
- **Prompt mode** — A structured natural-language prompt ready to paste into Miro AI (or to use as a manual build guide) when API access is not available.

Supports the following analyst board types:

| Board type | Use case |
| --- | --- |
| User story map | Epics across top, stories in columns below, personas as swim lanes |
| Process flow | AS-IS or TO-BE swim-lane diagrams |
| Stakeholder map | Influence × interest grid |
| Gap analysis | Current state / gap / target state columns |
| Impact/effort matrix | 2×2 prioritisation quadrant |
| Retrospective | Start / Stop / Continue (or 4Ls, Mad-Sad-Glad, etc.) |
| Affinity map | Clustered sticky notes from research data |

## When to use it

- User wants to create or populate a Miro board from existing content (stories, process notes, stakeholder list, etc.).
- User asks to "make a Miro board", "visualise this in Miro", or "create a [board type] in Miro".
- User has content from another skill output (e.g., `write-user-story`, `stakeholder-map`) and wants it on a board.
- User wants a Miro AI prompt to generate a board without writing API code.

## Prerequisites (API mode)

- A Miro account with a board created (or the skill will create one).
- A Miro personal access token or OAuth token: [developers.miro.com](https://developers.miro.com/docs/rest-api-build-your-first-hello-world-app).
- Python with `requests` installed (`uv pip install requests`).

## Instructions

### Step 1 — Identify the board type and content

Ask the user (if not stated):
1. Which board type from the list above?
2. What content to populate it with? (stories, process steps, stakeholder names, etc.)
3. Which mode — API or prompt?

### Step 2 — Choose the output mode

**API mode** — use when:
- User has a Miro access token.
- Content is structured and repeated (many sticky notes, large story maps).
- User wants a reproducible, scriptable board.

**Prompt mode** — use when:
- User wants to use Miro AI or build manually.
- No API token is available.
- Content is small enough to describe in text.

### Step 3 — Generate the output

Follow the board-type instructions below, then produce the output using the format for the chosen mode.

---

## Board type instructions

### User story map

- Create a **frame** for the entire board.
- Add **epics** as a horizontal row of shapes at the top (one shape per epic, left to right in priority order).
- Under each epic, add **user stories** as a vertical column of sticky notes (blue by default).
- Add **persona rows** as a left-margin label if multiple personas are in scope.
- Add a **release line** (horizontal connector) to separate MVP stories from later releases.

### Process flow (swim-lane)

- Create one **frame** per swim lane (actor or system).
- Add **process steps** as shapes (rectangles for tasks, diamonds for decisions) within each lane.
- Connect steps with **connectors** to show flow.
- Use **colour** to distinguish: happy path (green), exception path (orange), manual step (yellow).
- Add a **start** (circle) and **end** (circle with border) node.

### Stakeholder map

- Create a **2×2 frame** with axes: Influence (Y) × Interest (X).
- Quadrant labels: Manage closely (high/high), Keep satisfied (high/low), Keep informed (low/high), Monitor (low/low).
- Add each stakeholder as a **sticky note** in their quadrant.
- Colour-code by group (business, technical, external).

### Gap analysis board

- Create **three column frames**: Current State | Gap | Target State.
- Add **sticky notes** per topic row (process, data, technology, people).
- Use red for gaps, green for target state items, grey for current state.
- Add a **priority indicator** (high/medium/low label) to each gap.

### Impact/effort matrix

- Create a **2×2 frame** with axes: Impact (Y) × Effort (X).
- Quadrant labels: Quick wins (high/low), Major projects (high/high), Fill-ins (low/low), Thankless tasks (low/high).
- Add each item as a **sticky note** in the appropriate quadrant.

### Retrospective

- Create **column frames** per category (Start / Stop / Continue, or chosen format).
- Add **sticky notes** per observation.
- Use **voting dots** (circles) to indicate team consensus items.
- Add an **action items** frame at the right with owner and due date per action.

### Affinity map

- Create an **unsorted frame** for raw input sticky notes.
- Create **cluster frames** for each theme (label at top).
- Move sticky notes into clusters.
- Add a **theme label shape** above each cluster.

---

## Output format — API mode

```python
"""
Miro board creator — [Board type]: [Title]
Requirements: pip install requests
Set MIRO_TOKEN env variable before running.
"""

import os
import requests

TOKEN = os.environ["MIRO_TOKEN"]
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json",
}
BASE_URL = "https://api.miro.com/v2"


def create_board(name: str) -> str:
    """Create a new Miro board and return its ID."""
    response = requests.post(
        f"{BASE_URL}/boards",
        headers=HEADERS,
        json={"name": name, "policy": {"permissionsPolicy": {"collaborationToolsStartAccess": "all_editors"}}},
    )
    response.raise_for_status()
    board_id = response.json()["id"]
    print(f"Board created: {response.json()['viewLink']}")
    return board_id


def add_sticky(board_id: str, content: str, x: float, y: float, color: str = "yellow") -> str:
    """Add a sticky note to the board."""
    response = requests.post(
        f"{BASE_URL}/boards/{board_id}/sticky_notes",
        headers=HEADERS,
        json={
            "data": {"content": content, "shape": "square"},
            "style": {"fillColor": color},
            "position": {"x": x, "y": y, "origin": "center"},
        },
    )
    response.raise_for_status()
    return response.json()["id"]


def add_frame(board_id: str, title: str, x: float, y: float, width: float, height: float) -> str:
    """Add a frame (container) to the board."""
    response = requests.post(
        f"{BASE_URL}/boards/{board_id}/frames",
        headers=HEADERS,
        json={
            "data": {"title": title, "format": "custom", "type": "freeform"},
            "position": {"x": x, "y": y, "origin": "center"},
            "geometry": {"width": width, "height": height},
        },
    )
    response.raise_for_status()
    return response.json()["id"]


def add_text(board_id: str, content: str, x: float, y: float, font_size: int = 14) -> str:
    """Add a text label to the board."""
    response = requests.post(
        f"{BASE_URL}/boards/{board_id}/texts",
        headers=HEADERS,
        json={
            "data": {"content": content},
            "style": {"fontSize": str(font_size), "textAlign": "center"},
            "position": {"x": x, "y": y, "origin": "center"},
        },
    )
    response.raise_for_status()
    return response.json()["id"]


def add_connector(board_id: str, start_id: str, end_id: str) -> str:
    """Add a connector between two items."""
    response = requests.post(
        f"{BASE_URL}/boards/{board_id}/connectors",
        headers=HEADERS,
        json={
            "startItem": {"id": start_id},
            "endItem": {"id": end_id},
            "style": {"strokeColor": "#333333", "strokeWidth": "2"},
        },
    )
    response.raise_for_status()
    return response.json()["id"]


# ── Board content ──────────────────────────────────────────────────────────────

def build_board():
    board_id = create_board("[Board title]")

    # [Board-type-specific creation code goes here]
    # Example: add_frame, add_sticky, add_text, add_connector calls
    # with x/y coordinates laid out on a grid

    print("Done.")


if __name__ == "__main__":
    build_board()
```

*The skill fills in `build_board()` with board-type-specific calls using the content provided by the user.*

---

## Output format — Prompt mode

```markdown
## Miro AI prompt: [Board type] — [Title]

> Paste this prompt into Miro AI (board → AI assistant → "Generate board").

---

Create a [board type] Miro board titled "[Title]".

[Board-type-specific layout description]

Content to include:

[Structured list of items, epics, stakeholders, steps, etc.]

Formatting:
- Use [colour] sticky notes for [category].
- Use [colour] sticky notes for [category].
- Group related items in labelled frames.
- Add connectors between [items] to show [relationship].
```

---

## Examples

### Example 1 — User story map from epic content

**Input:** User provides an epic with 6 stories across 2 personas.
**Expected output (API mode):** Python script that creates a board, adds the epic as a header frame, adds 6 sticky notes in columns beneath it, adds 2 persona label texts on the left margin, and draws a release line after story 3.

### Example 2 — Stakeholder map (prompt mode)

**Input:** "Create a Miro stakeholder map for these 8 people: [list with influence/interest ratings]."
**Expected output (prompt mode):** A Miro AI prompt that describes the 2×2 grid, places each person in the correct quadrant, and colour-codes by team.

### Example 3 — Gap analysis board

**Input:** "I have a gap analysis output from the gap-analysis skill. Put it on a Miro board."
**Expected output:** Three-column board (Current State / Gap / Target State) with one row per topic, sticky notes colour-coded by priority, and a legend frame.

## Notes

- Miro API coordinates use pixels; (0, 0) is the board centre. Lay items out on a grid with consistent spacing (e.g., 250px between sticky notes, 400px between columns).
- Sticky note colour values accepted by the API: `"yellow"`, `"light_yellow"`, `"orange"`, `"light_green"`, `"cyan"`, `"light_pink"`, `"violet"`, `"red"`, `"light_blue"`, `"blue"`, `"dark_blue"`, `"black"`, `"gray"`, `"dark_gray"`, `"white"`.
- The Miro API rate limit is 100 requests per second per token. For large boards, add a small delay between calls.
- Prompt mode output quality depends on the Miro AI model version in use; review and adjust positions manually after generation.
- Board sharing policy defaults to "all editors can collaborate" — adjust the `permissionsPolicy` in `create_board()` if the board is sensitive.
