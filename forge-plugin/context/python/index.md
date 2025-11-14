# Python Context Files

Context files for Python code review, framework-specific patterns, and common issues detection.

## Files in this Directory

### `context_detection.md`

**Purpose**: Identify Python project type and framework from code patterns

**Use when**:
- Starting a new project review
- Determining which framework patterns to load
- Understanding project architecture
- Choosing appropriate review focus

**Detects**:
- Django projects (models, views, settings patterns)
- Flask projects (blueprints, app factory, decorators)
- FastAPI projects (Pydantic, async, dependency injection)
- Data Science projects (pandas, numpy, jupyter)
- Machine Learning projects (scikit-learn, tensorflow, pytorch)

**Load first**: Always start Python reviews with this file to identify the project type

---

### `common_issues.md`

**Purpose**: Universal Python problems found across all project types

**Use when**:
- Every Python code review
- Looking for typical Python pitfalls
- Checking basic Python quality

**Key issues covered**:
- Mutable default arguments
- Exception handling anti-patterns
- Import problems (circular, relative)
- Memory leaks (circular references, unclosed resources)
- Performance issues (string concatenation, inefficient loops)
- Concurrency problems (GIL, thread safety)

**Load for**: Every Python review regardless of framework

---

### `dependency_management.md`

**Purpose**: Package manager command reference and best practices

**Use when**:
- Installing, removing, or updating Python packages
- Managing project dependencies
- Working with different package managers (uv, poetry, conda, pip)
- Setting up dependency configuration files

**Covers**:
- Command reference for all major package managers
- Version constraint syntax (PEP 440)
- Configuration file formats (pyproject.toml, requirements.txt, environment.yml)
- Lock file management
- Best practices for version pinning
- Dependency conflict resolution
- CI/CD integration patterns

**Load for**: `skill:python-dependency-management` (always), dependency-related operations

---

### `virtual_environments.md`

**Purpose**: Virtual environment creation, activation, and management

**Use when**:
- Creating or detecting virtual environments
- Setting up project environments
- Troubleshooting environment issues
- Configuring IDE integration

**Covers**:
- venv, virtualenv, poetry, conda environment types
- Creation commands for all environment types
- Activation/deactivation procedures (cross-platform)
- Best practices for venv location and naming
- Environment configuration and variables
- Common troubleshooting scenarios
- IDE integration (VS Code, PyCharm, Jupyter)

**Load for**: `skill:python-dependency-management` (always), environment setup tasks

---

### `datascience_patterns.md`

**Purpose**: Data science and analytics code patterns

**Use when**:
- Project uses pandas, numpy, scipy
- Data manipulation and analysis code
- Statistical computing
- Data pipeline review

**Covers**:
- Pandas best practices (vectorization, memory, chaining)
- NumPy patterns (broadcasting, indexing, dtypes)
- Data validation and cleaning
- Memory management for large datasets
- Visualization patterns

**Load if**: `context_detection.md` identifies data science project

---

### `django_patterns.md`

**Purpose**: Django framework best practices and patterns

**Use when**:
- Django project detected
- Reviewing models, views, or templates
- Checking ORM usage
- Analyzing middleware or signals

**Covers**:
- Model design (fields, relationships, managers, migrations)
- View patterns (CBV, FBV, mixins)
- QuerySet optimization (select_related, prefetch_related, N+1)
- Form handling
- Middleware and signals
- Settings and configuration
- Security (CSRF, SQL injection, XSS)

**Load if**: Django imports or patterns detected

---

### `fastapi_patterns.md`

**Purpose**: FastAPI framework best practices and patterns

**Use when**:
- FastAPI project detected
- Reviewing async endpoints
- Checking Pydantic models
- Analyzing dependency injection

**Covers**:
- Pydantic models (request/response, validation)
- Dependency injection (database, auth, reusable)
- Async/await patterns (when to use, common mistakes)
- Path operations and routing
- Background tasks
- Error handling and middleware
- Testing patterns

**Load if**: FastAPI or Pydantic imports detected

---

### `flask_patterns.md`

**Purpose**: Flask framework best practices and patterns

**Use when**:
- Flask project detected
- Reviewing routes and blueprints
- Checking application structure
- Analyzing extensions

**Covers**:
- Application factory pattern
- Blueprints organization
- Request context and globals
- Extension integration (SQLAlchemy, Login, etc.)
- Configuration management
- Error handling
- Testing patterns

**Load if**: Flask imports or app.route decorators detected

---

### `ml_patterns.md`

**Purpose**: Machine learning code patterns and practices

**Use when**:
- ML model training code
- Data pipeline for ML
- Model deployment code
- ML experimentation

**Covers**:
- Model training patterns
- Data pipeline design
- Feature engineering
- Model evaluation and metrics
- Hyperparameter tuning
- Model serialization and deployment
- Reproducibility (seeds, versioning)
- Common ML pitfalls (data leakage, overfitting)

**Load if**: ML frameworks detected (sklearn, tensorflow, pytorch, etc.)

---

## Usage Workflow

### Standard Python Review Process

```markdown
1. Load context_detection.md
   → Identify framework/project type

2. Load common_issues.md
   → Always check universal Python problems

3. Load framework-specific file(s)
   → Django: django_patterns.md
   → Flask: flask_patterns.md
   → FastAPI: fastapi_patterns.md
   → Data Science: datascience_patterns.md
   → ML: ml_patterns.md

4. Load security context
   → ../security/security_guidelines.md
   → ../security/owasp_python.md (if applicable)
```

### Dependency Management Process

```markdown
1. Load dependency_management.md
   → Package manager commands and reference

2. Load virtual_environments.md
   → Venv creation and activation

3. Execute dependency operation
   → Use commands from dependency_management.md
   → Apply venv best practices from virtual_environments.md
```

### Multi-Framework Projects

Some projects use multiple frameworks. Load all relevant files:

```markdown
# Example: FastAPI with ML models
1. context_detection.md → Detects FastAPI + ML
2. common_issues.md → Universal Python
3. fastapi_patterns.md → API patterns
4. ml_patterns.md → Model patterns
5. security_guidelines.md → Especially for API inputs
```

## Quick Reference Matrix

| Project Type | Load These Files | Priority Order |
|--------------|------------------|----------------|
| **Django** | `context_detection.md`, `common_issues.md`, `django_patterns.md`, `security_guidelines.md` | 1, 2, 3, 4 |
| **Flask** | `context_detection.md`, `common_issues.md`, `flask_patterns.md`, `security_guidelines.md` | 1, 2, 3, 4 |
| **FastAPI** | `context_detection.md`, `common_issues.md`, `fastapi_patterns.md`, `security_guidelines.md` | 1, 2, 3, 4 |
| **Data Science** | `context_detection.md`, `common_issues.md`, `datascience_patterns.md` | 1, 2, 3 |
| **Machine Learning** | `context_detection.md`, `common_issues.md`, `ml_patterns.md`, `datascience_patterns.md` | 1, 2, 3, 4 |
| **Generic Python** | `common_issues.md`, `security_guidelines.md` | 1, 2 |
| **Dependency Management** | `dependency_management.md`, `virtual_environments.md` | 1, 2 |

## Pattern Detection Hints

Use these indicators from code to determine which files to load:

| If you see... | Load file... |
|---------------|--------------|
| `from django.` | `django_patterns.md` |
| `from flask import` | `flask_patterns.md` |
| `from fastapi import` | `fastapi_patterns.md` |
| `import pandas`, `import numpy` | `datascience_patterns.md` |
| `import sklearn`, `import tensorflow`, `import torch` | `ml_patterns.md` |
| `class Meta:`, `models.Model` | `django_patterns.md` |
| `@app.route` | `flask_patterns.md` |
| `@router.get`, `BaseModel` | `fastapi_patterns.md` |
| `.groupby(`, `.merge(`, `.pivot_table(` | `datascience_patterns.md` |
| `.fit(`, `.predict(`, `.score(` | `ml_patterns.md` |
| User mentions "install", "add package", "remove package" | `dependency_management.md`, `virtual_environments.md` |
| `pyproject.toml`, `requirements.txt`, `poetry.lock` | `dependency_management.md` |
| `.venv/`, `venv/`, virtual environment | `virtual_environments.md` |

## Related Skills

- **python-code-review**: Primary consumer of code review context files
- **python-dependency-management**: Uses dependency_management.md and virtual_environments.md
- **get-git-diff**: May use for commit message classification

## Maintenance Notes

- `common_issues.md`: Update with new Python anti-patterns as discovered
- Framework files: Update when major framework versions change patterns
- `context_detection.md`: Add new framework detection patterns as needed
- Keep examples minimal - full examples belong in skill documentation
