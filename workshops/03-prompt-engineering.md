# Workshop 03 — Prompt Engineering

**Duration:** 60 minutes
**Audience:** Intermediate and above
**Prerequisites:** Workshops 01 and 02 completed

---

## Goal

Write prompts that consistently produce higher-quality, more specific output. Understand why prompts work or fail.

---

## Exercise 1 — Rewrite a bad prompt (15 min)

Below are vague prompts. Rewrite each one, then compare the output of both.

**Prompt A:**
```
write a login function
```

Your rewrite should include: language, framework, what inputs it takes, what it returns, what errors it should handle.

**Prompt B:**
```
fix my code
```

(Select a piece of broken code first.)
Your rewrite: describe what the code is supposed to do, what the current behaviour is, and what the expected behaviour is.

**Prompt C:**
```
write tests
```

Your rewrite: framework, function under test, what cases to cover, expected output format.

**Debrief:** Which element of the rewrite made the biggest difference?

---

## Exercise 2 — Role and constraints (10 min)

Add a role and constraints to a prompt and compare results.

**Without role:**
```
Review this code for problems.
```

**With role and constraints:**
```
You are a senior backend engineer with a focus on security. Review this code for:
1. SQL injection vulnerabilities
2. Missing input validation
3. Insecure error messages

For each finding: state severity (high/medium/low), the line, and a specific fix.
```

Try both on the same code block. Compare depth and specificity.

**Debrief:** Does the role assignment change the type of feedback, or just the tone?

---

## Exercise 3 — Step-by-step vs one-shot (10 min)

**One-shot:**
```
Build me a REST endpoint that accepts a user ID, fetches their orders from the database,
filters to the last 30 days, and returns them as JSON sorted by date descending.
```

**Step-by-step:**
```
I need to build a REST endpoint for user orders. Before writing code, walk me through
the approach: what the endpoint signature should look like, what DB query to use, and
how to handle errors. I'll confirm before you write anything.
```

Run both. Which output is easier to review and correct?

**Debrief:** When would you use one-shot vs step-by-step?

---

## Exercise 4 — Improving `.github/copilot-instructions.md` (15 min)

Look at your team's or project's `copilot-instructions.md` (or create one from the template if you don't have one).

1. Ask Copilot a coding question relevant to your stack.
2. Does the response follow your conventions? (naming, error handling, test framework)
3. Identify one convention that isn't in the instructions.
4. Add it. Ask the same question again. Did the response change?

Apply the prompt engineering principles — be specific, give examples, state anti-patterns.

**Debrief:** Share what you added and whether it changed Copilot's output.

---

## Exercise 5 — Build a reusable prompt file (10 min)

Create a `.prompt.md` file for a task your team does repeatedly. Examples:

- Code review for a specific concern (security, performance, accessibility)
- Generating tests in your framework with your conventions
- Writing ADRs in your format
- Summarising a PR

Use the [prompt template](../templates/prompts/prompt_blank.prompt.md) as a starting point.

Test it: open the prompt file via the chat picker and run it on real code.

**Debrief:** Is the prompt file reusable as-is, or does it need per-use customisation?

---

## Key takeaways

- Specificity, context, role, and constraints are the four levers.
- Step-by-step beats one-shot for complex tasks — confirm the approach before implementation.
- `copilot-instructions.md` is itself a prompt — apply the same discipline.
- Reusable prompt files are worth building for repeated tasks — share them in `.github/prompts/`.
- Prompt engineering is a skill: it improves with deliberate practice.
