# GDPR and data protection

**When this concern applies:** The system processes personal data of EU or UK residents, or data that could be linked to an identifiable natural person. Also applies where the company is subject to UK GDPR, Swiss FADP, or adequacy-decision frameworks referencing GDPR principles.

**Why it matters:** Failure to build data protection into the architecture exposes the company to regulatory fines (up to 4% of global annual turnover under GDPR), mandatory breach disclosure, civil litigation, and severe reputational damage. More importantly, it harms the people whose data is mishandled. GDPR Article 25 requires data protection *by design and by default* — this is an architectural obligation, not a legal team problem.

**Regulatory / standard reference:** GDPR (EU 2016/679), UK GDPR, GDPR Articles 5 (principles), 25 (by design / by default), 32 (security of processing), 35 (DPIA trigger).

## Per-view prompts

### Logical view
- Is personal data concentrated in a clearly identified component (good — easier to reason about, audit, and restrict access), or scattered across many components (bad)?
- Are pseudonymisation or anonymisation points explicit in the architecture?
- Is there a dedicated component (or well-defined interface) for data-subject rights — access, rectification, erasure, portability (GDPR Art. 15–20)?
- Are different categories of personal data (general, special-category Art. 9, criminal Art. 10) architecturally separated?
- Do external integrations that receive personal data appear as explicit system-external components with their role labelled?

### Process view
- Where in each flow does personal data cross a trust boundary? Is the data minimised at that point?
- Is there an audit-trail emission at every step that processes personal data?
- Are retention clocks architecturally visible — i.e. can you point to the process that deletes / archives data after its retention period?
- Is the lawful basis for each processing step traceable (ideally attached to the data or event metadata)?

### Development view
- Is there a shared library or module that centralises personal-data handling (encryption helpers, pseudonymisation, access logging)? Or is each service rolling its own?
- Are there separate modules for regulated data versus non-regulated data, making it easy to verify what code touches what?

### Physical view
- **Data residency:** every datastore and backup location is in a jurisdiction compatible with the lawful basis. Cross-border transfers (especially to third countries) are explicitly documented with the transfer mechanism (adequacy, SCCs, BCRs).
- Encryption at rest on every datastore holding personal data, with customer-managed keys where sensitivity warrants.
- Encryption in transit end-to-end; TLS 1.2+ minimum, mTLS where the threat model requires.
- Key-management infrastructure shown explicitly (KMS, vault), with key rotation and revocation capability.
- Backup and replication destinations in compliant jurisdictions; backup retention aligns with the deletion obligations of the primary data.
- Logs containing personal data are themselves subject to retention limits — show the log-pipeline residency and retention policy.

### Scenarios view
- Does at least one scenario cover **data-subject access request (DSAR, Art. 15)** — how does the system produce a complete, structured copy of a subject's data on demand?
- Does at least one scenario cover **right to erasure (Art. 17)** — including from backups, caches, derived data, and exports?
- Does at least one scenario cover a **personal-data breach detection and 72-hour notification** flow (Art. 33)?

## Common mitigations

- **Data minimisation at ingress** — architectural pattern: normalise and drop unused fields at the edge before they enter internal datastores.
- **Pseudonymisation layer** — isolate the identifier mapping in a separate datastore with stricter access controls than the main data.
- **Dedicated DSAR service** — centralises the logic for finding a subject's data across all services; avoids every team reinventing this.
- **Tokenisation for payment / identity data** — replaces regulated data with tokens at the earliest possible point.
- **Audit log as an architectural primitive** — append-only, tamper-evident, with retention independent of main data.
- **Regional deployment** — deploy per-jurisdiction stacks rather than one global stack, especially for special-category data.
- **Consent management service** — records, versions, and enforces lawful bases and consent choices.

## Concrete failure modes to probe

- *Shadow copies:* dev copies, analytics exports, ML training sets. Each one is a separate GDPR surface. If the architecture doesn't show them, they're almost certainly present and unmanaged.
- *Vendor access:* support engineers, consultants, offshore teams. Who can access production data? Is it visible in the architecture?
- *Log bleed:* request / response logging that captures payloads containing personal data. Logs become an unintended personal-data store.
- *Third-party SDKs:* analytics, error tracking, session replay. These are processors under GDPR and often ship data out of region.
- *Derived data:* model features, embeddings, aggregates. These may still be personal data if they can re-identify individuals.

## References

- Regulation (EU) 2016/679 (GDPR) — https://eur-lex.europa.eu/eli/reg/2016/679/oj
- European Data Protection Board guidelines — https://edpb.europa.eu/our-work-tools/general-guidance_en
- ICO (UK) guidance on data protection by design — https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/accountability-and-governance/data-protection-by-design-and-default/
- ENISA guidelines on pseudonymisation techniques and best practices
- CNIL guidance on data protection impact assessments
