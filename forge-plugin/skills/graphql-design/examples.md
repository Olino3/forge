# GraphQL Design Examples

This file contains example scenarios demonstrating how to use the graphql-design skill for various GraphQL API design tasks.

---

## Example 1: Social Media Platform Schema Design

### Scenario
A social media startup needs a GraphQL API for their mobile and web apps. The API must handle user profiles, posts, comments, likes, and a follow system with real-time notifications.

### User Prompt
```
Design a GraphQL schema for our social media platform with users, posts, comments, likes, and real-time notifications
```

### Skill Execution

**Step 1 — Requirements**:
- Scope: New greenfield GraphQL API
- Consumers: React Native mobile app + React web SPA
- Real-time: Notifications and new post subscriptions
- Scale: 100K users, 1M posts, high read ratio

**Step 2 — Load Memory**:
- No existing memory; will create after generation

**Step 4 — Schema Types**:

```graphql
scalar DateTime
scalar URL

# ---- Core Types ----

type User {
  id: ID!
  username: String!
  displayName: String!
  avatarUrl: URL
  bio: String
  isVerified: Boolean!
  followersCount: Int!
  followingCount: Int!
  posts(first: Int = 10, after: String): PostConnection!
  followers(first: Int = 10, after: String): UserConnection!
  following(first: Int = 10, after: String): UserConnection!
  isFollowedByViewer: Boolean!
  createdAt: DateTime!
}

type Post {
  id: ID!
  author: User!
  content: String!
  mediaUrls: [URL!]!
  likesCount: Int!
  commentsCount: Int!
  isLikedByViewer: Boolean!
  comments(first: Int = 10, after: String): CommentConnection!
  createdAt: DateTime!
  updatedAt: DateTime
}

type Comment {
  id: ID!
  author: User!
  post: Post!
  content: String!
  likesCount: Int!
  isLikedByViewer: Boolean!
  createdAt: DateTime!
}

enum NotificationType {
  NEW_FOLLOWER
  POST_LIKED
  POST_COMMENTED
  MENTION
}

type Notification {
  id: ID!
  type: NotificationType!
  actor: User!
  target: NotificationTarget!
  read: Boolean!
  createdAt: DateTime!
}

union NotificationTarget = Post | Comment | User
```

**Step 5 — Operations**:

```graphql
# ---- Queries ----

type Query {
  # Viewer (authenticated user)
  viewer: User!

  # Users
  user(username: String!): User
  searchUsers(query: String!, first: Int = 10): UserConnection!

  # Posts
  post(id: ID!): Post
  feed(first: Int = 20, after: String): PostConnection!
  explorePosts(first: Int = 20, after: String): PostConnection!

  # Notifications
  notifications(first: Int = 20, after: String, unreadOnly: Boolean): NotificationConnection!
  unreadNotificationCount: Int!
}

# ---- Mutations ----

input CreatePostInput {
  content: String!
  mediaUrls: [URL!]
}

type CreatePostPayload {
  post: Post
  errors: [MutationError!]!
}

input AddCommentInput {
  postId: ID!
  content: String!
}

type AddCommentPayload {
  comment: Comment
  errors: [MutationError!]!
}

type Mutation {
  # Posts
  createPost(input: CreatePostInput!): CreatePostPayload!
  deletePost(id: ID!): DeletePayload!

  # Comments
  addComment(input: AddCommentInput!): AddCommentPayload!
  deleteComment(id: ID!): DeletePayload!

  # Likes (toggle)
  togglePostLike(postId: ID!): Post!
  toggleCommentLike(commentId: ID!): Comment!

  # Follow (toggle)
  toggleFollow(userId: ID!): User!

  # Notifications
  markNotificationsRead(ids: [ID!]!): MarkReadPayload!
}

# ---- Subscriptions ----

type Subscription {
  newNotification: Notification!
  newFeedPost: Post!
}

# ---- Error Types ----

type MutationError {
  message: String!
  field: String
  code: ErrorCode!
}

enum ErrorCode {
  VALIDATION_ERROR
  NOT_FOUND
  UNAUTHORIZED
  RATE_LIMITED
  CONTENT_POLICY_VIOLATION
}

type DeletePayload {
  deletedId: ID
  errors: [MutationError!]!
}

type MarkReadPayload {
  readCount: Int!
  errors: [MutationError!]!
}
```

**Step 6 — Resolver Architecture**:

```markdown
## DataLoader Strategy

| DataLoader | Batches | Used By |
|-----------|---------|---------|
| UserLoader | User IDs → Users | Post.author, Comment.author, Notification.actor |
| PostLoader | Post IDs → Posts | Comment.post |
| LikeStatusLoader | (userId, targetId) → Boolean | Post.isLikedByViewer, Comment.isLikedByViewer |
| FollowStatusLoader | (viewerId, targetId) → Boolean | User.isFollowedByViewer |

## Query Complexity Budget

| Field | Cost | Rationale |
|-------|------|-----------|
| Scalar fields | 1 | Single value |
| Entity fields (author, post) | 2 | DataLoader lookup |
| Connection fields | 5 + (first × child cost) | Paginated list |
| Maximum query cost | 1000 | |
| Maximum depth | 8 | |
```

**Step 7 — Output**:
File: `/claudedocs/graphql-design_social-platform_2025-01-15.md`

---

## Example 2: E-Commerce Federation Design

### Scenario
An e-commerce platform with 4 microservices (users, catalog, orders, reviews) needs a federated GraphQL gateway that composes a unified schema from all services.

### User Prompt
```
Design a federated GraphQL schema for our e-commerce platform across users, catalog, orders, and reviews services
```

### Skill Execution

**Step 1 — Requirements**:
- Scope: Federation design across 4 services
- Gateway: Apollo Federation v2
- Constraint: Each team owns their service and subgraph independently

**Step 6 — Federation Design**:

```markdown
## Subgraph Ownership

| Subgraph | Team | Entities Owned | Extended Entities |
|----------|------|---------------|-------------------|
| users | Identity | User, Address | — |
| catalog | Product | Product, Category, Variant | — |
| orders | Commerce | Order, OrderItem, Cart | User, Product |
| reviews | Content | Review, Rating | User, Product |

## Users Subgraph

    type User @key(fields: "id") {
      id: ID!
      email: String!
      name: String!
      addresses: [Address!]!
    }

    type Address {
      id: ID!
      street: String!
      city: String!
      country: String!
      isDefault: Boolean!
    }

    type Query {
      me: User
      user(id: ID!): User
    }

## Catalog Subgraph

    type Product @key(fields: "id") @key(fields: "sku") {
      id: ID!
      sku: String!
      name: String!
      description: String!
      price: Money!
      category: Category!
      variants: [Variant!]!
      inStock: Boolean!
    }

    type Category {
      id: ID!
      name: String!
      products(first: Int, after: String): ProductConnection!
    }

    type Query {
      product(id: ID!): Product
      products(first: Int, after: String, filter: ProductFilter): ProductConnection!
      categories: [Category!]!
    }

## Orders Subgraph (extends User and Product)

    extend type User @key(fields: "id") {
      id: ID! @external
      orders(first: Int, after: String): OrderConnection!
      cart: Cart
    }

    extend type Product @key(fields: "id") {
      id: ID! @external
      purchaseCount: Int!
    }

    type Order @key(fields: "id") {
      id: ID!
      status: OrderStatus!
      items: [OrderItem!]!
      total: Money!
      shippingAddress: Address!
      createdAt: DateTime!
    }

## Reviews Subgraph (extends User and Product)

    extend type User @key(fields: "id") {
      id: ID! @external
      reviews(first: Int, after: String): ReviewConnection!
    }

    extend type Product @key(fields: "id") {
      id: ID! @external
      reviews(first: Int, after: String): ReviewConnection!
      averageRating: Float
      reviewCount: Int!
    }

    type Review @key(fields: "id") {
      id: ID!
      author: User!
      product: Product!
      rating: Int!
      title: String!
      body: String!
      createdAt: DateTime!
    }

## Gateway Composed Query Example

The gateway composes a unified query that spans all subgraphs:

    query ProductPage($productId: ID!) {
      product(id: $productId) {        # catalog subgraph
        name
        price { amount currency }
        inStock
        purchaseCount                   # orders subgraph (extended)
        averageRating                   # reviews subgraph (extended)
        reviews(first: 5) {             # reviews subgraph (extended)
          edges {
            node {
              rating
              title
              author { name }           # users subgraph (resolved via @key)
            }
          }
        }
      }
    }
```

**Step 7 — Output**:
File: `/claudedocs/graphql-design_ecommerce-federation_2025-01-15.md`

---

## Example 3: REST-to-GraphQL Migration

### Scenario
A company has 30+ REST endpoints and wants to introduce GraphQL gradually without breaking existing REST consumers. They need a migration strategy and initial schema design.

### User Prompt
```
Plan a migration from our REST API to GraphQL. We have 30+ endpoints and can't break existing consumers.
```

### Skill Execution

**Step 4 — Migration Strategy**:

```markdown
## Migration Approach: GraphQL as Aggregation Layer

### Architecture

    ┌──────────────┐      ┌──────────────┐
    │  Web/Mobile  │      │  Legacy REST  │
    │  (new apps)  │      │  Consumers    │
    └──────┬───────┘      └──────┬───────┘
           │                      │
    ┌──────▼───────┐      ┌──────▼───────┐
    │   GraphQL    │      │   REST API   │
    │   Gateway    ├──────►   (unchanged) │
    └──────┬───────┘      └──────────────┘
           │
    ┌──────▼───────┐
    │  Data Sources │
    │  (DB, Services)│
    └──────────────┘

### Phase 1: Shadow GraphQL (Weeks 1-4)
- Deploy GraphQL server alongside REST
- Resolvers call existing REST endpoints (not DB directly)
- New clients can use GraphQL; REST continues unchanged
- Monitor query patterns and performance

### Phase 2: Direct Data Access (Weeks 5-8)
- Migrate high-traffic resolvers from REST proxying to direct DB access
- Add DataLoaders for batch optimization
- REST endpoints remain unchanged for legacy consumers

### Phase 3: Feature Parity + New Features (Weeks 9-16)
- Complete schema coverage of all REST endpoints
- New features built GraphQL-first
- Subscriptions for real-time features (no REST equivalent)

### Phase 4: REST Deprecation (Weeks 17+)
- Notify REST consumers of deprecation timeline
- REST endpoints become thin wrappers calling GraphQL resolvers
- Eventually remove REST layer

### Initial Schema (mapping from REST)

| REST Endpoint | GraphQL Equivalent |
|---------------|-------------------|
| `GET /users` | `query { users(first: 20) { ... } }` |
| `GET /users/:id` | `query { user(id: "...") { ... } }` |
| `POST /users` | `mutation { createUser(input: { ... }) { ... } }` |
| `GET /users/:id/orders` | `query { user(id: "...") { orders { ... } } }` |
| `GET /products?category=X` | `query { products(filter: { category: "X" }) { ... } }` |
```

**Step 7 — Output**:
File: `/claudedocs/graphql-design_rest-migration_2025-01-15.md`

---

## Summary of Use Cases

1. **Greenfield schema design** — Full type system, operations, subscriptions, and resolver architecture
2. **Federation design** — Multi-service graph with entity ownership and cross-subgraph composition
3. **REST-to-GraphQL migration** — Incremental adoption with backward compatibility

## Best Practices

- Always design schema-first — the SDL is your API contract
- Use Relay connections for all list fields, even if they seem small today
- Put business errors in mutation payloads, not GraphQL errors
- One DataLoader per entity type per request — never share across requests
- Set query complexity limits before going to production
- Deprecate fields with `@deprecated(reason: "Use X instead")` — never remove without warning
