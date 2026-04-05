# Workshop 01 — Inline Completions

**Duration:** 45 minutes
**Audience:** All developers, any experience level
**Prerequisites:** Copilot installed and working in your IDE

---

## Goal

Build comfort with inline completions: accepting, dismissing, cycling suggestions, and shaping output with comments and signatures.

---

## Exercise 1 — Accept and dismiss (5 min)

1. Open a new file in your primary language.
2. Write a comment: `// function that reverses a string`
3. Press Enter. Wait for a suggestion.
4. Press `Tab` to accept.
5. Delete it. Write the same comment, but this time press `Esc` to dismiss.
6. Press `Alt+]` (`Option+]` on Mac) to see an alternative suggestion.

**Debrief:** Did you get different suggestions? What influenced which one appeared first?

---

## Exercise 2 — Signature-driven completions (10 min)

Write only the function signature below (no comment). Observe what Copilot suggests for the body.

**Python:**
```python
def find_duplicates(items: list[str]) -> list[str]:
```

**Java:**
```java
public static List<String> findDuplicates(List<String> items) {
```

**TypeScript:**
```typescript
function findDuplicates(items: string[]): string[] {
```

Now rename the function to `get_repeated_values` / `getRepeatedValues`. Did the suggestion change?

**Debrief:** How much does the function name influence the output?

---

## Exercise 3 — Comment quality (15 min)

Try these three comment styles for the same task. Compare the suggestions.

**Vague:**
```python
# process data
```

**Specific:**
```python
# filter a list of orders to return only those with status "pending"
# and total value greater than 100, sorted by createdAt ascending
```

**With constraints:**
```python
# filter pending orders over 100 total, sorted by createdAt ascending
# input: list of Order dicts with keys: id, status, total, createdAt
# return: list of Order dicts
```

**Debrief:** Which comment produced the most useful suggestion? What made the difference?

---

## Exercise 4 — Partial acceptance (10 min)

1. Write a comment for a multi-step function (e.g. "read a CSV, validate each row, return list of valid rows").
2. When the suggestion appears, press `Ctrl+Right` (`Cmd+Right` on Mac) to accept one word at a time.
3. Try accepting the first line only, then continue writing your own second line.

**Debrief:** When is partial acceptance more useful than full acceptance?

---

## Exercise 5 — Real code (5 min)

Open a real file from a current project. Write a comment for a small function you actually need. Use what you learned in exercises 2 and 3.

**Debrief:** Did it produce something usable? What would you change about your comment?

---

## Key takeaways

- `Tab` accepts, `Esc` dismisses, `Alt+]` cycles alternatives.
- Signatures and specific comments consistently beat vague ones.
- Partial acceptance (`Ctrl+Right`) gives you fine-grained control.
- Copilot is better with more context — open related files, write good names.
