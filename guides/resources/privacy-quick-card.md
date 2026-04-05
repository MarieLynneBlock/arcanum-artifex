# Copilot Privacy — Quick Card

> Copilot Chat sends what you type to GitHub's servers. Think before you paste.

---

## OK to share

| What | Why it's fine |
| --- | --- |
| Code you wrote | It's your work product |
| Public code snippets | Already publicly available |
| Error messages and stack traces | Technical metadata, not personal data |
| Anonymised log samples | Real values removed or replaced |
| Table schemas and column names | Structural metadata, not data content |
| Test / synthetic data | Not real |
| General technical questions | No data involved |
| Function signatures and interfaces | No data content |

---

## Never share

| What | Why |
| --- | --- |
| Passwords, API keys, tokens | Credential exposure |
| Connection strings | Contains credentials and internal hostnames |
| PII — names, emails, phone numbers, addresses | Privacy / GDPR |
| National ID numbers, passport numbers | Sensitive personal data |
| Patient or health data | HIPAA / healthcare compliance |
| Financial records with real values | Regulatory risk |
| Classified or confidential business data | IP / contractual risk |
| Proprietary algorithms under NDA | IP exposure |
| Internal IP addresses, hostnames, DNS names | Infrastructure exposure |
| SSH keys, certificates | Credential exposure |

---

## When in doubt

**Anonymise first, then ask.**
Replace real values with placeholders before pasting:
- Customer names → `[CUSTOMER_NAME]`
- Email addresses → `user@example.com`
- IDs and numbers → `12345`
- Hostnames → `internal-server`

---

## One rule to remember

> If you wouldn't paste it into a public chat, don't paste it into Copilot Chat.

---

*Full guide: [responsible-use.md](../guidelines/responsible-use.md)*
