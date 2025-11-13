# Python Code Review Examples

This file contains example code review scenarios demonstrating common issues and recommended fixes.

## Example 1: Security Vulnerability - SQL Injection

### Before (Vulnerable Code)

```python
# user_service.py:15
def get_user_by_email(email):
    query = f"SELECT * FROM users WHERE email = '{email}'"
    cursor.execute(query)
    return cursor.fetchone()
```

### Review Comment

**Severity**: Critical
**Category**: Security
**File**: user_service.py:16

SQL injection vulnerability detected. User input is directly interpolated into SQL query, allowing attackers to execute arbitrary SQL commands.

**Attack example**:
```python
email = "'; DROP TABLE users; --"
# Results in: SELECT * FROM users WHERE email = ''; DROP TABLE users; --'
```

### After (Fixed Code)

```python
# user_service.py:15
def get_user_by_email(email):
    query = "SELECT * FROM users WHERE email = %s"
    cursor.execute(query, (email,))
    return cursor.fetchone()
```

**Reference**: OWASP A03:2021 - Injection

---

## Example 2: Performance Issue - N+1 Query Problem (Django)

### Before (Inefficient Code)

```python
# views.py:45
def get_posts_with_authors(request):
    posts = Post.objects.all()  # 1 query
    result = []
    for post in posts:
        result.append({
            'title': post.title,
            'author': post.author.name  # N additional queries!
        })
    return JsonResponse(result, safe=False)
```

### Review Comment

**Severity**: Important
**Category**: Performance
**File**: views.py:48

N+1 query problem detected. For 100 posts, this executes 101 database queries (1 for posts + 100 for authors). This causes severe performance degradation under load.

### After (Optimized Code)

```python
# views.py:45
def get_posts_with_authors(request):
    posts = Post.objects.select_related('author').all()  # 1 query with JOIN
    result = []
    for post in posts:
        result.append({
            'title': post.title,
            'author': post.author.name
        })
    return JsonResponse(result, safe=False)
```

**Performance gain**: 101 queries → 1 query (100x improvement for 100 posts)

**Reference**: Django QuerySet optimization

---

## Example 3: Code Quality - Mutable Default Argument

### Before (Buggy Code)

```python
# utils.py:22
def add_item(item, items=[]):
    items.append(item)
    return items

# Usage that reveals the bug:
list1 = add_item('a')  # ['a']
list2 = add_item('b')  # ['a', 'b'] - UNEXPECTED!
```

### Review Comment

**Severity**: Important
**Category**: Code Quality
**File**: utils.py:22

Mutable default argument antipattern. The default list `[]` is created once when the function is defined, not each time it's called. All invocations share the same list object, causing unexpected state persistence.

### After (Fixed Code)

```python
# utils.py:22
def add_item(item, items=None):
    if items is None:
        items = []
    items.append(item)
    return items

# Now works correctly:
list1 = add_item('a')  # ['a']
list2 = add_item('b')  # ['b'] - CORRECT!
```

**Reference**: Common Python Gotchas

---

## Example 4: PEP 8 Compliance - Naming Conventions

### Before (Non-compliant Code)

```python
# data_processor.py:10
def CalculateUserAge(BirthDate):
    CurrentYear = 2025
    user_birth_year = BirthDate.year
    AGE = CurrentYear - user_birth_year
    return AGE
```

### Review Comment

**Severity**: Minor
**Category**: Style
**File**: data_processor.py:10-15

Multiple PEP 8 naming violations:
- Function name should be `snake_case`, not `PascalCase`
- Parameter name should be `snake_case`, not `PascalCase`
- Local variables should be lowercase, not mixed case or UPPERCASE
- UPPERCASE is reserved for constants

### After (Compliant Code)

```python
# data_processor.py:10
def calculate_user_age(birth_date):
    current_year = 2025
    user_birth_year = birth_date.year
    age = current_year - user_birth_year
    return age
```

**Reference**: PEP 8 - Naming Conventions

---

## Example 5: Best Practice - Context Manager for Resource Handling

### Before (Resource Leak Risk)

```python
# file_processor.py:30
def process_log_file(filepath):
    file = open(filepath, 'r')
    data = file.read()
    results = analyze(data)
    file.close()  # May not execute if analyze() raises exception
    return results
```

### Review Comment

**Severity**: Important
**Category**: Best Practices
**File**: file_processor.py:31

Missing context manager for file handling. If `analyze()` raises an exception, `file.close()` never executes, leaving the file handle open (resource leak).

### After (Safe Code)

```python
# file_processor.py:30
def process_log_file(filepath):
    with open(filepath, 'r') as file:
        data = file.read()
        results = analyze(data)
    # File automatically closed even if exception occurs
    return results
```

**Bonus improvement**:
```python
# Even better with pathlib
from pathlib import Path

def process_log_file(filepath):
    data = Path(filepath).read_text()
    return analyze(data)
```

**Reference**: PEP 343 - The "with" Statement

---

## Example 6: Security - Hardcoded Credentials

### Before (Security Risk)

```python
# config.py:5
DATABASE_CONFIG = {
    'host': 'prod-db.example.com',
    'user': 'admin',
    'password': 'SuperSecret123!',  # NEVER do this
    'database': 'production'
}
```

### Review Comment

**Severity**: Critical
**Category**: Security
**File**: config.py:8

Hardcoded credentials detected. Passwords in source code:
1. Are visible to anyone with repository access
2. Get committed to version control history
3. Can't be rotated without code changes
4. May be exposed in logs or error messages

### After (Secure Code)

```python
# config.py:5
import os

DATABASE_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME', 'production')
}

# Validate required environment variables
required_vars = ['DB_USER', 'DB_PASSWORD']
missing = [var for var in required_vars if not os.getenv(var)]
if missing:
    raise RuntimeError(f"Missing required environment variables: {missing}")
```

**Additional security**:
```bash
# Use environment files (not committed to git)
echo "DB_PASSWORD=..." > .env
echo ".env" >> .gitignore
```

**Reference**: OWASP A07:2021 - Identification and Authentication Failures

---

## Example 7: Performance - Pandas Optimization

### Before (Inefficient Code)

```python
# data_analysis.py:50
import pandas as pd

def calculate_discounts(df):
    # Anti-pattern: Iterating over DataFrame rows
    discounts = []
    for index, row in df.iterrows():
        if row['total'] > 100:
            discount = row['total'] * 0.1
        else:
            discount = 0
        discounts.append(discount)
    df['discount'] = discounts
    return df
```

### Review Comment

**Severity**: Important
**Category**: Performance
**File**: data_analysis.py:53

Using `iterrows()` on DataFrame - this is one of the slowest operations in pandas. For 10,000 rows, this can be 100x slower than vectorized operations.

### After (Vectorized Code)

```python
# data_analysis.py:50
import pandas as pd

def calculate_discounts(df):
    # Vectorized operation - operates on entire column at once
    df['discount'] = (df['total'] * 0.1).where(df['total'] > 100, 0)
    return df

# Alternative using numpy where:
import numpy as np

def calculate_discounts(df):
    df['discount'] = np.where(df['total'] > 100, df['total'] * 0.1, 0)
    return df
```

**Performance**: Vectorized operations use optimized C code, achieving 50-100x speedup on large datasets.

**Reference**: Pandas Performance Optimization

---

## Example 8: Testing - Missing Edge Cases

### Before (Incomplete Tests)

```python
# test_validators.py:15
def test_email_validation():
    assert is_valid_email('user@example.com') == True
    assert is_valid_email('invalid-email') == False
```

### Review Comment

**Severity**: Important
**Category**: Testing
**File**: test_validators.py:15

Email validation tests are insufficient. Missing edge cases:
- Empty string
- None value
- Email with special characters
- Multiple @ symbols
- Missing domain
- Whitespace handling
- Maximum length validation

### After (Comprehensive Tests)

```python
# test_validators.py:15
import pytest

@pytest.mark.parametrize('email,expected', [
    # Valid emails
    ('user@example.com', True),
    ('first.last@example.co.uk', True),
    ('user+tag@example.com', True),

    # Invalid emails
    ('invalid-email', False),
    ('', False),
    ('user@', False),
    ('user@@example.com', False),
    ('@example.com', False),
    ('user @example.com', False),
    ('a' * 256 + '@example.com', False),  # Too long
])
def test_email_validation(email, expected):
    assert is_valid_email(email) == expected

def test_email_validation_with_none():
    with pytest.raises(TypeError):
        is_valid_email(None)
```

**Reference**: Testing Best Practices

---

## Example 9: Architecture - Separation of Concerns (FastAPI)

### Before (Tightly Coupled Code)

```python
# main.py:25
from fastapi import FastAPI
import psycopg2

app = FastAPI()

@app.get('/users/{user_id}')
def get_user(user_id: int):
    # Business logic mixed with data access and presentation
    conn = psycopg2.connect("dbname=mydb user=admin password=secret")
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")
    user = cursor.fetchone()
    conn.close()

    if user:
        return {'id': user[0], 'name': user[1], 'email': user[2]}
    return {'error': 'User not found'}
```

### Review Comment

**Severity**: Important
**Category**: Architecture
**File**: main.py:25-38

Multiple violations of separation of concerns:
1. Database connection logic in route handler
2. SQL injection vulnerability
3. Hardcoded credentials
4. No error handling
5. Manual dict construction
6. No dependency injection

### After (Layered Architecture)

```python
# models.py
from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str
    email: str

# database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

SQLALCHEMY_DATABASE_URL = os.getenv('DATABASE_URL')
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# repositories.py
from sqlalchemy.orm import Session
from . import models

class UserRepository:
    def get_by_id(self, db: Session, user_id: int):
        return db.query(models.User).filter(models.User.id == user_id).first()

# main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, database, repositories

app = FastAPI()
user_repo = UserRepository()

@app.get('/users/{user_id}', response_model=models.User)
def get_user(user_id: int, db: Session = Depends(database.get_db)):
    user = user_repo.get_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    return user
```

**Benefits**:
- Clear separation of concerns
- Dependency injection
- Type safety with Pydantic
- SQL injection protection via ORM
- Reusable repository pattern
- Proper error handling

**Reference**: FastAPI Best Practices, Repository Pattern

---

## Summary of Common Issues

1. **Security**: SQL injection, XSS, hardcoded credentials, insecure cryptography
2. **Performance**: N+1 queries, inefficient loops, missing indexes, no caching
3. **Code Quality**: Mutable defaults, global state, poor naming, missing docstrings
4. **Style**: PEP 8 violations, inconsistent formatting, magic numbers
5. **Best Practices**: Missing context managers, no type hints, poor error handling
6. **Testing**: Insufficient coverage, missing edge cases, no integration tests
7. **Architecture**: Tight coupling, mixed concerns, no dependency injection

Use these examples as reference when conducting reviews. Adapt the feedback style and technical depth to the codebase context.
