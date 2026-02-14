---
description: "Consolidated workflow to keep Forge documentation accurate and concise"
imports:
  - shared/forge-base.md
  - shared/forge-pr-creator.md
  - shared/forge-conventions.md
on:
  schedule: "0 7 * * 1,4"  # Monday + Thursday at 7am UTC
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
    labels: ["forge-automation", "documentation", "maintenance"]
    title-prefix: "[docs] "
    expires: 7
    draft: true
    if-no-changes: "ignore"
---

# Forge Doc Maintainer

**Consolidated Workflow** — Replaces:
- `forge-doc-sync.md` (accuracy and reference integrity)
- `forge-doc-unbloat.md` (verbosity reduction)

This workflow maintains high-signal Forge documentation by ensuring accuracy (counts, paths, references match reality) and reducing bloat (unnecessary verbosity, duplication). Runs twice weekly and creates a single unified draft PR with both sync fixes and unbloat improvements.

## Two-Stage Pipeline

This workflow executes in two sequential stages:

### Stage 1: Sync Check (Accuracy)

**Objective**: Validate that documented facts match repository reality.

**Target Documents**:
- `README.md`
- `ROADMAP.md`
- `CONTRIBUTING.md`
- `COOKBOOK.md`
- `TROUBLESHOOTING.md`
- `forge-plugin/context/index.md`
- `forge-plugin/hooks/HOOKS_GUIDE.md`
- Domain index files: `forge-plugin/context/*/index.md`

**Validation Checks**:

#### 1. Count Accuracy

Verify documented counts match actual repository state:

| Item | Source | Documentation Claims |
|------|--------|---------------------|
| Skills | `forge-plugin/skills/*/SKILL.md` | README.md, ROADMAP.md, CONTRIBUTING.md |
| Agents | `forge-plugin/agents/*.md` | README.md, ROADMAP.md, CONTRIBUTING.md |
| Commands | `forge-plugin/commands/*.md` | README.md, ROADMAP.md, COOKBOOK.md |
| Hooks | `forge-plugin/hooks/*.sh` (excluding lib/) | README.md, CONTRIBUTING.md, hooks/HOOKS_GUIDE.md |
| Context files | `forge-plugin/context/**/*.md` | README.md, context/index.md |
| External skills | Count from marketplace.json plugins | README.md, CONTRIBUTING.md |
| Plugins | `.claude-plugin/marketplace.json` entries | README.md, CONTRIBUTING.md |

**Method**:
- Count actual files matching patterns
- Parse documentation for count claims (look for numbers in proximity to item names)
- Report mismatches with actual vs. claimed counts

#### 2. Path and Structure Accuracy

Verify documented paths still exist:

- File path examples in CONTRIBUTING.md, COOKBOOK.md
- Directory structure examples in README.md
- Script paths in CONTRIBUTING.md, TROUBLESHOOTING.md
- Config file paths in all docs

**Method**:
- Extract all mentioned file paths using regex patterns (e.g., `path/to/file.ext`)
- Check if each path exists in the repository
- Report broken paths

#### 3. Reference Integrity

Verify referenced items actually exist:

| Referenced Item Type | Documentation Sources | Validation |
|---------------------|----------------------|------------|
| Commands | COOKBOOK.md, CONTRIBUTING.md | Check `forge-plugin/commands/{name}.md` exists |
| Skills | COOKBOOK.md, CONTRIBUTING.md | Check `forge-plugin/skills/{name}/SKILL.md` exists |
| Agents | COOKBOOK.md, CONTRIBUTING.md | Check `forge-plugin/agents/{name}.md` exists |
| Scripts | CONTRIBUTING.md, TROUBLESHOOTING.md | Check `scripts/{name}.sh` exists |
| Workflows | CONTRIBUTING.md, AGENTIC_FORGE.md | Check `.github/workflows/{name}.md` or `.yml` exists |
| Schemas | CONTRIBUTING.md | Check `forge-plugin/interfaces/schemas/{name}.schema.json` exists |

**Method**:
- Extract references using pattern matching
- Verify each reference points to an existing file
- Report dead references

#### 4. Capability Claim Accuracy

Identify stale or inaccurate capability claims:

- Features listed in README.md that are no longer implemented
- Workflow capabilities in AGENTIC_FORGE.md that are decommissioned
- Context domain claims that don't match `forge-plugin/context/` structure
- Hook event claims that aren't in `hooks/hooks.json`

**Method**:
- Manually review each capability claim against current codebase
- Look for obvious mismatches (e.g., "24 workflows" when only 9 exist)
- Flag claims that need human verification

#### 5. Index Consistency

Verify context index files match directory contents:

- `forge-plugin/context/index.md` should list all domain directories
- Each `forge-plugin/context/{domain}/index.md` should list all `.md` files in that domain
- No orphaned files (present in directory but not in index)
- No ghost entries (present in index but file doesn't exist)

**Method**:
- For each domain, list all `.md` files (excluding `index.md`)
- Parse domain `index.md` for file listings
- Report mismatches

**Output**: Structured list of sync issues:

```json
{
  "sync_issues": [
    {
      "category": "count",
      "file": "README.md",
      "claimed": "102 skills",
      "actual": "98 skills",
      "fix": "Update README.md line 45: '102 skills' → '98 skills'"
    },
    {
      "category": "path",
      "file": "CONTRIBUTING.md",
      "path": "scripts/old-script.sh",
      "exists": false,
      "fix": "Remove reference or update to correct path"
    },
    {
      "category": "reference",
      "file": "COOKBOOK.md",
      "reference": "analyze-performance (command)",
      "exists": false,
      "fix": "Remove reference or create missing command"
    },
    {
      "category": "index",
      "file": "forge-plugin/context/python/index.md",
      "orphan_files": ["new-feature.md"],
      "ghost_entries": ["old-feature.md"],
      "fix": "Add new-feature.md to index, remove old-feature.md"
    }
  ]
}
```

---

### Stage 2: Unbloat Review (Conciseness)

**Objective**: Improve scannability by removing unnecessary verbosity and duplication.

**Target Documents**: (Same as Stage 1)

**Unbloat Rules**:

#### 1. Remove Duplicate Paragraphs

Identify and consolidate:
- Exact duplicate paragraphs within the same file
- Semantically duplicate content (same information, different wording)
- Repeated guidance that appears in multiple sections

**Method**:
- Use difflib or similar to find high-similarity text blocks (>80% match)
- Keep the first/most complete occurrence
- Replace duplicates with short references: "See {section} above for {topic}."

#### 2. Convert Prose to Bullets

Replace overly long prose paragraphs with concise bullet points:
- Paragraphs listing multiple items should be bulleted lists
- Step-by-step instructions should be numbered lists
- Key points buried in prose should be extracted as bullets

**Criteria**:
- Paragraph >150 words with 3+ distinct points → bullet list
- Sequential instructions in prose → numbered list
- Definition lists in prose → table or definition list format

#### 3. Deduplicate Cross-File Guidance

Identify canonical locations for guidance and convert duplicates to references:

**Example**:
- If pull request checklist appears in both CONTRIBUTING.md and README.md
- Keep full version in CONTRIBUTING.md
- Replace README.md version with: "See [Pull Request Checklist](CONTRIBUTING.md#pull-request-checklist)"

#### 4. Simplify Over-Long Sentences

Break complex sentences into simpler, shorter ones:
- Sentences >40 words → split into 2-3 shorter sentences
- Remove filler words: "basically", "essentially", "quite a bit", "in order to"
- Use active voice instead of passive

#### 5. Preserve Critical Content

**DO NOT remove or simplify**:
- Technical constraints
- Safety rules
- Required workflow steps
- Acceptance criteria checklists
- Schema definitions
- Version compatibility notes
- Security policies

**Output**: Structured list of unbloat improvements:

```json
{
  "unbloat_improvements": [
    {
      "file": "README.md",
      "type": "duplicate",
      "location": "lines 120-135",
      "issue": "Duplicate installation instructions (also at lines 45-60)",
      "fix": "Remove duplicate, add reference: 'See Installation section above'"
    },
    {
      "file": "CONTRIBUTING.md",
      "type": "prose-to-bullets",
      "location": "lines 200-220",
      "issue": "Paragraph listing 5 contribution steps in prose (180 words)",
      "fix": "Convert to numbered list (60 words, same meaning)"
    },
    {
      "file": "COOKBOOK.md",
      "type": "simplify",
      "location": "lines 89-92",
      "issue": "Over-long sentence (65 words)",
      "fix": "Split into 3 sentences (same 65 words, clearer)"
    }
  ]
}
```

---

### PR Generation

**Objective**: Create a single draft PR with both sync fixes and unbloat improvements.

**PR Body Template**:

```markdown
# Documentation Maintenance

This PR synchronizes documentation with repository reality and reduces verbosity.

## Sync Fixes (Accuracy)

**Counts Updated**: {count}
- Skills: {old} → {new}
- Agents: {old} → {new}
- Workflows: {old} → {new}

**Broken Paths Fixed**: {count}
- {file}: Removed reference to deleted `{path}`

**Dead References Fixed**: {count}
- {file}: Removed reference to non-existent {type} `{name}`

**Index Consistency**: {count}
- {domain}/index.md: Added {n} orphaned files, removed {m} ghost entries

## Unbloat Improvements (Conciseness)

**Duplicates Removed**: {count}
- {file}: Removed duplicate paragraph at lines {range} (referenced canonical version)

**Prose Converted to Bullets**: {count}
- {file}: Converted {n}-word paragraph to {m}-item bulleted list

**Simplified Sentences**: {count}
- {file}: Split over-long sentence into {n} shorter sentences

**Word Count Reduction**: {old-total} words → {new-total} words ({percent}% reduction)

## Review Guidance

This is an automated documentation maintenance PR. Please verify:

1. ✅ All count updates are accurate
2. ✅ Broken path removals are correct (paths truly don't exist)
3. ✅ Dead reference removals are correct (items truly don't exist)
4. ✅ Unbloat changes preserve technical meaning
5. ✅ No critical content was removed

If approved, merge to update documentation.
If changes are needed, edit this PR or close and re-run with `workflow_dispatch`.
```

**Constraints**:
- Keep edits minimal, factual, and behavior-safe
- Do not rewrite style or tone unless needed for correctness
- Prefer focused updates over broad reformatting
- If nothing is out of sync AND no bloat is found, make no changes

**Exit Criteria**: If no sync issues and no unbloat opportunities are identified, output "Documentation is accurate and concise. No changes needed." and exit without creating a PR.

---

## Loop Prevention

Skip processing if the last doc maintenance PR was merged less than 3 days ago (avoid thrashing).

---

## Success Criteria

✅ Stage 1 accurately identifies all sync issues (counts, paths, references, indexes)  
✅ Stage 2 identifies meaningful unbloat opportunities without removing critical content  
✅ PR clearly separates sync fixes from unbloat improvements  
✅ All changes are minimal and reviewable  
✅ Word count reduction is measured and reported  
✅ No factual errors introduced (accuracy is preserved)  
