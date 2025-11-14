# Dependency Patterns and Preferences

## Version Constraint Style

- **Preferred Style**: caret
- **Examples**:
  - Production: `django^4.2` (allows 4.2.x updates, not 5.0)
  - Development: `pytest^7.4` (allows 7.4.x and 7.x updates, not 8.0)

## Dependency Organization

- **Production Dependencies**: In `[tool.poetry.dependencies]` section of pyproject.toml
- **Development Dependencies**: In `[tool.poetry.group.dev.dependencies]`
- **Optional Dependencies**: Not used in this project
- **Extras**: Not used in this project

## Common Patterns

### Installation Patterns

- Testing dependencies installed together: pytest, pytest-cov, pytest-django
- Linting and formatting tools grouped: black, isort, flake8, mypy
- Django ecosystem packages often updated together: django, django-rest-framework, django-cors-headers

### Update Patterns

- Django pinned to 4.2.x for LTS stability (updates only within 4.2 series)
- Testing tools updated frequently to latest compatible versions
- Third-party API clients (requests, httpx) kept current for security

### Removal Patterns

- When removing unused features, associated packages removed together
- Development dependencies never removed unless confirmed unused

## Package Groups

### Core Dependencies
- django (web framework)
- psycopg2-binary (PostgreSQL adapter)
- celery (task queue)
- redis (caching and Celery broker)

### Testing Dependencies
- pytest
- pytest-cov
- pytest-django
- factory-boy (test fixtures)

### Development Tools
- black (code formatting)
- isort (import sorting)
- flake8 (linting)
- mypy (type checking)

### Optional/Conditional Dependencies
None currently

## Known Issues and Workarounds

### Issue 1: psycopg2-binary on Apple Silicon
- **Problem**: psycopg2-binary sometimes fails to install on M1/M2 Macs
- **Workaround**: Use psycopg2 with system PostgreSQL libraries, or use Docker
- **Affected Packages**: psycopg2-binary

## Dependency Update History

- **2025-11-14**: Initial project setup with Django 4.2, pytest 7.4
- **2025-11-14**: Added black 23.11 for code formatting

## Notes

This project follows Poetry's semantic versioning with caret constraints. Django is intentionally kept at 4.2.x (LTS) and won't be updated to 5.x without explicit decision. Development dependencies are kept up to date with latest compatible versions.
