---
description: "Validate Forge agent configurations for schema compliance and reference integrity"
imports:
  - shared/forge-base.md
  - shared/forge-issue-creator.md
  - shared/forge-conventions.md
on:
  schedule: "weekly on wednesday"
  pull_request:
    types: [opened, synchronize]
    paths:
      - "forge-plugin/agents/*.config.json"
      - "forge-plugin/agents/*.md"
      - "forge-plugin/interfaces/schemas/agent_config.schema.json"
  workflow_dispatch:
permissions:
  contents: read
  issues: read
  pull-requests: read
tools:
  github:
    toolsets: [default]
safe-outputs:
  create-issue:
    labels: ["forge-automation", "refactoring", "agents"]
    title-prefix: "[agent-config] "
    max: 3
    close-older-issues: true
    expires: 14
---

# Forge Agent Config Validator

Validate all Forge agent definitions for schema compliance and cross-reference integrity.

## Checks

For each `forge-plugin/agents/{name}.config.json`:

1. **Schema compliance** against `forge-plugin/interfaces/schemas/agent_config.schema.json`.
2. **Skill references**: every skill in config exists in `forge-plugin/skills/`.
3. **Context domain references**: each configured domain exists under `forge-plugin/context/`.
4. **Memory directory**: configured memory path exists.
5. **Personality file parity**: matching `forge-plugin/agents/{name}.md` exists.
6. **MCP references**: referenced MCP docs exist in `forge-plugin/mcps/`.

## Scope

- On pull requests, prioritize changed agent assets.
- On schedule/manual runs, scan all agents.

## Output

Create issues only for real validation failures, with:
- Agent name and failing checks
- Evidence (paths, missing targets, schema keys)
- Exact remediation actions
