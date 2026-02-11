---
id: "python/flask_patterns"
domain: python
title: "Flask Patterns"
type: framework
estimatedTokens: 1000
loadingStrategy: onDemand
version: "1.0.0"
lastUpdated: "2026-02-10"
sections:
  - name: "Common Anti-Patterns"
    estimatedTokens: 103
    keywords: [anti-patterns]
  - name: "Application Factory"
    estimatedTokens: 54
    keywords: [application, factory]
  - name: "Blueprints"
    estimatedTokens: 51
    keywords: [blueprints]
  - name: "Request Context"
    estimatedTokens: 59
    keywords: [request, context]
  - name: "Common Detection Patterns"
    estimatedTokens: 119
    keywords: [detection, patterns]
  - name: "Security Issues"
    estimatedTokens: 66
    keywords: [security, issues]
  - name: "Extensions"
    estimatedTokens: 45
    keywords: [extensions]
  - name: "Testing"
    estimatedTokens: 20
    keywords: [testing]
  - name: "Tools"
    estimatedTokens: 14
    keywords: [tools]
  - name: "Official Resources"
    estimatedTokens: 20
    keywords: [official, resources]
tags: [python, flask, blueprints, factory, security, extensions]
---

# Flask Patterns

Quick reference for Flask best practices and common issues. For detailed examples, see [Flask documentation](https://flask.palletsprojects.com/).

---

## Common Anti-Patterns

| Anti-Pattern | What to Look For | Better Approach | Learn More |
|--------------|------------------|-----------------|------------|
| **Global app instance** | `app = Flask(__name__)` at module level | Use application factory pattern | [Application Factories](https://flask.palletsprojects.com/en/stable/patterns/appfactories/) |
| **No blueprints** | All routes in one file | Use blueprints for organization | [Blueprints](https://flask.palletsprojects.com/en/stable/blueprints/) |
| **Mutable globals** | Global variables for state | Use `g` object or session | [Context Globals](https://flask.palletsprojects.com/en/stable/api/#flask.g) |
| **Not using config objects** | Hardcoded config | Use `app.config.from_object()` | [Configuration](https://flask.palletsprojects.com/en/stable/config/) |
| **Database outside request context** | DB queries at module level | Use `before_request` or context managers | [Request Context](https://flask.palletsprojects.com/en/stable/reqcontext/) |
| **No CSRF protection** | Forms without CSRF tokens | Use Flask-WTF | [CSRF Protection](https://flask-wtf.readthedocs.io/en/stable/csrf.html) |
| **Direct request.args access** | No validation | Use Flask-WTF or marshmallow | [Form Validation](https://flask-wtf.readthedocs.io/) |

---

## Application Factory

| Issue | Detection Pattern | Best Practice |
|-------|-------------------|---------------|
| **No factory function** | App created at module level | Create `create_app()` function |
| **Config not externalized** | Settings in code | Use environment-based config |
| **Extensions not initialized** | Extension init outside factory | Init extensions in factory with `init_app()` |
| **Testing difficulties** | Can't create test app | Factory allows multiple app instances |

[Application Factories](https://flask.palletsprojects.com/en/stable/patterns/appfactories/)

---

## Blueprints

| Issue | Detection Pattern | Best Practice |
|-------|-------------------|---------------|
| **No blueprint organization** | All routes in `app.py` | Group routes by functionality |
| **Circular imports** | Blueprint imports app | Use `current_app` proxy |
| **No URL prefixes** | Routes without prefixes | Use `url_prefix` parameter |
| **Missing error handlers** | Generic 404/500 pages | Register blueprint-specific error handlers |

[Blueprints and Views](https://flask.palletsprojects.com/en/stable/blueprints/)

---

## Request Context

| Issue | Detection Pattern | Recommended Fix |
|-------|-------------------|-----------------|
| **Using `g` incorrectly** | Storing permanent state in `g` | Use `g` only for request-scoped data |
| **Database connections not closed** | No teardown handler | Use `@app.teardown_appcontext` |
| **Session manipulation outside request** | Accessing `session` at module level | Only access within request context |
| **Current_app outside context** | `current_app` used improperly | Ensure you're in an application context |

[The Request Context](https://flask.palletsprojects.com/en/stable/reqcontext/)

---

## Common Detection Patterns

```python
# ❌ Global app (anti-pattern)
app = Flask(__name__)
db = SQLAlchemy(app)

@app.route('/')
def index():
    return 'Hello'

# ✅ Application factory
def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app

# ❌ No blueprints
@app.route('/users/')
def list_users():
    pass

@app.route('/posts/')
def list_posts():
    pass

# ✅ With blueprints
from flask import Blueprint

users_bp = Blueprint('users', __name__, url_prefix='/users')

@users_bp.route('/')
def list_users():
    pass

# ❌ Mutable global state
user_data = {}  # Global mutable

@app.route('/store')
def store():
    user_data[request.args['key']] = 'value'  # Not thread-safe!

# ✅ Use request context
@app.route('/store')
def store():
    g.user_data = 'value'  # Request-scoped

# ❌ No form validation
@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']  # No validation, can fail
    return f'Hello {name}'

# ✅ With Flask-WTF
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired

class MyForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])

@app.route('/submit', methods=['GET', 'POST'])
def submit():
    form = MyForm()
    if form.validate_on_submit():
        return f'Hello {form.name.data}'
    return render_template('form.html', form=form)
```

---

## Security Issues

| Issue | Detection Pattern | Recommended Fix |
|-------|-------------------|-----------------|
| **No SECRET_KEY** | Missing or weak secret key | Generate strong random key, store in env vars |
| **Debug mode in production** | `app.run(debug=True)` | Never enable debug in production |
| **XSS vulnerability** | `Markup()` on user input | Always escape user input |
| **No HTTPS** | HTTP in production | Enforce HTTPS, use Flask-Talisman |
| **SQL injection** | String concatenation in queries | Use SQLAlchemy ORM or parameterized queries |

[Security Considerations](https://flask.palletsprojects.com/en/stable/security/)

---

## Extensions

| Extension | Use Case | Link |
|-----------|----------|------|
| **Flask-SQLAlchemy** | ORM integration | [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/) |
| **Flask-WTF** | Form handling & CSRF | [Flask-WTF](https://flask-wtf.readthedocs.io/) |
| **Flask-Login** | User session management | [Flask-Login](https://flask-login.readthedocs.io/) |
| **Flask-Migrate** | Database migrations | [Flask-Migrate](https://flask-migrate.readthedocs.io/) |
| **Flask-CORS** | CORS handling | [Flask-CORS](https://flask-cors.readthedocs.io/) |
| **Flask-Caching** | Caching | [Flask-Caching](https://flask-caching.readthedocs.io/) |

---

## Testing

```python
# ✅ Testing with factory pattern
def test_home():
    app = create_app('testing')
    client = app.test_client()

    response = client.get('/')
    assert response.status_code == 200
```

[Testing Flask Applications](https://flask.palletsprojects.com/en/stable/testing/)

---

## Tools

- **Flask-DebugToolbar**: Development debugging - [Flask-DebugToolbar](https://flask-debugtoolbar.readthedocs.io/)
- **pytest**: Testing framework - [pytest](https://docs.pytest.org/)
- **Black**: Code formatting - [Black](https://black.readthedocs.io/)

---

## Official Resources

- **Flask Documentation**: https://flask.palletsprojects.com/
- **Flask Mega-Tutorial**: https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world
- **Flask Patterns**: https://flask.palletsprojects.com/en/stable/patterns/
- **Awesome Flask**: https://github.com/mjhea0/awesome-flask

---

**Version**: 1.0.0 (Compacted)
**Last Updated**: 2025-11-14
**Maintained For**: python-code-review skill
