---
id: "security/owasp_python"
domain: security
title: "OWASP Top 10 for Python - Quick Reference"
type: reference
estimatedTokens: 350
loadingStrategy: onDemand
version: "0.2.0-alpha"
lastUpdated: "2026-02-10"
sections:
  - name: "Official OWASP Resources"
    estimatedTokens: 22
    keywords: [official, owasp, resources]
  - name: "Mapping OWASP to Python Code"
    estimatedTokens: 166
    keywords: [mapping, owasp, python, code]
  - name: "Quick OWASP‑Aligned Review Checklist"
    estimatedTokens: 106
    keywords: [quick, owaspaligned, review, checklist]
  - name: "Additional References"
    estimatedTokens: 16
    keywords: [additional, references]
tags: [security, owasp, python, top-10, vulnerabilities, audit]
---

# OWASP Top 10 for Python – Quick Reference

Pointers for applying OWASP Top 10 to Python apps without embedding long examples.

**Load this file** when doing a security audit or mapping findings to OWASP categories.

---

## 1. Official OWASP Resources

- OWASP Top 10 (current):  
  https://owasp.org/Top10/
- OWASP Python Security Project:  
  https://owasp.org/www-project-python-security/
- OWASP Cheat Sheet Series:  
  https://cheatsheetseries.owasp.org/

Use these as the canonical source for definitions, examples, and mitigations.

---

## 2. Mapping OWASP to Python Code

| OWASP Category | Typical Python Signals | Where to Look |
|----------------|------------------------|---------------|
| A01 – Broken Access Control | Missing authorization checks, direct object access by id, relying on client flags | Route decorators, view functions, permission checks |
| A02 – Cryptographic Failures | Custom crypto, weak hashes (MD5/SHA1), hardcoded keys | Auth modules, crypto helpers, settings/config |
| A03 – Injection | `cursor.execute(f"...{user_input}...")`, `shell=True`, raw ORM queries | DB access code, subprocess calls, template rendering |
| A04 – Insecure Design | No rate limiting, no lockout, missing security requirements | Auth flows, design docs, high‑risk endpoints |
| A05 – Security Misconfiguration | Debug enabled, default creds, missing security headers | App config, deployment manifests, middleware |
| A06 – Vulnerable Components | Old library versions, no scanning, ad‑hoc installs | `requirements.txt`, lockfiles, CI pipelines |
| A07 – Id & Auth Failures | Weak passwords, missing MFA, poor session handling | Login/register views, session config, token handling |
| A08 – Integrity Failures | Unsafe deserialization (`pickle`), unsigned updates | Serialization code, update mechanisms, CI/CD |
| A09 – Logging & Monitoring | No auth logs, no alerts, logs with sensitive data | Logging config, monitoring rules, SIEM integration |
| A10 – SSRF | `requests.get(user_url)` without validation | HTTP client wrappers, URL fetch utilities |

---

## 3. Quick OWASP‑Aligned Review Checklist

- [ ] A01: Every protected resource has explicit server‑side authorization checks.
- [ ] A02: Passwords and sensitive data use strong crypto and proper key management.
- [ ] A03: All data access and system calls use parameterized APIs and validated input.
- [ ] A04: High‑risk flows (login, payments, admin) have rate limiting and safe defaults.
- [ ] A05: Production configs disable debug, use security headers, and avoid default creds.
- [ ] A06: Dependencies are pinned, scanned regularly, and updated when vulnerable.
- [ ] A07: Authentication is robust (password policy, session handling, MFA where relevant).
- [ ] A08: Untrusted data is not deserialized unsafely; integrity is protected for critical data.
- [ ] A09: Security‑relevant events are logged and monitored without leaking secrets.
- [ ] A10: URL‑based integrations validate targets and block internal/metadata endpoints.

---

## 4. Additional References

- CWE Top 25: https://cwe.mitre.org/top25/
- NIST Secure Software Development Framework (SSDF): https://csrc.nist.gov/projects/ssdf

---

**Version**: 0.2.0-alpha (Compact Reference Format)
**Last Updated**: 2025-11-14
