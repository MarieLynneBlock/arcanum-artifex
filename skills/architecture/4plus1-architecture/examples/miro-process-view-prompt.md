# Miro Prompt — Process View

## How to use this file

Copy the prompt below, replace all `[PLACEHOLDER]` values with your system's actual data, and paste into Miro AI Sidekick. Attach the relevant sticky notes or doc from your board as context before running.

---

## Prompt Template

```
You are a senior distributed systems architect creating a formal Process View diagram for an architecture review. Your output must clearly communicate runtime behaviour, concurrency, and inter-process communication to a systems integration team.

CONTEXT FROM BOARD: [Select and attach: process inventory table, sequence flow notes, and any async channel descriptions you have prepared on the board]

Create the following on this Miro board in a structured frame titled "Process View — [SYSTEM NAME]":

STEP 1 — FRAME SETUP
Create one large outer frame titled "Process View — [SYSTEM NAME]" with background colour #F0F4F8 (light grey-blue). Divide the frame into two sections:
- Left section (65% width): "Sequence Diagram — [PRIMARY SCENARIO NAME]"
- Right section (35% width): "Process Communication Map"

STEP 2 — SWIMLANE SEQUENCE DIAGRAM (left section)
Create [N] vertical swimlanes inside the left section. Each swimlane represents one process:
- Swimlane 1: "[PROCESS NAME]" — header background #2D6A9F (blue), white text
- Swimlane 2: "[PROCESS NAME]" — header background #2D9F6A (green), white text
- Swimlane 3: "[PROCESS NAME]" — header background #9F2D6A (purple), white text
- Swimlane 4: "[PROCESS NAME]" — header background #9F6A2D (amber), white text
[Add one swimlane per process — do not combine processes]

Add a vertical dashed lifeline down the centre of each swimlane in colour #CCCCCC.

Add activation bars (solid coloured rectangles, 15px wide) on each lifeline to show when a process is active. Colour the activation bar to match the swimlane header.

Add messages between lifelines as horizontal arrows:
SYNCHRONOUS CALLS (solid arrow →, black, label above line):
[LIST EACH: "Arrow from [PROCESS A] to [PROCESS B]: label '[METHOD OR OPERATION NAME]'"]
RETURN VALUES (dashed arrow -->, grey, label above line):
[LIST EACH: "Return from [PROCESS B] to [PROCESS A]: label '[RETURN VALUE OR STATUS]'"]
ASYNCHRONOUS EVENTS (solid arrow →, colour #E07B39 orange, label above line with ⚡ prefix):
[LIST EACH: "⚡ Async from [PROCESS A] to [PROCESS B]: label '[EVENT NAME]'"]

Add a combined fragment box (dashed border rectangle) for:
- alt [condition] — alternative flows: "[CONDITION DESCRIPTION]"
- opt [condition] — optional flows
- loop [count] — loops
Label each combined fragment clearly in the top-left corner.

STEP 3 — PROCESS COMMUNICATION MAP (right section)
Create one rounded rectangle per process, coloured to match its swimlane header colour. Arrange vertically in the right section.
Connect processes with directional arrows:
- SOLID black arrow = synchronous HTTP/RPC call — label with protocol and endpoint (e.g., "HTTP POST /orders")
- ORANGE dashed arrow = async message/event — label with queue/topic name (e.g., "Kafka: order.placed")
- BLUE double-headed arrow = bidirectional sync — label with protocol
Add a small annotation to each async arrow: "🔁 at-least-once" or "🔁 exactly-once" based on your system's delivery semantics.

For each process node, add a small info card attached to it:
"[PROCESS NAME]
 Concurrency: [e.g., thread pool: 16 workers / async event loop / single-threaded]
 Failure mode: [e.g., circuit breaker 3s timeout / retry x3 / dead-letter queue]"

STEP 4 — FAILURE SCENARIO ANNOTATION
In the bottom of the left section, add [N] red (#FF4444) sticky notes — one per documented failure path:
- Sticky 1: "⚠ [FAILURE SCENARIO]: [what happens — e.g., 'Payment timeout: circuit breaker opens, 503 returned to client, order held in PENDING_PAYMENT state for 10 min']"
[repeat for each failure scenario]

STEP 5 — PERFORMANCE TARGETS TABLE
In the bottom-right of the right section, create a 3-column table with:
Headers: "Flow | Target Latency (p95) | Target Throughput"
Rows: [LIST EACH FLOW WITH ITS TARGETS]
Use alternating row background: white and #F5F5F5.

STEP 6 — LEGEND
In the top-right corner of the frame, add a small white card titled "Legend":
→  Synchronous call (blocks caller)
⚡→  Async event / message (non-blocking)
⇄  Bidirectional sync
⚠  Failure / error path
Orange = async channel
Grey dashed = return / response

DO NOT include: source code, class definitions, deployment infrastructure, database schema details, or business logic rules. Do not place any elements outside the main frame. Do not use generic placeholder names — use the actual process names provided in the board context.
```

---

## Calibration Notes

- **Swimlane count.** More than 6 swimlanes makes the diagram unreadable. If you have more, split into multiple sequence diagrams — one per critical scenario.
- **Async vs sync.** The colour distinction (orange for async) is the single most important visual choice in this view. Do not let Miro default to a uniform colour.
- **Specify parallel processes.** If steps can happen simultaneously (e.g., "while the notification service sends the email, the analytics service logs the event"), say so explicitly. Without this instruction, Miro AI defaults to a purely sequential flow.
- **Mention handoffs explicitly.** State actor transitions clearly — "API Gateway authenticates → Order Service processes → Payment Service charges" — so Miro AI creates distinct swimlanes with clear responsibility boundaries.
- **Failure stickies.** These are often omitted in generated diagrams. The explicit sticky note instruction forces their inclusion. Miro AI will not invent failure scenarios — if you do not mention them, they will not appear.
- **Start with the happy path.** Generate the main success flow first. Add failure paths and edge cases in a second iteration — overcomplicating the first draft is the most common prompting error.
- **Iteration tip.** After generation, add failure paths one at a time: "In the sequence diagram, add a red dashed arrow from [Process B] back to [Process A] labelled 'timeout: 503' after the [operation] arrow." Never request multiple structural changes in a single prompt.
- **Use existing board content.** If you have sequence flow notes or process descriptions as sticky notes on the board, select and attach them as context. Miro AI will build the sequence diagram incorporating those specific details.
