# Commit Message: [TYPE]([SCOPE]): [SUBJECT]

**Generated**: [YYYY-MM-DD HH:MM:SS]
**Skill**: commit-helper v1.0.0

---

## Change Analysis

### Files Changed

| File | Status | Insertions | Deletions |
|------|--------|------------|-----------|
| `[FILE_PATH]` | [A/M/D/R] | +[N] | -[N] |

### Change Statistics

| Metric | Count |
|--------|-------|
| Files Changed | [N] |
| Insertions | [N] (+) |
| Deletions | [N] (-) |
| Net Change | [±N] |

---

## Classification

- **Type**: `[TYPE]` — [JUSTIFICATION]
- **Scope**: `[SCOPE]` — [SCOPE_REASONING]
- **Breaking Change**: [Yes/No] — [EXPLANATION_IF_YES]

---

## Generated Commit Message

```
[TYPE]([SCOPE]): [SUBJECT_LINE]

[BODY_PARAGRAPH_1]

[BODY_PARAGRAPH_2]

[FOOTER_BREAKING_CHANGE]
[FOOTER_ISSUE_REFS]
```

### Subject Line
```
[TYPE]([SCOPE]): [SUBJECT_LINE]
```

### Body
```
[BODY_TEXT — wrapped at 72 characters per line]
```

### Footer
```
[BREAKING CHANGE: description — if applicable]
[Fixes #NNN — if applicable]
[Refs #NNN — if applicable]
[Co-authored-by: Name <email> — if applicable]
```

---

## Alternatives Considered

### Alternative 1
```
[ALT_TYPE]([ALT_SCOPE]): [ALT_SUBJECT]
```
**Rationale**: [WHY_THIS_COULD_ALSO_WORK]

### Alternative 2
```
[ALT_TYPE_2]([ALT_SCOPE_2]): [ALT_SUBJECT_2]
```
**Rationale**: [WHY_THIS_COULD_ALSO_WORK]

---

## Quality Checklist

- [ ] Subject uses imperative mood
- [ ] Subject is ≤72 characters ([ACTUAL_LENGTH] chars)
- [ ] Type correctly classifies the change
- [ ] Scope accurately identifies affected area
- [ ] Body explains motivation and context (if present)
- [ ] Body lines wrapped at 72 characters
- [ ] Breaking changes documented in footer (if applicable)
- [ ] Issue references included (if applicable)
- [ ] Message does not repeat the diff content

---

## Quick Apply

```bash
# Apply this commit message directly:
git commit -m "[TYPE]([SCOPE]): [SUBJECT_LINE]" -m "[BODY_TEXT]" -m "[FOOTER]"

# Or use the full message from a file:
git commit -F /claudedocs/[OUTPUT_FILENAME]
```

---

## Metadata

- **Analyzed by**: Claude Code commit-helper skill v1.0.0
- **Analysis date**: [YYYY-MM-DD HH:MM:SS]
- **Repository**: [REPO_PATH]
- **Base commit**: [SHORT_HASH] ([FULL_HASH])

---

<!--
Template Usage Instructions:

Replace all placeholders in [BRACKETS] with actual values:
- [TYPE] - Conventional Commits type (feat, fix, refactor, docs, etc.)
- [SCOPE] - Module or component affected (auth, api, parser, etc.)
- [SUBJECT_LINE] - Imperative description of the change (≤72 chars)
- [BODY_TEXT] - Detailed explanation of what and why (wrapped at 72 chars)
- [FOOTER] - Breaking changes, issue references, co-authors
- [FILE_PATH] - Path to changed file
- [A/M/D/R] - File operation (Added/Modified/Deleted/Renamed)
- [N] - Numeric values
- [SHORT_HASH] - 7-character commit hash of HEAD
- [FULL_HASH] - Full 40-character commit hash
- [JUSTIFICATION] - Why this type was chosen
- [SCOPE_REASONING] - Why this scope was chosen
- [OUTPUT_FILENAME] - Generated output filename

Conditional Sections:
- Include "Breaking Change" details only if breaking changes detected
- Include "Footer" section only if there are breaking changes or issue refs
- Include "Alternatives Considered" only if classification is ambiguous
- Omit "Body" section for trivial changes that need no explanation

Formatting:
- Use proper markdown syntax throughout
- Wrap commit message text in code blocks for easy copying
- Use tables for structured data
- Use checkboxes for the quality checklist

Output Location:
- Save to: /claudedocs/commit_msg_{short_hash}.md
- Ensure /claudedocs directory exists
- Use commit_msg_staged.md when no commit hash is available
-->
