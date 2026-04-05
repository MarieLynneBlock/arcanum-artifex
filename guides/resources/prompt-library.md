# GitHub Copilot — Prompt Library

Ready-to-use prompts. Copy, paste, adapt. Organised by task — not by role or language.

---

## Explain code

```
Explain what this code does in plain language. Focus on what it achieves, not line by line.
```

```
Explain this code to someone who knows programming but is unfamiliar with this language.
```

```
Walk me through this code step by step. Highlight any edge cases or assumptions it makes.
```

```
What is the purpose of this function? What would break if it were removed?
```

---

## Explain a command or expression

```
Explain this shell command step by step:
[paste command]
```

```
What does this regex match? Give three examples of strings it would and would not match:
[paste regex]
```

```
Explain this SQL query. What does each clause do and what result does it produce?
[paste query]
```

```
What does this cron expression mean in plain language?
[paste cron expression]
```

---

## Write a regex

```
Write a regex that matches [describe the pattern].
Show: the pattern, an explanation of each part, and three matching examples.
```

```
Write a regex that matches a valid email address. Explain each component.
```

```
Write a regex that matches a Belgian national number (NISS/INSZ).
```

```
Write a regex that extracts the HTTP status code and URL from an nginx access log line.
```

```
I have this regex but it's not matching correctly. Explain what it does and fix it:
[paste regex]
Expected to match: [example]
Currently matching: [example]
```

---

## Write SQL

```
Write a SQL query that [describe what you need].
Tables: [list tables and key columns]
```

```
Write a query that calculates [metric] per [dimension] for [time period].
Group by [column], sort by [column] descending.
Tables: [describe schema]
```

```
Optimise this SQL query. Explain what changes you made and why:
[paste query]
```

```
Rewrite this query to avoid the subquery and use a JOIN instead:
[paste query]
```

```
Write a query to detect duplicate rows in [table] based on [columns].
```

```
Write a query that pivots rows to columns. 
Input: [describe structure]. Output: [describe desired structure].
```

---

## Write a script

```
Write a Bash script that [describe the task].
Requirements:
- [requirement 1]
- [requirement 2]
Add error handling and log output to [path or stdout].
```

```
Write a PowerShell script that [describe the task].
Target: Windows Server [version]. Run as a scheduled task.
```

```
Write a Python script that reads a CSV from [source], filters rows where [condition],
and writes the result to [destination].
```

```
Write a shell one-liner that [describe the task].
```

---

## Write tests

```
Write unit tests for this function.
Framework: [Jest / JUnit 5 / pytest / xUnit]
Cover: happy path, null/empty input, boundary values, and expected exceptions.
[paste function]
```

```
What edge cases am I missing in these tests?
[paste tests]
```

```
Write an integration test for this endpoint.
Framework: [describe stack]
Test: successful response, authentication failure, and invalid input.
[paste endpoint]
```

---

## Review a PR / code review

```
Review this code for correctness, readability, and maintainability.
For each issue: state severity (high / medium / low), location, and a suggested fix.
[paste code or diff]
```

```
Review this code for security issues. Focus on OWASP top 10.
[paste code]
```

```
Review this code for performance issues. Focus on database access patterns and N+1 queries.
[paste code]
```

```
Is there anything in this diff that could break existing behaviour?
[paste diff]
```

---

## Write documentation

```
Write a docstring / Javadoc / JSDoc for this function.
Include: what it does, parameters, return value, and any exceptions thrown.
[paste function]
```

```
Write a README section that explains how to [describe the feature or module].
Audience: a developer joining the team for the first time.
```

```
Summarise what this module does in 3–5 sentences for a technical audience.
[paste code or describe the module]
```

```
Write an Architecture Decision Record for this decision.
Context: [describe the problem]
Decision: [what was decided]
Alternatives: [what was considered]
Consequences: [trade-offs]
Format: MADR
```

---

## Debug an error

```
I'm getting this error:
[paste error message and stack trace]

It occurs in this function:
[paste function]

What is causing it and how do I fix it?
```

```
This function returns incorrect results for this input. What is wrong?
Input: [value]
Expected output: [value]
Actual output: [value]
[paste function]
```

---

## Refactor code

```
Refactor this function to reduce complexity. Do not change its behaviour or signature.
Prefer early returns over nested conditionals.
[paste function]
```

```
Extract the repeated logic from these functions into a shared helper.
[paste functions]
```

```
Rename variables and functions in this code to make their purpose clearer.
[paste code]
```

---

## Generate data

```
Generate 10 rows of realistic sample data for a table with these columns:
[list columns and types]
Format: SQL INSERT statements / CSV / JSON
```

```
Generate a JSON payload that matches this schema:
[paste schema]
```

```
Generate test data that covers these edge cases:
[list cases]
```

---

## Format and convert

```
Convert this JSON to CSV. Use the top-level keys as column headers.
[paste JSON]
```

```
Convert this CSV to a SQL INSERT statement for a table named [table].
[paste CSV]
```

```
Format this JSON — it is minified and hard to read.
[paste JSON]
```

```
Convert this cron expression to a human-readable schedule:
[paste cron]
```
