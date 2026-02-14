---
name: "open-source-contributions"
description: "Create maintainer-friendly pull requests with clean code and professional communication. Covers fork/branch workflow, commit conventions, PR description templates, code style conformance, test coverage requirements, and contributor license agreements."
version: "1.0.0"
context:
  primary_domain: "engineering"
  always_load_files: []
  detection_required: false
  file_budget: 4
memory:
  scopes:
    - type: "skill-specific"
      files: [project_conventions.md, contribution_history.md]
    - type: "shared-project"
      usage: "reference"
## tags: [open-source, pull-request, contribution, git, github, fork, code-review, community]

# skill:open-source-contributions - Create Maintainer-Friendly Pull Requests

## Version: 1.0.0

## Purpose

Guide contributors through the full lifecycle of an open-source contribution — from understanding a project's conventions and forking its repository, to crafting clean commits, writing professional PR descriptions, and passing all CI checks. This skill produces contributions that maintainers can review quickly and merge confidently.

Use this skill when:
- Contributing a bug fix, feature, or documentation update to an open-source project
- Preparing a pull request that follows project-specific conventions
- Ensuring code style, test coverage, and commit format comply with contribution guidelines
- Drafting professional PR descriptions that reference issues and explain changes clearly

## File Structure

```
skills/open-source-contributions/
├── SKILL.md (this file)
└── examples.md
```

## Interface References

- **Context**: Loaded via [ContextProvider Interface](../../interfaces/context_provider.md)
- **Memory**: Accessed via [MemoryStore Interface](../../interfaces/memory_store.md)
- **Shared Patterns**: [Shared Loading Patterns](../../interfaces/shared_loading_patterns.md)
- **Schemas**: Validated against [context_metadata.schema.json](../../interfaces/schemas/context_metadata.schema.json) and [memory_entry.schema.json](../../interfaces/schemas/memory_entry.schema.json)

## Mandatory Workflow

> **IMPORTANT**: Execute ALL steps in order. Do not skip any step.

### Step 1: Initial Analysis

- Identify the target open-source project (repository URL, organization, license)
- Locate and read the project's contribution guidelines:
  - `CONTRIBUTING.md` — contribution workflow, coding standards, PR process
  - `CODE_OF_CONDUCT.md` — community standards and expected behavior
  - `.github/PULL_REQUEST_TEMPLATE.md` — required PR description format
  - `LICENSE` — license type and CLA requirements
- Identify the issue being addressed (bug report, feature request, enhancement)
- Confirm the issue is open and unassigned (or assigned to the contributor)
- Read existing discussion on the issue for context and maintainer preferences

### Step 2: Load Memory

> Follow [Standard Memory Loading](../../interfaces/shared_loading_patterns.md#pattern-1-standard-memory-loading) with `skill="open-source-contributions"` and `domain="engineering"`.

Load project-specific memory:
- `project_conventions.md` — previously learned conventions for this project
- `contribution_history.md` — past contributions, reviewer feedback, lessons learned

### Step 3: Load Context

> Follow [Standard Context Loading](../../interfaces/shared_loading_patterns.md#pattern-2-standard-context-loading) for the `engineering` domain. Stay within the file budget declared in frontmatter.

### Step 4: Analyze Project Conventions

**YOU MUST** examine the project's development environment and standards:

1. **Contribution workflow**: Read `CONTRIBUTING.md` for fork vs. branch model, PR process, review requirements
2. **Code style**: Check for `.editorconfig`, `.prettierrc`, `.eslintrc`, `pyproject.toml`, `rustfmt.toml`, or equivalent linter/formatter configs
3. **Commit conventions**: Determine if the project uses Conventional Commits, Angular-style, or a custom format; check for commitlint config
4. **Branch naming**: Identify branch naming conventions (e.g., `fix/issue-123`, `feature/add-export`)
5. **Test requirements**: Review test framework, coverage thresholds, and testing conventions
6. **CI/CD pipeline**: Examine `.github/workflows/`, `.travis.yml`, `Jenkinsfile`, or equivalent to understand required checks
7. **Documentation standards**: Check if changes require doc updates, changelog entries, or API doc generation

### Step 5: Prepare Clean Contribution

**YOU MUST** ensure the contribution is maintainer-friendly:

1. **Fork and branch strategy**:
   - Fork the repository (if not already forked)
   - Create a descriptively named branch from the latest upstream default branch
   - Keep the branch focused on a single concern

2. **Atomic commits**:
   - Each commit addresses one logical change
   - Commit messages follow the project's convention (or Conventional Commits as default)
   - No merge commits in the PR branch (rebase onto upstream if needed)

3. **Code changes**:
   - Match the project's existing code style exactly (indentation, naming, patterns)
   - Follow established architectural patterns in the codebase
   - No unrelated changes, whitespace fixes, or drive-by refactors
   - Add or update comments where the project convention expects them

4. **Tests**:
   - Add tests that cover the new behavior or verify the bug fix
   - Ensure all existing tests pass
   - Follow the project's testing patterns and framework
   - Include edge cases and error conditions

5. **Documentation**:
   - Update README, API docs, or inline documentation as needed
   - Add changelog entry if the project maintains one
   - Update type definitions or schema files if applicable

### Step 6: Craft PR Description

**YOU MUST** write a professional, complete PR description:

1. **Title**: Clear, concise summary following project conventions
2. **Issue reference**: Link to the issue being addressed (`Fixes #123`, `Closes #456`)
3. **Description of changes**: Explain what was changed and why, not just how
4. **Testing evidence**: Describe how the changes were tested; include test output
5. **Screenshots/recordings**: For UI changes, provide before/after visuals
6. **Migration notes**: If the change affects existing users, explain the migration path
7. **Checklist**: Complete any checklist items from the PR template
8. **Additional context**: Mention trade-offs, alternative approaches considered, or follow-up work

### Step 7: Pre-Submission Checklist

**YOU MUST** verify before submitting the PR:

- [ ] All CI checks pass locally (lint, build, test)
- [ ] No unrelated changes included in the diff
- [ ] Commits are clean, atomic, and follow project conventions
- [ ] PR is focused on a single concern (no feature creep)
- [ ] Branch is rebased on the latest upstream default branch
- [ ] CLA signed if the project requires one
- [ ] PR description is complete and professional
- [ ] Self-review performed — re-read every line of the diff

### Step 8: Generate Output

- Save output to `/claudedocs/open-source-contributions_{project}_{YYYY-MM-DD}.md`
- Follow naming conventions in `../OUTPUT_CONVENTIONS.md`
- Output includes: contribution plan, PR description draft, commit messages, checklist results

### Step 9: Update Memory

> Follow [Standard Memory Update](../../interfaces/shared_loading_patterns.md#pattern-3-standard-memory-update) for `skill="open-source-contributions"`. Store any newly learned patterns, conventions, or project insights.

Update memory files:
- **project_conventions.md**: Record discovered conventions (commit format, branch naming, code style, test patterns, CI requirements)
- **contribution_history.md**: Log this contribution (date, issue, PR, outcome, reviewer feedback)

## Compliance Checklist

Before completing, verify:

- [ ] All mandatory workflow steps executed in order
- [ ] Standard Memory Loading pattern followed (Step 2)
- [ ] Standard Context Loading pattern followed (Step 3)
- [ ] Project conventions analyzed and documented (Step 4)
- [ ] Contribution prepared with clean commits and tests (Step 5)
- [ ] PR description is complete and professional (Step 6)
- [ ] Pre-submission checklist passed (Step 7)
- [ ] Output saved with standard naming convention (Step 8)
- [ ] Standard Memory Update pattern followed (Step 9)

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-07-14 | Initial release — fork/branch workflow, commit conventions, PR descriptions, code style conformance, test coverage, CLA handling |
