---
name: security-reviewer
description: Security audits, threat modeling, and compliance assessment for existing codebases. Performs systematic security reviews using STRIDE threat modeling, attack surface analysis, authentication and authorization audits, data flow and trust boundary analysis, dependency vulnerability assessment, and compliance checking against OWASP Top 10, CWE, and SANS frameworks. Classifies findings by severity and maps to CWE IDs. Use for security audits, threat modeling, compliance assessments, and penetration testing guidance across any language or architecture.
---

# Security Reviewer

## ⚠️ MANDATORY COMPLIANCE ⚠️

**CRITICAL**: The 5-step workflow outlined in this document MUST be followed in exact order for EVERY security audit. Skipping steps or deviating from the procedure will result in incomplete and unreliable audit results. This is non-negotiable.

## File Structure

- **SKILL.md** (this file): Main instructions and MANDATORY workflow
- **examples.md**: Audit scenarios with example findings and remediation guidance
- **Context**: Security domain context loaded via `contextProvider.getDomainIndex("security")`. See [ContextProvider Interface](../../interfaces/context_provider.md).
  - `security_guidelines.md`, `owasp_python.md`, compliance frameworks, language-specific security patterns
- **Memory**: Project-specific memory accessed via `memoryStore.getSkillMemory("security-reviewer", "{project-name}")`. See [MemoryStore Interface](../../interfaces/memory_store.md).

## Audit Focus Areas

Security audits evaluate 8 critical dimensions across the target system:

1. **Threat Modeling (STRIDE)**: Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege — systematic identification of threats per component
2. **Attack Surface Analysis**: Entry points, external interfaces, data ingress/egress, exposed APIs, network boundaries, third-party integrations
3. **Authentication & Session Management Audit**: Credential storage, session lifecycle, token handling, MFA implementation, brute-force protections, password policies
4. **Authorization & Access Control Audit**: RBAC/ABAC enforcement, privilege escalation paths, horizontal/vertical access control, resource-level permissions, least privilege adherence
5. **Data Flow & Trust Boundary Analysis**: Sensitive data paths, encryption in transit/at rest, trust boundary crossings, data classification, PII handling, logging of sensitive data
6. **Dependency Vulnerability Assessment**: Known CVEs in dependencies, outdated packages, supply chain risks, lockfile integrity, transitive dependency analysis
7. **Compliance Checking (OWASP, CWE, SANS)**: OWASP Top 10 coverage, CWE mapping for all findings, SANS Top 25 alignment, framework-specific security benchmarks
8. **Penetration Testing Guidance**: Attack vector identification, exploitation scenarios, proof-of-concept guidance, risk-rated remediation priorities

**Note**: This skill focuses on auditing existing systems and code — not on writing new secure code. For proactive secure coding, use the `secure-code` skill instead.

---

## MANDATORY WORKFLOW (MUST FOLLOW EXACTLY)

### ⚠️ STEP 1: Define Audit Scope (REQUIRED)

**YOU MUST:**
1. **Identify the target system/codebase** to be audited:
   - Repository, service, or component boundaries
   - Technology stack and languages in use
   - Deployment environment (cloud, on-prem, hybrid)
2. **Determine compliance requirements**:
   - Applicable standards (OWASP Top 10, CWE, SANS, PCI-DSS, HIPAA, SOC 2)
   - Industry-specific regulations
   - Organization security policies
3. **Establish threat model boundaries**:
   - System actors (users, admins, external services, attackers)
   - Trust boundaries and zones
   - Data sensitivity classification (public, internal, confidential, restricted)
   - In-scope vs. out-of-scope components
4. Ask clarifying questions in Socratic format:
   - What is the primary function of this system?
   - What are the most critical assets to protect?
   - Are there known areas of concern?
   - What is the deployment and network architecture?

**DO NOT PROCEED WITHOUT DEFINING AUDIT SCOPE**

### ⚠️ STEP 2: Load Memory & Context (REQUIRED)

**YOU MUST:**
1. **CHECK PROJECT MEMORY FIRST**:
   - Identify the project name from the repository root or ask the user
   - Use `memoryStore.getSkillMemory("security-reviewer", "{project-name}")` to load project-specific audit history
   - **Cross-skill discovery**: Use `memoryStore.getByProject("{project-name}")` to check for findings from `secure-code`, `python-code-review`, or other skill audits
   - If memory exists: Review previous audit findings, known vulnerabilities, accepted risks
   - If no memory exists (empty result): Note this is first audit, you will create memory later
2. **USE CONTEXT INDEXES FOR EFFICIENT LOADING**:
   - Use `contextProvider.getDomainIndex("security")` to understand available security context files and when to load each

See [ContextProvider](../../interfaces/context_provider.md) and [MemoryStore](../../interfaces/memory_store.md) interfaces.

**DO NOT PROCEED WITHOUT COMPLETING THIS STEP**

### ⚠️ STEP 3: Load Security Context (REQUIRED)

**YOU MUST load relevant security context based on audit scope:**

1. **ALWAYS**: Use `contextProvider.getAlwaysLoadFiles("security")` to load core security guidelines and OWASP references
2. **Based on technology stack**: Use `contextProvider.getConditionalContext("security", detection)` to load language and framework-specific security patterns:
   - **If Python detected**: Loads `owasp_python.md`, Python-specific vulnerability patterns
   - **If JavaScript/Node detected**: Loads JS-specific security patterns (prototype pollution, XSS)
   - **If Java detected**: Loads Java-specific patterns (deserialization, JNDI)
   - **If infrastructure code detected**: Loads cloud security and IaC patterns
3. **Based on audit focus**: Use `contextProvider.getCrossDomainContext("security", triggers)` where triggers include:
   - Authentication code: Loads auth-specific guidelines
   - API endpoints: Loads API security patterns
   - Data storage: Loads data protection and encryption guidelines
   - Compliance audit: Loads full OWASP Top 10 and CWE reference material

**Progressive loading**: Only load files relevant to the detected stack and audit scope. The ContextProvider respects the 4-6 file token budget automatically.

**DO NOT SKIP LOADING RELEVANT CONTEXT FILES**

### ⚠️ STEP 4: Security Audit (REQUIRED)

**YOU MUST perform a systematic review using the STRIDE threat model:**

**For each component in scope, evaluate all STRIDE categories:**

- **Spoofing**: Can an attacker impersonate a legitimate user or system? Check authentication mechanisms, certificate validation, API key handling
- **Tampering**: Can data be modified without detection? Check integrity controls, input validation, database constraints, signed tokens
- **Repudiation**: Can actions be denied? Check audit logging, non-repudiation controls, transaction records
- **Information Disclosure**: Can sensitive data leak? Check error messages, logging, encryption, access controls, side-channel attacks
- **Denial of Service**: Can the system be made unavailable? Check rate limiting, resource exhaustion, input size limits, connection pooling
- **Elevation of Privilege**: Can an attacker gain unauthorized access? Check authorization enforcement, role boundaries, injection points

**Classify ALL findings by severity:**

| Severity | Criteria |
|----------|----------|
| **Critical** | Actively exploitable, data breach risk, no authentication bypass, RCE |
| **High** | Significant risk requiring prompt remediation, privilege escalation paths |
| **Medium** | Moderate risk, defense-in-depth gaps, non-standard configurations |
| **Low** | Minor issues, best practice deviations, informational findings |

**Map every finding to a CWE ID** (e.g., CWE-89: SQL Injection, CWE-287: Improper Authentication).

**DO NOT SKIP ANY STRIDE CATEGORY**

### ⚠️ STEP 5: Generate Audit Report & Update Memory (REQUIRED)

**YOU MUST generate a comprehensive audit report with these sections:**

1. **Executive Summary**: Scope, methodology, overall risk rating, critical findings count
2. **Detailed Findings**: Each finding with:
   - **Severity**: Critical / High / Medium / Low
   - **STRIDE Category**: Which threat category it falls under
   - **CWE ID**: Mapped Common Weakness Enumeration identifier
   - **Description**: What the vulnerability is and why it matters
   - **Evidence**: Code snippets, configuration excerpts, or data flow diagrams
   - **Impact**: What an attacker could achieve by exploiting this
   - **Remediation**: Concrete fix with code examples
   - **Reference**: Link to OWASP, CWE, or framework documentation
3. **Remediation Plan**: Prioritized action items ordered by severity and effort
4. **Compliance Status**: Pass/fail assessment against applicable standards (OWASP Top 10 coverage, CWE mapping)

Output the report to `claudedocs/` following `OUTPUT_CONVENTIONS.md`.

**After completing the audit, UPDATE PROJECT MEMORY**:

Use `memoryStore.update("security-reviewer", "{project-name}", ...)` to create or update memory files:

1. **audit_history**: Summary of audits performed with dates, scope, and key findings
2. **known_vulnerabilities**: Tracked vulnerabilities with status (open, remediated, accepted risk)
3. **threat_model**: STRIDE-based threat model for the system
4. **compliance_status**: Current compliance posture against applicable standards

Timestamps and staleness tracking are managed automatically by MemoryStore. See [MemoryStore Interface](../../interfaces/memory_store.md) for `update()` and `append()` method details.

**DO NOT PROVIDE INCOMPLETE AUDIT REPORTS**

---

## Interface References

- **ContextProvider**: [../../interfaces/context_provider.md](../../interfaces/context_provider.md) — Load security context by domain, tags, or sections
- **MemoryStore**: [../../interfaces/memory_store.md](../../interfaces/memory_store.md) — Read/write project-specific audit memory with lifecycle automation
- **SkillInvoker**: [../../interfaces/skill_invoker.md](../../interfaces/skill_invoker.md) — Delegate to related skills (`secure-code`, `python-code-review`)
- **ExecutionContext**: [../../interfaces/execution_context.md](../../interfaces/execution_context.md) — Pass context between chained commands

## Compliance Checklist

Before completing ANY audit, verify:
- [ ] Step 1: Audit scope defined including target system, compliance requirements, and threat model boundaries
- [ ] Step 2: Project memory loaded via `memoryStore.getSkillMemory()` and cross-skill discovery completed via `memoryStore.getByProject()`
- [ ] Step 3: Security context loaded via `contextProvider.getAlwaysLoadFiles()`, `getConditionalContext()`, and `getCrossDomainContext()`
- [ ] Step 4: Systematic STRIDE-based review completed with all findings classified by severity and mapped to CWE IDs
- [ ] Step 5: Audit report generated with executive summary, detailed findings, remediation plan, and compliance status AND project memory updated via `memoryStore.update()`

**FAILURE TO COMPLETE ALL STEPS INVALIDATES THE AUDIT**

## Version History

- v1.0.0 (2026-02-12): Initial release
  - STRIDE-based threat modeling workflow
  - OWASP Top 10 and CWE compliance checking
  - Attack surface analysis and trust boundary mapping
  - Dependency vulnerability assessment
  - Interface-based context and memory access
