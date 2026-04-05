# GitHub Copilot — Security Guide

What to watch for when using AI-generated code in enterprise environments.

---

## 1. Copilot can suggest insecure code

Copilot generates code based on patterns — it does not perform security analysis. Common vulnerability patterns it may suggest:

| Vulnerability | Example |
| --- | --- |
| SQL injection | String concatenation in queries instead of parameterised queries |
| XSS | Unsanitised user input rendered as HTML |
| Hardcoded secrets | API keys or passwords in source code |
| Insecure deserialization | Deserialising untrusted input without validation |
| Path traversal | User-controlled file paths without sanitisation |
| Weak cryptography | MD5, SHA1, or ECB mode used for sensitive data |
| Missing auth checks | Endpoints missing authorisation logic |

**These are not hypothetical.** Studies have found that Copilot-generated code has a higher rate of security vulnerabilities than human-written code when developers accept suggestions without review.

---

## 2. Copilot's built-in filters

Copilot has a **vulnerability prevention filter** that attempts to block insecure patterns in suggestions. It is not comprehensive — do not rely on it as your only control.

Enable **Duplicate Detection** in org settings to suppress suggestions matching public code (reduces licence and copy-paste vulnerability risk).

---

## 3. Developer rules

1. **Never accept a suggestion for auth, crypto, or input handling without reviewing it line by line.**
2. **Never paste secrets, credentials, or tokens into Copilot Chat** — they are sent to the model.
3. **Run your existing SAST tools** on AI-generated code. Copilot does not replace them.
4. **Be especially cautious with long completions** — the longer the suggestion, the harder it is to spot issues.

---

## 4. AI code review checklist

Use this when reviewing a PR that contains AI-generated code:

- [ ] All user inputs are validated and sanitised
- [ ] No credentials, keys, or tokens are hardcoded
- [ ] Queries use parameterised statements, not string concatenation
- [ ] Auth and authorisation checks are present on all relevant paths
- [ ] Cryptographic functions use current, approved algorithms
- [ ] Error messages do not expose internal details or stack traces
- [ ] File paths and URLs derived from user input are validated
- [ ] Dependencies introduced by the suggestion are known and approved
- [ ] SAST scan has been run and findings reviewed

---

## 5. Recommended SAST tools alongside Copilot

| Language | Tool |
| --- | --- |
| All | GitHub Advanced Security (CodeQL) |
| JavaScript / TypeScript | ESLint security plugins, Semgrep |
| Python | Bandit, Semgrep |
| Java | SpotBugs, SonarQube |
| C# / .NET | Roslyn analyzers, SonarQube |

---

## 6. Incident response

If a developer accidentally pastes sensitive data into Copilot Chat:
1. Rotate the exposed credential immediately.
2. Check audit logs for any usage of the credential.
3. Report to your security team per your incident response process.
4. GitHub does not provide a mechanism to delete specific chat messages retroactively.
