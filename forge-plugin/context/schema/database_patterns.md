---
id: "schema/database_patterns"
domain: schema
title: "Database Schema Patterns"
type: pattern
estimatedTokens: 2100
loadingStrategy: onDemand
version: "0.3.0-alpha"
lastUpdated: "2026-02-10"
sections:
  - name: "Overview"
    estimatedTokens: 12
    keywords: [overview]
  - name: "Relational Database (SQL) Patterns"
    estimatedTokens: 486
    keywords: [relational, database, sql, patterns]
  - name: "NoSQL Database Patterns"
    estimatedTokens: 276
    keywords: [nosql, database, patterns]
  - name: "Schema Design Anti-Patterns"
    estimatedTokens: 101
    keywords: [schema, design, anti-patterns]
  - name: "Performance Analysis Patterns"
    estimatedTokens: 49
    keywords: [performance, analysis, patterns]
  - name: "Data Type Selection Guide"
    estimatedTokens: 90
    keywords: [data, type, selection, guide]
  - name: "Migration Safety Patterns"
    estimatedTokens: 68
    keywords: [migration, safety, patterns]

tags: [schema, database, sql, nosql, indexes, normalization, migration, mongodb, redis]
---
# Database Schema Patterns

## Overview

This document provides patterns for analyzing and understanding database schemas across SQL and NoSQL systems.

---

## Relational Database (SQL) Patterns

### Table Structure Analysis

```sql
CREATE TABLE users (
    id BIGSERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP WITH TIME ZONE,  -- Soft delete
    
    CONSTRAINT email_format CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$')
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_created_at ON users(created_at DESC);
```

**Analysis Points**:
- **Primary Keys**: Auto-incrementing, UUIDs, composite keys
- **Data Types**: Precision, size limits, time zones
- **Constraints**: NOT NULL, UNIQUE, CHECK, DEFAULT
- **Indexes**: Single-column, composite, partial, expression-based
- **Soft Deletes**: deleted_at pattern for logical deletion
- **Audit Columns**: created_at, updated_at timestamps

---

### Foreign Key Relationships

```sql
CREATE TABLE posts (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL,
    title VARCHAR(200) NOT NULL,
    content TEXT,
    published_at TIMESTAMP WITH TIME ZONE,
    
    CONSTRAINT fk_posts_user
        FOREIGN KEY (user_id) 
        REFERENCES users(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE tags (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE
);

-- Many-to-Many relationship
CREATE TABLE post_tags (
    post_id BIGINT NOT NULL,
    tag_id INTEGER NOT NULL,
    
    PRIMARY KEY (post_id, tag_id),
    CONSTRAINT fk_post_tags_post 
        FOREIGN KEY (post_id) REFERENCES posts(id) ON DELETE CASCADE,
    CONSTRAINT fk_post_tags_tag 
        FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE
);
```

**Relationship Types**:
1. **One-to-Many**: users → posts (via user_id FK)
2. **Many-to-Many**: posts ↔ tags (via post_tags junction table)
3. **One-to-One**: Use unique constraint on FK

**Referential Actions**:
- CASCADE: Delete/update related rows
- RESTRICT: Prevent deletion if referenced
- SET NULL: Nullify FK on parent deletion
- SET DEFAULT: Use default value
- NO ACTION: Similar to RESTRICT

---

### Normalization Levels

#### 1NF (First Normal Form)
- Atomic values (no arrays in columns)
- Each column has unique name
- Order of rows doesn't matter

#### 2NF (Second Normal Form)
- Satisfies 1NF
- No partial dependencies (all non-key attributes depend on entire primary key)

#### 3NF (Third Normal Form)
- Satisfies 2NF
- No transitive dependencies (non-key attributes don't depend on other non-key attributes)

#### BCNF (Boyce-Codd Normal Form)
- Satisfies 3NF
- Every determinant is a candidate key

**When to Denormalize**:
- Read-heavy workloads
- Expensive joins
- Data warehouse/analytics
- Caching layers

---

### Index Strategy Analysis

```sql
-- Single-column index
CREATE INDEX idx_users_email ON users(email);

-- Composite index (order matters!)
CREATE INDEX idx_posts_user_published ON posts(user_id, published_at DESC);

-- Partial index (filtered)
CREATE INDEX idx_active_users ON users(email) WHERE deleted_at IS NULL;

-- Expression-based index
CREATE INDEX idx_users_lower_username ON users(LOWER(username));

-- Covering index (includes non-indexed columns)
CREATE INDEX idx_posts_covering ON posts(user_id) INCLUDE (title, published_at);

-- Full-text search index
CREATE INDEX idx_posts_content_fts ON posts USING GIN (to_tsvector('english', content));
```

**Index Analysis Checklist**:
- ✅ Indexes on foreign keys
- ✅ Indexes on WHERE clause columns
- ✅ Indexes on JOIN columns
- ✅ Composite indexes match query patterns (left-to-right)
- ❌ Over-indexing (slows writes, wastes space)
- ❌ Duplicate indexes
- ❌ Unused indexes

---

### Common SQL Patterns

#### Temporal Data (SCD Type 2)
```sql
CREATE TABLE customer_history (
    id BIGSERIAL PRIMARY KEY,
    customer_id BIGINT NOT NULL,
    name VARCHAR(100),
    email VARCHAR(255),
    valid_from TIMESTAMP NOT NULL,
    valid_to TIMESTAMP,  -- NULL = current version
    is_current BOOLEAN DEFAULT TRUE,
    
    CONSTRAINT chk_valid_range CHECK (valid_to IS NULL OR valid_to > valid_from)
);

CREATE INDEX idx_customer_current ON customer_history(customer_id) 
    WHERE is_current = TRUE;
```

#### Hierarchical Data (Closure Table)
```sql
CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

CREATE TABLE category_paths (
    ancestor_id INTEGER NOT NULL REFERENCES categories(id),
    descendant_id INTEGER NOT NULL REFERENCES categories(id),
    depth INTEGER NOT NULL,
    
    PRIMARY KEY (ancestor_id, descendant_id)
);
```

#### Event Sourcing
```sql
CREATE TABLE events (
    id BIGSERIAL PRIMARY KEY,
    aggregate_id UUID NOT NULL,
    event_type VARCHAR(100) NOT NULL,
    event_data JSONB NOT NULL,
    occurred_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    version INTEGER NOT NULL,
    
    CONSTRAINT uq_aggregate_version UNIQUE (aggregate_id, version)
);

CREATE INDEX idx_events_aggregate ON events(aggregate_id, version);
```

---

## NoSQL Database Patterns

### Document Database (MongoDB)

```javascript
// User document
{
  _id: ObjectId("507f1f77bcf86cd799439011"),
  username: "johndoe",
  email: "john@example.com",
  profile: {
    firstName: "John",
    lastName: "Doe",
    age: 30
  },
  roles: ["user", "admin"],
  addresses: [
    {
      type: "home",
      street: "123 Main St",
      city: "Springfield",
      zip: "12345"
    }
  ],
  createdAt: ISODate("2024-01-01T00:00:00Z"),
  updatedAt: ISODate("2024-01-01T00:00:00Z")
}
```

**Analysis Points**:
- **Embedded Documents**: Nested objects (profile, addresses)
- **Arrays**: Multi-valued fields (roles, addresses)
- **ObjectId**: 12-byte identifier
- **Schema Flexibility**: Fields can vary between documents
- **Indexes**: Single field, compound, multikey (arrays), text, geospatial

**Embedding vs Referencing**:
- **Embed**: One-to-few, data read together, atomic updates
- **Reference**: One-to-many, many-to-many, independent updates

---

### Key-Value Store (Redis)

```
# String
SET user:1001:name "John Doe"

# Hash (similar to document)
HSET user:1001 username "johndoe" email "john@example.com" age 30

# List (ordered)
LPUSH user:1001:notifications "New message" "Friend request"

# Set (unordered, unique)
SADD user:1001:roles "user" "admin"

# Sorted Set (ordered by score)
ZADD leaderboard 1000 "user:1001" 950 "user:1002"
```

**Patterns**:
- **Caching**: Time-to-live (TTL) on keys
- **Session Storage**: User sessions with expiration
- **Rate Limiting**: Counters with sliding windows
- **Pub/Sub**: Message queues and channels

---

### Column-Family Store (Cassandra)

```cql
CREATE TABLE users (
    user_id UUID PRIMARY KEY,
    username TEXT,
    email TEXT,
    created_at TIMESTAMP
);

-- Partition key + clustering key
CREATE TABLE posts_by_user (
    user_id UUID,
    post_id TIMEUUID,
    title TEXT,
    content TEXT,
    published_at TIMESTAMP,
    
    PRIMARY KEY (user_id, post_id)
) WITH CLUSTERING ORDER BY (post_id DESC);
```

**Key Concepts**:
- **Partition Key**: Determines data distribution (user_id)
- **Clustering Key**: Determines sort order within partition (post_id)
- **Wide Rows**: Many columns per partition
- **Denormalization**: Query-driven design (duplicate data for read performance)
- **Time-series Data**: TIMEUUID for time-ordered data

---

### Graph Database (Neo4j)

```cypher
// Node creation
CREATE (u:User {id: 1001, name: "John Doe", email: "john@example.com"})
CREATE (p:Post {id: 2001, title: "Hello World", content: "..."})

// Relationship creation
CREATE (u)-[:AUTHORED {created_at: datetime()}]->(p)
CREATE (u)-[:FOLLOWS {since: date()}]->(u2:User {id: 1002})

// Indexes
CREATE INDEX FOR (u:User) ON (u.email)
CREATE INDEX FOR (p:Post) ON (p.created_at)
```

**Analysis Points**:
- **Nodes**: Entities with labels and properties
- **Relationships**: Directed edges with types and properties
- **Labels**: Node types (User, Post)
- **Properties**: Key-value pairs on nodes/relationships
- **Patterns**: Graph traversal patterns for queries

---

## Schema Design Anti-Patterns

### 1. Entity-Attribute-Value (EAV)
❌ **Problem**: Over-generalized schema
```sql
CREATE TABLE entity_attributes (
    entity_id INT,
    attribute_name VARCHAR(50),
    attribute_value TEXT
);
-- Makes queries complex, loses type safety
```
✅ **Solution**: Use proper columns or JSON columns for flexibility

### 2. Polymorphic Associations
❌ **Problem**: Foreign key to multiple tables
```sql
CREATE TABLE comments (
    id INT PRIMARY KEY,
    commentable_type VARCHAR(50),  -- 'Post' or 'Photo'
    commentable_id INT,
    content TEXT
);
-- Can't use foreign key constraints
```
✅ **Solution**: Exclusive arcs or separate tables

### 3. Multicolumn Attributes
❌ **Problem**: Repeating column names
```sql
CREATE TABLE contacts (
    id INT PRIMARY KEY,
    phone1 VARCHAR(20),
    phone2 VARCHAR(20),
    phone3 VARCHAR(20)
);
```
✅ **Solution**: One-to-many relationship or JSON array

### 4. Metadata Tribbles
❌ **Problem**: Creating tables/columns at runtime
✅ **Solution**: Use configuration tables or flexible schemas

---

## Performance Analysis Patterns

### Query Optimization
1. **EXPLAIN ANALYZE**: Execution plan analysis
2. **Index Coverage**: Check if query uses indexes
3. **Join Order**: Smaller tables first
4. **Subquery vs JOIN**: Test both approaches
5. **Materialized Views**: Pre-computed aggregations

### Schema Optimization
1. **Partitioning**: Horizontal (by range/hash) or vertical (by columns)
2. **Archiving**: Move old data to separate tables
3. **Compression**: Column-level compression
4. **Connection Pooling**: Limit concurrent connections

---

## Data Type Selection Guide

### PostgreSQL
- **IDs**: BIGSERIAL (auto-increment) or UUID (distributed)
- **Text**: VARCHAR(n) with limit, TEXT for unlimited
- **Numbers**: INTEGER, BIGINT, NUMERIC(precision, scale)
- **Dates**: TIMESTAMP WITH TIME ZONE (always use timezone)
- **JSON**: JSONB (binary, indexed) over JSON
- **Arrays**: Native array types for small lists
- **Enums**: Custom ENUM types for fixed sets

### MySQL
- **IDs**: BIGINT AUTO_INCREMENT or BINARY(16) for UUID
- **Text**: VARCHAR(n), TEXT, MEDIUMTEXT, LONGTEXT
- **Numbers**: INT, BIGINT, DECIMAL(precision, scale)
- **Dates**: DATETIME vs TIMESTAMP (TIMESTAMP has limitations)
- **JSON**: JSON type (5.7+)

### MongoDB
- **ObjectId**: Default _id type
- **Strings**: UTF-8 strings
- **Numbers**: Int32, Int64, Double, Decimal128
- **Dates**: ISODate
- **Binary**: BinData
- **Arrays and Embedded Documents**: Native support

---

## Migration Safety Patterns

### Safe Schema Changes
✅ Add nullable columns
✅ Add indexes (with CONCURRENTLY in PostgreSQL)
✅ Add tables
✅ Rename with views (transition period)

### Dangerous Schema Changes
❌ Drop columns (lose data)
❌ Change column types (may fail)
❌ Add NOT NULL columns (requires default or backfill)
❌ Drop indexes (affects performance immediately)

### Multi-Step Migration Pattern
1. **Step 1**: Add new column (nullable)
2. **Step 2**: Backfill data
3. **Step 3**: Add NOT NULL constraint
4. **Step 4**: Remove old column

---

**Last Updated**: 2025-02-06
**Maintained by**: The Forge
