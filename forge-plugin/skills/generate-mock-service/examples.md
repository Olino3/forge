# Mock Service Generation Examples

This file demonstrates typical usage scenarios for the `generate-mock-service` skill.

---

## Example 1: Simple REST API Mock (Payment Service)

### User Request

"I need to mock a payment service API for testing our checkout flow. It should have endpoints for creating payments and checking payment status."

### Skill Execution

**Step 1-4**: Load context and understand mocking patterns.

**Step 5: Requirements Gathering**

Claude asks:
- **Service to mock?** → External Payment API (Stripe-like)
- **Mock implementation type?** → Express.js (familiar to team)
- **Endpoints and methods?** → 
  - POST /api/payments (create payment)
  - GET /api/payments/:id (get payment status)
- **Response scenarios?** → Success, insufficient funds, invalid card
- **Data requirements?** → Realistic payment objects with IDs, amounts, status
- **Behavior configuration?** → 100ms delay to simulate network
- **Port?** → 8081
- **Authentication?** → API key validation (header: X-API-Key)

**Step 6: Mock Generation**

Generated structure:
```
mock-payment-service/
├── server.js
├── package.json
├── Dockerfile
├── .env.example
├── data/
│   ├── payments-success.json
│   ├── payments-error.json
│   └── cards.json
├── middleware/
│   └── auth.js
├── routes/
│   └── payments.js
├── utils/
│   ├── delay.js
│   └── faker.js
├── examples/
│   └── test-requests.sh
└── README.md
```

**server.js** (generated):
```javascript
const express = require('express');
const cors = require('cors');
const morgan = require('morgan');
const { authMiddleware } = require('./middleware/auth');
const paymentRoutes = require('./routes/payments');
const { delayMiddleware } = require('./utils/delay');

const app = express();
const PORT = process.env.PORT || 8081;

// Middleware
app.use(cors());
app.use(express.json());
app.use(morgan('dev'));
app.use(delayMiddleware(100)); // 100ms delay

// Authentication
app.use('/api', authMiddleware);

// Routes
app.use('/api/payments', paymentRoutes);

// Health check
app.get('/health', (req, res) => {
  res.json({ status: 'ok', service: 'mock-payment-service' });
});

app.listen(PORT, () => {
  console.log(`🎭 Mock Payment Service running on port ${PORT}`);
  console.log(`   POST http://localhost:${PORT}/api/payments`);
  console.log(`   GET  http://localhost:${PORT}/api/payments/:id`);
});
```

**routes/payments.js** (generated):
```javascript
const express = require('express');
const router = express.Router();
const { v4: uuidv4 } = require('uuid');

// In-memory storage
const payments = new Map();

// Create payment
router.post('/', (req, res) => {
  const { amount, currency, card, description } = req.body;
  
  // Validation
  if (!amount || !currency || !card) {
    return res.status(400).json({
      error: 'Missing required fields',
      details: 'amount, currency, and card are required'
    });
  }
  
  // Simulate card decline scenario
  if (card.number === '4000000000000002') {
    return res.status(402).json({
      error: 'card_declined',
      message: 'Your card was declined'
    });
  }
  
  // Simulate insufficient funds
  if (card.number === '4000000000009995') {
    return res.status(402).json({
      error: 'insufficient_funds',
      message: 'Your card has insufficient funds'
    });
  }
  
  // Success case
  const paymentId = `pay_${uuidv4().replace(/-/g, '')}`;
  const payment = {
    id: paymentId,
    amount,
    currency,
    status: 'succeeded',
    created: Date.now(),
    description: description || 'Payment',
    card: {
      last4: card.number.slice(-4),
      brand: card.brand || 'visa'
    }
  };
  
  payments.set(paymentId, payment);
  
  res.status(201).json(payment);
});

// Get payment by ID
router.get('/:id', (req, res) => {
  const { id } = req.params;
  
  const payment = payments.get(id);
  
  if (!payment) {
    return res.status(404).json({
      error: 'not_found',
      message: `Payment ${id} not found`
    });
  }
  
  res.json(payment);
});

module.exports = router;
```

**middleware/auth.js** (generated):
```javascript
const authMiddleware = (req, res, next) => {
  const apiKey = req.headers['x-api-key'];
  
  if (!apiKey) {
    return res.status(401).json({
      error: 'unauthorized',
      message: 'Missing API key'
    });
  }
  
  // Mock validation (accept any key in test mode)
  const validKeys = process.env.VALID_API_KEYS?.split(',') || ['test-key-123'];
  
  if (!validKeys.includes(apiKey)) {
    return res.status(403).json({
      error: 'forbidden',
      message: 'Invalid API key'
    });
  }
  
  next();
};

module.exports = { authMiddleware };
```

**examples/test-requests.sh**:
```bash
#!/bin/bash

API_KEY="test-key-123"
BASE_URL="http://localhost:8081"

echo "Testing Mock Payment Service"
echo "=============================="

# Test 1: Create successful payment
echo -e "\n1. Creating successful payment..."
curl -X POST "$BASE_URL/api/payments" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $API_KEY" \
  -d '{
    "amount": 5000,
    "currency": "usd",
    "card": {
      "number": "4242424242424242",
      "brand": "visa"
    },
    "description": "Test payment"
  }'

# Test 2: Create payment with declined card
echo -e "\n\n2. Creating payment with declined card..."
curl -X POST "$BASE_URL/api/payments" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $API_KEY" \
  -d '{
    "amount": 5000,
    "currency": "usd",
    "card": {
      "number": "4000000000000002"
    }
  }'

# Test 3: Get payment status
echo -e "\n\n3. Getting payment status..."
PAYMENT_ID="pay_123456"
curl "$BASE_URL/api/payments/$PAYMENT_ID" \
  -H "X-API-Key: $API_KEY"
```

**Step 8: User Instructions**

```bash
# Install and run locally
cd mock-payment-service
npm install
npm start

# Or run with Docker
docker build -t mock-payment-service .
docker run -p 8081:8081 -e VALID_API_KEYS=test-key-123 mock-payment-service

# Test the API
chmod +x examples/test-requests.sh
./examples/test-requests.sh
```

---

## Example 2: WireMock for Complex Scenarios

### User Request

"I need to mock our order management system API with multiple scenarios: successful orders, inventory out-of-stock, and partial fulfillment."

### Requirements Gathering

- **Service to mock**: Order Management System
- **Mock type**: WireMock (stateful scenarios)
- **Endpoints**: POST /orders, GET /orders/:id, PUT /orders/:id/status
- **Scenarios**: Success, out-of-stock, partial fulfillment
- **Port**: 8082

### Generated Structure

```
mock-order-service/
├── wiremock/
│   ├── mappings/
│   │   ├── create-order-success.json
│   │   ├── create-order-out-of-stock.json
│   │   ├── get-order.json
│   │   └── update-order-status.json
│   └── __files/
│       ├── order-success-response.json
│       ├── order-error-response.json
│       └── order-partial-response.json
├── Dockerfile
├── docker-compose.yml
└── README.md
```

**mappings/create-order-success.json**:
```json
{
  "request": {
    "method": "POST",
    "urlPathPattern": "/api/orders",
    "bodyPatterns": [
      {
        "matchesJsonPath": "$.items[?(@.quantity <= 10)]"
      }
    ]
  },
  "response": {
    "status": 201,
    "bodyFileName": "order-success-response.json",
    "headers": {
      "Content-Type": "application/json"
    },
    "fixedDelayMilliseconds": 200
  }
}
```

**mappings/create-order-out-of-stock.json**:
```json
{
  "request": {
    "method": "POST",
    "urlPathPattern": "/api/orders",
    "bodyPatterns": [
      {
        "matchesJsonPath": "$.items[?(@.sku == 'SKU-999')]"
      }
    ]
  },
  "response": {
    "status": 400,
    "bodyFileName": "order-error-response.json",
    "headers": {
      "Content-Type": "application/json"
    }
  },
  "priority": 1
}
```

**Dockerfile**:
```dockerfile
FROM wiremock/wiremock:latest

COPY wiremock /home/wiremock

EXPOSE 8082

CMD ["--port", "8082", "--verbose"]
```

**Usage**:
```bash
# Run with Docker
docker build -t mock-order-service .
docker run -p 8082:8082 mock-order-service

# Test successful order
curl -X POST http://localhost:8082/api/orders \
  -H "Content-Type: application/json" \
  -d '{"items": [{"sku": "SKU-123", "quantity": 5}]}'

# Test out-of-stock
curl -X POST http://localhost:8082/api/orders \
  -H "Content-Type: application/json" \
  -d '{"items": [{"sku": "SKU-999", "quantity": 1}]}'
```

---

## Example 3: FastAPI Mock with Faker Data

### User Request

"I need a mock user service that returns realistic user data with names, emails, addresses. It should support pagination and filtering."

### Requirements Gathering

- **Service to mock**: User Management API
- **Mock type**: FastAPI (Python, realistic data)
- **Endpoints**: GET /users, GET /users/:id, POST /users
- **Data**: Use Faker for realistic names, emails, addresses
- **Port**: 8083

### Generated Structure

```
mock-user-service/
├── main.py
├── models.py
├── faker_utils.py
├── requirements.txt
├── Dockerfile
└── README.md
```

**main.py**:
```python
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
import uvicorn

from models import User, UserCreate
from faker_utils import generate_user, get_user_by_id, create_user

app = FastAPI(title="Mock User Service", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "mock-user-service"}

@app.get("/users", response_model=List[User])
def list_users(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    role: Optional[str] = None
):
    """Get paginated list of users"""
    start = (page - 1) * limit
    end = start + limit
    
    # Generate users on-the-fly
    users = [generate_user(i) for i in range(start, end)]
    
    # Filter by role if provided
    if role:
        users = [u for u in users if u.role == role]
    
    return users

@app.get("/users/{user_id}", response_model=User)
def get_user(user_id: int):
    """Get user by ID"""
    user = get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.post("/users", response_model=User, status_code=201)
def create_user_endpoint(user_data: UserCreate):
    """Create new user"""
    user = create_user(user_data)
    return user

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8083)
```

**faker_utils.py**:
```python
from faker import Faker
from models import User
from datetime import datetime
import random

fake = Faker()
created_users = {}

def generate_user(user_id: int) -> User:
    """Generate a realistic user with Faker"""
    # Use seed for consistency
    Faker.seed(user_id)
    
    roles = ["admin", "user", "moderator", "guest"]
    
    return User(
        id=user_id,
        email=fake.email(),
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        phone=fake.phone_number(),
        address={
            "street": fake.street_address(),
            "city": fake.city(),
            "state": fake.state(),
            "zip": fake.postcode(),
            "country": fake.country()
        },
        role=random.choice(roles),
        created_at=fake.date_time_this_year().isoformat(),
        is_active=random.choice([True, True, True, False])  # 75% active
    )

def get_user_by_id(user_id: int) -> User:
    """Get user by ID (consistent)"""
    return generate_user(user_id)

def create_user(user_data) -> User:
    """Create a new user"""
    new_id = len(created_users) + 1000
    user = User(
        id=new_id,
        **user_data.dict(),
        created_at=datetime.now().isoformat(),
        is_active=True
    )
    created_users[new_id] = user
    return user
```

**Usage**:
```bash
# Install and run
pip install -r requirements.txt
python main.py

# Test endpoints
curl http://localhost:8083/users?page=1&limit=5
curl http://localhost:8083/users/42
curl -X POST http://localhost:8083/users \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "first_name": "John", "last_name": "Doe", "role": "user"}'
```

---

## Example 4: GraphQL API Mock

### User Request

"I need to mock a GraphQL API for our frontend team to develop against while the backend is being built."

### Requirements Gathering

- **Service to mock**: GraphQL API (blog platform)
- **Mock type**: Express with Apollo Server
- **Schema**: Posts, Authors, Comments
- **Port**: 4000

### Generated Structure

```
mock-graphql-service/
├── server.js
├── schema.js
├── resolvers.js
├── data/
│   ├── posts.json
│   ├── authors.json
│   └── comments.json
├── package.json
└── README.md
```

**schema.js**:
```javascript
const { gql } = require('apollo-server-express');

const typeDefs = gql`
  type Post {
    id: ID!
    title: String!
    content: String!
    author: Author!
    comments: [Comment!]!
    createdAt: String!
  }

  type Author {
    id: ID!
    name: String!
    email: String!
    posts: [Post!]!
  }

  type Comment {
    id: ID!
    text: String!
    author: Author!
    post: Post!
    createdAt: String!
  }

  type Query {
    posts: [Post!]!
    post(id: ID!): Post
    authors: [Author!]!
    author(id: ID!): Author
  }

  type Mutation {
    createPost(title: String!, content: String!, authorId: ID!): Post!
    createComment(postId: ID!, authorId: ID!, text: String!): Comment!
  }
`;

module.exports = typeDefs;
```

**resolvers.js**:
```javascript
const posts = require('./data/posts.json');
const authors = require('./data/authors.json');
const comments = require('./data/comments.json');

const resolvers = {
  Query: {
    posts: () => posts,
    post: (_, { id }) => posts.find(p => p.id === id),
    authors: () => authors,
    author: (_, { id }) => authors.find(a => a.id === id),
  },
  
  Post: {
    author: (post) => authors.find(a => a.id === post.authorId),
    comments: (post) => comments.filter(c => c.postId === post.id),
  },
  
  Author: {
    posts: (author) => posts.filter(p => p.authorId === author.id),
  },
  
  Comment: {
    author: (comment) => authors.find(a => a.id === comment.authorId),
    post: (comment) => posts.find(p => p.id === comment.postId),
  },
  
  Mutation: {
    createPost: (_, { title, content, authorId }) => {
      const newPost = {
        id: String(posts.length + 1),
        title,
        content,
        authorId,
        createdAt: new Date().toISOString(),
      };
      posts.push(newPost);
      return newPost;
    },
    
    createComment: (_, { postId, authorId, text }) => {
      const newComment = {
        id: String(comments.length + 1),
        postId,
        authorId,
        text,
        createdAt: new Date().toISOString(),
      };
      comments.push(newComment);
      return newComment;
    },
  },
};

module.exports = resolvers;
```

**Usage**:
```bash
npm install
npm start

# Access GraphQL Playground at http://localhost:4000/graphql

# Example query:
query {
  posts {
    id
    title
    author {
      name
    }
    comments {
      text
    }
  }
}
```

---

## Example 5: Prism Mock from OpenAPI Spec

### User Request

"We have an OpenAPI 3.0 spec for our inventory API. Can you create a mock that validates requests against it?"

### Requirements Gathering

- **Service to mock**: Inventory API
- **Mock type**: Prism (OpenAPI-based)
- **Spec**: User provides openapi.yaml
- **Port**: 8084

### Generated Structure

```
mock-inventory-service/
├── openapi.yaml
├── docker-compose.yml
├── README.md
└── examples/
    └── test-requests.sh
```

**docker-compose.yml**:
```yaml
version: '3.8'

services:
  prism:
    image: stoplight/prism:latest
    command: mock -h 0.0.0.0 /openapi.yaml
    ports:
      - "8084:4010"
    volumes:
      - ./openapi.yaml:/openapi.yaml:ro
    environment:
      - PRISM_LOG_LEVEL=info
```

**Usage**:
```bash
# Start Prism mock server
docker-compose up

# Prism automatically:
# - Validates requests against schema
# - Generates example responses
# - Supports dynamic responses based on spec

# Test endpoints
curl http://localhost:8084/inventory/items
curl http://localhost:8084/inventory/items/12345

# Invalid request (Prism will return 400 with validation errors)
curl -X POST http://localhost:8084/inventory/items \
  -H "Content-Type: application/json" \
  -d '{"invalid": "data"}'
```

---

## Example 6: Webhook Simulator

### User Request

"I need to test webhook handling in my app. Can you create a mock that sends webhooks to my local service?"

### Requirements Gathering

- **Service to mock**: Webhook sender (e.g., Stripe webhooks)
- **Mock type**: Express.js with webhook simulation
- **Port**: 8085

### Generated Structure

```
mock-webhook-service/
├── server.js
├── webhooks/
│   ├── sender.js
│   └── templates.js
├── package.json
└── README.md
```

**server.js**:
```javascript
const express = require('express');
const { sendWebhook } = require('./webhooks/sender');
const templates = require('./webhooks/templates');

const app = express();
app.use(express.json());

const PORT = 8085;

// Control panel to trigger webhooks
app.post('/trigger/:event', async (req, res) => {
  const { event } = req.params;
  const { targetUrl, data } = req.body;
  
  const template = templates[event];
  if (!template) {
    return res.status(404).json({ error: `Event ${event} not found` });
  }
  
  const payload = template(data || {});
  
  try {
    await sendWebhook(targetUrl, payload);
    res.json({ message: `Webhook ${event} sent`, payload });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// List available webhook events
app.get('/events', (req, res) => {
  res.json({
    events: Object.keys(templates),
    usage: 'POST /trigger/:event with { targetUrl, data }'
  });
});

app.listen(PORT, () => {
  console.log(`🪝 Mock Webhook Service on port ${PORT}`);
});
```

**webhooks/templates.js**:
```javascript
module.exports = {
  'payment.succeeded': (data) => ({
    event: 'payment.succeeded',
    data: {
      id: data.id || 'pay_123',
      amount: data.amount || 5000,
      currency: data.currency || 'usd',
      status: 'succeeded',
      timestamp: Date.now()
    }
  }),
  
  'payment.failed': (data) => ({
    event: 'payment.failed',
    data: {
      id: data.id || 'pay_123',
      amount: data.amount || 5000,
      error: data.error || 'card_declined',
      timestamp: Date.now()
    }
  }),
  
  'order.created': (data) => ({
    event: 'order.created',
    data: {
      id: data.id || 'ord_123',
      items: data.items || [],
      total: data.total || 10000,
      timestamp: Date.now()
    }
  })
};
```

**Usage**:
```bash
npm start

# Trigger a webhook to your local service
curl -X POST http://localhost:8085/trigger/payment.succeeded \
  -H "Content-Type: application/json" \
  -d '{
    "targetUrl": "http://localhost:3000/webhooks",
    "data": { "amount": 5000 }
  }'

# List available events
curl http://localhost:8085/events
```

---

## Common Patterns

### Pattern 1: Delayed Responses
```javascript
const delay = (ms) => new Promise(resolve => setTimeout(resolve, ms));

app.use(async (req, res, next) => {
  await delay(process.env.MOCK_DELAY_MS || 100);
  next();
});
```

### Pattern 2: Random Failures
```javascript
app.use((req, res, next) => {
  const errorRate = parseFloat(process.env.ERROR_RATE || 0);
  if (Math.random() < errorRate) {
    return res.status(500).json({ error: 'Random server error' });
  }
  next();
});
```

### Pattern 3: Scenario Switching
```javascript
// Switch scenarios via header
app.use((req, res, next) => {
  req.scenario = req.headers['x-mock-scenario'] || 'default';
  next();
});
```

---

## Tips for Using Generated Mocks

1. **Start simple**: Begin with basic success/error responses
2. **Add scenarios incrementally**: Add edge cases as you discover them
3. **Use realistic data**: Tests are more valuable with realistic data
4. **Version control your mocks**: Track changes alongside your code
5. **Document triggers**: Explain how to trigger different scenarios
6. **Integrate with tests**: Use mocks in integration tests
7. **Match production closely**: Keep mocks in sync with real API
8. **Use environment variables**: Make mocks configurable
