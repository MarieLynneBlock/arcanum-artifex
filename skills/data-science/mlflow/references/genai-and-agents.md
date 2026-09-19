# GenAI, RAG, and Agents

Use this guide when tracing an application, comparing prompts/retrievers/models, evaluating agent
behaviour, or preparing monitoring. Start with an offline, bounded evaluation before introducing
paid judges, production traffic, broad instrumentation or mutable prompt aliases.

## Version the Whole Application

| Component | Evidence to preserve |
| --- | --- |
| Application | Code revision, routing logic, state policy, dependency lock |
| Provider/model | Provider, endpoint/deployment/model revision, region, generation settings |
| Prompt | Template and immutable version, variable schema, sanitised configuration |
| Retrieval | Corpus snapshot, chunking, embeddings, index, filters, reranker and top-k |
| Tools | Schema/implementation version, permissions, timeouts, retry/side-effect policy |
| Evaluation | Task set/split, reference labels, scorer/rubric/judge version, human review |
| Operations | Token/cost accounting, latency definition, concurrency, budget and failure rates |

Temperature zero is not a guarantee of determinism. Hosted model revisions, retrieval updates,
provider routing and execution order can change behaviour. Compare configurations on a common
versioned task set and repeat trials when variability affects the decision.

Prompt registry operations, where supported, belong to `mlflow.genai`. Resolve a mutable alias to
an immutable prompt version for evaluation/release. Log the actual resolved version, not only its
friendly alias. Do not log populated prompt text containing personal data or secrets as provenance.

## Layer Evaluation

| Layer | Example questions | Evidence |
| --- | --- | --- |
| Retrieval | Was the relevant material retrieved and ranked? | Labelled relevance, recall/NDCG at k, corpus/index ID |
| Response | Is the answer correct, supported and useful for the task? | References, deterministic checks, calibrated rubric |
| Tools | Was the right tool called with valid arguments and authorised effects? | Structured calls, outcomes, errors and sandbox assertions |
| End-to-end | Was the user's task completed within constraints? | Scenario outcome, retries, latency, cost and failure count |
| Safety/privacy | Were boundaries maintained under adverse inputs? | Approved regression scenarios, redacted traces, review |

Do not substitute fluent answers for task success or retrieval relevance for grounded generation.
For side-effecting tools, evaluate against a sandbox/mock with explicit state assertions. An agent's
claim that an action succeeded is not evidence that the intended state change occurred.

## Offline Evaluation API

`mlflow.genai.evaluate` accepts data with `inputs` dictionaries and optional `outputs` and
`expectations`, plus scorers and an optional `predict_fn`. When used, the prediction function receives
the input dictionary as keyword arguments. Verify actual input/output schemas before integrating a
framework-specific application or streaming response.

The runnable [GenAI example](../examples/genai_eval.py) uses `@mlflow.trace`, a deterministic
`@scorer`, and a synthetic lookup application. It verifies one assessment per trace, rejects scorer
errors/missing values, and compares row evidence with the aggregate. It contains one deliberate
quality failure; successful execution should not imply that every answer was correct.

For real tasks, define row identity, expected outcome/acceptable alternatives, slice membership,
error/timeout policy and input schema. Version the test data without exposing restricted content.
Use static outputs when isolating evaluator behaviour, and `predict_fn` when testing the application.
Trace-dependent scorers require real intermediate trace evidence; static answers alone do not
establish retrieval or tool correctness.

## Judges and Human Calibration

1. Prefer deterministic checks where the contract is exact: schema, citations present, allowed
   tool, arithmetic/result equality or required state transition.
2. For subjective qualities, define an anchored rubric with representative passing, failing and
   borderline examples. Use an independent calibration set reviewed by qualified humans.
3. Choose the provider/model explicitly; some built-in judges can invoke external, paid models.
   Obtain data-egress and budget approval before enabling them.
4. Measure human/judge agreement and systematic bias by slice. Check sensitivity to formatting,
   verbosity, answer position and content that tries to influence the evaluator.
5. Record judge/rubric versions and repeats. A judge-model change is an evaluation-protocol change,
   not a transparent implementation detail.
6. Review disagreement and scorer failures. Assessment exceptions may leave other rows running;
   a favourable aggregate over only completed scores is incomplete evidence.

Define minimum assessment coverage, maximum error rate, treatment of abstentions, required slice
counts, and cost/latency bounds. Report these with the quality score. Do not retry selected poor
outputs until they pass; predeclare the application retry and evaluation aggregation policy.

## Tracing and Privacy

- Decide which spans and fields are necessary before applying broad auto-instrumentation.
- Treat prompts, retrieved documents, tool arguments, outputs and trace metadata as potentially
  sensitive. Redact/minimise before export where required; restricting the UI alone is insufficient.
- Use approved synthetic data for instrumentation checks. Confirm asynchronous traces arrive and
  shutdown flushes complete; reconcile expected requests with stored traces.
- Keep correlation IDs pseudonymous and bounded. Avoid embedding credentials or raw personal
  identifiers in tags, session IDs or span attributes.
- Define sampling, retention, deletion and access policies separately from training artefacts.
  Sampled production traces cannot be assumed to represent all traffic or all failures.
- Separate user-visible latency, provider latency, tool time and evaluation overhead. Record token
  counts/cache effects and the pricing assumptions behind cost estimates.
- Inspect tracing support for the installed framework/client/server. Do not assume every scorer
  or trace search feature works identically on an older or managed backend.

## Agent Boundaries and Release

Evaluate tool errors, malformed inputs, missing permissions, unavailable dependencies, retries,
loops, budget exhaustion, cancellation and concurrency. Use benign adversarial fixtures that test
instruction boundaries and disclosure controls without real secrets or destructive actions.
Test multi-turn state isolation and confirm one user's context cannot leak into another's session.

Use a currently documented agent packaging interface only when the target platform supports it.
MLflow's older `ChatModel` interface is deprecated in favour of newer interfaces such as
`ResponsesAgent`; that does not establish support for every serving backend, tool protocol or
streaming adapter. Inspect the installed API and deploy-time requirements independently.

Offline evaluation, production monitoring and deployment are different workflows. Production
monitoring may have platform-specific scorer restrictions, retention and scheduling requirements.
Before release, require task success and failure coverage, calibrated evaluation, safe tool
authority, target-runtime checks, rollback and an accountable owner. Use the
[evaluation protocol](../assets/evaluation-protocol.md) and [release record](../assets/release-record.md).

Sources: [GenAI evaluation API](https://mlflow.org/docs/latest/api_reference/python_api/mlflow.genai.html),
[custom scorers](https://mlflow.org/docs/latest/genai/eval-monitor/scorers/custom/),
[pyfunc interfaces](https://mlflow.org/docs/latest/api_reference/python_api/mlflow.pyfunc.html).
