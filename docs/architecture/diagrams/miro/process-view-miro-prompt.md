# Miro prompt - Arcanum Artifex - Process view (swimlane)

## Canonical source reference
Source of truth: `diagrams/mermaid/process-view.mmd`.

The canonical Mermaid source has been expanded into the prompt below so this Miro prompt remains usable when copied outside the repository.

```mermaid
flowchart LR
	subgraph lane1[Product / Content Owner]
		p_start((Start))
		p_define[Define new workflow scope]
		p_submit[/Submit proposal PR/]
	end

	subgraph lane2[Architecture / Governance]
		g_review[Review architecture intent]
		g_gate{Policy and quality met?}
		g_feedback[/Request changes/]
		g_approve[Approve for merge]
	end

	subgraph lane3[Automation / CI]
		c_validate[Run smoke-test and link checks]
		c_pack[Assemble standalone bundle]
		c_publish[Publish merged bundle]
		c_end((End))
	end

	p_start --> p_define --> p_submit --> g_review --> g_gate
	g_gate -->|no| g_feedback -.-> p_define
	g_gate -->|yes| c_validate --> c_pack --> g_approve --> c_publish --> c_end
```

## Role
You are a senior architect creating a BPMN-style process view for a mixed audience.

## Input
Flow: idea to published workflow bundle.
Lanes (3): Product and Content, Architecture and Governance, Automation and CI.

Tasks/events/gateways:
- Start event
- User tasks: Define scope, Submit proposal
- Service tasks: Review intent, Validate bundle, Package and publish
- Gateway: Policy and quality met?
- User task: Request changes (feedback loop)
- End event

## Steps
1. Create frame titled Process view - Arcanum Artifex (swimlane) (2400x1400).
2. Create 3 horizontal lanes with neutral background.
3. Place start event (success), end event (error for rejected or terminal path marker where used).
4. Place user tasks in primary color and service tasks in success color.
5. Place gateway in warning color.
6. Draw sequence and feedback arrows with labels.
7. Add legend with shared mapping: user task=primary, service/start=success, gateway=warning, end/error=error.

## Expectation
- 1 frame, 3 lanes, 2 events, 4 service/user tasks, 1 gateway, labeled connectors.

## Narrowing
- No infrastructure nodes.
- No module ownership charts.
