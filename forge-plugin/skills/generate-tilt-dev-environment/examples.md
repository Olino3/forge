# Tilt Development Environment Generation Examples

This file demonstrates typical usage scenarios for the `generate-tilt-dev-environment` skill.

---

## Example 1: Simple Full-Stack Application (React + Python API)

### User Request

"I need to set up a local development environment for my full-stack app. I have a React frontend and a Python Flask API, with a PostgreSQL database."

### Skill Execution

**Step 1-4**: Load context and understand development patterns.

**Step 5: Requirements Gathering**

Claude asks:
- **Project type?** → Full-stack application
- **Services to containerize?** → Frontend (React), Backend (Flask), Database (PostgreSQL)
- **Programming languages?** → Node.js 20 (frontend), Python 3.11 (backend)
- **Database?** → PostgreSQL 15
- **Development dependencies?** → npm for frontend, pip for backend
- **Port configuration?** → Frontend: 3000, Backend: 8000, PostgreSQL: 5432
- **Environment variables?** → DATABASE_URL, API_URL, SECRET_KEY
- **Live reload?** → Yes for both frontend and backend

**Step 6: Project Generation**

Generated structure:
```
my-fullstack-app/
├── .docker/
│   ├── frontend/
│   │   └── Dockerfile
│   ├── backend/
│   │   └── Dockerfile
│   └── scripts/
│       └── init_db.sh
├── docker-compose.yml
├── Tiltfile
├── Makefile
├── .env.example
├── .env
├── .dockerignore
├── .gitignore
└── README.md
```

**Tiltfile** (generated):
```python
# Load environment variables
load('ext://dotenv', 'dotenv')
dotenv()

# Build and watch frontend
docker_build(
    'frontend',
    context='./frontend',
    dockerfile='.docker/frontend/Dockerfile',
    live_update=[
        sync('./frontend/src', '/app/src'),
        sync('./frontend/public', '/app/public'),
        run('npm install', trigger='./frontend/package.json'),
    ]
)

# Build and watch backend
docker_build(
    'backend',
    context='./backend',
    dockerfile='.docker/backend/Dockerfile',
    live_update=[
        sync('./backend/app', '/app/app'),
        run('pip install -r requirements.txt', trigger='./backend/requirements.txt'),
        restart_container()
    ]
)

# Deploy services
docker_compose('./docker-compose.yml')

# Define resources
k8s_resource('postgres', labels=['database'], port_forwards=5432)
k8s_resource('backend', labels=['api'], port_forwards=8000, resource_deps=['postgres'])
k8s_resource('frontend', labels=['web'], port_forwards=3000, resource_deps=['backend'])
```

**docker-compose.yml** (generated):
```yaml
version: '3.8'

services:
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: ${DB_NAME:-myapp}
      POSTGRES_USER: ${DB_USER:-postgres}
      POSTGRES_PASSWORD: ${DB_PASSWORD:-postgres}
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./.docker/scripts/init_db.sh:/docker-entrypoint-initdb.d/init.sh
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      timeout: 5s
      retries: 5

  backend:
    build:
      context: ./backend
      dockerfile: ../.docker/backend/Dockerfile
    environment:
      DATABASE_URL: postgresql://${DB_USER:-postgres}:${DB_PASSWORD:-postgres}@postgres:5432/${DB_NAME:-myapp}
      SECRET_KEY: ${SECRET_KEY:-dev-secret-key}
      FLASK_ENV: development
    ports:
      - "8000:8000"
    volumes:
      - ./backend:/app
    depends_on:
      postgres:
        condition: service_healthy
    command: flask run --host=0.0.0.0 --port=8000 --reload

  frontend:
    build:
      context: ./frontend
      dockerfile: ../.docker/frontend/Dockerfile
    environment:
      REACT_APP_API_URL: http://localhost:8000
    ports:
      - "3000:3000"
    volumes:
      - ./frontend/src:/app/src
      - ./frontend/public:/app/public
      - /app/node_modules
    depends_on:
      - backend
    command: npm start

volumes:
  postgres_data:
```

**Makefile** (generated):
```makefile
.PHONY: up down logs clean rebuild shell-backend shell-frontend shell-db

up:
	tilt up

down:
	tilt down

logs:
	tilt logs

clean:
	docker-compose down -v
	docker system prune -f

rebuild:
	tilt down
	docker-compose build --no-cache
	tilt up

shell-backend:
	docker-compose exec backend /bin/bash

shell-frontend:
	docker-compose exec frontend /bin/sh

shell-db:
	docker-compose exec postgres psql -U postgres -d myapp
```

**Step 8: User Instructions**

```bash
# Copy environment template
cp .env.example .env

# Start development environment
make up
# or
tilt up

# Access services:
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# PostgreSQL: localhost:5432
# Tilt UI: http://localhost:10350
```

---

## Example 2: Microservices Architecture

### User Request

"I have a microservices project with 3 services: user-service (Node.js), order-service (Python), and payment-service (Go). They all need Redis for caching and MongoDB for storage."

### Requirements Gathering

- **Project type**: Microservices architecture
- **Services**: 3 application services + Redis + MongoDB
- **Languages**: Node.js 18, Python 3.11, Go 1.21
- **Dependencies**: Redis 7, MongoDB 6
- **Ports**: User: 3001, Order: 3002, Payment: 3003, Redis: 6379, MongoDB: 27017

### Generated Structure

```
microservices-app/
├── .docker/
│   ├── user-service/Dockerfile
│   ├── order-service/Dockerfile
│   ├── payment-service/Dockerfile
│   └── scripts/
│       └── init_mongo.js
├── docker-compose.yml
├── Tiltfile
├── Makefile
├── .env.example
└── README.md
```

**Tiltfile** (key sections):
```python
# User Service (Node.js)
docker_build(
    'user-service',
    context='./user-service',
    dockerfile='.docker/user-service/Dockerfile',
    live_update=[
        sync('./user-service/src', '/app/src'),
        run('npm install', trigger='./user-service/package.json'),
        restart_container()
    ]
)

# Order Service (Python)
docker_build(
    'order-service',
    context='./order-service',
    dockerfile='.docker/order-service/Dockerfile',
    live_update=[
        sync('./order-service/app', '/app/app'),
        run('pip install -r requirements.txt', trigger='./order-service/requirements.txt'),
        restart_container()
    ]
)

# Payment Service (Go)
docker_build(
    'payment-service',
    context='./payment-service',
    dockerfile='.docker/payment-service/Dockerfile',
    live_update=[
        sync('./payment-service', '/go/src/app'),
        run('go build -o /app/server .', trigger=['./payment-service/*.go', './payment-service/go.mod']),
        restart_container()
    ]
)

docker_compose('./docker-compose.yml')

# Resource definitions with dependencies
k8s_resource('redis', labels=['cache'], port_forwards=6379)
k8s_resource('mongodb', labels=['database'], port_forwards=27017)
k8s_resource('user-service', labels=['microservice'], port_forwards=3001, resource_deps=['redis', 'mongodb'])
k8s_resource('order-service', labels=['microservice'], port_forwards=3002, resource_deps=['redis', 'mongodb'])
k8s_resource('payment-service', labels=['microservice'], port_forwards=3003, resource_deps=['redis', 'mongodb'])
```

---

## Example 3: Data Pipeline with Apache Kafka

### User Request

"I need to develop a data pipeline that reads from Kafka, processes with Python, and writes to Elasticsearch. I also need Kibana for visualization."

### Requirements Gathering

- **Project type**: Data pipeline
- **Services**: Python processor, Kafka, Zookeeper, Elasticsearch, Kibana
- **Language**: Python 3.11
- **Data flow**: Kafka → Python Processor → Elasticsearch
- **Ports**: Kafka: 9092, Elasticsearch: 9200, Kibana: 5601, Processor: 8080

### Generated Tiltfile

```python
# Kafka ecosystem
docker_compose('./docker-compose.yml')

# Python processor with live reload
docker_build(
    'data-processor',
    context='./processor',
    dockerfile='.docker/processor/Dockerfile',
    live_update=[
        sync('./processor/src', '/app/src'),
        run('pip install -r requirements.txt', trigger='./processor/requirements.txt'),
        restart_container()
    ]
)

# Resource definitions with proper dependencies
k8s_resource('zookeeper', labels=['infrastructure'])
k8s_resource('kafka', labels=['messaging'], port_forwards=9092, resource_deps=['zookeeper'])
k8s_resource('elasticsearch', labels=['search'], port_forwards=9200)
k8s_resource('kibana', labels=['visualization'], port_forwards=5601, resource_deps=['elasticsearch'])
k8s_resource('processor', labels=['pipeline'], port_forwards=8080, resource_deps=['kafka', 'elasticsearch'])

# Custom button to send test message
local_resource(
    'send-test-message',
    cmd='python scripts/send_test_message.py',
    labels=['tools'],
    trigger_mode=TRIGGER_MODE_MANUAL,
    resource_deps=['kafka']
)
```

---

## Example 4: Development with External Dependencies

### User Request

"I'm building a Django app that needs to connect to an external service mock for testing, plus local PostgreSQL and Redis."

### Requirements Gathering

- **Project type**: Web application
- **Main service**: Django (Python 3.11)
- **Dependencies**: PostgreSQL, Redis, Mock external API
- **Special needs**: Mock service for third-party API

### Generated docker-compose.yml

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: django_db
      POSTGRES_USER: django
      POSTGRES_PASSWORD: django
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  # Mock external payment API
  payment-api-mock:
    build:
      context: ./mocks/payment-api
      dockerfile: Dockerfile
    ports:
      - "8001:8000"
    environment:
      MOCK_MODE: true
      MOCK_DELAY_MS: 100

  django:
    build:
      context: ./
      dockerfile: .docker/django/Dockerfile
    environment:
      DATABASE_URL: postgresql://django:django@postgres:5432/django_db
      REDIS_URL: redis://redis:6379/0
      PAYMENT_API_URL: http://payment-api-mock:8000
      DJANGO_DEBUG: "true"
    ports:
      - "8000:8000"
    volumes:
      - ./app:/app
    depends_on:
      - postgres
      - redis
      - payment-api-mock
    command: python manage.py runserver 0.0.0.0:8000

volumes:
  postgres_data:
```

---

## Example 5: Mobile Backend with Multiple Databases

### User Request

"I need to set up a backend for a mobile app. It uses Express.js, PostgreSQL for relational data, MongoDB for user sessions, and Redis for caching."

### Requirements Gathering

- **Project type**: Mobile app backend
- **Service**: Express.js API (Node.js 20)
- **Databases**: PostgreSQL 15, MongoDB 6, Redis 7
- **Ports**: API: 3000, PostgreSQL: 5432, MongoDB: 27017, Redis: 6379

### Generated Tiltfile

```python
docker_compose('./docker-compose.yml')

docker_build(
    'api',
    context='./api',
    dockerfile='.docker/api/Dockerfile',
    live_update=[
        sync('./api/src', '/app/src'),
        run('npm install', trigger='./api/package.json'),
        restart_container()
    ]
)

# Resource organization
k8s_resource('postgres', labels=['database'], port_forwards=5432)
k8s_resource('mongodb', labels=['database'], port_forwards=27017)
k8s_resource('redis', labels=['cache'], port_forwards=6379)
k8s_resource('api', labels=['backend'], port_forwards=3000, 
             resource_deps=['postgres', 'mongodb', 'redis'])

# Custom health check button
local_resource(
    'health-check',
    cmd='curl http://localhost:3000/health',
    labels=['tools'],
    trigger_mode=TRIGGER_MODE_MANUAL,
    resource_deps=['api']
)

# Database migration runner
local_resource(
    'run-migrations',
    cmd='docker-compose exec -T api npm run migrate',
    labels=['tools'],
    trigger_mode=TRIGGER_MODE_MANUAL,
    resource_deps=['api']
)
```

**Makefile additions**:
```makefile
migrate:
	docker-compose exec api npm run migrate

seed:
	docker-compose exec api npm run seed

health:
	curl http://localhost:3000/health

test:
	docker-compose exec api npm test
```

---

## Example 6: Legacy Application Modernization

### User Request

"I have a legacy Java Spring Boot app and a .NET Core app that need to run together during a migration period."

### Requirements Gathering

- **Project type**: Legacy modernization
- **Services**: Java Spring Boot (legacy), .NET Core (new), MySQL (shared)
- **Languages**: Java 17, .NET 8
- **Database**: MySQL 8
- **Special needs**: Both apps access same database during transition

### Generated Tiltfile

```python
docker_compose('./docker-compose.yml')

# Legacy Java app
docker_build(
    'legacy-app',
    context='./legacy-app',
    dockerfile='.docker/legacy-app/Dockerfile',
    live_update=[
        sync('./legacy-app/src', '/app/src'),
        run('mvn compile', trigger='./legacy-app/pom.xml')
    ]
)

# New .NET app
docker_build(
    'new-app',
    context='./new-app',
    dockerfile='.docker/new-app/Dockerfile',
    live_update=[
        sync('./new-app', '/app'),
        run('dotnet restore', trigger='./new-app/*.csproj'),
        run('dotnet build', trigger=['./new-app/**/*.cs', './new-app/*.csproj'])
    ]
)

k8s_resource('mysql', labels=['database'], port_forwards=3306)
k8s_resource('legacy-app', labels=['java'], port_forwards=8080, resource_deps=['mysql'])
k8s_resource('new-app', labels=['dotnet'], port_forwards=5000, resource_deps=['mysql'])

# Add comparison tool
local_resource(
    'compare-responses',
    cmd='python scripts/compare_api_responses.py',
    labels=['testing'],
    trigger_mode=TRIGGER_MODE_MANUAL,
    resource_deps=['legacy-app', 'new-app']
)
```

---

## Common Patterns

### Pattern 1: Multi-Environment Support

Add environment-specific docker-compose files:

```
docker-compose.yml           # Base configuration
docker-compose.dev.yml       # Development overrides
docker-compose.test.yml      # Testing overrides
docker-compose.prod.yml      # Production configuration
```

Tiltfile selection:
```python
config_file = os.getenv('ENV', 'dev')
docker_compose(f'./docker-compose.{config_file}.yml')
```

### Pattern 2: Shared Development Libraries

For projects with shared libraries:

```python
docker_build(
    'service-a',
    context='.',
    dockerfile='services/service-a/Dockerfile',
    live_update=[
        sync('./shared-lib', '/app/shared-lib'),
        sync('./services/service-a', '/app/service-a'),
        run('pip install -e /app/shared-lib', trigger='./shared-lib/setup.py')
    ]
)
```

### Pattern 3: Database Seeding

Add init resources:

```python
local_resource(
    'init-database',
    cmd='docker-compose exec -T db psql -U postgres < scripts/seed.sql',
    resource_deps=['postgres'],
    labels=['init']
)
```

---

## Tips for Using Generated Environments

1. **Start with `make up`**: Easier than remembering tilt commands
2. **Use Tilt UI**: Visual dashboard at http://localhost:10350
3. **Check logs**: `make logs` or click service in Tilt UI
4. **Rebuild when needed**: `make rebuild` for fresh start
5. **Exec into containers**: `make shell-<service>` for debugging
6. **Clean regularly**: `make clean` to remove old volumes/containers
7. **Update .env**: Copy .env.example and customize for your setup
8. **Read README**: Generated documentation has environment-specific info
