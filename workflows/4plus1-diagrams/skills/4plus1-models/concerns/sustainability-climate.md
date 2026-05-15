# Sustainability and climate impact

**When this concern applies:** Any production system of material size. Mandatory to consider for systems running large-scale compute (ML training, data pipelines, high-throughput services) or those subject to corporate emissions reporting (CSRD in EU, TCFD-aligned reporting, SBTi commitments).

**Why it matters:** Digital systems' energy consumption has a material carbon footprint. Architectural choices — region selection, instance sizing, scaling policies, workload scheduling, data-movement patterns — directly affect emissions. Ignoring this is no longer defensible commercially (customers increasingly require suppliers to report emissions), regulatorily (CSRD obligations), or ethically. Sustainability is also often aligned with cost efficiency.

**Standards / references:** ISO/IEC 21031 (software carbon intensity), Green Software Foundation Principles, Software Carbon Intensity (SCI) specification, CSRD (EU Directive 2022/2464), TCFD recommendations, GHG Protocol.

## Per-view prompts

### Logical view
- Are there components that could be architected to run less often (batch versus streaming, on-demand versus always-on)?
- Are there components whose business value is marginal relative to their compute footprint? Often a candidate for retirement.
- Is caching a first-class part of the architecture, reducing redundant compute for the same result?

### Process view
- Are there flows that run continuously but only need to run periodically — e.g. hourly batch versus streaming?
- Are there flows that retry aggressively, amplifying load during failures?
- For ML inference flows: are predictions cached where the input has low cardinality? Is batching used where latency allows?

### Development view
- Is there an organisation-wide convention for measuring and attributing compute to specific code / services (enabling team-level accountability)?
- Are dependencies chosen with efficiency in mind (a lightweight runtime versus a heavy one when both would work)?

### Physical view
- **Region selection:** are cloud regions chosen for their grid carbon intensity and renewables proportion, not just latency? Cloud providers publish this (AWS, Azure, GCP carbon heatmaps).
- **Right-sizing:** are instance types matched to workload? Over-provisioning is wasted energy.
- **Auto-scaling:** does compute scale down when load is low, not just up when it's high? Many systems only scale one way.
- **Scheduling:** batch / training workloads scheduled for low-carbon periods where the grid permits (demand shifting).
- **Managed services vs self-hosted:** managed services are typically denser and more efficient than self-hosted infrastructure; use as a default where the security/compliance posture allows.
- **Data transfer:** cross-region and egress traffic have both cost and carbon implications; architect to keep hot data in-region.
- **Storage tiering:** cold data in cold storage, not in hot tiers. Lifecycle policies automated.
- **Observability:** include carbon / energy telemetry in dashboards (some cloud providers expose this directly).

### Scenarios view
- Does at least one scenario cover **idle-compute review** — how do operators identify and retire unused resources?
- Does at least one scenario cover **capacity planning** — growing demand handled efficiently, not by linear scale-out of hot tiers?

## Common mitigations

- **Carbon-aware region selection** — pick the lowest-intensity region that meets latency and data-residency constraints.
- **Right-size audits** — recurring review of instance sizing against actual utilisation; automate where possible.
- **Bidirectional autoscaling** — scale up AND down, with aggressive downscaling for non-business-hours.
- **Serverless / managed services** for workloads with bursty or unpredictable load.
- **Efficient ML** — model distillation, quantisation, pruning to reduce inference cost. Cache inference results where inputs repeat. Batch where latency allows.
- **Data lifecycle** — hot / warm / cold / archive tiering; automated policies to move or delete old data.
- **Caching at every layer** — CDN for static assets, application caches for expensive queries, result caches for deterministic computations.
- **Demand shifting** — schedule ML training and batch workloads for low-carbon periods if grid-intensity data is available.
- **Architecture reviews include carbon impact** — add it as a standing agenda item alongside cost, security, reliability.

## Anti-patterns to probe for

- *"Always-on" dev environments* — burn idle compute 24×7 for the convenience of rare usage.
- *Aggressive polling* — "check every second" when "check every minute" would do.
- *Untiered storage* — all data in the hottest, most expensive, most energy-intensive tier because no one set up lifecycle rules.
- *Multi-region deployments for DR but never tested* — you're paying (in energy) for a capability you don't exercise; consider whether the DR design is right-sized.
- *Container sprawl* — hundreds of microservices where tens would do; each container has runtime overhead.
- *Log everything forever* — log volume is a direct energy cost, and most logs are never read.

## References

- Green Software Foundation — https://greensoftware.foundation/
- Software Carbon Intensity (SCI) specification — https://sci.greensoftware.foundation/
- Cloud Carbon Footprint (open-source tool) — https://www.cloudcarbonfootprint.org/
- AWS Customer Carbon Footprint Tool, Azure Emissions Impact Dashboard, Google Cloud Carbon Footprint
- ISO/IEC 21031:2024
- CSRD (EU Directive 2022/2464) — https://eur-lex.europa.eu/eli/dir/2022/2464/oj
