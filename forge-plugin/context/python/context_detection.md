---
id: "python/context_detection"
domain: python
title: "Python Framework and Context Detection"
type: detection
estimatedTokens: 1050
loadingStrategy: onDemand
version: "0.1.0-alpha"
lastUpdated: "2026-02-10"
sections:
  - name: "Detection Strategy"
    estimatedTokens: 20
    keywords: [detection, strategy]
  - name: "Web Frameworks"
    estimatedTokens: 87
    keywords: [web, frameworks]
  - name: "Data Science / ML"
    estimatedTokens: 73
    keywords: [data, science]
  - name: "Quick Detection Table"
    estimatedTokens: 56
    keywords: [quick, detection, table]
  - name: "Configuration Files"
    estimatedTokens: 74
    keywords: [configuration, files]
  - name: "Directory Structure Patterns"
    estimatedTokens: 42
    keywords: [directory, structure, patterns]
  - name: "Multi-Framework Projects"
    estimatedTokens: 45
    keywords: [multi-framework, projects]
  - name: "ORM Detection"
    estimatedTokens: 48
    keywords: [orm, detection]
  - name: "Testing Framework Detection"
    estimatedTokens: 33
    keywords: [testing, framework, detection]
  - name: "Decision Tree"
    estimatedTokens: 38
    keywords: [decision, tree]
  - name: "Version Detection"
    estimatedTokens: 35
    keywords: [version, detection]
  - name: "Official Documentation"
    estimatedTokens: 26
    keywords: [official, documentation]
tags: [python, detection, framework, django, flask, fastapi, datascience, ml]
---

# Python Framework and Context Detection

Quick reference for identifying which Python framework or context is being used. Use this to determine which pattern files to load.

---

## Detection Strategy

1. **Check import statements** (most reliable)
2. **Examine file structure** (directory patterns)
3. **Look for configuration files** (framework-specific configs)
4. **Analyze code patterns** (decorators, class inheritance)

---

## Web Frameworks

| Framework | Key Imports | File Markers | Pattern Files to Load | Docs |
|-----------|-------------|--------------|----------------------|------|
| **Django** | `from django.db import models`<br/>`from django.http import HttpResponse` | `manage.py`<br/>`settings.py`<br/>`migrations/` | `django_patterns.md` | [Django docs](https://docs.djangoproject.com/) |
| **Flask** | `from flask import Flask`<br/>`from flask import request, jsonify` | `app.py` or `run.py`<br/>`templates/`<br/>`static/` | `flask_patterns.md` | [Flask docs](https://flask.palletsprojects.com/) |
| **FastAPI** | `from fastapi import FastAPI`<br/>`from pydantic import BaseModel` | `main.py`<br/>`routers/`<br/>`async def` everywhere | `fastapi_patterns.md` | [FastAPI docs](https://fastapi.tiangolo.com/) |

### Detection Patterns

```python
# Django
from django.db import models
class MyModel(models.Model): ...
urlpatterns = [...]

# Flask
from flask import Flask
app = Flask(__name__)
@app.route('/')

# FastAPI
from fastapi import FastAPI
app = FastAPI()
@app.get("/")
async def root():
```

---

## Data Science / ML

| Context | Key Imports | File Markers | Pattern Files to Load | Docs |
|---------|-------------|--------------|----------------------|------|
| **Data Science** | `import pandas as pd`<br/>`import numpy as np`<br/>`import matplotlib` | `.ipynb` notebooks<br/>`data/` folder<br/>`*.csv` files | `datascience_patterns.md` | [Pandas](https://pandas.pydata.org/)<br/>[NumPy](https://numpy.org/) |
| **Machine Learning** | `import sklearn`<br/>`import tensorflow as tf`<br/>`import torch` | `models/` folder<br/>`*.h5`, `*.pkl` files<br/>`train.py`, `predict.py` | `ml_patterns.md`<br/>`datascience_patterns.md` | [scikit-learn](https://scikit-learn.org/)<br/>[TensorFlow](https://tensorflow.org/)<br/>[PyTorch](https://pytorch.org/) |

### Detection Patterns

```python
# Data Science
import pandas as pd
import numpy as np
df = pd.read_csv(...)
df.groupby(...).agg(...)

# Machine Learning
from sklearn.model_selection import train_test_split
from tensorflow.keras import Model
import torch.nn as nn
model.fit(X_train, y_train)
```

---

## Quick Detection Table

Use this during review to quickly identify context:

| If You See... | Framework/Context | Load |
|---------------|-------------------|------|
| `models.Model`, `manage.py` | Django | `django_patterns.md` |
| `Flask(__name__)`, `@app.route` | Flask | `flask_patterns.md` |
| `FastAPI()`, `async def`, `BaseModel` | FastAPI | `fastapi_patterns.md` |
| `pd.DataFrame`, `np.array` | Data Science | `datascience_patterns.md` |
| `.fit()`, `.predict()`, `sklearn` | Machine Learning | `ml_patterns.md` |
| All of the above | Always load | `common_issues.md` |

---

## Configuration Files

| File | Framework | What It Indicates |
|------|-----------|-------------------|
| `manage.py` | Django | Django project root |
| `settings.py` with `INSTALLED_APPS` | Django | Django configuration |
| `app.py` with `Flask(__name__)` | Flask | Flask application |
| `main.py` with `FastAPI()` | FastAPI | FastAPI application |
| `requirements.txt` with framework name | Any | Project dependencies |
| `pyproject.toml` with `[tool.poetry]` | Any | Poetry-managed project |
| `setup.py` or `setup.cfg` | Any | Installable package |
| `*.ipynb` | Data Science | Jupyter notebooks |
| `environment.yml` | Data Science/ML | Conda environment |

---

## Directory Structure Patterns

### Django

```
project/
├── manage.py
├── settings.py
├── urls.py
├── models.py
└── migrations/
```

### Flask

```
project/
├── app.py
├── templates/
├── static/
└── config.py
```

### FastAPI

```
project/
├── main.py
├── routers/
├── models/
└── dependencies/
```

### Data Science

```
project/
├── notebooks/
├── data/
├── scripts/
└── outputs/
```

---

## Multi-Framework Projects

Some projects use multiple frameworks. Load all relevant pattern files:

| Combination | Example | Load |
|-------------|---------|------|
| FastAPI + ML | ML model serving API | `fastapi_patterns.md` + `ml_patterns.md` |
| Flask + Data Science | Data visualization dashboard | `flask_patterns.md` + `datascience_patterns.md` |
| Django + ML | ML-powered web app | `django_patterns.md` + `ml_patterns.md` |

---

## ORM Detection

| ORM | Key Imports | Pattern |
|-----|-------------|---------|
| **Django ORM** | `from django.db import models` | `class Model(models.Model):` |
| **SQLAlchemy** | `from sqlalchemy import Column`<br/>`from sqlalchemy.orm import declarative_base` | `Base = declarative_base()` |
| **Tortoise ORM** | `from tortoise import fields, models` | Async ORM for FastAPI |
| **Peewee** | `from peewee import Model, CharField` | Lightweight ORM |

---

## Testing Framework Detection

| Framework | Key Imports | Load Consideration |
|-----------|-------------|-------------------|
| **pytest** | `import pytest`<br/>`@pytest.fixture` | Consider test-specific patterns |
| **unittest** | `import unittest`<br/>`class Test(unittest.TestCase):` | Standard library testing |
| **Django tests** | `from django.test import TestCase` | Django-specific test patterns |

---

## Decision Tree

```
Start
  │
  ├─ Has Django imports? ──Yes──> Load django_patterns.md
  ├─ Has Flask imports? ──Yes──> Load flask_patterns.md
  ├─ Has FastAPI imports? ──Yes──> Load fastapi_patterns.md
  ├─ Has pandas/numpy? ──Yes──> Load datascience_patterns.md
  ├─ Has sklearn/tf/torch? ──Yes──> Load ml_patterns.md
  └─ None detected? ──> Load only common_issues.md
```

**Always load**: `common_issues.md` (universal Python problems)

---

## Version Detection

### Django

```python
import django
print(django.VERSION)  # (4, 2, 0, 'final', 0)
```

Impacts: Different Django versions have different patterns (check docs for version-specific features)

### Python

```python
import sys
print(sys.version_info)  # sys.version_info(major=3, minor=11, ...)
```

Impacts: Python 3.8+ (walrus operator), 3.10+ (match/case), 3.11+ (exception groups)

---

## Official Documentation

- **Django**: https://docs.djangoproject.com/
- **Flask**: https://flask.palletsprojects.com/
- **FastAPI**: https://fastapi.tiangolo.com/
- **pandas**: https://pandas.pydata.org/docs/
- **NumPy**: https://numpy.org/doc/
- **scikit-learn**: https://scikit-learn.org/stable/
- **TensorFlow**: https://www.tensorflow.org/api_docs
- **PyTorch**: https://pytorch.org/docs/

---

**Version**: 0.1.0-alpha (Compacted)
**Last Updated**: 2025-11-14
**Maintained For**: python-code-review skill
