# Secure Code Examples

This file contains example security hardening scenarios demonstrating common vulnerabilities and their remediation.

## Example 1: Hardening a REST API

Securing a Node.js/Express API against OWASP Top 10 vulnerabilities including input validation, authentication, and rate limiting.

### User Prompt

> "Review my Express API for security vulnerabilities. It handles user registration and data retrieval."

### Skill Execution

1. **Identify Security Scope**: REST API with `/api/users` endpoints — trust boundary at HTTP layer, user input via request body and query params, data flows from client through Express middleware to MongoDB
2. **Load Memory & Context**: `memoryStore.getSkillMemory("secure-code", "user-api")` — no prior memory; cross-skill check reveals schema analysis with user collection details
3. **Load Relevant Context**: Loaded `security_guidelines.md` (always), Node.js security patterns (conditional), API security and injection prevention (cross-domain triggers: API endpoints + database queries)
4. **Security Analysis**: Found 4 findings — NoSQL injection (Critical/A03), missing rate limiting (High/A04), excessive data exposure (High/A01), missing input validation (Medium/A03)
5. **Generate Secure Code & Update Memory**: Produced hardened code, saved report to `/claudedocs/secure-code_user-api_2026-02-12.md`, updated `memoryStore` with security profile and findings

### Before (Vulnerable Code)

```javascript
// routes/users.js
const express = require('express');
const router = express.Router();
const User = require('../models/User');

// User registration
router.post('/api/users', async (req, res) => {
  const user = new User(req.body);
  await user.save();
  res.json(user);
});

// User lookup
router.get('/api/users', async (req, res) => {
  const users = await User.find(req.query);
  res.json(users);
});

// User login
router.post('/api/login', async (req, res) => {
  const user = await User.findOne({
    email: req.body.email,
    password: req.body.password
  });
  if (user) {
    res.json({ token: user._id, user: user });
  } else {
    res.status(401).json({ error: 'Invalid credentials' });
  }
});

module.exports = router;
```

### Secure Code Output

**Finding 1 — NoSQL Injection via Query Parameters**
**Severity**: Critical | **OWASP**: A03 Injection
**Attack Scenario**: Attacker sends `GET /api/users?role[$ne]=null` to dump all users via MongoDB operator injection.

**Finding 2 — Missing Rate Limiting**
**Severity**: High | **OWASP**: A04 Insecure Design
**Attack Scenario**: Attacker brute-forces `/api/login` with credential stuffing at thousands of requests per second.

**Finding 3 — Excessive Data Exposure**
**Severity**: High | **OWASP**: A01 Broken Access Control
**Attack Scenario**: Login response returns the full user object including password hash, internal IDs, and PII.

**Finding 4 — Missing Input Validation**
**Severity**: Medium | **OWASP**: A03 Injection
**Attack Scenario**: Attacker submits arbitrary fields in `req.body` during registration, setting `role: "admin"` via mass assignment.

```javascript
// routes/users.js
const express = require('express');
const router = express.Router();
const rateLimit = require('express-rate-limit');
const { body, query, validationResult } = require('express-validator');
const bcrypt = require('bcrypt');
const jwt = require('jsonwebtoken');
const User = require('../models/User');

// Rate limiting for auth endpoints
const loginLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 10,
  message: { error: 'Too many login attempts, please try again later' }
});

// User registration — validate and sanitize input, hash password
router.post('/api/users', [
  body('email').isEmail().normalizeEmail(),
  body('password').isLength({ min: 12 }).matches(/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)/),
  body('name').trim().escape().isLength({ min: 1, max: 100 })
], async (req, res) => {
  const errors = validationResult(req);
  if (!errors.isEmpty()) {
    return res.status(400).json({ errors: errors.array() });
  }
  // Whitelist allowed fields to prevent mass assignment
  const { email, password, name } = req.body;
  const hashedPassword = await bcrypt.hash(password, 12);
  const user = new User({ email, password: hashedPassword, name });
  await user.save();
  // Return only safe fields
  res.status(201).json({ id: user._id, email: user.email, name: user.name });
});

// User lookup — sanitize query to prevent NoSQL injection
router.get('/api/users', [
  query('email').optional().isEmail().normalizeEmail(),
  query('name').optional().trim().escape()
], async (req, res) => {
  const errors = validationResult(req);
  if (!errors.isEmpty()) {
    return res.status(400).json({ errors: errors.array() });
  }
  // Build safe filter from validated params only
  const filter = {};
  if (req.query.email) filter.email = String(req.query.email);
  if (req.query.name) filter.name = String(req.query.name);
  const users = await User.find(filter).select('email name -_id');
  res.json(users);
});

// User login — rate limited, bcrypt comparison, JWT token
router.post('/api/login', loginLimiter, [
  body('email').isEmail().normalizeEmail(),
  body('password').notEmpty()
], async (req, res) => {
  const errors = validationResult(req);
  if (!errors.isEmpty()) {
    return res.status(400).json({ errors: errors.array() });
  }
  const user = await User.findOne({ email: req.body.email });
  if (!user || !(await bcrypt.compare(req.body.password, user.password))) {
    // Generic message prevents user enumeration
    return res.status(401).json({ error: 'Invalid email or password' });
  }
  const token = jwt.sign({ sub: user._id }, process.env.JWT_SECRET, { expiresIn: '1h' });
  res.json({ token });
});

module.exports = router;
```

**References**: [OWASP API Security Top 10](https://owasp.org/www-project-api-security/), [CWE-943: NoSQL Injection](https://cwe.mitre.org/data/definitions/943.html)

---

## Example 2: Secure File Upload Implementation

Preventing path traversal, validating file types, and enforcing size limits in a Python/Flask application.

### User Prompt

> "I need to add file upload to our Flask app. Make sure it's secure."

### Skill Execution

1. **Identify Security Scope**: File upload endpoint — trust boundary at multipart form data, data flows from client upload through filesystem write, entry point is `/upload` POST route
2. **Load Memory & Context**: `memoryStore.getSkillMemory("secure-code", "flask-app")` — found prior memory with Flask patterns; cross-skill discovery found code review noting missing CSRF protection
3. **Load Relevant Context**: Loaded `security_guidelines.md` (always), `owasp_python.md` and Flask security patterns (conditional), file operation and path traversal patterns (cross-domain trigger: file operations)
4. **Security Analysis**: Found 5 findings — path traversal (Critical/A01), unrestricted file type (High/A04), no size limit (Medium/A04), missing virus scan (Medium/A04), insecure filename in response (Low/A05)
5. **Generate Secure Code & Update Memory**: Produced hardened upload handler, saved report to `/claudedocs/secure-code_flask-app_2026-02-12.md`, updated `memoryStore` with file upload security patterns

### Before (Vulnerable Code)

```python
# app.py
import os
from flask import Flask, request, jsonify

app = Flask(__name__)
UPLOAD_DIR = "/var/uploads"

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    filepath = os.path.join(UPLOAD_DIR, file.filename)
    file.save(filepath)
    return jsonify({"path": filepath})
```

### Secure Code Output

**Finding 1 — Path Traversal via Filename**
**Severity**: Critical | **OWASP**: A01 Broken Access Control
**Attack Scenario**: Attacker uploads file with name `../../../etc/cron.d/backdoor` to write arbitrary files outside the upload directory.

**Finding 2 — Unrestricted File Type**
**Severity**: High | **OWASP**: A04 Insecure Design
**Attack Scenario**: Attacker uploads `.php`, `.jsp`, or `.py` file that the web server may execute if misconfigured.

**Finding 3 — No File Size Limit**
**Severity**: Medium | **OWASP**: A04 Insecure Design
**Attack Scenario**: Attacker uploads multi-gigabyte file causing disk exhaustion and denial of service.

```python
# app.py
import os
import uuid
import hashlib
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10 MB limit

UPLOAD_DIR = "/var/uploads"
ALLOWED_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.gif', '.pdf', '.txt'}
# Magic bytes for file type validation
MAGIC_BYTES = {
    '.png': b'\x89PNG',
    '.jpg': b'\xff\xd8\xff',
    '.jpeg': b'\xff\xd8\xff',
    '.gif': b'GIF8',
    '.pdf': b'%PDF',
}

def validate_file_type(file_stream, extension):
    """Validate file content matches its declared extension via magic bytes."""
    header = file_stream.read(8)
    file_stream.seek(0)
    if extension in MAGIC_BYTES:
        return header.startswith(MAGIC_BYTES[extension])
    return True  # Allow extensions without magic byte checks (e.g., .txt)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files['file']
    if not file.filename:
        return jsonify({"error": "Empty filename"}), 400

    # Sanitize filename and validate extension
    safe_name = secure_filename(file.filename)
    _, ext = os.path.splitext(safe_name)
    ext = ext.lower()

    if ext not in ALLOWED_EXTENSIONS:
        return jsonify({"error": f"File type '{ext}' not allowed"}), 400

    # Validate file content matches extension
    if not validate_file_type(file.stream, ext):
        return jsonify({"error": "File content does not match extension"}), 400

    # Generate unique filename to prevent overwrites and info leakage
    unique_name = f"{uuid.uuid4().hex}{ext}"
    filepath = os.path.join(UPLOAD_DIR, unique_name)

    # Verify resolved path is within upload directory
    real_upload_dir = os.path.realpath(UPLOAD_DIR)
    real_filepath = os.path.realpath(filepath)
    if not real_filepath.startswith(real_upload_dir + os.sep):
        return jsonify({"error": "Invalid file path"}), 400

    file.save(filepath)

    # Return safe identifier, not internal path
    file_hash = hashlib.sha256(open(filepath, 'rb').read()).hexdigest()
    return jsonify({"id": unique_name, "hash": file_hash}), 201
```

**References**: [OWASP File Upload Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html), [CWE-22: Path Traversal](https://cwe.mitre.org/data/definitions/22.html)

---

## Example 3: Secrets Management Migration

Moving from hardcoded credentials to environment variables and vault integration.

### User Prompt

> "Our app has database passwords and API keys hardcoded in the config file. Help us move to proper secrets management."

### Skill Execution

1. **Identify Security Scope**: Application configuration — trust boundary at config files and environment, data flows from config through connection setup to external services, entry points are all modules importing config
2. **Load Memory & Context**: `memoryStore.getSkillMemory("secure-code", "backend-service")` — found prior memory noting three external service integrations; cross-skill discovery found dependency audit flagging outdated database driver
3. **Load Relevant Context**: Loaded `security_guidelines.md` (always), secrets management and crypto patterns (conditional on secrets management concern), environment isolation patterns (cross-domain trigger: credential storage)
4. **Security Analysis**: Found 4 findings — hardcoded database password (Critical/A02), API key in source code (Critical/A02), secrets in git history (High/A05), no credential rotation (Medium/A04)
5. **Generate Secure Code & Update Memory**: Produced vault-integrated config module, saved report to `/claudedocs/secure-code_backend-service_2026-02-12.md`, updated `memoryStore` with secrets management patterns

### Before (Vulnerable Code)

```python
# config.py
DATABASE_CONFIG = {
    "host": "prod-db.internal.company.com",
    "port": 5432,
    "database": "app_production",
    "user": "admin",
    "password": "SuperSecret123!",
}

STRIPE_API_KEY = "sk_live_abc123def456ghi789"
SENDGRID_KEY = "SG.xxxxxxxxxxxxxxxxxxxx"

AWS_ACCESS_KEY = "AKIAIOSFODNN7EXAMPLE"
AWS_SECRET_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
```

### Secure Code Output

**Finding 1 — Hardcoded Database Password**
**Severity**: Critical | **OWASP**: A02 Cryptographic Failures
**Attack Scenario**: Anyone with read access to the repository (including CI logs, backup tapes, or leaked source code) gains direct production database access.

**Finding 2 — API Keys in Source Code**
**Severity**: Critical | **OWASP**: A02 Cryptographic Failures
**Attack Scenario**: Leaked Stripe live key allows attacker to process fraudulent charges; AWS keys grant full account access.

**Finding 3 — Secrets in Git History**
**Severity**: High | **OWASP**: A05 Security Misconfiguration
**Attack Scenario**: Even after removing secrets from code, `git log` exposes every credential ever committed. Attackers routinely scan public repos for this.

**Finding 4 — No Credential Rotation**
**Severity**: Medium | **OWASP**: A04 Insecure Design
**Attack Scenario**: Compromised credentials remain valid indefinitely without rotation, extending the window of exploitation.

**Phase 1: Environment Variables (Immediate Fix)**

```python
# config.py — Phase 1: Environment variables with validation
import os
import sys

def _require_env(name):
    """Retrieve required environment variable or fail fast at startup."""
    value = os.environ.get(name)
    if not value:
        print(f"FATAL: Required environment variable '{name}' is not set.", file=sys.stderr)
        sys.exit(1)
    return value

DATABASE_CONFIG = {
    "host": _require_env("DB_HOST"),
    "port": int(os.environ.get("DB_PORT", "5432")),
    "database": _require_env("DB_NAME"),
    "user": _require_env("DB_USER"),
    "password": _require_env("DB_PASSWORD"),
}

STRIPE_API_KEY = _require_env("STRIPE_API_KEY")
SENDGRID_KEY = _require_env("SENDGRID_KEY")

# AWS credentials should use IAM roles, not access keys
# If keys are unavoidable, load from environment
AWS_ACCESS_KEY = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
```

**Phase 2: Vault Integration (Production Hardening)**

```python
# config.py — Phase 2: HashiCorp Vault integration with caching and rotation
import os
import sys
import time
import hvac

class SecretsManager:
    """Centralized secrets access with vault integration and TTL-based caching."""

    def __init__(self):
        self._cache = {}
        self._client = None

    def _get_vault_client(self):
        if self._client is None:
            vault_addr = os.environ.get("VAULT_ADDR", "https://vault.internal.company.com:8200")
            vault_token = os.environ.get("VAULT_TOKEN")
            if not vault_token:
                # Fall back to Kubernetes auth or AppRole in production
                self._client = hvac.Client(url=vault_addr)
                role_id = os.environ.get("VAULT_ROLE_ID")
                secret_id = os.environ.get("VAULT_SECRET_ID")
                self._client.auth.approle.login(role_id=role_id, secret_id=secret_id)
            else:
                self._client = hvac.Client(url=vault_addr, token=vault_token)
        return self._client

    def get_secret(self, path, key, ttl=300):
        """Retrieve a secret from vault with TTL-based caching."""
        cache_key = f"{path}/{key}"
        cached = self._cache.get(cache_key)
        if cached and time.time() - cached["fetched_at"] < ttl:
            return cached["value"]

        client = self._get_vault_client()
        response = client.secrets.kv.v2.read_secret_version(path=path)
        value = response["data"]["data"][key]
        self._cache[cache_key] = {"value": value, "fetched_at": time.time()}
        return value

secrets = SecretsManager()

DATABASE_CONFIG = {
    "host": secrets.get_secret("database/prod", "host"),
    "port": int(secrets.get_secret("database/prod", "port")),
    "database": secrets.get_secret("database/prod", "name"),
    "user": secrets.get_secret("database/prod", "user"),
    "password": secrets.get_secret("database/prod", "password"),
}

STRIPE_API_KEY = secrets.get_secret("payments/stripe", "api_key")
SENDGRID_KEY = secrets.get_secret("email/sendgrid", "api_key")
```

**Remediation Steps**:

1. **Immediately rotate all exposed credentials** — database password, Stripe key, SendGrid key, AWS keys
2. Add `config.py` patterns to `.gitignore` and use `git filter-repo` to purge secrets from git history
3. Deploy Phase 1 (environment variables) as an immediate fix
4. Set up HashiCorp Vault (or AWS Secrets Manager / Azure Key Vault) for Phase 2
5. Configure automated credential rotation policies (90-day maximum)
6. Add pre-commit hooks (e.g., `detect-secrets`, `gitleaks`) to prevent future secret commits

**References**: [OWASP Secrets Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html), [CWE-798: Hardcoded Credentials](https://cwe.mitre.org/data/definitions/798.html)
