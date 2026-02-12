---
id: "security/index"
domain: security
title: "Security Context Files"
type: index
estimatedTokens: 1200
loadingStrategy: always
version: "0.2.0-alpha"
lastUpdated: "2026-02-10"
indexedFiles:
  - id: "security/security_guidelines"
    path: "security_guidelines.md"
    type: reference
    loadingStrategy: onDemand
  - id: "security/owasp_python"
    path: "owasp_python.md"
    type: reference
    loadingStrategy: onDemand
sections:
  - name: "Files in this Directory"
    estimatedTokens: 51
    keywords: [files, this, directory]
  - name: "Files in this Folder"
    estimatedTokens: 96
    keywords: [files, this, folder]
  - name: "Typical Usage Pattern"
    estimatedTokens: 35
    keywords: [typical, usage, pattern]
  - name: "Maintenance Notes"
    estimatedTokens: 106
    keywords: [maintenance]
  - name: "Quick Reference by Code Type"
    estimatedTokens: 81
    keywords: [quick, reference, code, type]
  - name: "Security Review Checklist"
    estimatedTokens: 133
    keywords: [security, review, checklist]
  - name: "Common Vulnerability Patterns"
    estimatedTokens: 100
    keywords: [vulnerability, patterns]
  - name: "Integration with Python Context"
    estimatedTokens: 54
    keywords: [integration, python, context]
  - name: "Framework-Specific Security Notes"
    estimatedTokens: 63
    keywords: [framework-specific, security]
  - name: "Related Skills"
    estimatedTokens: 12
    keywords: [related, skills]
  - name: "When to Escalate"
    estimatedTokens: 55
    keywords: [escalate]
  - name: "Maintenance Notes"
    estimatedTokens: 31
    keywords: [maintenance]
tags: [security, index, navigation, owasp, python, vulnerabilities]
---

# Security Context Files

Context files for security-focused code review, vulnerability detection, and secure coding practices.

## Files in this Directory

### `security_guidelines.md`

**Purpose**: Practical secure coding guidelines with code examples

**Use when**:
- Reviewing any code that handles user input
- Checking authentication or authorization code
- Analyzing database queries
- Reviewing file operations
- Checking cryptographic operations
# Security Context Files (Compact)

Compact Python security references that point to OWASP and other authoritative guides.

Use them together with framework-specific context files (Django, Flask, FastAPI) for best results.

---

## Files in this Folder

### `security_guidelines.md`

Python security guidelines quick reference.

- Links to OWASP Cheat Sheet Series, OWASP Python Security, OWASP Top 10, CWE Top 25
- Table of review areas (validation, SQL/NoSQL, XSS, auth, crypto, file upload, command injection, deserialization, SSRF, logging)
- Short checklist for Python security code review

**Use when** you want a **checklist + links** for secure Python coding practices without in-file tutorials.

### `owasp_python.md`

OWASP Top 10 for Python quick reference.

- Links to OWASP Top 10, OWASP Python Security, OWASP Cheat Sheet Series
- Table mapping OWASP categories (A01–A10) to typical Python signals and where to look in the code
- Compact OWASP-aligned checklist for findings coverage

**Use when** you need to **map findings to OWASP categories** or ensure coverage of common risk classes.

---

## Typical Usage Pattern

1. Start with language/framework context (Django/Flask/FastAPI pattern files).
2. Load `security_guidelines.md` for a **what-to-check** view and deep-dive links.
3. Load `owasp_python.md` to **tag findings with OWASP categories** and confirm coverage.

This keeps framework-specific details in their own files while aligning all findings with standard security guidance.

---

## Maintenance Notes

- Keep OWASP and CWE links current; avoid duplicating content from those sites.
- When OWASP versions change, update category names/descriptions, not detailed examples.
- Prefer adding or updating links/checklist items over embedding long code samples.

```markdown
1. Always load security_guidelines.md first
   → Covers common security patterns
   → Practical examples for immediate issues
   
2. If comprehensive audit needed:
   → Load owasp_python.md
   → Check all OWASP Top 10 categories
   → Document findings by category
```

### Risk-Based Loading

**High Risk Code** (always load both files):
- Authentication/authorization systems
- Payment processing
- Personal data handling
- Admin interfaces
- API gateways

**Medium Risk Code** (load `security_guidelines.md`):
- Standard CRUD operations with user input
- File uploads
- Report generation
- Email handling

**Low Risk Code** (spot check with `security_guidelines.md`):
- Internal utilities
- Data transformations without user input
- Static content generation

---

## Quick Reference by Code Type

| Code Type | Load File | Focus Areas |
|-----------|-----------|-------------|
| **Login/Auth** | Both | Authentication, session, password handling |
| **Database Access** | `security_guidelines.md` | SQL injection, parameterization, ORM |
| **User Input** | `security_guidelines.md` | Validation, sanitization, XSS |
| **File Operations** | `security_guidelines.md` | Path traversal, upload validation |
| **API Endpoints** | Both | Input validation, rate limiting, auth |
| **Crypto Operations** | Both | Algorithm choice, key management |
| **Configuration** | `security_guidelines.md` | Secrets management, environment vars |
| **Dependencies** | `owasp_python.md` | Vulnerable components, version pinning |
| **Error Handling** | `security_guidelines.md` | Information disclosure, safe errors |

---

## Security Review Checklist

Use this to determine which sections to focus on:

### Input Handling
- [ ] All user input validated? → `security_guidelines.md` "Input Validation"
- [ ] Type checking enforced? → `security_guidelines.md` "Type Validation"
- [ ] Length limits applied? → `security_guidelines.md` "String Length Limits"

### Injection Prevention
- [ ] SQL queries parameterized? → `security_guidelines.md` "SQL Injection Prevention"
- [ ] Template rendering safe? → `security_guidelines.md` "Cross-Site Scripting"
- [ ] No command injection? → `owasp_python.md` "Injection"

### Authentication & Authorization
- [ ] Password handling secure? → `security_guidelines.md` "Authentication"
- [ ] Session management proper? → `owasp_python.md` "Authentication Failures"
- [ ] Access controls in place? → `owasp_python.md` "Broken Access Control"

### Cryptography
- [ ] Strong algorithms used? → `security_guidelines.md` "Cryptography"
- [ ] Keys managed securely? → `owasp_python.md` "Cryptographic Failures"
- [ ] Secure random for security? → `security_guidelines.md` "Secure Random"

### Configuration & Secrets
- [ ] Secrets not hardcoded? → `security_guidelines.md` "Environment & Secrets"
- [ ] Debug mode disabled? → `owasp_python.md` "Security Misconfiguration"
- [ ] Environment-based config? → `security_guidelines.md` "Configuration"

---

## Common Vulnerability Patterns

Quick lookup for specific vulnerability types:

| Vulnerability | File | Section | Common in |
|---------------|------|---------|-----------|
| SQL Injection | `security_guidelines.md` | "SQL Injection Prevention" | Database queries |
| XSS | `security_guidelines.md` | "Cross-Site Scripting" | Template rendering |
| Path Traversal | `security_guidelines.md` | "Input Validation" | File operations |
| CSRF | `security_guidelines.md` | "API Security" | Form submissions |
| Hardcoded Secrets | `security_guidelines.md` | "Environment & Secrets" | Configuration |
| Weak Crypto | `security_guidelines.md` | "Cryptography" | Password hashing |
| Command Injection | `owasp_python.md` | "Injection" | subprocess calls |
| Insecure Deserialization | `owasp_python.md` | "Data Integrity" | pickle, yaml |
| SSRF | `owasp_python.md` | "SSRF" | HTTP requests |
| Broken Access Control | `owasp_python.md` | "Broken Access Control" | Authorization |

---

## Integration with Python Context

Security reviews should combine security context with framework context:

```markdown
# Example: Django API security review

1. Load ../python/context_detection.md
   → Identify as Django project
   
2. Load ../python/django_patterns.md
   → Understand Django-specific patterns
   
3. Load security_guidelines.md
   → Apply general security practices
   
4. Load owasp_python.md (if comprehensive)
   → Check OWASP categories
   
5. Check Django-specific security:
   - CSRF tokens in forms
   - XSS protection in templates
   - SQL injection in QuerySets
   - Authorization in views
```

---

## Framework-Specific Security Notes

### Django
- Built-in CSRF protection (check it's enabled)
- Template auto-escaping (verify not disabled)
- ORM prevents SQL injection (watch for `.raw()` and `.extra()`)
- Check: `django_patterns.md` + `security_guidelines.md`

### Flask
- No built-in CSRF (check Flask-WTF or manual)
- Template escaping (Jinja2 auto-escapes)
- Manual auth required (check implementation)
- Check: `flask_patterns.md` + `security_guidelines.md`

### FastAPI
- Pydantic validation (verify models used)
- Dependency injection for auth (check implementation)
- No built-in CSRF for non-browser APIs
- Check: `fastapi_patterns.md` + `security_guidelines.md`

---

## Related Skills

- **python-code-review**: Primary consumer for Python security analysis
- **get-git-diff**: May flag security-related changes for review

---

## When to Escalate

Some findings require immediate attention:

**CRITICAL** (stop and report immediately):
- SQL injection vulnerabilities
- Hardcoded credentials or API keys
- Command injection
- Authentication bypass
- Insecure deserialization of untrusted data

**HIGH** (flag prominently):
- XSS vulnerabilities
- Path traversal
- Weak cryptography
- Missing access controls
- Information disclosure

**MEDIUM** (include in review):
- Missing input validation
- Improper error handling
- Outdated dependencies with known CVEs
- Rate limiting missing

---

## Maintenance Notes

- `security_guidelines.md`: Update with new Python security best practices
- `owasp_python.md`: Update when OWASP Top 10 changes (typically every 3-4 years)
- Both files: Add new vulnerability patterns as they emerge
- Keep examples current with modern Python (3.10+) and framework versions
