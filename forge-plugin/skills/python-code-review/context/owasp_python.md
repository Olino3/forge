# OWASP Top 10 for Python Applications

This file maps the OWASP Top 10 vulnerabilities to Python-specific implementations and prevention strategies.

## A01:2021 - Broken Access Control

### Description
Failure to properly enforce restrictions on authenticated users, allowing access to unauthorized resources.

### Python Vulnerabilities

**Insecure Direct Object References (IDOR)**:
```python
# VULNERABLE
@app.route('/api/user/<user_id>')
def get_user(user_id):
    user = User.query.get(user_id)
    return jsonify(user.to_dict())  # Any authenticated user can access any profile!

# SECURE
@app.route('/api/user/<user_id>')
@login_required
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    # Check authorization
    if user.id != current_user.id and not current_user.is_admin:
        abort(403, "Access denied")
    return jsonify(user.to_dict())
```

**Missing Function Level Access Control**:
```python
# VULNERABLE
@app.route('/admin/delete-user/<user_id>', methods=['POST'])
def delete_user(user_id):
    User.query.filter_by(id=user_id).delete()
    return "User deleted"

# SECURE
from functools import wraps

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

@app.route('/admin/delete-user/<user_id>', methods=['POST'])
@login_required
@admin_required
def delete_user(user_id):
    User.query.filter_by(id=user_id).delete()
    return "User deleted"
```

### Prevention
- Implement proper authorization checks at every access point
- Use role-based access control (RBAC) or attribute-based access control (ABAC)
- Deny by default
- Test authorization logic thoroughly

---

## A02:2021 - Cryptographic Failures

### Description
Failures related to cryptography which often lead to exposure of sensitive data.

### Python Vulnerabilities

**Weak Password Hashing**:
```python
# VULNERABLE
import hashlib
password_hash = hashlib.md5(password.encode()).hexdigest()  # Too fast, no salt

# VULNERABLE
import hashlib
password_hash = hashlib.sha256(password.encode()).hexdigest()  # Still too fast

# SECURE
import bcrypt

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt(rounds=12)  # Cost factor
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
```

**Insecure Encryption**:
```python
# VULNERABLE - DES is broken
from Crypto.Cipher import DES
cipher = DES.new(key, DES.MODE_ECB)

# SECURE - Use Fernet (AES-128)
from cryptography.fernet import Fernet

key = Fernet.generate_key()
f = Fernet(key)
encrypted = f.encrypt(b"Secret data")
decrypted = f.decrypt(encrypted)
```

**Transmitting Sensitive Data Over HTTP**:
```python
# VULNERABLE
import requests
response = requests.post('http://api.example.com/login', data={'password': pwd})

# SECURE
response = requests.post('https://api.example.com/login', data={'password': pwd})

# Force HTTPS in Flask
from flask_talisman import Talisman
Talisman(app, force_https=True)
```

### Prevention
- Use bcrypt, scrypt, or Argon2 for password hashing
- Use strong encryption algorithms (AES-256, ChaCha20)
- Enforce HTTPS/TLS for all sensitive data transmission
- Never store sensitive data in plain text
- Use proper key management (HSM, key vaults)

---

## A03:2021 - Injection

### Description
Application is vulnerable when user data is not validated, filtered, or sanitized.

### Python Vulnerabilities

**SQL Injection**:
```python
# VULNERABLE
email = request.form['email']
cursor.execute(f"SELECT * FROM users WHERE email = '{email}'")

# SECURE - Parameterized query
cursor.execute("SELECT * FROM users WHERE email = %s", (email,))

# SECURE - ORM
user = User.query.filter_by(email=email).first()
```

**Command Injection**:
```python
# VULNERABLE
import subprocess
filename = request.args['file']
subprocess.run(f"cat {filename}", shell=True)  # CRITICAL

# SECURE
subprocess.run(['cat', filename], shell=False)

# BETTER - Validate input
import shlex
safe_filename = shlex.quote(filename)
subprocess.run(['cat', safe_filename])
```

**NoSQL Injection (MongoDB)**:
```python
# VULNERABLE
from pymongo import MongoClient
username = request.json['username']
password = request.json['password']
user = db.users.find_one({'username': username, 'password': password})
# Attack: {"username": {"$ne": null}, "password": {"$ne": null}}

# SECURE - Type validation
if not isinstance(username, str) or not isinstance(password, str):
    abort(400, "Invalid input")
user = db.users.find_one({'username': username, 'password': password})
```

**LDAP Injection**:
```python
# VULNERABLE
import ldap
username = request.form['username']
search_filter = f"(uid={username})"
# Attack: username = "*)(uid=*))(|(uid=*"

# SECURE - Escape special characters
import ldap.filter
username = ldap.filter.escape_filter_chars(request.form['username'])
search_filter = f"(uid={username})"
```

### Prevention
- Use parameterized queries / prepared statements
- Use ORM/ODM properly (avoid raw queries)
- Validate and sanitize all user input
- Use allowlists for acceptable inputs
- Escape special characters when building queries

---

## A04:2021 - Insecure Design

### Description
Missing or ineffective security controls in the design phase.

### Python Examples

**Missing Rate Limiting**:
```python
# VULNERABLE - No rate limiting on auth
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    if authenticate(username, password):
        return "Success"
    return "Failed"

# SECURE
from flask_limiter import Limiter
limiter = Limiter(app, key_func=get_remote_address)

@app.route('/login', methods=['POST'])
@limiter.limit("5 per minute")
def login():
    username = request.form['username']
    password = request.form['password']
    if authenticate(username, password):
        return "Success"
    return "Failed"
```

**Lack of Account Lockout**:
```python
# SECURE - Implement account lockout
from datetime import datetime, timedelta

def authenticate(username, password):
    user = User.query.filter_by(username=username).first()

    if user.locked_until and datetime.utcnow() < user.locked_until:
        return False, "Account locked"

    if not verify_password(password, user.password_hash):
        user.failed_attempts += 1
        if user.failed_attempts >= 5:
            user.locked_until = datetime.utcnow() + timedelta(minutes=30)
        db.session.commit()
        return False, "Invalid credentials"

    # Reset on successful login
    user.failed_attempts = 0
    user.locked_until = None
    db.session.commit()
    return True, "Success"
```

### Prevention
- Threat modeling during design phase
- Secure design patterns and principles
- Defense in depth
- Principle of least privilege
- Fail securely

---

## A05:2021 - Security Misconfiguration

### Description
Missing hardening, default configurations, verbose error messages.

### Python Vulnerabilities

**Debug Mode in Production**:
```python
# VULNERABLE
app = Flask(__name__)
app.config['DEBUG'] = True  # NEVER in production!
# Exposes source code, stack traces, environment variables

# SECURE
import os
app.config['DEBUG'] = os.environ.get('FLASK_ENV') == 'development'
```

**Verbose Error Messages**:
```python
# VULNERABLE
@app.errorhandler(500)
def internal_error(error):
    return str(error), 500  # Exposes stack traces!

# SECURE
@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Internal error: {error}")
    return "An internal error occurred", 500
```

**Default Credentials**:
```python
# VULNERABLE
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'admin'  # Default password!

# SECURE
ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME')
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD')
if not ADMIN_USERNAME or not ADMIN_PASSWORD:
    raise RuntimeError("Admin credentials not configured")
```

**Missing Security Headers**:
```python
# SECURE
from flask_talisman import Talisman

csp = {
    'default-src': "'self'",
    'script-src': ["'self'", 'https://cdn.example.com'],
    'style-src': ["'self'", "'unsafe-inline'"],
}

Talisman(app,
    force_https=True,
    strict_transport_security=True,
    content_security_policy=csp,
    x_content_type_options=True,
    x_frame_options='SAMEORIGIN'
)
```

### Prevention
- Disable debug mode in production
- Remove or secure development features
- Use minimal, hardened configurations
- Implement proper error handling
- Keep frameworks and dependencies updated
- Configure security headers

---

## A06:2021 - Vulnerable and Outdated Components

### Description
Using components with known vulnerabilities.

### Python Prevention

**Dependency Scanning**:
```bash
# Check for vulnerable dependencies
pip-audit

# Keep dependencies updated
pip list --outdated
pip install --upgrade package-name
```

**Pin Dependencies**:
```python
# requirements.txt - Pin exact versions
Flask==2.3.2
requests==2.31.0
cryptography==41.0.3

# Or use version ranges carefully
Flask>=2.3.0,<3.0.0
```

**Automated Updates**:
```yaml
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 10
```

### Prevention
- Inventory all components and versions
- Regularly scan for vulnerabilities (pip-audit)
- Remove unused dependencies
- Only obtain components from official sources
- Monitor for security advisories

---

## A07:2021 - Identification and Authentication Failures

### Description
Weak authentication and session management.

### Python Vulnerabilities

**Weak Password Policy**:
```python
# VULNERABLE
def register(username, password):
    if len(password) < 6:  # Too weak!
        return "Password too short"
    create_user(username, password)

# SECURE
import re

def validate_password(password):
    if len(password) < 12:
        return False, "Password must be at least 12 characters"
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain uppercase letter"
    if not re.search(r'[a-z]', password):
        return False, "Password must contain lowercase letter"
    if not re.search(r'[0-9]', password):
        return False, "Password must contain digit"
    if not re.search(r'[!@#$%^&*]', password):
        return False, "Password must contain special character"
    return True, "Valid"
```

**Session Fixation**:
```python
# VULNERABLE
@app.route('/login', methods=['POST'])
def login():
    if authenticate(request.form['username'], request.form['password']):
        session['user_id'] = user.id  # Doesn't regenerate session ID!
        return "Success"

# SECURE
from flask import session
import secrets

@app.route('/login', methods=['POST'])
def login():
    if authenticate(request.form['username'], request.form['password']):
        # Regenerate session ID
        session.clear()
        session.regenerate()
        session['user_id'] = user.id
        return "Success"
```

**Permitting Brute Force**:
```python
# See rate limiting examples in A04
```

### Prevention
- Implement multi-factor authentication (MFA)
- Strong password requirements
- Account lockout mechanisms
- Session ID regeneration on login
- Secure session management
- No credential stuffing vulnerabilities

---

## A08:2021 - Software and Data Integrity Failures

### Description
Failures related to code and infrastructure that don't protect against integrity violations.

### Python Vulnerabilities

**Unsafe Deserialization**:
```python
# VULNERABLE - Pickle allows arbitrary code execution
import pickle
data = pickle.loads(untrusted_input)  # CRITICAL!

# SECURE - Use JSON
import json
data = json.loads(untrusted_input)  # Safe

# If pickle needed, sign the data
import hmac
import hashlib

SECRET_KEY = b'your-secret-key'

def safe_pickle_dumps(obj):
    pickled = pickle.dumps(obj)
    signature = hmac.new(SECRET_KEY, pickled, hashlib.sha256).digest()
    return signature + pickled

def safe_pickle_loads(data):
    signature = data[:32]
    pickled = data[32:]
    expected = hmac.new(SECRET_KEY, pickled, hashlib.sha256).digest()
    if not hmac.compare_digest(signature, expected):
        raise ValueError("Invalid signature")
    return pickle.loads(pickled)
```

**Unsigned Package Installation**:
```bash
# VULNERABLE
pip install package-name --trusted-host pypi.org

# SECURE
pip install package-name  # Verifies signatures by default
pip install --require-hashes -r requirements.txt
```

### Prevention
- Use digital signatures for critical operations
- Don't deserialize untrusted data with pickle/PyYAML unsafe loader
- Verify integrity of downloaded packages
- Use code signing
- Implement CI/CD pipeline security

---

## A09:2021 - Security Logging and Monitoring Failures

### Description
Insufficient logging and monitoring that prevents detecting breaches.

### Python Implementation

**Proper Logging**:
```python
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('security.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Log security events
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    if authenticate(username, password):
        logger.info(f"Successful login for user: {username} from IP: {request.remote_addr}")
        return "Success"
    else:
        logger.warning(f"Failed login attempt for user: {username} from IP: {request.remote_addr}")
        return "Failed"

# Log unauthorized access attempts
@app.route('/admin/panel')
@login_required
def admin_panel():
    if not current_user.is_admin:
        logger.warning(f"Unauthorized access attempt to /admin/panel by user: {current_user.username}")
        abort(403)
    return render_template('admin.html')
```

**Events to Log**:
```python
# Authentication events
logger.info(f"User {username} logged in")
logger.warning(f"Failed login for {username}")
logger.info(f"User {username} logged out")
logger.warning(f"Account locked: {username}")

# Authorization events
logger.warning(f"Unauthorized access attempt: {username} to {resource}")
logger.info(f"Permission granted: {username} to {resource}")

# Input validation failures
logger.warning(f"Invalid input detected: {input_type} from {request.remote_addr}")

# Critical operations
logger.info(f"User {username} deleted by admin {admin_username}")
logger.info(f"Configuration changed by {username}")
```

### Prevention
- Log all authentication/authorization events
- Log input validation failures
- Use structured logging (JSON format)
- Ensure logs are tamper-proof
- Implement alerting for suspicious patterns
- Don't log sensitive data (passwords, tokens, PII)

---

## A10:2021 - Server-Side Request Forgery (SSRF)

### Description
Web application fetching remote resources without validating user-supplied URL.

### Python Vulnerabilities

**Unvalidated URL Fetching**:
```python
# VULNERABLE
import requests
url = request.args['url']
response = requests.get(url)  # Could access internal services!
# Attack: url = "http://localhost:6379/" (Redis), "http://169.254.169.254/latest/meta-data/" (AWS metadata)

# SECURE
from urllib.parse import urlparse
import ipaddress

ALLOWED_DOMAINS = {'api.example.com', 'cdn.example.com'}

def is_safe_url(url):
    parsed = urlparse(url)

    # Require HTTPS
    if parsed.scheme != 'https':
        return False

    # Block localhost and loopback
    if parsed.hostname in ('localhost', '127.0.0.1', '::1'):
        return False

    # Block private IP ranges
    try:
        ip = ipaddress.ip_address(parsed.hostname)
        if ip.is_private or ip.is_loopback or ip.is_link_local:
            return False
    except ValueError:
        pass  # Not an IP address

    # Whitelist domains
    if parsed.hostname not in ALLOWED_DOMAINS:
        return False

    return True

url = request.args['url']
if not is_safe_url(url):
    abort(400, "Invalid URL")

response = requests.get(url, timeout=5, allow_redirects=False)
```

**File URL Scheme**:
```python
# VULNERABLE
url = request.args['url']
response = requests.get(url)
# Attack: url = "file:///etc/passwd"

# SECURE
parsed = urlparse(url)
if parsed.scheme not in ('http', 'https'):
    abort(400, "Invalid URL scheme")
```

### Prevention
- Validate and sanitize all user-supplied URLs
- Use allowlists for domains/IP addresses
- Block private IP ranges and cloud metadata endpoints
- Disable redirects or validate redirect targets
- Network segmentation
- Implement response size limits

---

## Security Checklist for Python Code Review

### Authentication & Authorization
- [ ] Strong password policy enforced
- [ ] Passwords hashed with bcrypt/argon2 (not MD5/SHA)
- [ ] Multi-factor authentication available
- [ ] Session IDs regenerated on login
- [ ] Authorization checks on all protected resources
- [ ] No IDOR vulnerabilities

### Injection Prevention
- [ ] All SQL queries parameterized
- [ ] No command injection (shell=False)
- [ ] Input validation on all user input
- [ ] Output encoding/escaping for XSS prevention

### Cryptography
- [ ] HTTPS/TLS enforced
- [ ] Strong encryption algorithms (AES-256)
- [ ] Secrets not hardcoded
- [ ] Secure random number generation (secrets module)

### Configuration
- [ ] Debug mode disabled in production
- [ ] Error messages don't expose sensitive info
- [ ] Security headers configured
- [ ] Dependencies up to date

### Data Protection
- [ ] Sensitive data encrypted at rest
- [ ] Sensitive data encrypted in transit
- [ ] No sensitive data in logs
- [ ] Secure session configuration

### Application Logic
- [ ] Rate limiting on authentication
- [ ] Account lockout implemented
- [ ] CSRF protection enabled
- [ ] File uploads validated and restricted
- [ ] SSRF protection on URL fetching

### Logging & Monitoring
- [ ] Security events logged
- [ ] Logs don't contain sensitive data
- [ ] Alerting configured for suspicious activity

## References

- OWASP Top 10 2021: https://owasp.org/Top10/
- OWASP Python Security: https://owasp.org/www-project-python-security/
- OWASP Cheat Sheet Series: https://cheatsheetseries.owasp.org/
- CWE Top 25: https://cwe.mitre.org/top25/
