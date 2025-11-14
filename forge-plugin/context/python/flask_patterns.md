# Flask Patterns and Best Practices

This file contains Flask-specific patterns, anti-patterns, and best practices for code review.

## Application Factory Pattern

### Anti-Pattern: Global App Instance

```python
# WRONG - Hard to test, can't run multiple instances
from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hardcoded-secret'  # Also wrong!

@app.route('/')
def index():
    return "Hello"

if __name__ == '__main__':
    app.run()
```

### Good Pattern: Application Factory

```python
# CORRECT - Testable, configurable
from flask import Flask

def create_app(config_name='development'):
    app = Flask(__name__)
    app.config.from_object(f'config.{config_name.capitalize()}Config')

    # Initialize extensions
    from extensions import db, migrate, login_manager
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # Register blueprints
    from blueprints.auth import auth_bp
    from blueprints.api import api_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(api_bp, url_prefix='/api')

    return app

# config.py
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///dev.db'

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
```

---

## Blueprint Organization

### Good Pattern: Feature-Based Blueprints

```python
# blueprints/auth/__init__.py
from flask import Blueprint

auth_bp = Blueprint('auth', __name__, template_folder='templates')

from . import routes, models

# blueprints/auth/routes.py
from . import auth_bp
from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Login logic
        pass
    return render_template('auth/login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

# app.py
from blueprints.auth import auth_bp
app.register_blueprint(auth_bp, url_prefix='/auth')
```

### Directory Structure

```
app/
├── __init__.py              # Application factory
├── config.py                # Configuration
├── extensions.py            # Extension initialization
├── models.py                # Shared models
├── blueprints/
│   ├── auth/
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   ├── forms.py
│   │   └── templates/
│   ├── api/
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   └── schemas.py
│   └── main/
│       ├── __init__.py
│       ├── routes.py
│       └── templates/
├── static/
└── templates/
    └── base.html
```

---

## Request Handling Patterns

### Request Data Access

```python
# WRONG - No validation
@app.route('/user', methods=['POST'])
def create_user():
    username = request.form['username']  # KeyError if missing!
    email = request.json['email']  # AttributeError if not JSON!
    return "Created"

# CORRECT - Safe access with defaults
@app.route('/user', methods=['POST'])
def create_user():
    # For form data
    username = request.form.get('username')
    if not username:
        return {"error": "Username required"}, 400

    # For JSON
    data = request.get_json()
    if not data or 'email' not in data:
        return {"error": "Email required"}, 400

    email = data['email']
    # Validate and create user...
    return {"message": "Created"}, 201
```

### Request Context

```python
# WRONG - Accessing request outside context
from flask import request

user_agent = request.headers.get('User-Agent')  # RuntimeError!

# CORRECT - Inside view or with app context
@app.route('/')
def index():
    user_agent = request.headers.get('User-Agent')  # Works!
    return f"Your UA: {user_agent}"

# For background tasks, use copy
@app.route('/async')
def async_task():
    # Copy needed data before spawning thread
    user_id = session.get('user_id')
    request_data = request.get_json()

    def background_work():
        # Don't access request or session here!
        process_data(user_id, request_data)

    thread = Thread(target=background_work)
    thread.start()
    return "Processing"
```

---

## Session Management

### Security Best Practices

```python
# config.py
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')  # Required for sessions!
    SESSION_COOKIE_SECURE = True  # HTTPS only
    SESSION_COOKIE_HTTPONLY = True  # No JavaScript access
    SESSION_COOKIE_SAMESITE = 'Lax'  # CSRF protection
    PERMANENT_SESSION_LIFETIME = timedelta(hours=1)

# WRONG - Storing sensitive data in session
session['password'] = password  # NEVER!
session['credit_card'] = cc_number  # NEVER!

# CORRECT - Store only user ID
session['user_id'] = user.id

# CORRECT - Use server-side sessions for sensitive data
from flask_session import Session
app.config['SESSION_TYPE'] = 'redis'
Session(app)
```

---

## Database Patterns (Flask-SQLAlchemy)

### N+1 Query Problem

```python
# WRONG - N+1 queries
users = User.query.all()
for user in users:
    print(user.profile.bio)  # N additional queries!

# CORRECT - Eager loading
users = User.query.options(db.joinedload(User.profile)).all()
for user in users:
    print(user.profile.bio)  # No additional queries
```

### Session Management

```python
# WRONG - Not committing
user = User(username='john')
db.session.add(user)
# Forgot to commit!

# WRONG - Not handling errors
try:
    db.session.add(user)
    db.session.commit()
except:
    pass  # Silently fails!

# CORRECT - Commit with error handling
try:
    db.session.add(user)
    db.session.commit()
except IntegrityError as e:
    db.session.rollback()
    logger.error(f"Database error: {e}")
    return {"error": "User already exists"}, 400
except Exception as e:
    db.session.rollback()
    logger.error(f"Unexpected error: {e}")
    return {"error": "Internal server error"}, 500
```

### Connection Pooling

```python
# config.py
class Config:
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 10,
        'pool_recycle': 3600,
        'pool_pre_ping': True,  # Test connections before using
    }
```

---

## Security Patterns

### CSRF Protection

```python
# extensions.py
from flask_wtf.csrf import CSRFProtect
csrf = CSRFProtect()

# __init__.py
from extensions import csrf
csrf.init_app(app)

# In forms
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

class UserForm(FlaskForm):
    username = StringField('Username')
    submit = SubmitField('Submit')
    # CSRF token automatically added

# In templates
<form method="post">
    {{ form.csrf_token }}
    {{ form.username.label }} {{ form.username() }}
    {{ form.submit() }}
</form>

# For AJAX with fetch
const csrfToken = document.querySelector('meta[name="csrf-token"]').content;
fetch('/api/data', {
    method: 'POST',
    headers: {
        'X-CSRFToken': csrfToken,
        'Content-Type': 'application/json'
    },
    body: JSON.stringify(data)
});
```

### SQL Injection Prevention

```python
# WRONG - SQL injection
username = request.args.get('username')
user = db.session.execute(f"SELECT * FROM users WHERE username = '{username}'")

# CORRECT - Parameterized query
user = db.session.execute(
    "SELECT * FROM users WHERE username = :username",
    {'username': username}
)

# BETTER - Use ORM
user = User.query.filter_by(username=username).first()
```

### XSS Prevention

```python
# Jinja2 auto-escapes by default
{{ user_input }}  # Safe - automatically escaped

# WRONG - Marking user input as safe
{{ user_input|safe }}  # XSS vulnerability!

# CORRECT - Only for trusted content
{{ admin_generated_html|safe }}

# Manual escaping if needed
from markupsafe import escape
safe_input = escape(user_input)
```

### File Upload Security

```python
from werkzeug.utils import secure_filename
import os

UPLOAD_FOLDER = '/var/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf'}
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file", 400

    file = request.files['file']
    if file.filename == '':
        return "No filename", 400

    if file and allowed_file(file.filename):
        # Sanitize filename
        filename = secure_filename(file.filename)

        # Add unique prefix to prevent overwrites
        import uuid
        unique_filename = f"{uuid.uuid4()}_{filename}"

        filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(filepath)

        # Validate file type by content (magic bytes)
        import magic
        mime = magic.from_file(filepath, mime=True)
        if mime not in ['image/jpeg', 'image/png', 'image/gif', 'application/pdf']:
            os.remove(filepath)
            return "Invalid file type", 400

        return {"filename": unique_filename}, 201

    return "File type not allowed", 400
```

---

## Error Handling

### Custom Error Pages

```python
# WRONG - Exposing stack traces
@app.route('/error')
def trigger_error():
    raise Exception("Something went wrong")
# Shows full stack trace in production!

# CORRECT - Custom error handlers
@app.errorhandler(404)
def not_found(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()  # Rollback any pending transactions
    logger.error(f"Internal error: {error}")
    return render_template('errors/500.html'), 500

@app.errorhandler(Exception)
def handle_exception(e):
    # Log the error
    logger.exception("Unhandled exception")

    # Return JSON for API routes
    if request.path.startswith('/api/'):
        return {"error": "Internal server error"}, 500

    # Return HTML for web routes
    return render_template('errors/500.html'), 500
```

---

## Configuration Management

### Good Pattern

```python
# config.py
import os
from datetime import timedelta

class Config:
    """Base configuration"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-CHANGE-THIS'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Email
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'localhost')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 25))
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///dev.db'

class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = False
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

    # Production-only settings
    SESSION_COOKIE_SECURE = True
    PERMANENT_SESSION_LIFETIME = timedelta(hours=1)

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

# Usage in app factory
def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    return app
```

---

## Authentication Patterns (Flask-Login)

### Good Pattern

```python
# models.py
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# extensions.py
from flask_login import LoginManager

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Please log in to access this page.'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# routes.py
from flask_login import login_user, logout_user, login_required, current_user

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            # Validate next_page to prevent open redirect
            if not next_page or not is_safe_url(next_page):
                next_page = url_for('main.index')
            return redirect(next_page)
        flash('Invalid username or password')
    return render_template('auth/login.html', form=form)

def is_safe_url(target):
    from urllib.parse import urlparse, urljoin
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc
```

---

## API Development (Flask-RESTful)

### Good Pattern

```python
from flask_restful import Resource, Api, reqparse, fields, marshal_with
from flask import request

api = Api(app)

# Response marshalling
user_fields = {
    'id': fields.Integer,
    'username': fields.String,
    'email': fields.String,
    'created_at': fields.DateTime(dt_format='iso8601')
}

class UserResource(Resource):
    @marshal_with(user_fields)
    def get(self, user_id):
        user = User.query.get_or_404(user_id)
        return user

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', required=True, help='Username is required')
        parser.add_argument('email', required=True, help='Email is required')
        parser.add_argument('password', required=True, help='Password is required')
        args = parser.parse_args()

        # Validation
        if User.query.filter_by(username=args['username']).first():
            return {'error': 'Username already exists'}, 400

        user = User(username=args['username'], email=args['email'])
        user.set_password(args['password'])

        try:
            db.session.add(user)
            db.session.commit()
            return marshal(user, user_fields), 201
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error creating user: {e}")
            return {'error': 'Internal server error'}, 500

api.add_resource(UserResource, '/api/users', '/api/users/<int:user_id>')
```

---

## Logging Configuration

```python
import logging
from logging.handlers import RotatingFileHandler
import os

def configure_logging(app):
    if not app.debug and not app.testing:
        # Create logs directory if it doesn't exist
        if not os.path.exists('logs'):
            os.mkdir('logs')

        # File handler
        file_handler = RotatingFileHandler(
            'logs/app.log',
            maxBytes=10240000,  # 10MB
            backupCount=10
        )
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s '
            '[in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('Application startup')

# In app factory
configure_logging(app)
```

---

## Testing Patterns

```python
# tests/conftest.py
import pytest
from app import create_app, db

@pytest.fixture(scope='module')
def test_app():
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture(scope='function')
def client(test_app):
    return test_app.test_client()

@pytest.fixture(scope='function')
def runner(test_app):
    return test_app.test_cli_runner()

# tests/test_routes.py
def test_index(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Welcome' in response.data

def test_login(client):
    response = client.post('/auth/login', data={
        'username': 'testuser',
        'password': 'testpass'
    }, follow_redirects=True)
    assert response.status_code == 200
```

---

## Common Flask Anti-Patterns to Flag

- [ ] Global app instance instead of application factory
- [ ] Hardcoded SECRET_KEY or config values
- [ ] Debug=True in production
- [ ] No CSRF protection on forms
- [ ] SQL injection in raw queries
- [ ] XSS via |safe filter on user input
- [ ] No file type validation on uploads
- [ ] No error handlers (exposing stack traces)
- [ ] Accessing request/session outside context
- [ ] Not handling database errors and rollback
- [ ] Open redirect vulnerabilities in login
- [ ] No rate limiting on authentication
- [ ] Storing sensitive data in sessions
- [ ] No connection pooling configuration
- [ ] Missing security headers

## References

- Flask Documentation: https://flask.palletsprojects.com/
- Flask Mega-Tutorial by Miguel Grinberg
- Flask Web Development by Miguel Grinberg
- Flask-Security: https://flask-security.readthedocs.io/
