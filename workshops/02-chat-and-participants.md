# Workshop 02 — Chat & Participants

**Duration:** 60 minutes
**Audience:** All developers
**Prerequisites:** Workshop 01 completed, Copilot Chat installed

---

## Goal

Use Copilot Chat confidently: slash commands, context attachment, and `@workspace` for cross-file questions.

---

## Exercise 1 — Slash commands (15 min)

### /explain
1. Open a file with a function you didn't write (or one you haven't looked at recently).
2. Select the entire function.
3. Open chat and type `/explain`.
4. Read the response. Ask a follow-up: "What would happen if the input is null?"

### /fix
1. Introduce a deliberate bug (wrong operator, off-by-one, missing return).
2. Select the broken function.
3. Type `/fix`. Did it find the bug?

### /tests
1. Select a function that has no tests.
2. Type `/tests`.
3. Specify the framework: `/tests using JUnit 5 and Mockito` (or your stack's equivalent).
4. Review the output — are the edge cases covered?

**Debrief:** Which command was most immediately useful? Where did you need to adjust the output?

---

## Exercise 2 — Attaching context (15 min)

1. Open chat with a blank prompt.
2. Ask: "How does error handling work in this project?"
3. Note the response quality.
4. Now type the same question but add: `#file:` and attach your main error handling file or service.
5. Compare the two responses.

Try also:
- `#folder:src/` to attach a directory.
- Selecting code in the editor before opening chat — Copilot uses the selection as context.

**Debrief:** How much did the attached context change the response?

---

## Exercise 3 — @workspace (15 min)

`@workspace` gives Copilot access to the entire project. Use it for questions that span files.

Try these prompts (adapt to your codebase):

1. `@workspace what are the main entry points of this application?`
2. `@workspace how does the application handle authentication?`
3. `@workspace show me an example of how we write unit tests in this project`
4. `@workspace what dependencies does this project use and what are they for?`

**Debrief:** Where was `@workspace` accurate? Where did it get things wrong or incomplete?

---

## Exercise 4 — Iterating in conversation (10 min)

Start a conversation and keep going — don't restart for each question.

1. Ask Copilot to write a function (your choice).
2. Ask it to add input validation.
3. Ask it to add error handling.
4. Ask it to write a test for it.
5. Ask it to explain the test to you.

**Debrief:** How did Copilot maintain context across the conversation? Where did it lose track?

---

## Exercise 5 — Real task (5 min)

Pick a real task from your current work — something small (30–60 min of work). Use chat to:
- Ask for an approach before writing any code.
- Get a starting point for the implementation.
- Ask it to review what you write.

**Debrief:** Did this change how you approached the task?

---

## Key takeaways

- `/explain`, `/fix`, `/tests`, `/doc` are your most-used commands.
- `#file:` and `#folder:` dramatically improve response relevance.
- `@workspace` is for cross-file questions — it's slower but more aware.
- Iterate in the same conversation — Copilot uses the full history.
- Select code before opening chat to scope the question automatically.
