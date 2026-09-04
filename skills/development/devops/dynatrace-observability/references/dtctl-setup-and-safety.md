# dtctl Setup and Safety

Use this reference before running Dynatrace terminal commands, especially in CI/CD or production contexts.

## Install and authenticate

```bash
# macOS/Linux with Homebrew
brew install dynatrace-oss/tap/dtctl

# OAuth login, recommended for interactive work
dtctl auth login --context my-env --environment "https://<env>.apps.dynatrace.com"

# Validate local setup
dtctl doctor
```

For headless or CI/CD environments, use a platform token stored outside the skill folder:

```bash
dtctl config set-context my-env \
  --environment "https://<env>.apps.dynatrace.com" \
  --token-ref my-token \
  --safety-level readonly

dtctl config set-credentials my-token --token "$DT_API_TOKEN"
```

Do not hard-code tokens, authorization headers, tenant URLs, or account identifiers into reports, examples, scripts, or committed configuration.

## Context checks

Run these before querying production data or applying changes:

```bash
dtctl config current-context
dtctl config describe-context "$(dtctl config current-context)"
dtctl commands --brief -o json
```

Use per-command context overrides instead of switching global context when comparing environments:

```bash
dtctl get workflows --context staging --plain
dtctl query 'fetch logs | limit 1' --context prod --plain
```

## Safety levels

Safety levels are client-side protection against accidental destructive operations. They are not an authorisation boundary.

| Level | Use when | Guidance |
| --- | --- | --- |
| `readonly` | Production monitoring, audit, incident triage | Preferred default for read-only production analysis. |
| `readwrite-mine` | Personal development and sandbox resources | Preferred default when creating owned resources. |
| `readwrite-all` | Shared team environments | Use only when team-wide mutation is intentional. |
| `dangerously-unrestricted` | Explicit admin or emergency operations | Requires strong justification; avoid for routine work. |

Actual permissions are controlled by Dynatrace token scopes. If a command fails with a permission error, inspect required scopes rather than raising the safety level first.

`dtctl` defaults a context to `readwrite-all` when no safety level is set, so set `--safety-level readonly` explicitly for production and analysis contexts.

For permission failures, expired credentials, missing contexts, ambiguous tenant targets, or scope gaps that block evidence collection, use [fallback-guidance.md](fallback-guidance.md) before changing the command or investigation conclusion.

## Command discovery

Use `dtctl commands` to avoid guessing available verbs, resources, or flags.

```bash
# Compact machine-readable command catalogue
dtctl commands --brief -o json

# Human-readable guide for agents and runbooks
dtctl commands howto

# Inspect the commands for a specific resource
dtctl commands workflow -o json
```

For the token scopes a command needs, check its `--help` output or the dtctl token-scopes reference rather than assuming a scope flag exists.

## Output modes

For automation and agent analysis:

- Prefer `--plain` for readable output without colour or prompts.
- Prefer `-o json` or `-o yaml` when another command or agent must parse output.
- Avoid parsing default table output; column order and formatting can change.
- Use `--dry-run` for mutating operations when available.
- Use `--context` for one-off environment targeting.

## Query execution

```bash
# Execute DQL safely with shell quoting
dtctl query 'fetch logs | limit 20' --plain

# Validate DQL syntax before using it in automation
dtctl verify query 'fetch spans | limit 1'
```

Use single quotes around DQL in shell commands to avoid `$`, backslash, and quote interpretation by the shell. Use files for long queries when supported by the local command version.

## Helper script

This skill includes `scripts/validate-dtctl-context.sh` for a quick local readiness check. It verifies that `dtctl` is available, prints the current context, describes that context, and runs `dtctl doctor`.

```bash
./scripts/validate-dtctl-context.sh
```

## Anti-patterns

- Do not parse table output in scripts; use structured output.
- Do not assume resource names are unique; use exact IDs for destructive or sensitive operations.
- Do not treat safety levels as security controls; use least-privilege token scopes.
- Do not skip `dtctl doctor` after authentication or context changes.
- Do not run mutating commands from a production context without checking safety level and intent.
