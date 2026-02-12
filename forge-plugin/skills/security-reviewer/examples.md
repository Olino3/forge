# Security Reviewer Examples

This file contains example security audit scenarios demonstrating the 5-step mandatory workflow, common findings, and remediation guidance.

## Example 1: Web Application Security Audit (Django)

### User Prompt

> "Perform a full OWASP Top 10 security audit of our Django e-commerce application."

### Skill Execution

**Step 1 — Define Audit Scope**: Target is a Django 4.2 e-commerce application with PostgreSQL, Redis session store, Stripe payment integration, and REST API. Compliance requirements: OWASP Top 10, PCI-DSS for payment handling. Trust boundaries: public internet → web server → application → database → payment gateway.

**Step 2 — Load Memory & Context**: `memoryStore.getSkillMemory("security-reviewer", "ecommerce-app")` returns previous audit from 3 months ago with 2 unresolved medium-severity findings. Cross-skill discovery via `memoryStore.getByProject("ecommerce-app")` reveals `python-code-review` found N+1 queries in order processing.

**Step 3 — Load Security Context**: Loaded `security_guidelines.md` and `owasp_python.md` via `contextProvider.getAlwaysLoadFiles("security")`. Loaded Django-specific patterns via `contextProvider.getConditionalContext("security", {framework: "django"})`. Loaded auth and API patterns via `contextProvider.getCrossDomainContext("security", ["authentication", "api_endpoints", "payment_processing"])`.

**Step 4 — Security Audit (STRIDE)**: Systematic review of all Django views, middleware, models, and API endpoints against STRIDE categories.

**Step 5 — Generate Audit Report & Update Memory**: Full report with 12 findings, remediation plan, and OWASP Top 10 compliance matrix.

### Audit Report Output

```markdown
# Security Audit Report — ecommerce-app
**Date**: 2026-02-12
**Auditor**: Security Reviewer Skill
**Scope**: Full OWASP Top 10 audit of Django e-commerce application

## Executive Summary

| Metric | Value |
|--------|-------|
| Components Audited | 47 views, 23 models, 12 API endpoints, 8 middleware |
| Critical Findings | 2 |
| High Findings | 3 |
| Medium Findings | 5 |
| Low Findings | 2 |
| Overall Risk Rating | HIGH |

## Detailed Findings

### Finding 1: Insecure Direct Object Reference in Order API

**Severity**: Critical
**STRIDE Category**: Elevation of Privilege
**CWE**: CWE-639 (Authorization Bypass Through User-Controlled Key)
**File**: api/views.py:87

**Description**: The order detail endpoint uses the order ID directly from the URL without verifying the requesting user owns the order. Any authenticated user can access any order's details including payment information.

**Evidence**:
```python
# api/views.py:87
class OrderDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, order_id):
        order = Order.objects.get(id=order_id)  # No ownership check!
        return Response(OrderSerializer(order).data)
```

**Impact**: Attackers can enumerate order IDs and access other customers' order details, shipping addresses, and partial payment information.

**Remediation**:
```python
# api/views.py:87
class OrderDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, order_id):
        order = get_object_or_404(
            Order, id=order_id, user=request.user  # Ownership enforced
        )
        return Response(OrderSerializer(order).data)
```

**Reference**: OWASP A01:2021 - Broken Access Control

### Finding 2: Missing CSRF Protection on Payment Webhook

**Severity**: Critical
**STRIDE Category**: Tampering
**CWE**: CWE-352 (Cross-Site Request Forgery)
**File**: payments/views.py:42

**Description**: The Stripe webhook endpoint has `@csrf_exempt` but does not verify the Stripe webhook signature, allowing attackers to forge payment confirmation events.

**Evidence**:
```python
# payments/views.py:42
@csrf_exempt
def stripe_webhook(request):
    payload = json.loads(request.body)
    event_type = payload['type']  # No signature verification!
    if event_type == 'payment_intent.succeeded':
        mark_order_paid(payload['data']['object']['metadata']['order_id'])
```

**Impact**: Attackers can send forged webhook payloads to mark orders as paid without actual payment.

**Remediation**:
```python
# payments/views.py:42
@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except (ValueError, stripe.error.SignatureVerificationError):
        return HttpResponse(status=400)
    if event['type'] == 'payment_intent.succeeded':
        mark_order_paid(event['data']['object']['metadata']['order_id'])
    return HttpResponse(status=200)
```

**Reference**: OWASP A08:2021 - Software and Data Integrity Failures

### Finding 3: Session Fixation Vulnerability

**Severity**: High
**STRIDE Category**: Spoofing
**CWE**: CWE-384 (Session Fixation)
**File**: settings.py:112

**Description**: Django session is not rotated after login. `SESSION_COOKIE_HTTPONLY` is set but `request.session.cycle_key()` is not called post-authentication in the custom login view.

**Remediation**: Ensure `django.contrib.auth.login()` is used (which calls `cycle_key()` automatically) or call `request.session.cycle_key()` explicitly after custom authentication.

**Reference**: OWASP A07:2021 - Identification and Authentication Failures

## Remediation Plan

| Priority | Finding | Effort | Target |
|----------|---------|--------|--------|
| P0 | IDOR in Order API | Low | Immediate |
| P0 | Missing webhook signature | Low | Immediate |
| P1 | Session fixation | Low | 1 week |
| P1 | Missing rate limiting on login | Medium | 1 week |
| P1 | Verbose error messages in production | Low | 1 week |
| P2 | Weak password policy | Medium | 2 weeks |

## OWASP Top 10 Compliance Status

| Category | Status | Findings |
|----------|--------|----------|
| A01: Broken Access Control | ❌ FAIL | Finding 1 (IDOR) |
| A02: Cryptographic Failures | ✅ PASS | — |
| A03: Injection | ✅ PASS | ORM used consistently |
| A04: Insecure Design | ⚠️ WARN | Missing rate limiting |
| A05: Security Misconfiguration | ⚠️ WARN | DEBUG=True in staging |
| A06: Vulnerable Components | ✅ PASS | Dependencies current |
| A07: Auth Failures | ❌ FAIL | Finding 3 (Session) |
| A08: Integrity Failures | ❌ FAIL | Finding 2 (Webhook) |
| A09: Logging Failures | ⚠️ WARN | No security event logging |
| A10: SSRF | ✅ PASS | — |
```

---

## Example 2: STRIDE Threat Model for Microservices

### User Prompt

> "Build a STRIDE threat model for our API gateway plus 3 microservices architecture."

### Skill Execution

**Step 1 — Define Audit Scope**: Architecture consists of an API Gateway (Kong), User Service (Node.js), Order Service (Python/FastAPI), and Notification Service (Go). Services communicate via gRPC internally and REST externally. Data stores: PostgreSQL (User, Order), Redis (sessions, cache), RabbitMQ (async messaging). Trust boundaries: Internet → API Gateway → Internal Services → Databases.

**Step 2 — Load Memory & Context**: `memoryStore.getSkillMemory("security-reviewer", "microservices-platform")` returns empty — first audit. Cross-skill discovery finds no prior skill memory for this project.

**Step 3 — Load Security Context**: Loaded core security guidelines. Loaded API security patterns and microservices-specific context via conditional and cross-domain loading for authentication, API endpoints, and message queue triggers.

**Step 4 — Security Audit (STRIDE)**: Applied STRIDE to each component and communication channel.

**Step 5 — Generate Audit Report & Update Memory**: Threat model document with per-component STRIDE analysis and risk matrix.

### Audit Report Output

```markdown
# STRIDE Threat Model — microservices-platform
**Date**: 2026-02-12
**Scope**: API Gateway + User Service + Order Service + Notification Service

## Executive Summary

| Metric | Value |
|--------|-------|
| Components Modeled | 4 services, 3 data stores, 1 message broker |
| Trust Boundaries | 4 (Internet, DMZ, Internal, Data) |
| Threats Identified | 18 |
| Critical Threats | 3 |
| High Threats | 5 |

## Trust Boundary Diagram

```
Internet → [API Gateway (Kong)] → Internal Zone
                                    ├── User Service (Node.js) → PostgreSQL
                                    ├── Order Service (FastAPI) → PostgreSQL
                                    ├── Notification Service (Go)
                                    └── RabbitMQ (async messaging)
                                    └── Redis (sessions/cache)
```

## STRIDE Analysis by Component

### API Gateway (Kong)

| Threat | Category | Severity | Description |
|--------|----------|----------|-------------|
| T-GW-01 | Spoofing | Critical | JWT validation bypass if `alg: none` is not explicitly rejected. CWE-327. |
| T-GW-02 | Denial of Service | High | No per-client rate limiting configured; API flood attacks possible. CWE-770. |
| T-GW-03 | Information Disclosure | Medium | Gateway error responses expose internal service topology. CWE-209. |

**Remediation for T-GW-01**:
```yaml
# kong.yml - JWT plugin configuration
plugins:
  - name: jwt
    config:
      algorithms:
        - RS256    # Explicitly allow only RS256
      # 'none' algorithm is rejected by not being listed
      secret_is_base64: false
```

### User Service (Node.js)

| Threat | Category | Severity | Description |
|--------|----------|----------|-------------|
| T-US-01 | Spoofing | High | Password reset tokens use `Math.random()` — predictable. CWE-330. |
| T-US-02 | Information Disclosure | High | User enumeration via different error messages for valid/invalid emails on login. CWE-203. |
| T-US-03 | Tampering | Medium | User profile update accepts `role` field in request body without filtering. CWE-915. |

**Remediation for T-US-01**:
```javascript
// Before: predictable token generation
const token = Math.random().toString(36).substring(2);

// After: cryptographically secure token
const crypto = require('crypto');
const token = crypto.randomBytes(32).toString('hex');
```

### Inter-Service Communication

| Threat | Category | Severity | Description |
|--------|----------|----------|-------------|
| T-ISC-01 | Spoofing | Critical | gRPC calls between services have no mutual TLS — any internal process can impersonate a service. CWE-295. |
| T-ISC-02 | Tampering | High | RabbitMQ messages are unsigned — a compromised service can inject malicious messages. CWE-345. |
| T-ISC-03 | Repudiation | Medium | No correlation IDs in inter-service calls — difficult to trace request chains for audit. CWE-778. |

## Risk Matrix

| Likelihood \ Impact | Low | Medium | High | Critical |
|---------------------|-----|--------|------|----------|
| **High** | — | T-US-03 | T-GW-02, T-ISC-02 | T-GW-01, T-ISC-01 |
| **Medium** | — | T-GW-03, T-ISC-03 | T-US-01, T-US-02 | — |
| **Low** | T-NS-02 | T-NS-01 | — | — |

## Remediation Priority

1. **Immediate**: T-GW-01 (JWT bypass), T-ISC-01 (mutual TLS)
2. **This Sprint**: T-US-01 (token randomness), T-ISC-02 (message signing), T-GW-02 (rate limiting)
3. **Next Sprint**: T-US-02 (user enumeration), T-US-03 (mass assignment), T-ISC-03 (correlation IDs)
```

---

## Example 3: Dependency Vulnerability Assessment

### User Prompt

> "Audit our npm and pip dependencies for known CVEs and supply chain risks."

### Skill Execution

**Step 1 — Define Audit Scope**: Target is a full-stack application with a React frontend (npm/package-lock.json) and a Flask backend (pip/requirements.txt + Pipfile.lock). Scope includes direct and transitive dependencies. Compliance requirement: No critical or high CVEs in production dependencies.

**Step 2 — Load Memory & Context**: `memoryStore.getSkillMemory("security-reviewer", "fullstack-app")` returns previous dependency audit from 6 weeks ago identifying 3 vulnerabilities — 1 was patched, 2 remain. Cross-skill discovery finds no additional context.

**Step 3 — Load Security Context**: Loaded core security guidelines via `contextProvider.getAlwaysLoadFiles("security")`. Loaded dependency-specific context via `contextProvider.getCrossDomainContext("security", ["dependencies", "supply_chain"])` for CVE database references and supply chain risk indicators.

**Step 4 — Security Audit**: Analyzed `package-lock.json` and `Pipfile.lock` against known CVE databases. Evaluated supply chain indicators: maintainer count, download trends, typosquatting risk, install script presence.

**Step 5 — Generate Audit Report & Update Memory**: Dependency audit report with CVE findings, supply chain risk assessment, and upgrade plan.

### Audit Report Output

```markdown
# Dependency Vulnerability Assessment — fullstack-app
**Date**: 2026-02-12
**Scope**: npm (342 packages) + pip (67 packages) — direct and transitive

## Executive Summary

| Metric | npm | pip | Total |
|--------|-----|-----|-------|
| Direct Dependencies | 28 | 15 | 43 |
| Transitive Dependencies | 314 | 52 | 366 |
| Critical CVEs | 1 | 0 | 1 |
| High CVEs | 2 | 1 | 3 |
| Medium CVEs | 4 | 2 | 6 |
| Supply Chain Risks | 2 | 1 | 3 |
| Overall Risk Rating | HIGH | MEDIUM | HIGH |

## Critical & High CVE Findings

### CVE-2024-XXXXX: Prototype Pollution in lodash (npm)

**Severity**: Critical
**CWE**: CWE-1321 (Improperly Controlled Modification of Object Prototype Attributes)
**Package**: lodash@4.17.20 (transitive via react-scripts)
**CVSS**: 9.8

**Description**: Prototype pollution vulnerability allows attackers to inject properties into Object.prototype, potentially leading to RCE in server-side rendering contexts.

**Impact**: If lodash is used in SSR or API routes, attackers can achieve remote code execution.

**Remediation**:
```json
// package.json — force resolution to patched version
{
  "overrides": {
    "lodash": ">=4.17.21"
  }
}
```

### CVE-2024-YYYYY: SQL Injection in SQLAlchemy (pip)

**Severity**: High
**CWE**: CWE-89 (SQL Injection)
**Package**: SQLAlchemy==1.4.46
**CVSS**: 8.1

**Description**: Specific usage of `text()` construct with string formatting is vulnerable to SQL injection in versions prior to 1.4.49.

**Impact**: If raw SQL via `text()` is used with user input, attackers can execute arbitrary SQL.

**Remediation**:
```txt
# requirements.txt
SQLAlchemy>=2.0.23  # Upgrade to 2.x (preferred) or >=1.4.49 (minimum)
```

### CVE-2024-ZZZZZ: ReDoS in semver (npm)

**Severity**: High
**CWE**: CWE-1333 (Inefficient Regular Expression Complexity)
**Package**: semver@5.7.1 (transitive via 6 packages)
**CVSS**: 7.5

**Description**: Regular expression denial of service via crafted version strings.

**Remediation**:
```json
{
  "overrides": {
    "semver": ">=5.7.2"
  }
}
```

## Supply Chain Risk Assessment

### Risk 1: Typosquatting Candidate — `colorsjs` (npm)

**Risk Level**: High
**Indicator**: Package name is 1 character different from popular `colors` package. Installed 3 weeks ago with only 47 total downloads. Single anonymous maintainer.

**Recommendation**: Verify this is the intended package. If meant to use `colors`, replace immediately:
```bash
npm uninstall colorsjs && npm install colors
```

### Risk 2: Abandoned Package — `flask-cors` (pip)

**Risk Level**: Medium
**Indicator**: No releases in 18 months, 23 open issues, no maintainer activity. No known CVEs but security patches unlikely.

**Recommendation**: Monitor for alternatives or pin to current version with manual security review.

### Risk 3: Install Script Detected — `node-sass` (npm)

**Risk Level**: Medium
**Indicator**: Package runs native compilation scripts during `npm install`. Supply chain risk via build-time code execution.

**Recommendation**: Migrate to `sass` (Dart Sass) which requires no native compilation:
```bash
npm uninstall node-sass && npm install sass
```

## Remediation Plan

| Priority | Action | Package | Effort |
|----------|--------|---------|--------|
| P0 | Upgrade | lodash → >=4.17.21 | Low |
| P0 | Verify | colorsjs — confirm or remove | Low |
| P1 | Upgrade | SQLAlchemy → >=2.0.23 | Medium |
| P1 | Upgrade | semver → >=5.7.2 | Low |
| P2 | Migrate | node-sass → sass | Medium |
| P2 | Monitor | flask-cors — watch for alternatives | Low |

## Dependency Hygiene Recommendations

1. **Enable automated scanning**: Configure Dependabot or Snyk for continuous CVE monitoring
2. **Pin transitive dependencies**: Use lockfiles (`package-lock.json`, `Pipfile.lock`) and verify integrity hashes
3. **Audit install scripts**: Run `npm audit signatures` and review packages with install hooks
4. **Establish upgrade cadence**: Monthly dependency updates with automated CI testing
5. **Minimize dependency surface**: Remove unused packages, prefer stdlib alternatives where possible
```

---

## Summary of Common Audit Findings

1. **Access Control**: IDOR, missing authorization checks, privilege escalation
2. **Authentication**: Weak tokens, session fixation, missing MFA, user enumeration
3. **Injection**: SQL, command, template injection via unsanitized inputs
4. **Cryptography**: Weak algorithms, predictable randomness, hardcoded secrets
5. **Dependencies**: Known CVEs, abandoned packages, typosquatting, supply chain risks
6. **Architecture**: Missing trust boundaries, unsigned inter-service communication, no mTLS
7. **Compliance**: OWASP Top 10 gaps, missing audit logging, insufficient monitoring

Use these examples as reference when conducting security audits. Adapt the depth and focus to the target system's architecture and compliance requirements.
