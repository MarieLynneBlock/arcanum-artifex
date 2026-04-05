# GitHub Copilot — Responsible Use Guide

For enterprise coaches, leads, and developers. Covers what Copilot does with your data, when not to use it, and IP considerations.

---

## 1. What Copilot sends to the model

When you use Copilot, the following is sent to GitHub's servers:

**Inline completions:**
- The file you are currently editing (surrounding context)
- Other open files in the editor (for context matching)
- File path and language

**Copilot Chat:**
- Your chat messages
- Any files, code selections, or context you explicitly attach
- The conversation history for the current session

**What is NOT sent:**
- Your entire repository
- Files matched by `.copilotignore`
- Files excluded via org-level content exclusions (admin-configured)

> GitHub Copilot Business and Enterprise: prompts and suggestions are not used to train the model, and are not retained beyond the request. Individual plan: check the current [GitHub privacy policy](https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement) for retention terms.

---

## 2. When NOT to use Copilot

Do not use Copilot (completions or chat) when working with:

| Context | Risk |
| --- | --- |
| Credentials, API keys, passwords | Sent as context to the model |
| PII (names, emails, ID numbers) | Data privacy / compliance |
| Classified or confidential business data | May violate data handling policies |
| Patient or health data (HIPAA) | Regulatory risk |
| Financial data under strict compliance | Regulatory risk |
| Proprietary algorithms under NDA | IP exposure |

**Rule of thumb:** if you wouldn't paste it into a public chat, don't paste it into Copilot Chat.

Use `.copilotignore` and org-level content exclusions to prevent Copilot from reading sensitive files automatically.

---

## 3. IP and copyright considerations

- Copilot is trained on publicly available code, including open-source code with various licenses.
- Copilot may occasionally suggest code that closely resembles existing open-source code.
- GitHub Copilot Business and Enterprise include a **Duplicate Detection** filter that suppresses suggestions matching public code — enable this in org settings.
- Always review generated code before committing, especially long blocks.
- Your organisation's standard code review process applies to AI-generated code — it is not exempt.

**Who owns the output?**
Generated code is considered your work product — you are responsible for it, including correctness, security, and license compliance.

---

## 4. Acceptable use principles

1. **Review everything.** Copilot suggestions are a starting point, not a final answer. Treat them like code from a junior developer — read before you accept.
2. **Don't share secrets.** Never paste credentials, tokens, or sensitive data into Copilot Chat.
3. **Use exclusions.** Configure `.copilotignore` and org-level exclusions for sensitive directories.
4. **Attribute appropriately.** If Copilot produces a significant block you use verbatim, check it for licence conflicts.
5. **Stay in scope.** Use Copilot for development tasks. Don't use it to process personal data or make compliance decisions.

---

## 5. Talking points for teams

Use these when introducing Copilot to developers:

- "Copilot is an assistant, not a replacement. You are still the engineer — you decide what goes in."
- "Treat the chat like a search engine: useful, but verify the output."
- "The same code review standards apply. AI-generated code gets reviewed too."
- "If you wouldn't paste it into Google, don't paste it into Copilot Chat."
