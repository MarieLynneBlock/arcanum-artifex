# Security

**When this concern applies:** Always. Every system has security-relevant properties; the question is whether they're explicit or implicit.

**Why it matters:** Security failures have direct operational, legal, financial, and human consequences. Security, like reliability, is a quality attribute that only gets easy to reason about if it's expressed in the architecture — bolted-on-later security is almost always weaker than designed-in security.

**Standards / references:** ISO/IEC 27001 Annex A, NIST Cybersecurity Framework, OWASP ASVS, CIS Controls, SLSA framework (supply chain).

## Per-view prompts

### Logical view
- Where is the trust boundary? Every component on the "outside" of the system must be treated as potentially hostile in the threat model.
- Is authentication centralised or scattered? Centralised is typically better (single component to harden and audit).
- Is authorisation consistent? Look for components making their own authZ decisions versus delegating to a shared authZ service.
- Are security-critical components (authN, authZ, cryptography, secrets handling) clearly named and separate from business logic?

### Process view
- Is authentication enforced before any component processes a request, and is the authenticated principal propagated through the rest of the flow?
- Are there flows that bypass the primary authN (internal APIs called "trusted", cron jobs with wildcard perms, support-backdoor endpoints)? Call them out explicitly.
- Is authorisation checked at each trust boundary — not just at the edge?
- Is there a flow that handles credential / key compromise response (revoke, rotate, notify)?
- Are errors logged with enough context for incident response but without leaking secrets?

### Development view
- Is there a shared security library (cryptography, input validation, output encoding) that teams use — or is each team rolling their own?
- Are secrets handled by a dedicated module, not scattered across services?
- Is dependency management architecturally visible — SBOM generation, vulnerability scanning gate in CI?
- Is there a clear separation between code that handles untrusted input and code that handles trusted internal data?

### Physical view
- **Network segmentation:** public, private, isolated subnets — are the boundaries meaningful? Are security groups / NSGs / firewall rules scoped to least privilege?
- **Ingress posture:** WAF in front of public endpoints? DDoS protection? TLS termination with modern cipher suites?
- **Secrets / keys:** a dedicated KMS / vault is shown; secrets are never in environment variables, config files, or container images.
- **Identity and access management:** roles scoped to least privilege. No "god-mode" human IAM roles on production. Programmatic access uses short-lived credentials.
- **Audit logging:** all control-plane actions logged to a destination the operators cannot tamper with (cross-account, write-only, immutable).
- **Incident-response path:** can the operators isolate a compromised component (network-level), revoke its credentials (IAM), and replace it (pipeline) without manual intervention?

### Scenarios view
- Does at least one scenario cover an **attack path** — credential compromise, injection, supply-chain attack, or insider threat — and the detection + response flow?
- Does at least one scenario cover a **key rotation or credential-compromise response**?
- Does at least one scenario cover **incident reconstruction from audit logs** — i.e. "could we answer a regulator's question about what happened on date X with just the logs we retain?"

## Common mitigations

- **Defence in depth** — multiple independent controls (network, identity, application, data) so a single bypass doesn't compromise the system.
- **Zero trust** — no network location implies trust. Every request authenticated and authorised regardless of origin.
- **Least privilege** — every principal (human, service) has only the permissions required for its specific job.
- **Centralised authN/authZ** — a shared identity provider and policy engine (e.g. OAuth2 with OIDC, OPA for policy) so authorisation rules are testable and auditable.
- **Immutable infrastructure** — servers / containers are replaced, not mutated. Eliminates whole classes of persistent compromise.
- **Supply-chain integrity** — signed artefacts, SBOM generation, dependency pinning, provenance attestation (SLSA levels).
- **Secret rotation automation** — secrets have a defined lifetime; rotation is automated, not manual.
- **Tamper-evident audit logging** — separate account / tenant, append-only, retention > regulatory minimum.
- **Runtime security monitoring** — anomaly detection on API calls, file-integrity monitoring, container runtime monitoring.

## Threat models to consider (adapt to system)

- **STRIDE:** Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege.
- **OWASP Top 10** for web-facing components.
- **MITRE ATT&CK** for mapping observed threats to detection / response capabilities.
- **Insider threat** — privileged insiders are often the weakest link; is the architecture able to limit their blast radius?

## References

- NIST Cybersecurity Framework 2.0 — https://www.nist.gov/cyberframework
- OWASP ASVS — https://owasp.org/www-project-application-security-verification-standard/
- ISO/IEC 27001 — https://www.iso.org/standard/27001
- SLSA (Supply-chain Levels for Software Artefacts) — https://slsa.dev/
- CIS Controls — https://www.cisecurity.org/controls
