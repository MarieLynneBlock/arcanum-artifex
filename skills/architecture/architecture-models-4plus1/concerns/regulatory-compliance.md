# Regulatory compliance (sector-specific)

**When this concern applies:** The system operates in a regulated sector — financial services (FCA, PRA, SEC, BaFin), healthcare (MDR, HIPAA, NHS DSPT), public sector (GOV.UK standards, EU public-sector obligations), telecoms (Ofcom, BEREC), energy (Ofgem), gambling (Gambling Commission), or any sector with sector-specific registration, authorisation, or reporting obligations.

**Why it matters:** Sector regulators can withdraw authorisation to operate, impose remedial orders, fine, or prosecute. Unlike cross-sector regulation (GDPR, cybersecurity), sector regulation often requires specific architectural controls (segregated environments, specific approval workflows, prescribed reporting formats). These obligations are easiest to satisfy when they're reflected in the architecture, not retrofitted.

**Standards / references:** varies by sector — see the section below for common ones.

## Per-view prompts (generic — adapt to specific sector)

### Logical view
- Is there a clear separation between **regulated business logic** and non-regulated components? Regulators often want to audit a bounded perimeter, not the whole platform.
- Are there components for **regulatory reporting** — generating the submissions the sector regulator requires, on the cadence they require?
- Is there a **compliance / control library** that centralises the implementation of regulated controls (KYC, AML, transaction monitoring, adverse-event reporting, safeguarding, etc.)?

### Process view
- Where in each business flow does a regulated check happen? Is the check's outcome recorded for audit?
- Are there flows for **regulatory notifications / reporting** — e.g. suspicious-activity report, adverse event, breach notification — with the statutory deadline modelled?
- Is there a flow for **regulator-initiated inquiries** — e.g. "produce all records relating to customer X between dates Y and Z"?

### Development view
- Are regulated and non-regulated code paths separable, so a sector-specific audit doesn't need to examine the entire codebase?
- Are there change-control processes architecturally visible — in regulated sectors, changes to regulated components often require separate approval workflows, testing evidence, and release documentation.
- Is there a separate repository for regulatory-artefact production (reports, evidence exports)?

### Physical view
- Is there an environment-separation that reflects regulatory boundaries — e.g. a dedicated "regulated" environment with stricter access controls and audit?
- Data residency aligned with sector obligations (e.g. UK financial data not leaving UK jurisdictional control; medical data aligned to local medical-data rules).
- Backups and DR in compliant locations with compliant retention.
- Clear evidence of certifications required by the sector (SOC 2, ISO 27001, PCI-DSS, HITRUST, Cyber Essentials, G-Cloud, etc.).

### Scenarios view
- At least one scenario covers **regulator information request** — produce records, audit trail, and decision rationale for a specific case.
- At least one scenario covers the **primary regulated event** for the sector — e.g. in finance: suspicious activity report; in healthcare: adverse event; in gambling: self-exclusion enforcement.
- At least one scenario covers **control failure** — a required control didn't fire; how is this detected, reported, and remediated?

## Sector-specific notes

The default concern module above is sector-agnostic. For specific sectors, consider forking a dedicated concern file:

### Financial services (banking, investments, payments)
Typical obligations: KYC / AML (UK MLR 2017, EU AMLD, US BSA), transaction reporting (MiFID II / EMIR / SFTR in EU, CAT in US), conduct and suitability, consumer duty, operational resilience (DORA in EU, PRA SS2/21 in UK), payment systems (PSD2, PSR, ACH rules). Typical controls: SAR pipeline, trade-reporting pipeline, transaction-monitoring engine, regulatory-reporting warehouse, sanctions-screening service, client-money segregation.

### Healthcare
Typical obligations: MDR / IVDR (EU), FDA 21 CFR Part 11 (US), HIPAA (US), NHS DSPT / DCB0129 / DCB0160 (UK), ISO 13485, ISO 14971. Typical controls: adverse-event reporting, electronic-signature audit trail, clinical-risk management, software-as-medical-device classification and lifecycle, privacy controls meeting healthcare-specific rules.

### Public sector (UK / EU)
Typical obligations: GOV.UK Service Standard, Technology Code of Practice, Secure by Design, Digital Identity and Attributes Trust Framework (UK), accessibility (PSBAR 2018 / WCAG 2.2 AA), Public Records Act. Typical controls: GDS service assessments, open-data publication, FOI / EIR request handling.

### Telecoms
Ofcom / BEREC obligations, NIS / NIS2 (critical national infrastructure), lawful-intercept obligations (highly regulated — involve specialist counsel).

### Energy / utilities
Ofgem / national regulator obligations, NIS2 as critical national infrastructure, smart-meter data regulation, market-reporting obligations (REMIT in EU).

### Gambling
Gambling Commission (UK) technical standards, self-exclusion (GAMSTOP), player protection, responsible gambling controls, licensing conditions (LCCP).

## Common mitigations

- **Regulated-environment pattern** — dedicated environment (physical or logical) with stricter IAM, logging, change control; regulated components deployed only there.
- **Evidence-as-code** — generate audit evidence (access reviews, control test results, reports) automatically from the system's telemetry rather than manually.
- **Regulatory reporting warehouse** — a dedicated store that denormalises operational data into the schemas regulators expect, cleanly separating business operations from reporting obligations.
- **Four-eyes / maker-checker architecture** — for regulated actions, the architecture enforces approval by a second principal, logged.
- **Time-stamped immutable log** — for most sector regulators, the log is the evidence. Architect it as a first-class system, not a by-product.
- **Change management evidence** — every production change to regulated components produces a ticket, test evidence, approval, and deploy record; these must be architecturally retrievable.

## References

- See sector-specific sections above.
- Company counsel / compliance team should maintain the current list of applicable obligations; this concern file provides the architectural framing, not the legal determination.
