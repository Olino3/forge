---
name: secure-code
description: Secure coding practices and vulnerability prevention. Performs systematic security analysis across input validation, authentication, injection prevention, cryptography, secrets management, dependency security, API hardening, and data protection. Classifies findings by OWASP Top 10 categories and produces hardened code with explanations. Use for security audits, pre-deployment hardening, threat modeling of code changes, and secure design reviews across any language or framework.
---

# Secure Code

## ⚠️ MANDATORY COMPLIANCE ⚠️

**CRITICAL**: The 5-step workflow outlined in this document MUST be followed in exact order for EVERY security analysis. Skipping steps or deviating from the procedure will result in incomplete and unreliable security assessments. This is non-negotiable.

## File Structure

- **SKILL.md** (this file): Main instructions and MANDATORY workflow
- **examples.md**: Security hardening scenarios with before/after examples
- **Context**: Security domain context loaded via `contextProvider.getDomainIndex("security")`. See [ContextProvider Interface](../../interfaces/context_provider.md).
  - `security_guidelines.md`, `owasp_python.md`, language-specific security patterns
- **Memory**: Project-specific memory accessed via `memoryStore.getSkillMemory("secure-code", "{project-name}")`. See [MemoryStore Interface](../../interfaces/memory_store.md).

## Security Focus Areas

Security analysis evaluates 8 critical dimensions:

1. **Input Validation & Sanitization**: Whitelist validation, encoding, type coercion, boundary checks
2. **Authentication & Authorization**: Session management, token handling, privilege escalation, RBAC enforcement
3. **Injection Prevention (SQL, XSS, Command)**: Parameterized queries, output encoding, shell escaping, ORM misuse
4. **Cryptography Best Practices**: Algorithm selection, key management, entropy, hashing, TLS configuration
5. **Secrets Management**: Credential storage, environment isolation, vault integration, rotation policies
6. **Dependency Security**: Known CVEs, outdated packages, supply chain risks, lockfile integrity
7. **Secure API Design**: Rate limiting, authentication schemes, CORS, input schemas, error disclosure
8. **Data Protection & Privacy**: Encryption at rest/in transit, PII handling, logging hygiene, data minimization

**Note**: Focus on substantive vulnerabilities requiring human judgment, not theoretical risks. Classify all findings by OWASP Top 10 categories where applicable.

---

## MANDATORY WORKFLOW (MUST FOLLOW EXACTLY)

### ⚠️ STEP 1: Identify Security Scope (REQUIRED)

**YOU MUST:**
1. Determine what code to analyze — specific files, modules, or the full application
2. Identify **trust boundaries** — where untrusted input enters the system (HTTP endpoints, file uploads, CLI args, message queues, database reads)
3. Map **data flows** — how data moves from entry points through processing to storage or output
4. Identify **entry points** — public APIs, event handlers, scheduled tasks, webhook receivers
5. Ask clarifying questions:
   - What is the threat model? (public-facing API, internal service, CLI tool?)
   - Any known security concerns or compliance requirements?
   - What authentication/authorization mechanisms are in place?

**DO NOT PROCEED WITHOUT IDENTIFYING TRUST BOUNDARIES AND DATA FLOWS**

### ⚠️ STEP 2: Load Memory & Context (REQUIRED)

**YOU MUST:**
1. **CHECK PROJECT MEMORY FIRST**:
   - Identify the project name from the repository root or ask the user
   - Use `memoryStore.getSkillMemory("secure-code", "{project-name}")` to load project-specific security patterns
   - **Cross-skill discovery**: Use `memoryStore.getByProject("{project-name}")` to check for code review findings, schema analysis results, or dependency audit insights from other skills
   - If memory exists: Review previously identified vulnerabilities, security patterns, and remediation history
   - If no memory exists (empty result): Note this is first analysis, you will create memory later
2. **USE CONTEXT INDEXES FOR EFFICIENT LOADING**:
   - Use `contextProvider.getDomainIndex("security")` to understand security context files and when to use each
   - Use language-specific domain indexes as needed (e.g., `contextProvider.getDomainIndex("python")`, `contextProvider.getDomainIndex("dotnet")`)

See [ContextProvider](../../interfaces/context_provider.md) and [MemoryStore](../../interfaces/memory_store.md) interfaces.

**DO NOT PROCEED WITHOUT COMPLETING THIS STEP**

### ⚠️ STEP 3: Load Relevant Context (REQUIRED)

**YOU MUST use the indexes to load only relevant files**:

1. **ALWAYS**: Load OWASP guidelines via `contextProvider.getAlwaysLoadFiles("security")` (e.g., `security_guidelines.md`)
2. **Based on language/framework detected**: Use `contextProvider.getConditionalContext("security", detection)` to load language-specific security patterns:
   - **If Python detected**: Loads `owasp_python.md`, Python-specific crypto and injection patterns
   - **If Node.js detected**: Loads Node.js security patterns (prototype pollution, ReDoS, etc.)
   - **If .NET detected**: Loads .NET security patterns (deserialization, CSRF tokens, etc.)
3. **Based on security concern**: Use `contextProvider.getCrossDomainContext("security", triggers)`:
   - Auth code: Loads authentication and authorization patterns
   - API endpoints: Loads API security and rate limiting guidance
   - Database queries: Loads injection prevention patterns
   - File operations: Loads path traversal and upload security patterns
   - Cryptography: Loads crypto best practices and key management guidance

**Progressive loading**: Only load files relevant to the detected language, framework, and security concerns. The ContextProvider respects the 4-6 file token budget automatically.

**DO NOT SKIP LOADING RELEVANT CONTEXT FILES**

### ⚠️ STEP 4: Security Analysis (REQUIRED)

**YOU MUST perform a systematic review for EACH security dimension**:

**Input Validation & Sanitization**: Missing validation, type confusion, encoding bypasses, boundary violations, allow-list vs deny-list
**Authentication & Authorization**: Broken auth flows, missing checks, privilege escalation, insecure session handling, JWT misuse
**Injection Prevention**: SQL/NoSQL injection, XSS (stored/reflected/DOM), command injection, LDAP injection, template injection
**Cryptography**: Weak algorithms (MD5/SHA1 for passwords), hardcoded keys, insufficient entropy, missing TLS, ECB mode usage
**Secrets Management**: Hardcoded credentials, secrets in logs, missing rotation, insecure storage, environment leakage
**Dependency Security**: Known CVEs in dependencies, outdated packages, typosquatting risks, lockfile inconsistencies
**API Security**: Missing rate limiting, excessive data exposure, broken object-level authorization, mass assignment
**Data Protection**: PII in logs, missing encryption at rest, insecure data transfer, excessive data retention

**Classify each finding by OWASP Top 10 category**:
- A01: Broken Access Control
- A02: Cryptographic Failures
- A03: Injection
- A04: Insecure Design
- A05: Security Misconfiguration
- A06: Vulnerable and Outdated Components
- A07: Identification and Authentication Failures
- A08: Software and Data Integrity Failures
- A09: Security Logging and Monitoring Failures
- A10: Server-Side Request Forgery (SSRF)

**DO NOT SKIP ANY SECURITY DIMENSION**

### ⚠️ STEP 5: Generate Secure Code & Update Memory (REQUIRED)

**YOU MUST produce hardened code with explanations**:

1. **For EVERY finding, provide**:
   - **Severity**: Critical / High / Medium / Low
   - **OWASP Category**: Which Top 10 category it maps to
   - **Description**: What the vulnerability is and why it matters
   - **Attack Scenario**: How an attacker could exploit it
   - **Secure Code**: Hardened replacement with inline comments explaining the fix
   - **Reference**: Link to OWASP, CWE, or language-specific security docs

2. **Generate output report**:
   - Save to `/claudedocs/secure-code_{project}_{YYYY-MM-DD}.md`
   - Follow naming conventions in `../OUTPUT_CONVENTIONS.md`
   - Include executive summary, findings by severity, and remediation roadmap

3. **Format guidelines**:
   - Explain WHY (threat model impact, not just "this is insecure")
   - Show HOW to fix with production-ready code
   - Be specific with file:line references
   - Prioritize findings by exploitability and impact

**DO NOT PROVIDE INCOMPLETE RECOMMENDATIONS**

**After completing the analysis, UPDATE PROJECT MEMORY**:

Use `memoryStore.update("secure-code", "{project-name}", ...)` to create or update memory files:

1. **security_profile**: Architecture, trust boundaries, auth mechanisms, compliance requirements
2. **known_vulnerabilities**: Previously identified issues and their remediation status
3. **security_patterns**: Project-specific security conventions and patterns discovered
4. **audit_history**: Summary of audits performed with dates and key findings

Timestamps and staleness tracking are managed automatically by MemoryStore. See [MemoryStore Interface](../../interfaces/memory_store.md) for `update()` and `append()` method details.

---

## Interface References

- **Context**: Loaded via [ContextProvider Interface](../../interfaces/context_provider.md)
- **Memory**: Accessed via [MemoryStore Interface](../../interfaces/memory_store.md)
- **Shared Patterns**: [Shared Loading Patterns](../../interfaces/shared_loading_patterns.md)
- **Schemas**: Validated against [context_metadata.schema.json](../../interfaces/schemas/context_metadata.schema.json) and [memory_entry.schema.json](../../interfaces/schemas/memory_entry.schema.json)

## Compliance Checklist

Before completing ANY security analysis, verify:
- [ ] Step 1: Security scope identified — trust boundaries, data flows, and entry points mapped
- [ ] Step 2: Project memory loaded via `memoryStore.getSkillMemory()` and context detected via `contextProvider`
- [ ] Step 3: All relevant context files loaded via `contextProvider.getAlwaysLoadFiles()`, `getConditionalContext()`, and `getCrossDomainContext()`
- [ ] Step 4: Systematic security review completed for ALL dimensions with OWASP Top 10 classification
- [ ] Step 5: Hardened code generated with explanations AND project memory updated via `memoryStore.update()`

**FAILURE TO COMPLETE ALL STEPS INVALIDATES THE SECURITY ANALYSIS**

## Version History

- v1.0.0 (2026-02-12): Initial release
