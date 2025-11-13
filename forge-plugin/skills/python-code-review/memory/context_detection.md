# Framework and Context Detection

This file provides guidance on identifying which Python framework or context is being used, so you can load the appropriate pattern files.

## Detection Strategy

1. **Check import statements** - Most reliable indicator
2. **Examine file structure** - Directory patterns reveal frameworks
3. **Look for configuration files** - Framework-specific configs
4. **Analyze code patterns** - Decorators, class inheritance

## Web Frameworks

### Django Detection

**Import patterns**:
```python
from django.db import models
from django.http import HttpResponse
from django.views import View
from django.contrib.auth.models import User
import django
```

**File structure**:
```
project/
├── manage.py              # Django management script
├── settings.py            # Django settings
├── urls.py                # URL configuration
├── wsgi.py / asgi.py      # WSGI/ASGI application
├── models.py              # Database models
└── migrations/            # Database migrations
```

**Configuration files**:
- `manage.py` presence
- `settings.py` with `INSTALLED_APPS`, `MIDDLEWARE`, `DATABASES`

**Code patterns**:
```python
# Models inherit from models.Model
class User(models.Model):
    pass

# Views inherit from View or use function-based views
class MyView(View):
    pass

def my_view(request):
    pass

# URL patterns
urlpatterns = [...]
```

**When detected**: Load `memory/django_patterns.md`

---

### Flask Detection

**Import patterns**:
```python
from flask import Flask, request, jsonify
from flask import render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import flask
```

**File structure**:
```
project/
├── app.py or run.py       # Main application file
├── templates/             # Jinja2 templates
├── static/                # Static files
├── models.py              # Optional models
└── config.py              # Configuration
```

**Code patterns**:
```python
# App instantiation
app = Flask(__name__)

# Route decorators
@app.route('/path')
def handler():
    pass

# Blueprints
from flask import Blueprint
bp = Blueprint('name', __name__)
```

**When detected**: Load `memory/flask_patterns.md`

---

### FastAPI Detection

**Import patterns**:
```python
from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import fastapi
```

**File structure**:
```
project/
├── main.py                # Main application file
├── models.py              # Pydantic models
├── routers/               # API routers
├── dependencies.py        # Dependency injection
└── schemas.py             # Request/response schemas
```

**Code patterns**:
```python
# App instantiation
app = FastAPI()

# Route decorators with type hints
@app.get("/items/{item_id}")
async def read_item(item_id: int):
    pass

# Pydantic models
class Item(BaseModel):
    name: str
    price: float

# Dependency injection
def get_db():
    yield db

@app.get("/users")
def get_users(db: Session = Depends(get_db)):
    pass
```

**When detected**: Load `memory/fastapi_patterns.md`

---

## Data Science & Analytics

### Pandas/NumPy Detection

**Import patterns**:
```python
import pandas as pd
import numpy as np
from pandas import DataFrame, Series
```

**File patterns**:
```
project/
├── notebooks/             # Jupyter notebooks
├── data/                  # Data files (CSV, Excel, etc.)
├── analysis.py            # Analysis scripts
└── visualization.py       # Plotting scripts
```

**Code patterns**:
```python
# DataFrame operations
df = pd.read_csv('data.csv')
df['column'].apply(lambda x: x * 2)

# NumPy arrays
arr = np.array([1, 2, 3])
result = np.mean(arr)
```

**When detected**: Load `memory/datascience_patterns.md`

---

## Machine Learning Frameworks

### PyTorch Detection

**Import patterns**:
```python
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
import torch.optim as optim
```

**Code patterns**:
```python
# Neural network models
class MyModel(nn.Module):
    def __init__(self):
        super().__init__()

# Tensor operations
x = torch.tensor([1, 2, 3])
loss = criterion(output, target)
```

**When detected**: Load `memory/ml_patterns.md`

---

### TensorFlow/Keras Detection

**Import patterns**:
```python
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential
```

**Code patterns**:
```python
# Sequential model
model = Sequential([
    layers.Dense(64, activation='relu'),
    layers.Dense(10, activation='softmax')
])

# Model compilation
model.compile(optimizer='adam', loss='categorical_crossentropy')

# TensorFlow operations
x = tf.constant([1, 2, 3])
```

**When detected**: Load `memory/ml_patterns.md`

---

### Scikit-learn Detection

**Import patterns**:
```python
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import sklearn
```

**Code patterns**:
```python
# Model training
model = RandomForestClassifier()
model.fit(X_train, y_train)
predictions = model.predict(X_test)

# Preprocessing
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
```

**When detected**: Load `memory/ml_patterns.md`

---

## Multiple Framework Detection

### Scenario: Web + Data Science
```python
# Flask + Pandas
from flask import Flask
import pandas as pd

app = Flask(__name__)

@app.route('/analyze')
def analyze():
    df = pd.read_csv('data.csv')
    return df.describe().to_json()
```

**Action**: Load both `memory/flask_patterns.md` AND `memory/datascience_patterns.md`

### Scenario: FastAPI + ML
```python
# FastAPI + PyTorch
from fastapi import FastAPI
import torch

app = FastAPI()
model = torch.load('model.pt')

@app.post('/predict')
async def predict(data: InputData):
    prediction = model(data.features)
    return {'prediction': prediction}
```

**Action**: Load both `memory/fastapi_patterns.md` AND `memory/ml_patterns.md`

---

## Configuration File Detection

### requirements.txt / pyproject.toml

Parse dependencies to identify frameworks:

```python
# requirements.txt
Django==4.2.0           → Django
Flask==2.3.2            → Flask
fastapi==0.104.1        → FastAPI
pandas==2.1.0           → Data Science
torch==2.1.0            → ML
tensorflow==2.14.0      → ML
scikit-learn==1.3.0     → ML
```

### pyproject.toml (Poetry)
```toml
[tool.poetry.dependencies]
django = "^4.2"         → Django
flask = "^2.3"          → Flask
fastapi = "^0.104"      → FastAPI
```

---

## Automated Detection Logic

### Recommended Detection Order

1. **Check imports first** (most reliable)
   - Scan first 50 lines of .py files
   - Look for framework-specific imports

2. **Check file structure**
   - Look for `manage.py` (Django)
   - Look for `app.py` / `main.py` with FastAPI/Flask patterns
   - Look for `notebooks/` (Data Science)

3. **Check configuration files**
   - Parse `requirements.txt`
   - Parse `pyproject.toml`
   - Check `setup.py`

4. **Default to common_issues.md**
   - If no framework detected, use general Python patterns

### Detection Script Example

```python
import ast
from pathlib import Path

def detect_frameworks(file_path):
    frameworks = set()

    with open(file_path) as f:
        content = f.read()

    try:
        tree = ast.parse(content)
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    module = alias.name.split('.')[0]
                    if module == 'django':
                        frameworks.add('django')
                    elif module == 'flask':
                        frameworks.add('flask')
                    elif module == 'fastapi':
                        frameworks.add('fastapi')
                    elif module in ('pandas', 'numpy'):
                        frameworks.add('datascience')
                    elif module in ('torch', 'tensorflow', 'sklearn'):
                        frameworks.add('ml')

            elif isinstance(node, ast.ImportFrom):
                module = node.module.split('.')[0] if node.module else ''
                if module == 'django':
                    frameworks.add('django')
                elif module == 'flask':
                    frameworks.add('flask')
                elif module == 'fastapi':
                    frameworks.add('fastapi')
                elif module in ('pandas', 'numpy'):
                    frameworks.add('datascience')
                elif module in ('torch', 'tensorflow', 'sklearn'):
                    frameworks.add('ml')

    except SyntaxError:
        pass

    return frameworks
```

---

## Context Priority Matrix

When multiple frameworks are detected, prioritize loading in this order:

1. **Web framework first** (Django/Flask/FastAPI)
   - These define the application structure
   - Security concerns are critical

2. **Data processing second** (Pandas/NumPy)
   - Performance patterns important
   - Data validation critical

3. **ML framework third** (PyTorch/TensorFlow/sklearn)
   - Specialized patterns
   - Model security and performance

4. **Always load common_issues.md**
   - Universal Python anti-patterns apply regardless of framework

---

## Edge Cases

### Microservices Architecture
Multiple files, each using different frameworks:
- Review each file with its appropriate context
- Track framework switches between files

### Legacy Code
No modern framework detected:
- Load `memory/common_issues.md` only
- Focus on general Python best practices

### Mixed Python Versions
Python 2 vs Python 3:
- Check for `from __future__ import` statements
- Python 2 code should trigger modernization recommendations
- Flag print statements without parentheses (Python 2 syntax)

### No Framework (Scripts/Utilities)
Simple Python scripts without frameworks:
- Load `memory/common_issues.md`
- Focus on code quality, error handling, and general best practices

---

## Summary Decision Tree

```
START
  |
  v
Check imports for framework patterns
  |
  +-- Django detected? → Load django_patterns.md
  +-- Flask detected? → Load flask_patterns.md
  +-- FastAPI detected? → Load fastapi_patterns.md
  +-- Pandas/NumPy detected? → Load datascience_patterns.md
  +-- Torch/TF/sklearn detected? → Load ml_patterns.md
  +-- None detected → Use common_issues.md only
  |
  v
ALWAYS load common_issues.md
  |
  v
Proceed with review
```

## File Loading Commands

When frameworks are detected, read the appropriate files:

```
Django → Read memory/django_patterns.md
Flask → Read memory/flask_patterns.md
FastAPI → Read memory/fastapi_patterns.md
Data Science → Read memory/datascience_patterns.md
ML → Read memory/ml_patterns.md
Always → Read memory/common_issues.md
```

For security-focused reviews, additionally read:
- `context/security_guidelines.md`
- `context/owasp_python.md`

For style reviews, additionally read:
- `context/pep8_standards.md`
