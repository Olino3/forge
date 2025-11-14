# Context Directory Index

This directory contains **shared contextual knowledge** that provides consistent guidance across all skills. Context files are organized by domain and serve as reference materials for standards, patterns, and best practices.

## Purpose

Context files provide:
- **Standards and References**: Language specifications, format definitions
- **Best Practices**: Recommended patterns and approaches
- **Common Patterns**: Recurring code structures and idioms
- **Guidelines**: Security, quality, and compliance rules

## Directory Structure

```
context/
├── index.md (this file)
├── git/
│   ├── diff_patterns.md
│   └── git_diff_reference.md
├── python/
│   ├── common_issues.md
│   ├── context_detection.md
│   ├── datascience_patterns.md
│   ├── django_patterns.md
│   ├── fastapi_patterns.md
│   ├── flask_patterns.md
│   └── ml_patterns.md
└── security/
    ├── owasp_python.md
    └── security_guidelines.md
```

## Quick Reference Guide

### Git Context (`git/`)

**When to use**: Analyzing diffs, commits, version control changes

| File | Use For | Key Topics |
|------|---------|------------|
| `git_diff_reference.md` | Understanding diff format | Unified diff syntax, hunks, metadata, special cases |
| `diff_patterns.md` | Identifying change types | Feature additions, bug fixes, refactoring, security fixes, breaking changes |

**Load when**: Working with `skill:get-git-diff` or analyzing version control changes

---

### Python Context (`python/`)

**When to use**: Reviewing Python code, understanding frameworks

| File | Use For | Key Topics |
|------|---------|------------|
| `common_issues.md` | Identifying typical problems | Mutable defaults, exception handling, import issues, performance |
| `context_detection.md` | Identifying project type | Detecting Django/Flask/FastAPI/ML frameworks from code patterns |
| `datascience_patterns.md` | Data science code review | Pandas, NumPy, data validation, memory management |
| `django_patterns.md` | Django best practices | Models, views, querysets, middleware, signals |
| `fastapi_patterns.md` | FastAPI best practices | Pydantic models, dependency injection, async patterns, routing |
| `flask_patterns.md` | Flask best practices | Blueprints, application factory, extensions, context |
| `ml_patterns.md` | Machine learning code | Model training, data pipelines, evaluation, deployment |

**Load when**: Using `skill:python-code-review` or analyzing Python projects

**Context detection workflow**:
1. Start with `context_detection.md` to identify framework
2. Load framework-specific patterns file
3. Load `common_issues.md` for universal Python problems

---

### Security Context (`security/`)

**When to use**: Security-focused reviews, vulnerability assessment

| File | Use For | Key Topics |
|------|---------|------------|
| `owasp_python.md` | OWASP Top 10 vulnerabilities | Injection, auth, XSS, insecure design, security misconfiguration |
| `security_guidelines.md` | Secure coding practices | Input validation, SQL injection, XSS, CSRF, crypto, secrets |

**Load when**: Security review requested or high-risk code detected (auth, data handling, user input)

**Always load for**: Authentication code, database queries, user input handling, file operations

---

## Usage Patterns

### For Skills

Skills should load context files in this order:

1. **Check memory first** - Load project-specific knowledge from `../../memory/skills/{skill-name}/{project-name}/`
2. **Load relevant context** - Use this index to identify which context files are needed
3. **Perform analysis** - Apply context knowledge to the specific task
4. **Update memory** - Store project-specific insights learned during analysis

### Loading Context Efficiently

**Instead of reading all files**, use this index to target specific files:

```markdown
# Example: Python code review for FastAPI project

1. Load context_detection.md (detect it's FastAPI)
2. Load fastapi_patterns.md (framework-specific)
3. Load common_issues.md (universal Python)
4. Load security_guidelines.md (if auth/input handling present)
```

**For git diff analysis**:
```markdown
1. Load git_diff_reference.md (understand format)
2. Load diff_patterns.md (classify changes)
```

### When to Add New Context

Add new context files when:
- ✅ Knowledge applies to **multiple projects** (not project-specific)
- ✅ Information is **reference material** (standards, patterns, guidelines)
- ✅ Content is **relatively stable** (doesn't change frequently per project)

**Don't add to context** if:
- ❌ Information is **project-specific** (belongs in memory/)
- ❌ Content is **dynamic** (changes with each analysis)
- ❌ Knowledge is **temporary** (belongs in skill output)

---

## Context vs Memory

| Aspect | Context | Memory |
|--------|---------|--------|
| **Location** | `forge-plugin/context/` | `forge-plugin/memory/skills/{skill-name}/{project-name}/` |
| **Scope** | Universal, all projects | Project-specific |
| **Nature** | Static reference | Dynamic learning |
| **Updates** | Rare (when standards change) | Frequent (each skill invocation) |
| **Examples** | PEP8 rules, OWASP Top 10 | This project's naming conventions |
| **Read by** | All skills, all projects | Specific skill for specific project |

---

## Maintenance Guidelines

### For Developers

- **Update context** when standards or best practices evolve
- **Version context files** if major changes occur
- **Keep context focused** - one domain per directory
- **Document changes** in version history

### For Skills

- **Load context explicitly** - reference files by path
- **Don't modify context** - it's read-only reference
- **Combine with memory** - context + project memory = complete understanding
- **Cache if needed** - context rarely changes within a session

---

## Related Documentation

- **Skills**: See `forge-plugin/skills/` for skill implementations
- **Memory**: See `forge-plugin/memory/` for project-specific learning
- **Plugin**: See `forge-plugin/.claude-plugin/plugin.json` for plugin metadata
- **Architecture**: See `/home/olino3/git/forge/CLAUDE.md` for system overview