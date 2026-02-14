---
description: "Enforce Forge coding conventions and style consistency"
imports:
  - shared/forge-base.md
  - shared/forge-pr-creator.md
  - shared/forge-conventions.md
on:
  pull_request:
    types: [opened, synchronize]
    branches: [develop, main]
    paths:
      - "forge-plugin/**"
  workflow_dispatch:
permissions:
  contents: read
  issues: read
  pull-requests: read
tools:
  github:
    toolsets: [default]
safe-outputs:
  create-pull-request:
    labels: ["forge-automation", "style", "conventions"]
    title-prefix: "[style] "
    expires: 7
    draft: true
    if-no-changes: "ignore"
---

# Forge Convention Enforcer

Enforce naming, formatting, and structural conventions across Forge assets.

## Style Rules

1. **Naming conventions**
   - Skill directories use kebab-case.
   - Agent files are paired `{name}.md` + `{name}.config.json`.
   - Context and command files use kebab-case.
2. **Context frontmatter**
   - Required metadata fields exist and align with domain/file path.
3. **Hook script standards**
   - Bash hooks include `set -euo pipefail`.
   - Hook scripts avoid unsafe/destructive command patterns.
4. **Markdown conventions**
   - ATX headings are consistent with surrounding repository style.
5. **Interface reference rule**
   - Prefer interface references over hardcoded filesystem paths in instructional docs.

## Constraints

- Keep fixes minimal and behavior-preserving.
- Focus on convention violations in changed files first.
- Group related convention fixes into coherent PR updates.

