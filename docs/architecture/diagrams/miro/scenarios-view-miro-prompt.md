# Miro prompt - Arcanum Artifex - Scenarios view

## Canonical source reference
Source of truth: `diagrams/mermaid/scenarios-view.mmd`.

The canonical Mermaid source has been expanded into the prompt below so this Miro prompt remains usable when copied outside the repository.

```mermaid
flowchart LR
	actor([Contributor]) --> start((Start))
	start --> step1[Create workflow folder]
	step1 --> step2[Add workflow, agent, prompts, templates]
	step2 --> gate{Standalone and links valid?}
	gate -->|yes| step3[Run smoke-test]
	gate -->|no| step4[Fix packaging and links]
	step4 -.-> step2
	step3 --> step5[Open PR and request review]
	step5 --> end((End))
```

## Role
Create a scenario validation view for mixed audience.

## Input
Scenario: Add a new workflow bundle.
Steps: scaffold, populate assets, validate, PR, merge.
Decision: packaging valid?
Alternate: rework and retry.

## Steps
1. Create frame titled Scenarios view - Arcanum Artifex.
2. Place actor, start event, steps, gateway, alternate step, and end event.
3. Use shared semantic colors for step types and outcomes.
4. Label yes/no branches and retry loop.
5. Add compact coverage note mapping scenario to all 4 core views.

## Expectation
- 1 frame, 1 actor, 2 events, 4 steps, 1 gateway, 2 branch labels.

## Narrowing
- No full deployment details.
- No deep module tree.
