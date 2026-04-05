# GitHub Copilot — Admin Guide

For GitHub org admins responsible for enabling and governing Copilot across the organisation.

---

## 1. Prerequisites

- GitHub organisation on a **Copilot Business** or **Copilot Enterprise** plan.
- Admin access to the GitHub organisation.
- Users must have individual GitHub accounts — seats are assigned per user.

---

## 2. Enable Copilot for the organisation

1. Go to your GitHub organisation → **Settings → Copilot → Access**.
2. Under **Access**, choose:
   - **Allow for all members** — all org members get access.
   - **Allow for selected members** — you control seat assignment.
3. Click **Save**.

Members selected will receive an email and can start using Copilot after installing the IDE extension.

---

## 3. Seat management

- Seats are assigned per user. Cost is per seat per month.
- Add seats: **Settings → Copilot → Access → Add members**.
- Remove seats: same screen — removing a seat revokes access immediately.
- Review usage: **Settings → Copilot → Usage** — shows active vs inactive seats.
- Inactive seats (no usage in 30 days) are candidates for reclamation.

---

## 4. Policy settings

Go to **Settings → Copilot → Policies** to configure:

| Policy | Options | Notes |
| --- | --- | --- |
| Suggestions matching public code | Allow / Block | Block = Duplicate Detection enabled |
| Copilot Chat in IDE | Enabled / Disabled | |
| Copilot on GitHub.com | Enabled / Disabled | |
| Copilot in CLI | Enabled / Disabled | |
| Copilot pull request summaries | Enabled / Disabled | Enterprise only |
| Copilot code review | Enabled / Disabled | Enterprise only |

**Recommendation:** Enable Duplicate Detection (block suggestions matching public code) in all enterprise environments.

---

## 5. Content exclusions

Content exclusions prevent Copilot from reading specific files or paths — for the entire organisation, not just a single repo.

Go to **Settings → Copilot → Content exclusion**.

Format (YAML):

```yaml
- pattern: "**/.env*"
- pattern: "**/secrets/**"
- pattern: "**/migrations/**"
```

Content exclusions apply to completions and chat context. They override `.copilotignore` and cannot be bypassed by individual users.

**Use for:** secrets directories, regulated data, proprietary algorithm files.

---

## 6. Knowledge bases (Enterprise only)

Knowledge bases let Copilot index internal documentation and codebases for use in chat.

1. Go to **Settings → Copilot → Knowledge bases**.
2. Create a knowledge base and link repositories or wikis.
3. Users access it with `@github` + the knowledge base name in chat.

Useful for: onboarding docs, internal API references, architecture decisions.

---

## 7. Audit logs

All Copilot admin actions are logged in the GitHub audit log.

Go to **Settings → Audit log** → filter by `copilot`.

Key events to monitor:
- `copilot.seat_assigned` / `copilot.seat_cancelled`
- `copilot.policy_updated`
- `copilot.content_exclusion_updated`

Export audit logs via the API or SIEM integration for compliance reporting.

---

## 8. Copilot Business vs Enterprise

| Feature | Business | Enterprise |
| --- | --- | --- |
| Inline completions | Yes | Yes |
| Copilot Chat (IDE) | Yes | Yes |
| Policy management | Yes | Yes |
| Content exclusions | Yes | Yes |
| Audit logs | Yes | Yes |
| PR summaries | No | Yes |
| Copilot code review | No | Yes |
| Knowledge bases | No | Yes |
| Fine-tuned models | No | Yes (roadmap) |

---

## 9. Rollout checklist

- [ ] Copilot plan purchased and enabled for org
- [ ] Seat access policy configured (all members or selected)
- [ ] Duplicate Detection enabled
- [ ] Content exclusions configured for sensitive paths
- [ ] Responsible use and security guides shared with all users
- [ ] IDE setup guides shared per team's IDE
- [ ] Audit log monitoring configured
