# FastAPI Patterns and Best Practices

This file contains FastAPI-specific patterns, anti-patterns, and best practices for code review.

## Pydantic Models and Type Safety

### Request/Response Models

**Good Pattern**:
```python
from pydantic import BaseModel, Field, validator, EmailStr
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8)
    age: Optional[int] = Field(None, ge=0, le=150)

    @validator('username')
    def username_alphanumeric(cls, v):
        assert v.isalnum(), 'must be alphanumeric'
        return v

    class Config:
        schema_extra = {
            "example": {
                "username": "johndoe",
                "email": "john@example.com",
                "password": "secretpassword",
                "age": 30
            }
        }

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime

    class Config:
        orm_mode = True  # For SQLAlchemy models

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    age: Optional[int] = Field(None, ge=0, le=150)
```

**Anti-Pattern**:
```python
# WRONG - No validation
@app.post("/users")
def create_user(data: dict):
    # No type checking, no validation!
    username = data.get('username')
    return {"id": 1}

# WRONG - Exposing internal model
@app.get("/users/{user_id}")
def get_user(user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    return user  # Returns SQLAlchemy model with password_hash!
```

---

## Dependency Injection

### Database Session Management

**Good Pattern**:
```python
from sqlalchemy.orm import Session
from fastapi import Depends

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/users/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
```

### Authentication Dependencies

**Good Pattern**:
```python
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise credentials_exception
    return user

def get_current_active_user(current_user: User = Depends(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

# Usage
@app.get("/users/me")
def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user
```

### Reusable Dependencies

**Good Pattern**:
```python
# Common query parameters
class CommonQueryParams:
    def __init__(
        self,
        skip: int = 0,
        limit: int = 100,
        sort_by: Optional[str] = None
    ):
        self.skip = skip
        self.limit = limit
        self.sort_by = sort_by

@app.get("/users")
def list_users(
    commons: CommonQueryParams = Depends(),
    db: Session = Depends(get_db)
):
    query = db.query(User).offset(commons.skip).limit(commons.limit)
    if commons.sort_by:
        query = query.order_by(commons.sort_by)
    return query.all()
```

---

## Async/Await Patterns

### When to Use Async

**Good Pattern - I/O-bound operations**:
```python
import httpx
from fastapi import FastAPI

app = FastAPI()

@app.get("/fetch-data")
async def fetch_external_data():
    async with httpx.AsyncClient() as client:
        response = await client.get("https://api.example.com/data")
        return response.json()

# Database operations with async driver
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

@app.get("/users/{user_id}")
async def get_user(user_id: int, db: AsyncSession = Depends(get_async_db)):
    result = await db.execute(select(User).filter(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
```

**Anti-Pattern - Mixing sync and async incorrectly**:
```python
# WRONG - Blocking I/O in async function
@app.get("/slow")
async def slow_endpoint():
    time.sleep(5)  # Blocks the event loop!
    return {"message": "Done"}

# WRONG - Not awaiting async functions
@app.get("/fetch")
async def fetch():
    response = httpx.AsyncClient().get("https://api.example.com")  # Not awaited!
    return response

# CORRECT - Use run_in_threadpool for blocking operations
from fastapi.concurrency import run_in_threadpool

@app.get("/cpu-intensive")
async def cpu_intensive():
    result = await run_in_threadpool(blocking_cpu_operation)
    return {"result": result}
```

---

## Path Operations and Routing

### Path Parameters with Validation

**Good Pattern**:
```python
from fastapi import Path, Query

@app.get("/users/{user_id}")
def get_user(
    user_id: int = Path(..., gt=0, description="The ID of the user to retrieve")
):
    return {"user_id": user_id}

@app.get("/items/")
def list_items(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, gt=0, le=1000),
    search: Optional[str] = Query(None, min_length=3, max_length=50)
):
    return {"skip": skip, "limit": limit, "search": search}
```

### Router Organization

**Good Pattern**:
```python
# routers/users.py
from fastapi import APIRouter, Depends

router = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[Depends(get_current_user)]
)

@router.get("/")
def list_users():
    return {"users": []}

@router.get("/{user_id}")
def get_user(user_id: int):
    return {"user_id": user_id}

@router.post("/")
def create_user(user: UserCreate):
    return {"user": user}

# main.py
from routers import users, items, auth

app = FastAPI()
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(items.router, prefix="/api/v1")
```

---

## Exception Handling

### Custom Exception Handlers

**Good Pattern**:
```python
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError

class ItemNotFoundException(Exception):
    def __init__(self, item_id: int):
        self.item_id = item_id

@app.exception_handler(ItemNotFoundException)
async def item_not_found_handler(request: Request, exc: ItemNotFoundException):
    return JSONResponse(
        status_code=404,
        content={"message": f"Item {exc.item_id} not found"}
    )

@app.exception_handler(IntegrityError)
async def integrity_error_handler(request: Request, exc: IntegrityError):
    return JSONResponse(
        status_code=400,
        content={"message": "Database integrity error", "detail": str(exc)}
    )

# Usage in routes
@app.get("/items/{item_id}")
def get_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise ItemNotFoundException(item_id)
    return item
```

---

## Background Tasks

**Good Pattern**:
```python
from fastapi import BackgroundTasks

def send_email(email: str, message: str):
    # Simulate sending email
    print(f"Sending email to {email}: {message}")

@app.post("/users/")
async def create_user(
    user: UserCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    # Create user
    db_user = User(**user.dict())
    db.add(db_user)
    db.commit()

    # Send welcome email in background
    background_tasks.add_task(send_email, user.email, "Welcome!")

    return db_user
```

**Anti-Pattern**:
```python
# WRONG - Long-running task blocks response
@app.post("/process")
async def process_data(data: dict):
    result = expensive_computation(data)  # Takes 30 seconds!
    return {"result": result}

# CORRECT - Use background task or Celery
@app.post("/process")
async def process_data(data: dict, background_tasks: BackgroundTasks):
    task_id = generate_task_id()
    background_tasks.add_task(expensive_computation, data, task_id)
    return {"task_id": task_id, "status": "processing"}
```

---

## Security Patterns

### Password Hashing

**Good Pattern**:
```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

@app.post("/users/")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    hashed_password = hash_password(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    return {"username": user.username}
```

### JWT Authentication

**Good Pattern**:
```python
from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@app.post("/token")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
```

### CORS Configuration

**Good Pattern**:
```python
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Development - permissive
if settings.ENVIRONMENT == "development":
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
else:
    # Production - restrictive
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["https://yourdomain.com"],
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE"],
        allow_headers=["Authorization", "Content-Type"],
    )
```

**Anti-Pattern**:
```python
# WRONG - Allow all origins in production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Security risk!
    allow_credentials=True,
)
```

---

## Database Patterns

### Avoiding N+1 Queries

**Anti-Pattern**:
```python
# WRONG - N+1 queries
@app.get("/posts")
def list_posts(db: Session = Depends(get_db)):
    posts = db.query(Post).all()
    result = []
    for post in posts:
        result.append({
            "title": post.title,
            "author": post.author.name,  # N additional queries!
            "category": post.category.name  # N more queries!
        })
    return result
```

**Good Pattern**:
```python
# CORRECT - Eager loading
from sqlalchemy.orm import joinedload

@app.get("/posts", response_model=List[PostResponse])
def list_posts(db: Session = Depends(get_db)):
    posts = db.query(Post)\
        .options(joinedload(Post.author))\
        .options(joinedload(Post.category))\
        .all()
    return posts
```

### Transaction Management

**Good Pattern**:
```python
from fastapi import HTTPException

@app.post("/transfer")
def transfer_money(
    transfer: TransferRequest,
    db: Session = Depends(get_db)
):
    try:
        # Debit from sender
        sender = db.query(Account).filter(Account.id == transfer.from_id).first()
        if sender.balance < transfer.amount:
            raise HTTPException(status_code=400, detail="Insufficient funds")

        sender.balance -= transfer.amount

        # Credit to recipient
        recipient = db.query(Account).filter(Account.id == transfer.to_id).first()
        recipient.balance += transfer.amount

        db.commit()
        return {"status": "success"}

    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Transfer failed: {e}")
        raise HTTPException(status_code=500, detail="Transfer failed")
```

---

## Response Model Patterns

### Response Model with ORM

**Good Pattern**:
```python
from pydantic import BaseModel
from typing import List

class AuthorResponse(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True

class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    author: AuthorResponse

    class Config:
        orm_mode = True

@app.get("/posts/{post_id}", response_model=PostResponse)
def get_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(Post)\
        .options(joinedload(Post.author))\
        .filter(Post.id == post_id)\
        .first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post  # Automatically converted to PostResponse
```

### Excluding Sensitive Fields

**Good Pattern**:
```python
class UserInDB(BaseModel):
    id: int
    username: str
    email: str
    hashed_password: str

    class Config:
        orm_mode = True

class UserPublic(BaseModel):
    id: int
    username: str
    # email and hashed_password excluded

    class Config:
        orm_mode = True

@app.get("/users/{user_id}", response_model=UserPublic)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    # Returns only id and username, hashed_password automatically excluded
    return user
```

---

## Middleware Patterns

**Good Pattern**:
```python
from fastapi import Request
import time

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"{request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Status: {response.status_code}")
    return response
```

---

## Testing Patterns

**Good Pattern**:
```python
from fastapi.testclient import TestClient
import pytest

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def test_db():
    # Setup test database
    Base.metadata.create_all(bind=engine)
    yield
    # Teardown
    Base.metadata.drop_all(bind=engine)

def test_create_user(client, test_db):
    response = client.post("/users/", json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpass123"
    })
    assert response.status_code == 201
    assert response.json()["username"] == "testuser"

def test_unauthorized_access(client):
    response = client.get("/users/me")
    assert response.status_code == 401
```

---

## Common FastAPI Anti-Patterns to Flag

- [ ] No Pydantic models (using dict instead)
- [ ] Returning ORM models with sensitive fields
- [ ] Blocking I/O in async functions
- [ ] Not awaiting async operations
- [ ] Allow all origins in CORS (production)
- [ ] No password hashing (storing plain text)
- [ ] Hardcoded SECRET_KEY
- [ ] N+1 database queries
- [ ] No error handling in database operations
- [ ] Long-running tasks blocking response
- [ ] No input validation on path/query parameters
- [ ] Missing response_model causing data leaks
- [ ] Not using dependency injection
- [ ] Mixing sync/async database operations incorrectly
- [ ] No authentication/authorization on protected routes

## Performance Best Practices

1. Use async for I/O-bound operations
2. Use `response_model` to avoid over-fetching
3. Implement pagination for list endpoints
4. Use database query optimization (select_related/joinedload)
5. Implement caching for expensive operations
6. Use background tasks for non-critical operations
7. Limit request body size
8. Use connection pooling

## References

- FastAPI Documentation: https://fastapi.tiangolo.com/
- Pydantic Documentation: https://pydantic-docs.helpmanual.io/
- SQLAlchemy Documentation: https://docs.sqlalchemy.org/
- FastAPI Best Practices: https://github.com/zhanymkanov/fastapi-best-practices
