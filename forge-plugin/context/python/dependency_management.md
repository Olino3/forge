---
id: "python/dependency_management"
domain: python
title: "Python Dependency Management Reference"
type: reference
estimatedTokens: 1000
loadingStrategy: onDemand
version: "1.0.0"
lastUpdated: "2026-02-10"
sections:
  - name: "Quick Command Reference"
    estimatedTokens: 167
    keywords: [quick, command, reference]
  - name: "Version Constraint Syntax"
    estimatedTokens: 75
    keywords: [version, constraint, syntax]
  - name: "Configuration Files"
    estimatedTokens: 41
    keywords: [configuration, files]
  - name: "Best Practices"
    estimatedTokens: 69
    keywords: [best]
  - name: "Common Issues"
    estimatedTokens: 49
    keywords: [issues]
  - name: "CI/CD Integration"
    estimatedTokens: 10
    keywords: [cicd, integration]
  - name: "Detection Patterns"
    estimatedTokens: 52
    keywords: [detection, patterns]
  - name: "Official Documentation Links"
    estimatedTokens: 37
    keywords: [official, documentation, links]
tags: [python, dependencies, pip, poetry, uv, conda, versioning]
---

# Python Dependency Management Reference

Quick reference for managing Python dependencies across different package managers. For detailed documentation, see official sources linked below.

---

## Quick Command Reference

### Package Manager Comparison

| Manager | Use Case | Config File | Lock File | Docs |
|---------|----------|-------------|-----------|------|
| **uv** | Modern, fast | pyproject.toml | uv.lock | [uv docs](https://github.com/astral-sh/uv) |
| **poetry** | Complete project mgmt | pyproject.toml | poetry.lock | [poetry docs](https://python-poetry.org/docs/) |
| **conda** | Scientific computing | environment.yml | conda.lock | [conda docs](https://docs.conda.io/) |
| **pip** | Standard installer | requirements.txt | N/A | [pip docs](https://pip.pypa.io/) |
| **pipenv** | Dev environments | Pipfile | Pipfile.lock | [pipenv docs](https://pipenv.pypa.io/) |
| **pdm** | PEP 582 compliant | pyproject.toml | pdm.lock | [PDM docs](https://pdm.fming.dev/) |

### Command Translation Table

| Operation | uv | poetry | conda | pip |
|-----------|----|---------||-----|
| Install | `uv pip install` | `poetry add` | `conda install` | `pip install` |
| Install (dev) | `uv pip install --group dev` | `poetry add --group dev` | `conda install` | `pip install` |
| Remove | `uv pip uninstall` | `poetry remove` | `conda remove` | `pip uninstall` |
| Update | `uv pip install -U` | `poetry update` | `conda update` | `pip install -U` |
| List | `uv pip list` | `poetry show` | `conda list` | `pip list` |
| Outdated | `uv pip list --outdated` | `poetry show --outdated` | `conda search --outdated` | `pip list --outdated` |

---

## Version Constraint Syntax

See [PEP 440](https://peps.python.org/pep-0440/) and [PEP 508](https://peps.python.org/pep-0508/) for full specification.

### Common Constraints

| Constraint | Syntax | Example | Meaning |
|------------|--------|---------|---------|
| Exact | `==` | `django==4.2.7` | Exactly 4.2.7 |
| Minimum | `>=` | `requests>=2.28.0` | 2.28.0 or higher |
| Compatible | `~=` | `flask~=2.3.0` | 2.3.0 <= version < 2.4.0 |
| Caret (Poetry) | `^` | `fastapi^0.100.0` | 0.100.0 <= version < 1.0.0 |
| Range | `>=,<` | `pandas>=1.5,<2.0` | Between 1.5 and 2.0 |
| Exclusion | `!=` | `sphinx!=3.0.0` | Any except 3.0.0 |

**Extras syntax**: `package[extra1,extra2]>=1.0`
**Environment markers**: `package>=1.0; python_version>='3.8'`

---

## Configuration Files

### pyproject.toml

**Poetry format**: See [Poetry pyproject.toml](https://python-poetry.org/docs/pyproject/)
**PEP 621 format (uv, pdm)**: See [PEP 621](https://peps.python.org/pep-0621/)

### requirements.txt

**Format**: One package per line with optional version constraints
**Docs**: [pip requirements files](https://pip.pypa.io/en/stable/reference/requirements-file-format/)

### environment.yml (Conda)

**Format**: YAML with channels and dependencies
**Docs**: [Conda environment files](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#create-env-file-manually)

### Pipfile

**Format**: TOML with sources, packages, dev-packages
**Docs**: [Pipfile specification](https://github.com/pypa/pipfile)

---

## Best Practices

### Version Pinning Strategy

**Applications** (deployed):
- Use exact pins: `package==1.2.3`
- Commit lock files
- [Why pin dependencies](https://nvie.com/posts/pin-your-packages/)

**Libraries** (published):
- Use minimum constraints: `package>=1.0`
- Allow flexibility for consumers
- [Library packaging guide](https://packaging.python.org/en/latest/guides/distributing-packages-using-setuptools/)

### Lock File Management

**Always commit**:
- poetry.lock, uv.lock, Pipfile.lock, pdm.lock, conda.lock

**Never commit**:
- Virtual environment directories (.venv, venv)
- __pycache__, *.pyc

See [gitignore templates](https://github.com/github/gitignore/blob/main/Python.gitignore)

### Security Updates

**Tools**:
- [safety](https://pyup.io/safety/) - Check for known vulnerabilities
- [pip-audit](https://github.com/pypa/pip-audit) - Audit for security issues

```bash
pip install safety && safety check
pip install pip-audit && pip-audit
```

---

## Common Issues

### Dependency Conflicts

**Tools for resolution**:
- Poetry: Built-in resolver
- pip: [pip-tools](https://github.com/jazzband/pip-tools) with pip-compile
- conda: Often better for scientific packages

**See**: [Dependency resolution guide](https://pip.pypa.io/en/stable/topics/dependency-resolution/)

### Slow Installations

**Solutions**:
- Use **uv** (10-100x faster than pip)
- Enable pip caching
- Use binary wheels

**See**: [pip caching](https://pip.pypa.io/en/stable/topics/caching/)

### SSL Certificate Errors

**Fix certificate store**:
```bash
pip install --upgrade certifi
```

**See**: [pip SSL issues](https://pip.pypa.io/en/stable/topics/https-certificates/)

---

## CI/CD Integration

**GitHub Actions**: [setup-python action](https://github.com/actions/setup-python)
**GitLab CI**: [Python CI/CD](https://docs.gitlab.com/ee/ci/examples/test-python-project.html)
**Docker**: [Python Docker best practices](https://docs.docker.com/language/python/build-images/)

---

## Detection Patterns

Use these to identify package manager:

| Pattern | Manager |
|---------|---------|
| `uv.lock` exists | uv |
| `poetry.lock` exists | poetry |
| `environment.yml` exists | conda |
| `Pipfile` exists | pipenv |
| `pdm.lock` exists | pdm |
| `[tool.poetry]` in pyproject.toml | poetry |
| `[tool.uv]` in pyproject.toml | uv |
| `[tool.pdm]` in pyproject.toml | pdm |
| Only `requirements.txt` | pip |

---

## Official Documentation Links

- **uv**: https://github.com/astral-sh/uv
- **Poetry**: https://python-poetry.org/docs/
- **Conda**: https://docs.conda.io/
- **pip**: https://pip.pypa.io/en/stable/
- **pipenv**: https://pipenv.pypa.io/
- **PDM**: https://pdm.fming.dev/
- **PEP 440** (Versioning): https://peps.python.org/pep-0440/
- **PEP 508** (Dependencies): https://peps.python.org/pep-0508/
- **PEP 621** (Project Metadata): https://peps.python.org/pep-0621/
- **Python Packaging Guide**: https://packaging.python.org/

---

**Version**: 1.0.0 (Compacted)
**Last Updated**: 2025-11-14
**Maintained For**: python-dependency-management skill
