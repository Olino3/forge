---
description: "Generate release notes from merged PRs for tags and published releases"
imports:
  - shared/forge-base.md
  - shared/forge-issue-creator.md
  - shared/forge-conventions.md
  - shared/model-claude-haiku.md
engine:
  id: copilot
  model: claude-haiku-4.5
on:
  push:
    tags:
      - "v*"
      - "release-*"
  release:
    types: [published]
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
    labels: ["forge-automation", "release", "notes"]
    title-prefix: "[release-notes] "
    max: 1
    expires: 30
---

# Forge Release Notes Generator

Generate structured release notes from merged pull requests since the previous release boundary.

## Scope

- Include merged pull requests since the last tag/release.
- Group entries by category:
  - 🚀 Features
  - 🐛 Fixes
  - ⚠️ Breaking Changes
  - 🧰 Maintenance
  - 📚 Documentation
- Include contributor acknowledgements.

## Classification Rules

Use PR labels, titles, and conventional commit hints to classify:

- `feat:` or `enhancement` -> Features
- `fix:` or `bug` -> Fixes
- `breaking`, `!`, or explicit migration notes -> Breaking Changes
- `chore`, `refactor`, `deps`, workflow maintenance -> Maintenance
- `docs` -> Documentation

## Output

Create one issue titled:

`[release-notes] {tag-or-release-name} Draft Notes`

Issue body format:

```markdown
# Release Notes Draft — {tag}

## Summary
- Release boundary: {previous_tag} -> {current_tag}
- PRs analyzed: {count}
- Contributors: {count}

## 🚀 Features
- {PR title} ([#{pr}]) — {short summary}

## 🐛 Fixes
- ...

## ⚠️ Breaking Changes
- {PR title} ([#{pr}]) — {migration note}

## 🧰 Maintenance
- ...

## 📚 Documentation
- ...

## Contributors
- @{username}

## Upgrade Notes
- {breaking-change migration guidance}
- {dependency/compatibility note}
```

## Constraints

- Skip creation if an equivalent release-note draft issue already exists for the same tag.
- Keep notes factual and derived from merged PR content only.
- Include PR links in every section entry.

