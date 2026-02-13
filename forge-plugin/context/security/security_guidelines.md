---
id: "security/security_guidelines"
domain: security
title: "Python Security Guidelines - Quick Reference"
type: reference
estimatedTokens: 250
loadingStrategy: onDemand
version: "0.3.0-alpha"
lastUpdated: "2025-11-14"
sections:
  - name: "Authoritative References"
    estimatedTokens: 30
    keywords: [owasp, cwe, security-project]
  - name: "What to Check"
    estimatedTokens: 100
    keywords: [input-validation, sql-injection, xss, auth, crypto, ssrf]
  - name: "Tooling & Automation"
    estimatedTokens: 40
    keywords: [pip-audit, semgrep, bandit]
  - name: "Quick Security Review Checklist"
    estimatedTokens: 60
    keywords: [checklist, validation, parameterized, secrets]
tags: [security, owasp, python, review-checklist]
crossDomainTriggers: []
---

# Python Security Guidelines – Quick Reference

Compact guide to where to look for Python security best practices during code review.

**Load this file** for any security‑sensitive Python review (web apps, APIs, CLIs handling untrusted input).

---

## 1. Authoritative References

- OWASP Cheat Sheet Series (all topics):  
  https://cheatsheetseries.owasp.org/
- OWASP Python Security Project:  
  https://owasp.org/www-project-python-security/
- OWASP Top 10 (current):  
  https://owasp.org/Top10/
- CWE Top 25:  
  https://cwe.mitre.org/top25/

---

## 2. What to Check (by Area)

Use these as pointers; follow the links for detailed patterns and examples.

| Area | What to Look For | Where to Read |
|------|------------------|---------------|
| Input validation | Untrusted input, missing type/length/format checks | OWASP Input Validation Cheat Sheet |
| SQL / NoSQL / LDAP | String interpolation in queries, dynamic identifiers | OWASP SQL Injection Cheat Sheet, NoSQL Injection Cheat Sheet |
| XSS & HTML output | Templates rendering user data, `|safe`/raw HTML usage | OWASP XSS Prevention Cheat Sheet |
| Auth & sessions | Password handling, sessions, login flows | OWASP Authentication Cheat Sheet, Session Management Cheat Sheet |
| Crypto & secrets | Custom crypto, weak hashes, hardcoded keys | OWASP Cryptographic Storage Cheat Sheet |
| Files & paths | File uploads, path joins, traversal risks | OWASP File Upload Cheat Sheet |
| Commands & subprocess | `shell=True`, user‑controlled arguments | OWASP Command Injection Prevention |
| Deserialization | Use of `pickle`, unsafe yaml loaders | OWASP Deserialization Cheat Sheet |
| SSRF & HTTP calls | `requests.get(user_url)` patterns | OWASP SSRF Prevention Cheat Sheet |
| Logging & errors | Sensitive data in logs, detailed errors to users | OWASP Logging Cheat Sheet |

---

## 3. Tooling & Automation

- Dependency scanning:  
  - `pip-audit`: https://github.com/pypa/pip-audit  
  - PyPI advisories: https://pypi.org/security/
- Static analysis:  
  - Semgrep: https://semgrep.dev/ (Python rulesets)  
  - Bandit: https://bandit.readthedocs.io/
- Framework docs:  
  - Django security: https://docs.djangoproject.com/en/stable/topics/security/  
  - Flask security patterns: https://flask.palletsprojects.com/en/latest/security/  
  - FastAPI security: https://fastapi.tiangolo.com/advanced/security/

---

## 4. Quick Security Review Checklist

- [ ] User input validated (type, range, length, whitelist where possible).
- [ ] Database access uses parameterized queries or safe ORM APIs.
- [ ] No obvious XSS sinks (raw HTML, `|safe` on user‑controlled data).
- [ ] Passwords hashed with bcrypt/argon2/scrypt (never plain or MD5/SHA1).
- [ ] No hardcoded secrets, keys, or tokens in code.
- [ ] File operations guard against path traversal and validate content type/size.
- [ ] No `shell=True` with user input; subprocess calls are argument‑based.
- [ ] Untrusted data is not deserialized with `pickle`/unsafe loaders.
- [ ] Outbound HTTP calls validate destination (SSRF concerns) as needed.
- [ ] Logging avoids passwords, tokens, and sensitive PII.

---

**Version**: 0.3.0-alpha (Compact Reference Format)
**Last Updated**: 2025-11-14
