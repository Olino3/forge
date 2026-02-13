---
description: "Auto-diagnose CI test failures and propose fixes after consecutive failures"
imports:
  - shared/forge-base.md
  - shared/forge-pr-creator.md
  - shared/forge-conventions.md
on:
  workflow_run:
    workflows: ["Forge Tests"]
    types: [completed]
    branches:
      - main
      - develop
  workflow_dispatch:
permissions:
  contents: read
  actions: read
  issues: read
  pull-requests: read
tools:
  github:
    toolsets: [default]
safe-outputs:
  create-pull-request:
    labels: ["forge-automation", "ci-fix", "auto-diagnosis"]
    title-prefix: "[ci-fix] "
    expires: 7
    draft: true
    if-no-changes: "ignore"
---

# Forge CI Failure Diagnostician

Auto-investigate CI test failures and propose fixes after detecting consecutive failures on the same branch.

## Trigger Conditions

This workflow activates when the "Forge Tests" workflow completes. It only proceeds if:

1. The workflow run **failed** (conclusion: failure)
2. This is the **2nd consecutive failure** on the same branch
3. The failure occurred on a tracked branch (main, develop, or PR branches)

**Rationale**: Single failures may be transient or flaky. Consecutive failures indicate a persistent issue requiring investigation.

## Consecutive Failure Detection

**Step 1: Get Current Run Context**

Retrieve from the triggering workflow_run event:
- Run ID
- Conclusion (must be "failure")
- Head branch name
- Head SHA
- Workflow ID

If conclusion is not "failure", exit with: "✅ Workflow passed — no diagnosis needed"

**Step 2: Query Previous Runs**

Use GitHub API to list the previous 5 workflow runs for:
- Same workflow ID
- Same branch
- Status: completed
- Sort: created descending (most recent first)

**Step 3: Check Consecutive Failure**

Examine the run immediately before the current one:
- If previous run conclusion was "success", exit with: "ℹ️ Single failure detected — waiting for 2nd consecutive failure before diagnosis"
- If previous run conclusion was "failure", proceed to analysis
- If no previous run exists, exit with: "ℹ️ First run on branch — no baseline for comparison"

**Step 4: Log Failure Context**

Output diagnostic context:
```
🔴 Consecutive failure detected on branch: {branch}
- Current run: {run_id} (failed)
- Previous run: {prev_run_id} (failed)
- Triggering commit: {sha}
- Proceeding with root cause analysis...
```

## Log Retrieval and Analysis

**Step 1: Fetch Workflow Run Jobs**

Use GitHub API to list all jobs for the failed workflow run:
- Identify which jobs failed (conclusion: failure)
- Extract job names, step names, and step conclusions
- Note: Multiple jobs may have failed

**Step 2: Download Failure Logs**

For each failed job:
- Download job logs using GitHub API
- Focus on failed steps only
- Extract last 100 lines of each failed step (most relevant errors)
- Capture stdout and stderr

**Step 3: Parse Error Patterns**

Analyze logs to identify failure categories:

| Category | Detection Pattern | Examples |
|----------|------------------|----------|
| **Test Assertion** | "AssertionError", "FAILED", "expected X but got Y" | Pytest failures, test mismatches |
| **Build Error** | "SyntaxError", "ImportError", "ModuleNotFoundError" | Python syntax, missing imports |
| **Dependency** | "No module named", "package not found", "version conflict" | Missing pip packages |
| **Linting** | "shellcheck", "format error", "style violation" | Shellcheck warnings, format issues |
| **Environment** | "command not found", "permission denied", "timeout" | System setup, permissions |

**Step 4: Extract Key Evidence**

For each failed job, capture:
- Job name and step name
- Failure category
- Primary error message (first error or assertion)
- Stack trace (if present, last 20 lines)
- Failed file paths (if mentioned in logs)

## Root Cause Identification

**Step 1: Correlate with Recent Changes**

Query commits between last successful run and current failed run:
- List commits on the branch
- Identify changed files
- Cross-reference changed files with files mentioned in error logs

**Step 2: Determine Primary Root Cause**

Analyze patterns across all failures:
- If multiple test failures reference same file → likely issue in that file
- If all failures are same category → systemic issue (e.g., dependency)
- If failures span categories → check for common changed file

**Step 3: Generate Root Cause Summary**

Create structured summary:

```markdown
## Root Cause Analysis

**Primary Category**: {category}
**Affected Jobs**: {job1, job2, ...}
**Likely Culprit Files**: {file1, file2, ...}

### Evidence

{job_name} / {step_name}:
- Error: {primary_error_message}
- File: {affected_file}
- Line: {line_number}

### Recent Changes

These commits introduced changes to affected areas:
- {sha}: {commit_message} by {author}
  - Modified: {changed_files}
```

## Fix Proposal Generation

**Step 1: Determine Fix Strategy**

Based on root cause category:

| Category | Fix Strategy |
|----------|-------------|
| **Test Assertion** | Examine test code and implementation; propose code fix to align behavior |
| **Build Error** | Fix syntax errors, add missing imports, correct typos |
| **Dependency** | Update requirements.txt, workflow dependencies, or installation steps |
| **Linting** | Apply shellcheck suggestions, fix formatting per linter output |
| **Environment** | Update workflow file: add missing tools, adjust permissions, increase timeouts |

**Step 2: Generate Code Changes**

For each identified issue:
- Read the affected file(s)
- Identify specific lines requiring changes
- Propose minimal, surgical fixes
- Preserve surrounding code context

**Constraints**:
- Fix only files directly related to the failure
- Do not refactor unrelated code
- Preserve existing test coverage
- Follow Forge conventions (see forge-conventions import)

**Step 3: Create Validation Plan**

Propose verification steps:
```markdown
## Validation Steps

After applying this fix:

- [ ] Run `forge-tests.yml` workflow manually via workflow_dispatch
- [ ] Verify {specific_job} passes
- [ ] Check that {specific_test} now passes
- [ ] Confirm no new failures introduced
```

## PR Creation

Create a single draft pull request with:

**Title Format**: `[ci-fix] fix {primary_issue} in {affected_area}`

Examples:
- `[ci-fix] fix test_hook_syntax assertion in layer1 tests`
- `[ci-fix] fix missing jq dependency in CI workflow`
- `[ci-fix] fix ImportError in memory lifecycle tests`

**PR Body Template**:

```markdown
## 🔴 CI Failure Diagnosis

**Auto-generated by**: forge-ci-failure-diagnostician
**Detected**: Consecutive failures on `{branch}`
**Failed Workflow**: {workflow_name} (runs {run_id1}, {run_id2})
**Analysis Date**: {date}

---

## 📊 Failure Summary

| Metric | Value |
|--------|-------|
| Failed Jobs | {count} |
| Primary Category | {category} |
| Affected Files | {file_count} |
| Commits Since Last Success | {commit_count} |

---

## 🔍 Root Cause Analysis

{root_cause_summary}

---

## 🛠️ Proposed Fix

### Changes

{describe changes made to each file}

### Rationale

{explain why these changes fix the issue}

---

## 📋 Evidence

<details>
<summary>Failed Job: {job_name}</summary>

**Step**: {step_name}
**Conclusion**: failure

**Error Output** (last 50 lines):
```
{log_excerpt}
```

</details>

{repeat for each failed job}

---

## ✅ Validation Steps

- [ ] Run forge-tests.yml workflow via workflow_dispatch
- [ ] Verify {specific_test/job} passes
- [ ] Check no new failures introduced
- [ ] Review changes for correctness

---

## 🔗 Related

- Failing run: {workflow_run_url}
- Previous failing run: {previous_run_url}
- Commits: {commit_range_url}

---

⚠️ **This is an auto-generated diagnostic PR** — review carefully before merging.
The AI analysis may not be perfect. Validate all changes.
```

## Output Constraints

- **Expiration**: PRs auto-close after 7 days if not merged (`expires: 7`)
- **Draft**: All PRs created as drafts (`draft: true`)
- **No changes**: If no fix can be proposed, do not create PR (`if-no-changes: ignore`)
- **Note**: Only one PR will be created per workflow run due to the nature of the trigger

## Edge Cases

**Case 1: Multiple Unrelated Failures**

If failures span multiple categories with no common root cause:
- Create PR addressing the most critical/blocking failure only
- Note other failures in PR body under "Additional Failures" section
- Suggest manual investigation for complex multi-failure scenarios

**Case 2: Environment/Workflow File Issues**

If root cause is in workflow files (e.g., missing dependencies in forge-tests.yml):
- Note: gh-aw workflows cannot modify workflow files
- Create issue instead of PR with title: `[ci-fix] {issue} requires workflow file update`
- Provide exact changes needed in issue body
- Tag with "manual-intervention" label

**Case 3: Cannot Determine Root Cause**

If log analysis is inconclusive:
- Create issue (not PR) summarizing failure context
- Include full log excerpts
- Tag with "needs-investigation" label
- Suggest manual debugging steps

**Case 4: Flaky Test Suspected**

If failure pattern suggests flakiness (e.g., timeout, race condition):
- Include "possible-flaky-test" label
- Propose test stabilization (retries, timeouts, mocking)
- Reference flaky test patterns in error logs

## Success Metrics

Track effectiveness over time:
- **Fix accuracy**: % of auto-generated PRs that are merged
- **Time to resolution**: Time from 2nd failure to fix merge
- **False positive rate**: PRs closed without merge due to incorrect diagnosis

Target: >60% merge rate for diagnostic PRs within 2 weeks of rollout.
