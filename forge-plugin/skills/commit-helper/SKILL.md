---
name: commit-helper
## description: Crafts meaningful change chronicles by analyzing git diffs and generating precise, convention-compliant commit messages. Evaluates change scope, classifies modifications, detects breaking changes, and produces structured commit messages following Conventional Commits or project-specific conventions. Like Hephaestus inscribing the purpose of each forged artifact, this skill ensures every commit tells the story of its changes with clarity and intent.

# Commit Message Chronicler

## ⚠️ MANDATORY COMPLIANCE ⚠️

**CRITICAL**: The 4-step workflow outlined in this document MUST be followed in exact order for EVERY commit message generation. Skipping steps or deviating from the procedure will result in inaccurate or incomplete commit messages. This is non-negotiable.

## File Structure

- **SKILL.md** (this file): Main instructions and MANDATORY workflow
- **examples.md**: Usage scenarios with different commit types and generated messages
- **Memory**: Project-specific memory accessed via `memoryStore.getSkillMemory("commit-helper", "{project-name}")`. See [MemoryStore Interface](../../interfaces/memory_store.md).
- **templates/**:
  - `commit_template.md`: Standard commit message output format template


## Interface References

- **Context**: Loaded via [ContextProvider Interface](../../interfaces/context_provider.md)
- **Memory**: Accessed via [MemoryStore Interface](../../interfaces/memory_store.md)
- **Shared Patterns**: [Shared Loading Patterns](../../interfaces/shared_loading_patterns.md)

## Focus Areas

Commit message crafting evaluates 7 critical dimensions:

1. **Change Classification**: Categorize as feat, fix, refactor, docs, style, test, chore, perf, ci, build, or revert
2. **Scope Detection**: Identify the module, component, or subsystem affected by the change
3. **Breaking Change Identification**: Detect API changes, removed features, schema migrations, or interface modifications that break backward compatibility
4. **Message Clarity**: Ensure the subject line is imperative, concise (≤72 chars), and descriptive of the *what* and *why*
5. **Convention Compliance**: Follow Conventional Commits specification or project-specific commit conventions
6. **Context Preservation**: Capture motivation, trade-offs, and related issue references in the commit body
7. **Narrative Quality**: Craft messages that tell the story of the change — not just what changed, but why it matters

**Note**: The skill analyzes staged or diffed changes to generate messages. It does not execute `git commit` itself unless explicitly requested.

---

## Purpose

[TODO: Add purpose description]


## MANDATORY WORKFLOW (MUST FOLLOW EXACTLY)

### ⚠️ STEP 1: Analyze Changes (REQUIRED)

**YOU MUST:**
1. Use the `get-git-diff` skill or run `git diff --staged` to obtain the current changes
2. If no staged changes exist, check `git diff` for unstaged changes and inform the user
3. Run `git diff --stat --staged` to get a high-level summary of affected files and line counts
4. Run `git diff --name-status --staged` to identify file operations (A/M/D/R)
5. Read the actual diff content to understand the substance of each change

**DO NOT PROCEED WITHOUT UNDERSTANDING THE CHANGES**

### ⚠️ STEP 2: Determine Context (REQUIRED)

**YOU MUST:**
1. **Classify the change type**: Determine the primary Conventional Commits type:
   - `feat`: A new feature or capability
   - `fix`: A bug fix or correction
   - `refactor`: Code restructuring without behavior change
   - `docs`: Documentation-only changes
   - `style`: Formatting, whitespace, or cosmetic changes (no logic change)
   - `test`: Adding or updating tests
   - `chore`: Maintenance tasks, dependency updates, tooling
   - `perf`: Performance improvements
   - `ci`: CI/CD pipeline changes
   - `build`: Build system or external dependency changes
   - `revert`: Reverting a previous commit
2. **Identify scope**: Determine the affected module, component, or area (e.g., `auth`, `api`, `parser`, `cli`)
3. **Detect breaking changes**: Look for removed public APIs, changed function signatures, renamed exports, schema migrations, or configuration format changes
4. **Check project memory**: Use `memoryStore.getSkillMemory("commit-helper", "{project-name}")` to load project-specific commit conventions, preferred scopes, or style guidelines. See [MemoryStore Interface](../../interfaces/memory_store.md) for method details.
5. **Gather additional context**: If the change purpose is ambiguous, ask the user clarifying questions:
   - What motivated this change?
   - Is this related to a specific issue or ticket?
   - Are there any breaking changes the diff doesn't make obvious?

**DO NOT PROCEED WITHOUT CLASSIFYING THE CHANGE**

### ⚠️ STEP 3: Craft Commit Message (REQUIRED)

**YOU MUST:**
1. **Compose the subject line** following this format:
   ```
   <type>(<scope>): <imperative description>
   ```
   - Use imperative mood ("add" not "added", "fix" not "fixes")
   - Keep to 72 characters or fewer
   - Do not end with a period
   - Be specific: "fix null pointer in user lookup" not "fix bug"
2. **Write the body** (if the change warrants explanation):
   - Separate from subject with a blank line
   - Wrap at 72 characters per line
   - Explain *what* changed and *why*, not *how* (the diff shows how)
   - Include motivation, context, and contrast with previous behavior
3. **Add footer** (if applicable):
   - `BREAKING CHANGE: <description>` for breaking changes
   - `Fixes #<issue>` or `Closes #<issue>` for issue references
   - `Refs #<issue>` for related but not closing references
   - Co-author trailers if applicable
4. **Use the template** from `templates/commit_template.md` for output formatting

**DO NOT USE VAGUE OR GENERIC MESSAGES**

### ⚠️ STEP 4: Review & Refine (REQUIRED)

**YOU MUST validate the message against these criteria:**
1. **Subject line check**:
   - [ ] Uses correct type prefix
   - [ ] Scope is accurate and consistent with project conventions
   - [ ] Imperative mood used
   - [ ] 72 characters or fewer
   - [ ] No trailing period
   - [ ] Specific and descriptive
2. **Body check** (if present):
   - [ ] Explains motivation and context
   - [ ] Wrapped at 72 characters
   - [ ] Does not repeat the diff
3. **Footer check** (if applicable):
   - [ ] Breaking changes documented with `BREAKING CHANGE:` prefix
   - [ ] Issue references use correct format
4. **Present the final message** to the user for approval
5. **Offer alternatives**: If the change could be classified differently, present 1-2 alternative messages with explanation of the trade-offs

**DO NOT SKIP VALIDATION**

**OPTIONAL: Update Project Memory**

If project-specific conventions are discovered during the process, use `memoryStore.update("commit-helper", "{project-name}", ...)` to store insights:
- Preferred commit types and scopes
- Project-specific conventions (e.g., ticket number format, scope naming)
- Common patterns observed in existing commit history

See [MemoryStore Interface](../../interfaces/memory_store.md) for `update()` and `append()` method details.

---

## Compliance Checklist

Before completing ANY commit message generation, verify:
- [ ] Step 1: Changes analyzed using git diff (staged or otherwise)
- [ ] Step 2: Change type classified, scope identified, breaking changes checked
- [ ] Step 3: Commit message crafted following Conventional Commits format with template
- [ ] Step 4: Message validated against all quality criteria and presented to user

**FAILURE TO COMPLETE ALL STEPS INVALIDATES THE COMMIT MESSAGE**

---

## Output File Naming Convention

**Format**: `commit_msg_{short_hash}.md`

Where:
- `{short_hash}` = First 7 characters of the current HEAD commit hash

**Examples**:
- `commit_msg_a1b2c3d.md` (for changes based on HEAD a1b2c3d)
- `commit_msg_staged.md` (when generating for staged but uncommitted changes)

**Alternative**: If the user requests the message be applied directly, use `git commit -m` with the generated message instead of file output.

---

## Conventional Commits Quick Reference

### Format
```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

### Types
| Type | Description |
|------|-------------|
| `feat` | A new feature |
| `fix` | A bug fix |
| `docs` | Documentation only changes |
| `style` | Changes that do not affect meaning of code |
| `refactor` | Code change that neither fixes a bug nor adds a feature |
| `perf` | A code change that improves performance |
| `test` | Adding missing tests or correcting existing tests |
| `build` | Changes to build system or external dependencies |
| `ci` | Changes to CI configuration files and scripts |
| `chore` | Other changes that don't modify src or test files |
| `revert` | Reverts a previous commit |

### Breaking Changes
```
feat(api)!: remove deprecated /users/search endpoint

BREAKING CHANGE: The /users/search endpoint has been removed.
Use /users?q=<query> instead.
```

---

## Further Reading

Refer to official documentation:
- **Commit Conventions**:
  - Conventional Commits: https://www.conventionalcommits.org/
  - Angular Commit Guidelines: https://github.com/angular/angular/blob/main/CONTRIBUTING.md#commit
- **Best Practices**:
  - How to Write a Git Commit Message: https://cbea.ms/git-commit/
  - Pro Git Book: https://git-scm.com/book/en/v2

---

## Version History

- v1.1.0 (2026-02-10): Migrated to interface-based memory access
  - Replaced hardcoded memory paths with MemoryStore interface calls
  - Added references to MemoryStore interface documentation
- v1.0.0 (2025-01-XX): Initial release
  - Mandatory 4-step workflow for commit message generation

### Step 1: Initial Analysis

Gather inputs and determine scope and requirements.

### Step 2: Load Memory

Load project-specific memory via MemoryStore interface.

### Step 3: Load Context

Load relevant context files via ContextProvider interface.

### Step 4: Core Implementation

Execute the skill-specific core action.

### Step 5: Generate Output

Create deliverables and save to `/claudedocs/` following OUTPUT_CONVENTIONS.md.

### Step 6: Update Memory

Update project memory with new patterns and decisions.
