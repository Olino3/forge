# Cross-Domain Context References

Maps when skills should load context from multiple domains. Consult this file during Step 5 of the [Context Loading Protocol](loading_protocol.md).

## Cross-Domain Trigger Matrix

| Primary Domain | Trigger Condition | Secondary Context to Load |
|---|---|---|
| python/ | Auth, password, or input handling code detected | `security/security_guidelines.md` |
| python/ | SQL queries, ORM usage, or database models detected | `security/security_guidelines.md` |
| python/ | Schema/migration files in diff | `schema/common_patterns.md` |
| dotnet/ | Auth, Identity, or JWT code detected | `security/security_guidelines.md` |
| dotnet/ | Database queries, EF migrations present | `security/security_guidelines.md` |
| dotnet/ | Schema or migration files in diff | `schema/common_patterns.md` |
| angular/ | API integration, HTTP calls, or form input code | `security/security_guidelines.md` |
| angular/ | API schema/contract files detected | `schema/common_patterns.md` |
| schema/ | Database schema with PII or sensitive data | `security/security_guidelines.md` |
| Any code review | Performance-critical code flagged | `{domain}/performance_patterns.md` |
| Any code review | Schema/migration files in diff | `schema/common_patterns.md` |
| Any code review | Infrastructure or deployment files | `azure/index.md` (for Azure projects) |

## How to Use

1. Determine your **primary domain** (the main language/framework being analyzed)
2. Scan the trigger conditions for your primary domain
3. If a trigger matches, load the specified secondary context file
4. Secondary context supplements but does not replace primary domain context

## Priority Rules

When multiple cross-domain triggers match:

1. **Security context** takes highest priority (always load if triggered)
2. **Schema context** when data structures are involved
3. **Performance context** when optimization is relevant
4. **Infrastructure context** when deployment files are present

## Token Budget Consideration

Cross-domain files count toward the 4-6 file budget per invocation (see `loading_protocol.md`). If already at the limit, prioritize security context over other cross-domain files.

---

*Last Updated: 2026-02-10*
