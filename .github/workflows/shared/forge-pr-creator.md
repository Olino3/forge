---
description: "Shared PR creation configuration for Forge workflows"
permissions:
  contents: read
safe-outputs:
  create-pull-request:
    base-branch: "${{ github.event.pull_request.base.ref || github.event.repository.default_branch }}"
    if-no-changes: "ignore"
---
