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
- Analyzing API endpoints

**Key sections**:
- **Input Validation**: Path traversal, type validation, length limits
- **SQL Injection Prevention**: Parameterized queries, ORM usage, dynamic SQL
- **Cross-Site Scripting (XSS)**: Template escaping, safe HTML, content types
- **Authentication & Authorization**: Password handling, session management, RBAC
- **Cryptography**: Hashing, encryption, key management, secure random
- **File Operations**: Path validation, secure uploads, temporary files
- **API Security**: Rate limiting, CORS, API keys, token validation
- **Environment & Secrets**: Configuration, secret management, logging
- **Dependency Security**: Version pinning, vulnerability scanning
- **Error Handling**: Information disclosure, safe errors, logging

**Load for**: Every security-sensitive code review

**Priority areas** (always check):
- Authentication/authorization code
- User input handling
- Database queries (raw SQL especially)
- File system operations
- Cryptographic operations
- Session management
- API endpoints
- Configuration/secrets handling

---

### `owasp_python.md`

**Purpose**: OWASP Top 10 vulnerabilities specific to Python applications

**Use when**:
- Comprehensive security audit requested
- High-security requirements
- Compliance review (SOC2, ISO27001, etc.)
- Pre-production security check
- Reviewing security-critical features

**OWASP Top 10 Coverage**:
1. **Broken Access Control**: Authorization checks, path traversal, IDOR
2. **Cryptographic Failures**: Weak crypto, plaintext secrets, insecure protocols
3. **Injection**: SQL, command, LDAP, template injection
4. **Insecure Design**: Missing security controls, business logic flaws
5. **Security Misconfiguration**: Debug mode, default credentials, exposed endpoints
6. **Vulnerable Components**: Outdated dependencies, known CVEs
7. **Authentication Failures**: Weak passwords, session issues, credential stuffing
8. **Data Integrity Failures**: Unsigned data, insecure deserialization, untrusted sources
9. **Logging & Monitoring Failures**: Missing logs, insufficient monitoring
10. **Server-Side Request Forgery (SSRF)**: Unvalidated URLs, internal network access

**Load for**: Comprehensive security reviews or when specific OWASP categories apply

---

## Usage Workflow

### Standard Security Review

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
