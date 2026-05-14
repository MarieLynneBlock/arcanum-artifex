# Bias and fairness (AI/ML systems)

**When this concern applies:** The system uses machine-learning models — supervised, unsupervised, generative, or foundation-model-based — whose outputs influence decisions about people or resource allocation. Also applies to rules-based systems that encode consequential decisions (credit scoring, hiring, eligibility).

**Why it matters:** ML models reflect the data they're trained on, including the biases in that data. Systems that encode biased decisions at scale cause systematic harm — denying credit, opportunity, or services to people based on protected characteristics — and expose the company to regulatory action under the EU AI Act, equal-treatment laws, and sectoral regulations (FCA, SEC, ICO, equality commissions). Architectural choices determine whether bias can be detected, monitored, and mitigated.

**Regulatory / standard references:** EU AI Act (2024/1689), ISO/IEC 42001 (AI management systems), NIST AI Risk Management Framework, GDPR Art. 22 (automated decision-making), UK Equality Act 2010.

## Per-view prompts

### Logical view
- Are model components clearly identified and separated from feature-engineering and decision-orchestration components?
- Is there a dedicated **fairness evaluation** component (or well-defined interface) that can be invoked on the model's outputs?
- Is there an explicit **human-in-the-loop** or override mechanism when the model's output affects a person?
- Is the data used for training architecturally distinct from the data used for inference, and is feature parity between them auditable?
- Are feature inputs that include or proxy for protected characteristics (race, gender, age, disability, socioeconomic status, postcode-as-proxy) flagged as such?

### Process view
- At inference time, is there a step that records the input, output, model version, and confidence for later audit?
- If the model is uncertain (below a confidence threshold), does the process route to human review, or does it silently return a potentially wrong answer?
- Is there a monitoring feedback loop — does model performance on live data get measured, stratified by subgroup, and alerted on?
- Under Art. 22 GDPR, is there a process by which a data subject can request human review of an automated decision?

### Development view
- Is there a shared ML-platform module that standardises model cards, data cards, and evaluation metrics?
- Are evaluation notebooks and fairness-assessment scripts versioned alongside the model code?
- Is there a separate repository / module for the model-governance artefacts (cards, DPIAs, model risk assessments)?

### Physical view
- Is training infrastructure separated from inference infrastructure (for security, for cost attribution, for regulatory clarity)?
- Are training data sources and inference data sources documented at the infrastructure level — can an auditor trace the lineage?
- Is there a feature store / model registry? Is it versioned?
- Does the model-monitoring infrastructure capture enough to detect distribution drift, concept drift, and fairness-metric drift?

### Scenarios view
- Does at least one scenario cover **model uncertainty** — what happens when confidence is below threshold?
- Does at least one scenario cover a **contested / appealed decision** — how is a human review triggered, performed, and logged?
- Does at least one scenario cover **model-drift detection** — how is it surfaced and who acts on it?
- Does at least one scenario cover **retraining with new data** — how is fairness re-evaluated before deployment?

## Common mitigations

- **Model cards and data cards** — documented artefacts co-located with the model specifying training data sources, intended use, known limitations, and evaluated metrics (including fairness metrics stratified by subgroup).
- **Challenger / shadow model pattern** — run a second model in parallel for comparison; flag divergent decisions.
- **Confidence-threshold routing** — low-confidence decisions go to human review, not auto-execution.
- **Human-override queue** — affected parties can request review; reviews feed back into training data where appropriate (with care).
- **Fairness-aware pipelines** — metrics like demographic parity, equalised odds, calibration computed automatically per release, with thresholds enforced before deployment.
- **Counterfactual explanation service** — for consequential decisions, provide the affected person with a plausible explanation ("had your income been X, the decision would have changed").
- **Regular red-team evaluation** — deliberately probe for biased outputs; publish results internally.
- **External audit trail** — structured, append-only log of every consequential decision, sufficient to reconstruct it for a regulator.

## EU AI Act context (at a glance — this is a 2024 regulation, verify current interpretation with counsel)

- **Unacceptable risk** — banned outright. Includes some social-scoring and emotion-recognition contexts.
- **High-risk** — heavy requirements. Includes employment, creditworthiness, essential-services eligibility, law enforcement, biometric categorisation. Requires risk management, data governance, documentation, transparency, human oversight, accuracy / robustness / cybersecurity.
- **Limited risk** — transparency obligations (e.g. user knows they're interacting with AI).
- **Minimal risk** — voluntary codes of conduct.
- **General-purpose AI models** — separate obligations, especially for systemic-risk models.

If the system uses any ML component in a consequential decision, assume high-risk until legal has cleared otherwise, and architect for the requirements (documentation, logging, human oversight) accordingly.

## Red flags to probe for

- *"The model is the source of truth."* Models are probabilistic; they are evidence, not truth. If the architecture treats model output as ground truth, there's no room for correction.
- *"We retrain on production data."* Feedback loops where the model's own decisions become its training data can amplify bias catastrophically over time. The architecture should make this visible and guardable.
- *"The model is a black box so we can't audit it."* The architecture should make the inputs, outputs, and decision context recoverable even if the model internals are opaque.
- *"We removed the protected attribute from the features."* Proxies (postcode for race, name for gender) still carry the signal. Fairness requires measurement, not just field removal.

## References

- EU AI Act (Regulation (EU) 2024/1689) — https://eur-lex.europa.eu/eli/reg/2024/1689/oj
- NIST AI Risk Management Framework — https://www.nist.gov/itl/ai-risk-management-framework
- ISO/IEC 42001:2023 — AI management systems — https://www.iso.org/standard/81230.html
- Partnership on AI — "About ML" best practices — https://partnershiponai.org/
- Fairlearn, AIF360, What-If Tool — open-source libraries for fairness evaluation
