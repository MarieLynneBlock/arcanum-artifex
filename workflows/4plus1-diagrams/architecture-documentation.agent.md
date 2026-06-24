---
name: Architecture Documentation (4plus1-diagrams)
description: Discoverable entrypoint for the standalone 4plus1-diagrams workflow bundle. Supports draw.io and Miro outputs with no MCP dependency.
tools: []
metadata:
  skill-author: 'Marie-Lynne Block'
  version: 1.0.0
---

# Discoverable Entrypoint

This file is the discoverable launcher for this standalone bundle.

## Source of truth inside this folder

- Orchestrator agent: `agents/architecture-documentation.agent.md`
- Workflow playbook: `WORKFLOW.md`
- Prompt entrypoint: `prompts/4plus1-diagrams.prompt.md`

## Required behavior

1. Open and follow `agents/architecture-documentation.agent.md` exactly.
2. Use `WORKFLOW.md` as the execution source of truth.
3. Keep this launcher thin; do not duplicate bundle logic here.
4. Enforce a clean start: one compact intake checklist first, then targeted follow-ups only when blocked.
