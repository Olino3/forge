---
id: "git/diff_patterns"
domain: git
title: "Common Diff Patterns - Quick Reference"
type: reference
estimatedTokens: 200
loadingStrategy: onDemand
version: "0.3.0-alpha"
lastUpdated: "2026-02-10"
sections:
  - name: "Change Type Patterns"
    estimatedTokens: 60
    keywords: [feature, bugfix, refactor, config, docs]
  - name: "Risk Indicators"
    estimatedTokens: 60
    keywords: [security, breaking-change, database, performance]
  - name: "Review Checklist"
    estimatedTokens: 40
    keywords: [checklist, review, scope]
tags: [git, diff, patterns, risk-assessment]
crossDomainTriggers: []
---

# Common Diff Patterns – Quick Reference

Compact cues for classifying diffs and spotting risk. Use links for deeper guidance.

**Load this file** when summarizing or classifying git diffs.

---

## 1. Change Type Patterns

| Pattern | Detection Cues | Key Questions | References |
|---------|----------------|---------------|------------|
| Feature addition | New files (`A`), many insertions, new tests/assets | Are tests/docs updated? New deps vetted? | Git basics: https://git-scm.com/book/en/v2/Git-Basics-Recording-Changes-to-the-Repository |
| Bug fix | Few files, small logical changes, message mentions "fix" | Root cause understood? Similar bug elsewhere? | Code review: https://google.github.io/eng-practices/review/ |
| Refactor | Many renames (`R`), moves, import changes | Purely structural? Behavior unchanged? Tests stable? | Refactoring: https://martinfowler.com/books/refactoring.html |
| Dependency update | `package.json`, lockfiles, `requirements.txt` | Major/minor? Breaking changes? Security motivation? | SemVer: https://semver.org/ |
| Security fix | Auth/validation changes, CVE IDs, security keywords | All attack paths covered? Regression tests added? | OWASP: https://owasp.org/ |
| DB migration | `migrations/`, schema/model changes | Backwards compatible? Rollback? Data migration plan? | DB migrations: https://www.liquibase.org/get-started/best-practices |
| Config change | `.env`, config files, feature flags | Safe defaults? Sensitive values? Environment‑specific? | 12‑factor config: https://12factor.net/config |

---

## 2. Structural & Risk Patterns

| Pattern | Detection | Why It Matters |
|---------|-----------|----------------|
| Large single‑file diff | Hundreds of lines changed in one file | Risk of hidden behavior changes or formatting noise |
| Many tiny changes | 50+ files, small edits | Global rename, dependency API change – check consistency |
| Binary changes | `Binary files differ` | Check if large assets belong in repo (Git LFS, etc.) |
| Merge resolution | Merge commits with unexpected edits | Verify no accidental code from manual conflict resolution |

---

## 3. Red Flags

| Anti‑Pattern | What to Look For | Action |
|------------|------------------|--------|
| Commented‑out code | Lines added with code in comments | Ask to delete instead of keep dead code |
| Debug logging | `console.log`, `print("DEBUG")`, breakpoints | Remove or guard behind feature flags |
| Hardcoded secrets | Keys/tokens/passwords in code or config | Treat as incident; rotate & remove immediately |
| TODOs in new code | `TODO`, `FIXME` in added lines | Confirm tracking issue and justify debt |
| Mass deletions | Large negative line count | Ensure deletion is intentional and documented |

---

## 4. Quick Diff Review Checklist

- [ ] Scope: files/lines changed make sense for the described intent.
- [ ] Tests: updated/added where behavior changes.
- [ ] Docs: updated for user‑visible or API changes.
- [ ] Risk: security, DB, and breaking API changes are clearly justified.
- [ ] Hygiene: no secrets, debug code, or commented‑out blocks remain.

---

## 5. Helpful References

- Git docs: https://git-scm.com/doc
- Code review best practices: https://google.github.io/eng-practices/review/
- Semantic Versioning: https://semver.org/
- OWASP secure coding quick ref: https://owasp.org/www-project-secure-coding-practices-quick-reference-guide/

---

**Version**: 0.3.0-alpha (Compact Reference Format)
**Last Updated**: 2025-11-14
**Maintained For**: get-git-diff skill
