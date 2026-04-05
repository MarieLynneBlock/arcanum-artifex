# GitHub Copilot — Prompt Engineering Guide

How to write prompts that produce better results from Copilot Chat and inline completions.

---

## 1. Core principles

**Specificity beats generality.**
Vague prompts produce vague output. Tell Copilot exactly what you want, what constraints apply, and what the output should look like.

**Context is everything.**
Copilot only knows what it can see. Give it the right files, tell it about your stack, and describe the surrounding system.

**Iterate, don't restart.**
If the first response is wrong, correct it in the same conversation. Copilot has the context of your prior messages — use it.

---

## 2. Inline completion techniques

### Write the function signature first
```python
def calculate_compound_interest(principal: float, rate: float, years: int) -> float:
```
A typed, descriptive signature gives Copilot a strong signal before you've written a word of the body.

### Use descriptive comments
```javascript
// Returns paginated results sorted by createdAt descending, filtered by userId
// Throws NotFoundError if userId does not exist
async function getUserPosts(userId, page, pageSize) {
```

### Name variables clearly
`userAuthToken` beats `t`. `isEmailVerified` beats `flag`. Good names compound across the file.

### Write the first line yourself
If Copilot's opening line is wrong, write the correct first line. It will continue from where you are.

---

## 3. Chat prompt patterns

### The explain-then-ask pattern
Give context before your question:

```
This is a Node.js API using Express and Prisma. The users table has columns:
id, email, createdAt, role (enum: admin | user).

Write a middleware function that checks if the current user has the admin role.
```

### Role assignment
```
You are a senior Java engineer. Review this method for performance issues and
suggest improvements. Focus on database access patterns and N+1 queries.
```

### Constrained output
```
Write a Python function that parses a CSV file and returns a list of dicts.
Requirements:
- Use the csv module from the standard library only
- Handle missing values by defaulting to None
- Skip header row
- Return type: list[dict[str, str | None]]
```

### Step-by-step for complex tasks
```
I need to add rate limiting to our Express API. Walk me through the steps
before writing any code. I'll confirm the approach before we implement.
```

---

## 4. Context techniques (VS Code)

| Technique | How | When |
| --- | --- | --- |
| Attach a file | `#file:src/auth/middleware.ts` | When Copilot needs to see a specific file |
| Use `@workspace` | `@workspace explain the auth flow` | Cross-file questions |
| Select code first | Highlight before opening chat | Scopes the question to that code |
| Open relevant files | Have files open in tabs | Copilot reads open editors for context |

---

## 5. Anti-patterns

| Anti-pattern | Problem | Fix |
| --- | --- | --- |
| `write a login function` | No context — Copilot guesses the stack | Describe language, framework, auth method |
| Accepting the first suggestion without reading | Correctness not guaranteed | Read before `Tab` |
| One giant prompt | Hard to iterate | Break into smaller steps |
| Asking about files not in context | Copilot can't see them | Attach with `#file:` or use `@workspace` |
| Pasting full stack traces without context | Copilot doesn't know the codebase | Include the function that threw the error |

---

## 6. Prompts by use case

### Explain unfamiliar code
```
/explain

What does this function do? What are the edge cases it handles?
```

### Debug an error
```
I'm getting this error in a Spring Boot app:
[paste error]

The error occurs in this method:
[paste method]

What is causing it and how do I fix it?
```

### Generate tests
```
/tests

Write unit tests for this function using JUnit 5 and Mockito.
Cover: happy path, null input, empty list input, and exception handling.
```

### Write documentation
```
/doc

Write a Javadoc comment for this method. Include @param, @return, and @throws.
Use present tense. Keep it under 5 lines.
```

### Refactor
```
Refactor this method to reduce cyclomatic complexity. Do not change behaviour.
Keep the same method signature. Prefer early returns over nested conditionals.
```

### Code review
```
Review this pull request diff for:
1. Security vulnerabilities (OWASP top 10)
2. Performance issues
3. Missing error handling

For each finding, state: severity (high/medium/low), location, and suggested fix.
```

---

## 7. Writing good `.github/copilot-instructions.md`

The instructions file is itself a prompt — apply the same principles:

- State the stack explicitly (language, framework, version).
- Give naming conventions with examples.
- List anti-patterns, not just patterns.
- Keep it under 500 words — every word is prepended to every request.
- Test it: after writing, ask Copilot a coding question and check if the response reflects your instructions.
