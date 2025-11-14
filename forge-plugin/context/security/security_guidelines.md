# Python Security Guidelines

This file contains security best practices for Python code review.

## Input Validation and Sanitization

### Never Trust User Input

**Rule**: All external input must be validated, sanitized, and treated as potentially malicious.

```python
# BAD - No validation
def get_user_file(filename):
    with open(f"/data/{filename}") as f:
        return f.read()
# Attack: filename = "../../etc/passwd"

# GOOD - Path validation
from pathlib import Path

def get_user_file(filename):
    base_dir = Path("/data")
    file_path = (base_dir / filename).resolve()

    # Ensure path is within allowed directory
    if not file_path.is_relative_to(base_dir):
        raise ValueError("Invalid file path")

    with open(file_path) as f:
        return f.read()
```

### Type Validation

```python
# BAD - Assumes type
def set_age(age):
    user.age = age  # Could be string, negative, etc.

# GOOD - Explicit validation
def set_age(age: int) -> None:
    if not isinstance(age, int):
        raise TypeError("Age must be an integer")
    if age < 0 or age > 150:
        raise ValueError("Age must be between 0 and 150")
    user.age = age
```

### String Length Limits

```python
# BAD - No length limit
username = request.form['username']
user.username = username  # Could be 1GB string (DoS)

# GOOD - Enforce limits
MAX_USERNAME_LENGTH = 50

username = request.form.get('username', '')
if len(username) > MAX_USERNAME_LENGTH:
    raise ValueError(f"Username too long (max {MAX_USERNAME_LENGTH})")
user.username = username
```

## SQL Injection Prevention

### Always Use Parameterized Queries

```python
# CRITICAL BUG - SQL Injection
email = request.form['email']
cursor.execute(f"SELECT * FROM users WHERE email = '{email}'")

# CORRECT - Parameterized query
email = request.form['email']
cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
```

### ORM Usage

```python
# Django ORM - Safe
from django.db.models import Q

email = request.GET['email']
users = User.objects.filter(email=email)  # Safe - parameterized

# SQLAlchemy - Safe
from sqlalchemy import select

email = request.args['email']
stmt = select(User).where(User.email == email)  # Safe - parameterized

# DANGEROUS - Raw SQL
User.objects.raw(f"SELECT * FROM users WHERE email = '{email}'")  # Vulnerable!
```

### Dynamic Table/Column Names

```python
# When you MUST use dynamic identifiers, use allowlists:
ALLOWED_COLUMNS = {'name', 'email', 'created_at'}

def get_sorted_users(sort_by):
    if sort_by not in ALLOWED_COLUMNS:
        raise ValueError("Invalid sort column")

    # Use identifier quoting
    from psycopg2 import sql
    query = sql.SQL("SELECT * FROM users ORDER BY {}").format(
        sql.Identifier(sort_by)
    )
    cursor.execute(query)
```

## Authentication and Session Management

### Password Storage

```python
# NEVER EVER - Plain text passwords
user.password = request.form['password']  # CRITICAL SECURITY BUG

# BAD - MD5/SHA1 (too fast, no salt)
import hashlib
user.password = hashlib.md5(password.encode()).hexdigest()

# GOOD - bcrypt/argon2
import bcrypt

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt(rounds=12)
    return bcrypt.hashpw(password.encode(), salt).decode()

def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed.encode())
```

### Session Tokens

```python
# BAD - Predictable token
import time
session_token = str(time.time())  # Guessable!

# GOOD - Cryptographically secure random
import secrets

session_token = secrets.token_urlsafe(32)  # 256 bits of entropy
```

### Password Reset Tokens

```python
# BAD - Never expire
reset_token = generate_token()
user.reset_token = reset_token

# GOOD - Time-limited, single-use
from datetime import datetime, timedelta

reset_token = secrets.token_urlsafe(32)
user.reset_token = reset_token
user.reset_token_expires = datetime.utcnow() + timedelta(hours=1)
user.reset_token_used = False
```

## Cryptography

### Use Standard Libraries

```python
# BAD - Custom crypto (never do this)
def my_encrypt(data):
    return ''.join(chr(ord(c) + 13) for c in data)  # Toy cipher!

# GOOD - Use cryptography library
from cryptography.fernet import Fernet

def encrypt_data(data: bytes, key: bytes) -> bytes:
    f = Fernet(key)
    return f.encrypt(data)

def decrypt_data(encrypted: bytes, key: bytes) -> bytes:
    f = Fernet(key)
    return f.decrypt(encrypted)
```

### Key Management

```python
# BAD - Hardcoded keys
ENCRYPTION_KEY = b'my-secret-key-12345'  # NEVER!

# GOOD - Environment variables
import os

ENCRYPTION_KEY = os.environ.get('ENCRYPTION_KEY')
if not ENCRYPTION_KEY:
    raise RuntimeError("ENCRYPTION_KEY must be set")

# BETTER - Key management service (AWS KMS, Azure Key Vault, etc.)
```

### Random Number Generation

```python
# BAD - Predictable randomness for security
import random
token = random.randint(100000, 999999)  # Predictable!

# GOOD - Cryptographically secure
import secrets
token = secrets.randbelow(900000) + 100000
```

## Cross-Site Scripting (XSS)

### Template Auto-Escaping

```python
# Django - Auto-escaping enabled by default
{{ user_input }}  # Automatically escaped

# Flask/Jinja2 - Auto-escaping enabled
{{ user_input }}  # Automatically escaped

# Manual escaping when needed
from markupsafe import escape
safe_output = escape(user_input)
```

### Dangerous Filters

```python
# Django - DANGEROUS
{{ user_input|safe }}  # Never use with user input!

# Flask - DANGEROUS
{{ user_input|safe }}  # Never use with user input!

# Only use |safe with trusted content
{{ admin_generated_html|safe }}  # OK if admin-controlled
```

### Content Security Policy

```python
# Flask example
from flask import Flask, make_response

@app.after_request
def set_csp(response):
    response.headers['Content-Security-Policy'] = (
        "default-src 'self'; "
        "script-src 'self' https://cdn.example.com; "
        "style-src 'self' 'unsafe-inline'"
    )
    return response
```

## XML/JSON Parsing

### XML External Entity (XXE) Prevention

```python
# BAD - Vulnerable to XXE attacks
import xml.etree.ElementTree as ET
tree = ET.parse(user_uploaded_file)  # Dangerous!

# GOOD - Disable external entities
import defusedxml.ElementTree as ET
tree = ET.parse(user_uploaded_file)  # Safe
```

### JSON Parsing

```python
# BAD - eval() on JSON (NEVER DO THIS)
data = eval(request.body)  # Code execution vulnerability!

# GOOD - Use json module
import json
data = json.loads(request.body)

# GOOD - Limit size to prevent DoS
MAX_JSON_SIZE = 1024 * 1024  # 1MB

if len(request.body) > MAX_JSON_SIZE:
    raise ValueError("Payload too large")
data = json.loads(request.body)
```

## File Upload Security

### Filename Sanitization

```python
# BAD - Use uploaded filename directly
filename = uploaded_file.filename
filepath = os.path.join('/uploads', filename)
# Attack: filename = "../../etc/passwd"

# GOOD - Sanitize filename
from werkzeug.utils import secure_filename
import uuid

original_filename = uploaded_file.filename
safe_filename = secure_filename(original_filename)
unique_filename = f"{uuid.uuid4()}_{safe_filename}"
filepath = os.path.join('/uploads', unique_filename)
```

### File Type Validation

```python
# BAD - Trust file extension
if filename.endswith('.jpg'):
    process_image(file)  # Could be malicious PHP file renamed!

# GOOD - Validate magic bytes
import magic

def is_valid_image(file_path):
    mime = magic.from_file(file_path, mime=True)
    allowed_types = {'image/jpeg', 'image/png', 'image/gif'}
    return mime in allowed_types
```

### File Size Limits

```python
# Flask example
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB

# Django example
FILE_UPLOAD_MAX_MEMORY_SIZE = 16 * 1024 * 1024

# Manual validation
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

if uploaded_file.size > MAX_FILE_SIZE:
    raise ValueError("File too large")
```

## Command Injection Prevention

### Never Use shell=True with User Input

```python
# CRITICAL - Command injection
import subprocess
filename = request.form['filename']
subprocess.run(f"cat {filename}", shell=True)  # VULNERABLE!
# Attack: filename = "file.txt; rm -rf /"

# GOOD - Use list arguments, no shell
subprocess.run(['cat', filename], shell=False)

# BETTER - Validate input first
import shlex
safe_filename = shlex.quote(filename)
subprocess.run(['cat', safe_filename])
```

### Path Traversal Prevention

```python
# BAD
file_path = f"/data/{user_input}"
subprocess.run(['process', file_path])

# GOOD
from pathlib import Path

base_dir = Path("/data")
requested_path = (base_dir / user_input).resolve()

if not requested_path.is_relative_to(base_dir):
    raise ValueError("Invalid path")

subprocess.run(['process', str(requested_path)])
```

## Authorization and Access Control

### Never Rely on Client-Side Checks

```python
# BAD - Only client-side check
if request.form.get('is_admin') == 'true':
    delete_all_users()  # Attacker can set is_admin=true!

# GOOD - Server-side authorization
if current_user.is_admin:
    delete_all_users()
else:
    raise PermissionError("Admin access required")
```

### Insecure Direct Object References (IDOR)

```python
# BAD - No ownership check
@app.route('/document/<doc_id>')
def get_document(doc_id):
    doc = Document.query.get(doc_id)
    return doc.content  # Any user can access any document!

# GOOD - Verify ownership
@app.route('/document/<doc_id>')
@login_required
def get_document(doc_id):
    doc = Document.query.get_or_404(doc_id)
    if doc.owner_id != current_user.id:
        abort(403)  # Forbidden
    return doc.content
```

## Deserialization Security

### Pickle is Dangerous

```python
# NEVER - Pickle from untrusted sources
import pickle
data = pickle.loads(untrusted_data)  # Remote code execution!

# GOOD - Use JSON for serialization
import json
data = json.loads(untrusted_data)  # Safe (no code execution)

# If you must use pickle, sign it
import hmac
import pickle

def serialize(obj, secret_key):
    pickled = pickle.dumps(obj)
    signature = hmac.new(secret_key, pickled, 'sha256').hexdigest()
    return pickled + signature.encode()

def deserialize(data, secret_key):
    signature = data[-64:]
    pickled = data[:-64]
    expected_sig = hmac.new(secret_key, pickled, 'sha256').hexdigest()
    if not hmac.compare_digest(signature.decode(), expected_sig):
        raise ValueError("Invalid signature")
    return pickle.loads(pickled)
```

## Server-Side Request Forgery (SSRF)

### URL Validation

```python
# BAD - Fetch arbitrary URLs
import requests
url = request.form['url']
response = requests.get(url)  # Could access internal services!

# GOOD - Validate and restrict URLs
from urllib.parse import urlparse

ALLOWED_DOMAINS = {'api.example.com', 'cdn.example.com'}

def is_safe_url(url):
    parsed = urlparse(url)

    # Block private IPs
    if parsed.hostname in ('localhost', '127.0.0.1', '0.0.0.0'):
        return False

    # Block private networks
    import ipaddress
    try:
        ip = ipaddress.ip_address(parsed.hostname)
        if ip.is_private or ip.is_loopback:
            return False
    except ValueError:
        pass  # Not an IP, check domain

    # Whitelist domains
    if parsed.hostname not in ALLOWED_DOMAINS:
        return False

    return True

url = request.form['url']
if not is_safe_url(url):
    raise ValueError("Invalid URL")
response = requests.get(url, timeout=5)
```

## Logging and Error Handling

### Don't Log Sensitive Data

```python
# BAD - Logs password
logger.info(f"User {username} logged in with password {password}")

# GOOD - Don't log sensitive info
logger.info(f"User {username} logged in")

# BAD - Detailed errors to user
try:
    db.execute(query)
except Exception as e:
    return str(e)  # Exposes DB structure!

# GOOD - Generic error to user, detailed log internally
try:
    db.execute(query)
except Exception as e:
    logger.error(f"Database error: {e}")
    return "An error occurred. Please try again."
```

## Security Headers

### Essential Headers

```python
# Flask example
@app.after_request
def set_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    return response
```

## Secrets Management

### Never Commit Secrets

```python
# BAD - Hardcoded in code
API_KEY = "sk-1234567890abcdef"  # NEVER!
DATABASE_PASSWORD = "super_secret_pass"  # NEVER!

# GOOD - Environment variables
import os

API_KEY = os.environ.get('API_KEY')
if not API_KEY:
    raise RuntimeError("API_KEY environment variable not set")

# BETTER - Secrets manager (AWS Secrets Manager, HashiCorp Vault)
import boto3

def get_secret(secret_name):
    client = boto3.client('secretsmanager')
    response = client.get_secret_value(SecretId=secret_name)
    return response['SecretString']
```

## Rate Limiting

### Prevent Brute Force Attacks

```python
# Flask-Limiter example
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@app.route("/login", methods=["POST"])
@limiter.limit("5 per minute")
def login():
    # Login logic
    pass
```

## Security Testing Tools

Consider using security analysis tools:
- **pip-audit**: Audit Python packages for security issues
- **semgrep**: Static analysis for security patterns

```bash
pip-audit
semgrep --config=auto .
```

## Common Vulnerability Checklist

- [ ] All user input validated and sanitized
- [ ] SQL queries parameterized (no string interpolation)
- [ ] Passwords hashed with bcrypt/argon2
- [ ] Session tokens cryptographically secure
- [ ] No hardcoded secrets or credentials
- [ ] File uploads validated (type, size, filename)
- [ ] Command execution uses list args, not shell=True
- [ ] Authorization checks on all protected resources
- [ ] No pickle deserialization of untrusted data
- [ ] SSRF protection on URL fetching
- [ ] Security headers configured
- [ ] Sensitive data not logged
- [ ] Rate limiting on authentication endpoints
- [ ] Dependencies up to date and vulnerability-free
- [ ] HTTPS enforced (no plain HTTP)

## References

- OWASP Python Security Cheat Sheet
- CWE Top 25 Most Dangerous Software Weaknesses
- Python Security Best Practices
- PEP 543 - A Unified TLS API
