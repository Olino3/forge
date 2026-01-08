# Tutorial 12: Secrets Management and Security Best Practices

## Overview

Handling secrets (API keys, passwords, database credentials) securely is critical for professional applications. This tutorial covers environment variables, secrets management, and security best practices in Ruby applications, with special focus on preventing common vulnerabilities.

## Python Comparison

Security concepts are **universal**, but implementation details differ:

| Concept | Ruby | Python |
|---------|------|--------|
| Environment Variables | ENV, dotenv gem | os.environ, python-dotenv |
| Secrets Encryption | Rails credentials, Vault | django-environ, Vault |
| Password Hashing | bcrypt gem | bcrypt, passlib |
| CSRF Protection | Rails built-in | Django built-in |
| SQL Injection | ActiveRecord escapes | Django ORM escapes |

## 1. Environment Variables

### The Problem: Hardcoded Secrets

```ruby
# BAD - Never hardcode secrets!
class ApiClient
  API_KEY = "sk_live_abc123xyz789"  # Exposed in source control!
  DATABASE_URL = "postgres://user:password@localhost/db"
  
  def connect
    # ...
  end
end
```

**Never commit secrets to version control!**

**Python comparison:**
```python
# BAD - Same problem
API_KEY = "sk_live_abc123xyz789"  # Don't do this!
```

### The Solution: Environment Variables

```ruby
# GOOD - Use environment variables
class ApiClient
  API_KEY = ENV['API_KEY']
  DATABASE_URL = ENV['DATABASE_URL']
  
  def connect
    raise 'API_KEY not set' if API_KEY.nil?
    # ...
  end
end
```

**Python comparison:**
```python
import os

API_KEY = os.environ['API_KEY']
DATABASE_URL = os.environ['DATABASE_URL']
```

### Using dotenv for Development

```ruby
# Gemfile
group :development, :test do
  gem 'dotenv-rails'
end
```

Create `.env` file:
```bash
# .env (NEVER commit this file!)
API_KEY=sk_test_abc123
DATABASE_URL=postgres://localhost/myapp_development
STRIPE_SECRET_KEY=sk_test_xyz789
AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
REDIS_URL=redis://localhost:6379/0
```

Add to `.gitignore`:
```bash
# .gitignore
.env
.env.local
.env.*.local
```

Load environment variables:
```ruby
# config/application.rb (Rails)
require 'dotenv/load' if Rails.env.development? || Rails.env.test?

# Or for non-Rails
require 'dotenv/load'
```

**Python comparison:**
```python
# pip install python-dotenv
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv('API_KEY')
```

### Environment-Specific Configuration

```bash
# .env.development
DATABASE_URL=postgres://localhost/myapp_development
API_ENDPOINT=https://api.staging.example.com

# .env.production
DATABASE_URL=postgres://prod-server/myapp_production
API_ENDPOINT=https://api.example.com

# .env.test
DATABASE_URL=postgres://localhost/myapp_test
API_ENDPOINT=https://api.test.example.com
```

### Accessing ENV Variables

```ruby
# Basic access
api_key = ENV['API_KEY']

# With fallback
port = ENV['PORT'] || 3000

# With fetch (raises if not found)
api_key = ENV.fetch('API_KEY')

# With fetch and default
timeout = ENV.fetch('TIMEOUT', '30')

# Parse integers
max_threads = ENV.fetch('MAX_THREADS', '5').to_i

# Parse booleans
debug = ENV.fetch('DEBUG', 'false') == 'true'

# Parse arrays
allowed_hosts = ENV.fetch('ALLOWED_HOSTS', '').split(',')
```

## 2. Rails Encrypted Credentials

Rails 5.2+ includes encrypted credentials:

```bash
# Edit credentials (opens in $EDITOR)
rails credentials:edit

# For specific environment
rails credentials:edit --environment production
```

Credentials file:
```yaml
# config/credentials.yml.enc (encrypted)
secret_key_base: abc123...
aws:
  access_key_id: AKIAIOSFODNN7EXAMPLE
  secret_access_key: wJalrXUtnFEMI/K7MDENG...
stripe:
  publishable_key: pk_live_abc123
  secret_key: sk_live_xyz789
database:
  password: supersecretpassword
```

Accessing credentials:
```ruby
# Access nested values
Rails.application.credentials.aws[:access_key_id]
Rails.application.credentials.stripe[:secret_key]

# Dig for deep nesting
Rails.application.credentials.dig(:aws, :access_key_id)

# In configuration
config.stripe_secret_key = Rails.application.credentials.stripe[:secret_key]
```

**Master key:**
- Stored in `config/master.key`
- **Never commit master.key!** (already in .gitignore)
- Deploy by setting `RAILS_MASTER_KEY` environment variable

**Python (Django) comparison:**
```python
# Django doesn't have built-in encryption
# Use django-environ or django-encrypted-secrets

from environ import Env
env = Env()

AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
```

## 3. HashiCorp Vault

For enterprise-grade secrets management:

```ruby
# Gemfile
gem 'vault'

# config/initializers/vault.rb
require 'vault'

Vault.configure do |config|
  config.address = ENV['VAULT_ADDR']
  config.token = ENV['VAULT_TOKEN']
end

# Usage
secret = Vault.logical.read('secret/data/myapp')
db_password = secret.data[:data][:db_password]

# Write secret
Vault.logical.write('secret/data/myapp', data: {
  db_password: 'newpassword'
})
```

**Python comparison:**
```python
import hvac

client = hvac.Client(url=os.environ['VAULT_ADDR'])
client.token = os.environ['VAULT_TOKEN']

secret = client.secrets.kv.v2.read_secret_version(path='myapp')
db_password = secret['data']['data']['db_password']
```

## 4. Password Security

### Hashing Passwords with bcrypt

```ruby
# Gemfile
gem 'bcrypt'

# User model
class User < ApplicationRecord
  has_secure_password  # Rails magic!
  
  # Requires 'password_digest' column in database
end

# Usage
user = User.create(
  email: 'alice@example.com',
  password: 'secure_password_123',
  password_confirmation: 'secure_password_123'
)

# Authentication
user.authenticate('secure_password_123')  # => user object
user.authenticate('wrong_password')       # => false
```

Under the hood:
```ruby
require 'bcrypt'

# Hashing
password = 'mysecretpassword'
password_hash = BCrypt::Password.create(password)
# => "$2a$12$abc..."

# Verifying
password_hash == 'mysecretpassword'  # => true
password_hash == 'wrongpassword'     # => false

# Cost factor (higher = more secure but slower)
password_hash = BCrypt::Password.create(password, cost: 12)
```

**Python comparison:**
```python
import bcrypt

# Hashing
password = b"mysecretpassword"
password_hash = bcrypt.hashpw(password, bcrypt.gensalt())

# Verifying
bcrypt.checkpw(password, password_hash)  # True
```

### Password Strength Validation

```ruby
class User < ApplicationRecord
  validates :password, 
    length: { minimum: 12 },
    format: {
      with: /\A(?=.*[a-z])(?=.*[A-Z])(?=.*\d)/,
      message: 'must include uppercase, lowercase, and number'
    },
    if: :password_required?

  validate :password_complexity

  private

  def password_complexity
    return if password.blank?
    
    if password.length < 12
      errors.add :password, 'must be at least 12 characters'
    end
    
    unless password.match?(/[a-z]/) && password.match?(/[A-Z]/)
      errors.add :password, 'must include both upper and lower case'
    end
    
    unless password.match?(/\d/)
      errors.add :password, 'must include at least one number'
    end
    
    if common_password?(password)
      errors.add :password, 'is too common'
    end
  end

  def common_password?(password)
    common_passwords = %w[password 12345678 qwerty welcome admin]
    common_passwords.include?(password.downcase)
  end
end
```

## 5. Common Security Vulnerabilities

### SQL Injection Prevention

```ruby
# BAD - SQL Injection vulnerable!
email = params[:email]
User.where("email = '#{email}'")  # Never do this!

# If params[:email] = "' OR '1'='1"
# SQL becomes: SELECT * FROM users WHERE email = '' OR '1'='1'
# Returns all users!

# GOOD - Use parameterized queries
User.where("email = ?", params[:email])

# BETTER - Use hash syntax
User.where(email: params[:email])

# GOOD - Named placeholders
User.where("email = :email AND active = :active", 
  email: params[:email], 
  active: true
)
```

**Python (Django) comparison:**
```python
# BAD
User.objects.raw(f"SELECT * FROM users WHERE email = '{email}'")  # Vulnerable!

# GOOD
User.objects.filter(email=email)  # Django ORM escapes automatically
```

### Cross-Site Scripting (XSS) Prevention

```ruby
# Rails automatically escapes output in ERB templates

# SAFE - Automatically escaped
<%= @user.name %>
# If name = "<script>alert('XSS')</script>"
# Renders as: &lt;script&gt;alert('XSS')&lt;/script&gt;

# UNSAFE - Raw HTML (only use for trusted content!)
<%== @user.bio %>  # or <%= raw @user.bio %>

# SAFE - Sanitize user input
<%= sanitize @user.bio, tags: %w[p br strong em], attributes: %w[href] %>

# In controllers - use strong parameters
class UsersController < ApplicationController
  def create
    @user = User.new(user_params)
    # ...
  end

  private

  def user_params
    params.require(:user).permit(:name, :email)  # Whitelist only
  end
end
```

**Python (Django) comparison:**
```python
# Django templates auto-escape
{{ user.name }}  # Safe

# Explicitly mark as safe (only for trusted content!)
{{ user.bio|safe }}

# In views
from django.utils.html import escape
safe_name = escape(user_name)
```

### Cross-Site Request Forgery (CSRF) Prevention

```ruby
# Rails protects against CSRF automatically

# app/controllers/application_controller.rb
class ApplicationController < ActionController::Base
  protect_from_forgery with: :exception  # Default in Rails
end

# In forms, Rails adds CSRF token automatically:
<%= form_with model: @user do |f| %>
  # CSRF token included automatically
<% end %>

# For AJAX requests
# app/javascript/application.js
const token = document.querySelector('meta[name="csrf-token"]').content;

fetch('/api/users', {
  method: 'POST',
  headers: {
    'X-CSRF-Token': token,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify(data)
});
```

**Python (Django) comparison:**
```python
# Django also protects automatically
# {% csrf_token %} in templates

# In views
from django.views.decorators.csrf import csrf_protect

@csrf_protect
def my_view(request):
    # ...
```

### Mass Assignment Protection

```ruby
# BAD - Mass assignment vulnerability
class UsersController < ApplicationController
  def create
    @user = User.new(params[:user])  # ALL params passed!
    # Attacker could send: { user: { admin: true } }
  end
end

# GOOD - Strong parameters (whitelist)
class UsersController < ApplicationController
  def create
    @user = User.new(user_params)
  end

  private

  def user_params
    params.require(:user).permit(:name, :email, :password)
    # 'admin' not permitted, will be ignored
  end
end

# For nested attributes
def user_params
  params.require(:user).permit(
    :name, 
    :email,
    address_attributes: [:street, :city, :zip],
    phone_numbers_attributes: [:number, :type]
  )
end
```

**Python (Django) comparison:**
```python
# Use forms to whitelist fields
from django import forms

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'email', 'password']  # Whitelist
```

### Insecure Direct Object References

```ruby
# BAD - No authorization check
class PostsController < ApplicationController
  def edit
    @post = Post.find(params[:id])  # Any user can edit any post!
  end
end

# GOOD - Scope to current user
class PostsController < ApplicationController
  before_action :authenticate_user!

  def edit
    @post = current_user.posts.find(params[:id])
    # Will 404 if post doesn't belong to current user
  end
end

# Or with authorization gem (Pundit)
class PostsController < ApplicationController
  def edit
    @post = Post.find(params[:id])
    authorize @post  # Raises exception if not authorized
  end
end

# app/policies/post_policy.rb
class PostPolicy < ApplicationPolicy
  def edit?
    user.id == record.user_id || user.admin?
  end
end
```

## 6. Secure Session Management

```ruby
# config/initializers/session_store.rb
Rails.application.config.session_store :cookie_store,
  key: '_myapp_session',
  secure: Rails.env.production?,  # HTTPS only in production
  httponly: true,                  # Not accessible via JavaScript
  same_site: :lax                  # CSRF protection

# Session timeout
class ApplicationController < ActionController::Base
  before_action :check_session_expiry

  private

  def check_session_expiry
    if session[:expires_at] && session[:expires_at] < Time.current
      reset_session
      redirect_to login_path, alert: 'Session expired'
    else
      session[:expires_at] = 30.minutes.from_now
    end
  end
end
```

## 7. API Authentication

### Token-Based Authentication

```ruby
# JWT (JSON Web Token)
gem 'jwt'

class User < ApplicationRecord
  def generate_jwt
    payload = {
      user_id: id,
      exp: 24.hours.from_now.to_i
    }
    JWT.encode(payload, Rails.application.credentials.secret_key_base)
  end

  def self.decode_jwt(token)
    decoded = JWT.decode(token, Rails.application.credentials.secret_key_base)[0]
    HashWithIndifferentAccess.new(decoded)
  rescue JWT::DecodeError
    nil
  end
end

# In controller
class ApiController < ApplicationController
  before_action :authenticate_request

  private

  def authenticate_request
    header = request.headers['Authorization']
    token = header.split(' ').last if header
    decoded = User.decode_jwt(token)
    
    @current_user = User.find(decoded[:user_id]) if decoded
  rescue ActiveRecord::RecordNotFound
    render json: { error: 'Unauthorized' }, status: :unauthorized
  end
end
```

**Python (Flask) comparison:**
```python
import jwt

def generate_jwt(user_id):
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(hours=24)
    }
    return jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')

def decode_jwt(token):
    try:
        return jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
    except jwt.DecodeError:
        return None
```

## Best Practices Checklist

- [ ] **Never** hardcode secrets in source code
- [ ] Use environment variables for configuration
- [ ] Add `.env` to `.gitignore`
- [ ] Use Rails encrypted credentials for sensitive data
- [ ] Hash passwords with bcrypt (never store plain text)
- [ ] Use strong parameter filtering (mass assignment protection)
- [ ] Enable CSRF protection
- [ ] Escape user input in views (XSS prevention)
- [ ] Use parameterized queries (SQL injection prevention)
- [ ] Implement proper authorization checks
- [ ] Use HTTPS in production
- [ ] Set secure session cookies
- [ ] Implement session timeout
- [ ] Keep dependencies updated (`bundle audit`)
- [ ] Use Content Security Policy headers
- [ ] Implement rate limiting for APIs
- [ ] Log security events
- [ ] Regular security audits

## Tools and Gems

```ruby
# Gemfile
gem 'brakeman'      # Security scanner
gem 'bundler-audit' # Dependency vulnerability scanner
gem 'rack-attack'   # Rate limiting
gem 'secure_headers' # Security headers

# Run scans
bundle exec brakeman
bundle exec bundle-audit
```

## Exercises

1. **Environment Setup**: Configure a Rails app with dotenv and encrypted credentials.

2. **Password Security**: Implement secure password hashing and validation.

3. **Find Vulnerabilities**: Run Brakeman on a sample app and fix issues.

4. **JWT Authentication**: Build an API with JWT token authentication.

5. **Security Audit**: Review a Rails app for common vulnerabilities (SQL injection, XSS, CSRF, mass assignment).

## Summary

Security is not optional. Handle secrets properly, validate and sanitize all user input, use parameterized queries, enable CSRF protection, and keep dependencies updated. Ruby and Rails provide excellent security tools—use them!

**Key Takeaways:**
- Use environment variables and encrypted credentials
- Hash passwords with bcrypt
- Prevent SQL injection with parameterized queries
- Escape user input to prevent XSS
- Use strong parameters for mass assignment protection
- Enable CSRF protection
- Implement proper authorization
- Regular security audits with Brakeman and bundler-audit

**Congratulations!** You've completed all 12 Ruby development tutorials. You're now equipped with professional Ruby development skills!
