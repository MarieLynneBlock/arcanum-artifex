# Miro prompt — SynthClaim — Development view

Paste into Miro AI Sidekick. Elements derived from `../03-development-view.md`.

---

## Role

You are a senior platform engineer working in Miro AI. Your job is to produce a **Development view** — a repository and module map — for SynthClaim on a clean Miro frame. Audience: developers and software managers; keep implementation-specific names but flag ownership and build artefact types clearly.

## Input

**System:** SynthClaim — hybrid cloud claims platform.

**Scope:** Repositories, modules within repos, cross-repo dependencies, code ownership, build artefact types. Not runtime behaviour (process view) and not deployment topology (physical view).

**Repositories to depict (exact list, with ownership and artefact type):**

1. **synthclaim-platform** — shared libraries — owned by Platform Engineering — Java jar + Python wheel
   - Modules: platform-security, platform-observability, platform-event-contracts, platform-identity, platform-data
2. **synthclaim-portal** — policyholder SPA — owned by Digital Customer Experience — OCI image
   - Modules: portal-app, portal-sdk
3. **synthclaim-adjudicator-console** — internal SPA — owned by Claims Operations Tech — OCI image
   - Modules: console-app
4. **synthclaim-api-edge** — Kong config + plugins — owned by Platform Engineering — OCI image
   - Modules: kong-config, custom-plugins
5. **synthclaim-intake** — intake service — owned by Intake squad — Java jar + OCI image
   - Modules: intake-api, intake-domain, intake-adapters
6. **synthclaim-lifecycle** — lifecycle service (regulated) — owned by Claims Core squad — Java jar + OCI image
   - Modules: lifecycle-api, lifecycle-domain, mainframe-adapter, decision-module
7. **synthclaim-docpipe** — document pipeline — owned by Data Engineering — Python wheel + OCI image
   - Modules: airflow-dags, ocr-lib, field-extraction
8. **synthclaim-ml** — ML pipelines and inference (regulated — EU AI Act) — owned by Data Science — Python wheel + OCI image
   - Modules: training-pipelines, inference-service, evaluation-suite, registry-client
9. **synthclaim-dsar** — DSAR service (regulated) — co-owned by Platform Engineering and DPO — Java jar + OCI image
   - Modules: dsar-api, data-connectors
10. **synthclaim-infra** — IaC — owned by Platform Engineering — Terraform modules, Ansible playbooks, Helm charts
    - Modules: terraform-modules, ansible-playbooks, helm-charts

**Cross-repo dependencies (exact, many-to-one onto synthclaim-platform):**
- portal-sdk → platform-event-contracts
- console-app → platform-identity, platform-observability
- custom-plugins (edge) → platform-security, platform-identity
- intake-api → platform-security, platform-observability
- intake-adapters → platform-event-contracts
- lifecycle-api → platform-security, platform-observability, platform-event-contracts, platform-data
- docpipe airflow-dags → platform-observability, platform-event-contracts
- ml inference-service → ml registry-client, platform-observability
- dsar-api → platform-security, platform-observability
- Infra (terraform-modules) deploys all application repos (dashed arrows)

**Context on the board:** none assumed.

## Steps

1. Create a frame titled **"Development view — SynthClaim"**, approximately 2800 × 1800 px, landscape.
2. Place a legend in the **top-right** (320 × 260 px):
   - Rounded rectangle (pale blue) = shared library repo
   - Rounded rectangle (pale amber) = application repo
   - Rounded rectangle (pale purple) = infrastructure-as-code repo
   - Small label "(regulated)" next to a repo = subject to stricter change control
   - Solid arrow = compile-time dependency
   - Dashed arrow = deploys / provisions (Terraform)
   - Label below each repo = owning team + primary artefact type
3. Create a large **pale-blue group** at the top of the frame titled "synthclaim-platform — Shared libraries (Platform Engineering)". Inside, place **5 smaller rounded rectangles** for the modules: platform-security, platform-observability, platform-event-contracts, platform-identity, platform-data.
4. Below, arrange the **8 application repos** as pale-amber groups in a 4-column × 2-row grid. For each repo group:
   - Title the group with the repo name + owning team + artefact type (e.g. "synthclaim-lifecycle — Claims Core squad — Java jar + OCI image — (regulated)").
   - Inside, place the listed modules as small rounded rectangles, labelled.
5. At the bottom of the frame, place the **pale-purple group** for synthclaim-infra, with its three modules inside: terraform-modules, ansible-playbooks, helm-charts. Title it "synthclaim-infra — Platform Engineering".
6. Mark each regulated repo (synthclaim-lifecycle, synthclaim-ml, synthclaim-dsar) with a small red "(regulated)" badge in the group title.
7. Draw **solid arrows** from application modules to the shared-library modules they depend on (per the dependency list). Arrows may cross layers — route orthogonally with elbow connectors. Label arrows only where the target library isn't obvious.
8. Draw **dashed arrows** from `terraform-modules` (inside synthclaim-infra) to each application repo group — representing that Terraform provisions infrastructure for each.
9. Add a title at the top: **"SynthClaim — Development view — v1.0 — 2026-04-18"**.
10. Below the infra group, add a small text block listing the **CI/CD stack**: "GitLab (source) → Jenkins (build) → Nexus & ECR (registries) → Terraform Cloud + ArgoCD (deploy). Gates: SAST, dep-scan, SBOM, integration tests, four-eyes approval for regulated repos, canary deploy."
11. Align everything to the grid; ensure no arrow crosses a group border without needing to; minimise crossings.

## Expectation

The final frame must contain exactly:
- **1 frame**
- **1 title block**
- **1 legend** (6 entries)
- **1 CI/CD summary text block** at the bottom
- **1 pale-blue shared-library group** containing **5 module rectangles**
- **8 pale-amber application repo groups** containing their listed modules (total ~24 module rectangles)
- **3 "(regulated)" red badges** on lifecycle, ml, dsar
- **1 pale-purple infra group** with **3 module rectangles**
- **~15 solid dependency arrows** from application modules to shared-library modules
- **~8 dashed provisioning arrows** from terraform-modules to application groups
- All text readable; every group labelled with owner + artefact type.

## Narrowing

Do **NOT** include:
- Runtime behaviour, deployment topology, logical decomposition — these belong in other views.
- Internal package-level detail within modules (e.g. individual Java classes).
- Dependencies between application modules in different repos unless they go through `platform-event-contracts` or similar shared interfaces — direct peer-to-peer cross-repo deps would be a smell.
- Version numbers (these change; the diagram is the structural picture).
- Commercial dependencies (Kong, SageMaker, Kafka) — this is about our code, not vendors'.
- Decorative elements.
- Shapes not in the legend.
