# database-schema-analysis Examples

## Usage Scenarios

This document provides practical examples of using the `database-schema-analysis` skill in various contexts.

---

## Example 1: PostgreSQL Production Database Analysis

### Scenario
You need to document an existing PostgreSQL database for a new team and identify optimization opportunities.

### User Request
```
Please use skill:database-schema-analysis to analyze our PostgreSQL production database. Connection details: [provided separately]
```

### Skill Workflow

**Step 1**: Database Identification
- Identifies PostgreSQL 14.x
- Connects to specified database
- Confirms read-only access for safety

**Step 2**: Socratic Questions
```
I've connected to your PostgreSQL database. Before proceeding:

1. Should I analyze all schemas or focus on specific ones (public, app, etc.)?
2. Do you have query logs I can analyze for index recommendations?
3. Are there known performance issues or slow queries?
4. Need this for documentation, migration planning, or optimization?
5. Any compliance requirements (PII handling, encryption)?
```

**User Response**:
```
1. Focus on 'public' and 'app' schemas
2. Yes, can provide slow query log
3. User dashboard queries are slow
4. Both optimization and documentation
5. GDPR compliance - we have PII fields
```

**Step 3**: Schema Extraction
```sql
SELECT table_name, table_schema 
FROM information_schema.tables 
WHERE table_schema IN ('public', 'app');

SELECT * FROM information_schema.columns 
WHERE table_schema IN ('public', 'app');

SELECT * FROM information_schema.table_constraints 
WHERE table_schema IN ('public', 'app');

SELECT * FROM pg_indexes 
WHERE schemaname IN ('public', 'app');
```

**Step 4**: Analysis
- 47 tables identified
- Maps foreign key relationships
- Identifies 12 PII fields (email, phone, address)
- Finds 3 missing indexes on foreign keys
- Detects N+1 query pattern in user dashboard
- Normalization: Mostly 3NF, one violation in user_profiles

**Step 5**: Report Generation

```markdown
# PostgreSQL Database Analysis Report

## Executive Summary
- **Database**: PostgreSQL 14.9
- **Schemas**: public (35 tables), app (12 tables)
- **Total Tables**: 47
- **Total Indexes**: 89
- **PII Fields**: 12 (requires GDPR compliance)
- **Health Score**: 7.5/10

## Key Findings
1. ✅ Good normalization (mostly 3NF)
2. ⚠️ Missing indexes on 3 foreign keys (performance impact)
3. ⚠️ PII fields not encrypted at rest
4. ⚠️ User dashboard has N+1 query pattern
5. ✅ Proper use of constraints and data types

## Entity Catalog

### users table
| Column | Type | Nullable | Default | Constraints |
|--------|------|----------|---------|-------------|
| id | bigint | NO | nextval('users_id_seq') | PRIMARY KEY |
| username | varchar(50) | NO | | UNIQUE |
| email | varchar(255) | NO | | UNIQUE (PII) |
| password_hash | varchar(255) | NO | | |
| created_at | timestamp with time zone | NO | CURRENT_TIMESTAMP | |

[... full catalog ...]

## Relationship Diagram
```
users (1) ──< posts (N)
users (1) ──< comments (N)
posts (1) ──< comments (N)
users (1) ── user_profiles (1)
posts (N) ──> tags (N) via post_tags
```

## Index Recommendations

### Missing Indexes (HIGH PRIORITY)
1. **posts.user_id** - Foreign key, used in 80% of queries
   ```sql
   CREATE INDEX idx_posts_user_id ON posts(user_id);
   ```

2. **comments.post_id** - Foreign key, N+1 query pattern
   ```sql
   CREATE INDEX idx_comments_post_id ON comments(post_id);
   ```

3. **user_profiles.user_id** - Unique foreign key
   ```sql
   CREATE UNIQUE INDEX idx_user_profiles_user_id ON user_profiles(user_id);
   ```

### Redundant Indexes (REMOVAL RECOMMENDED)
1. **idx_users_email_lower** - Duplicate of unique constraint
   ```sql
   DROP INDEX idx_users_email_lower;
   ```

## Performance Optimization

### Query Pattern Issues
**N+1 Query Pattern Detected**:
```sql
-- Current: 1 + N queries
SELECT * FROM users WHERE id = ?;
SELECT * FROM posts WHERE user_id = ? FOR EACH USER;

-- Recommended: Use JOIN
SELECT u.*, p.* FROM users u 
LEFT JOIN posts p ON p.user_id = u.id 
WHERE u.id = ?;
```

### Partitioning Recommendation
**posts table** (15M rows, growing 100K/day):
- Partition by created_at (monthly)
- Archive posts older than 2 years

## GDPR Compliance

### PII Fields Identified
| Table | Column | Type | Encrypted | Recommendation |
|-------|--------|------|-----------|----------------|
| users | email | varchar | NO | Enable pgcrypto or column-level encryption |
| users | phone | varchar | NO | Encrypt at application level |
| user_profiles | address | text | NO | Consider tokenization |
| user_profiles | birth_date | date | NO | Mask in non-production environments |

### Recommendations
1. Implement column-level encryption for PII
2. Add data retention policies (GDPR right to erasure)
3. Implement audit logging for PII access
4. Consider pseudonymization for analytics
```

---

## Example 2: MongoDB Migration Analysis

### Scenario
Migrating from MongoDB to PostgreSQL and need schema mapping.

### User Request
```
We're migrating from MongoDB to PostgreSQL. Analyze our MongoDB collections at mongodb://localhost/myapp and suggest a relational schema.
```

### Skill Workflow

**Step 1-2**: MongoDB identification, context loading

**Step 3**: Document Sampling
```javascript
// Sample 1000 documents per collection
db.users.aggregate([{ $sample: { size: 1000 } }])
db.posts.aggregate([{ $sample: { size: 1000 } }])
```

**Step 4**: Schema Inference
- users collection: Embedded addresses (array), roles (array)
- posts collection: References to users, embedded tags

**Step 5**: Migration Report
```markdown
# MongoDB → PostgreSQL Migration Analysis

## Current MongoDB Schema

### users collection
```json
{
  "_id": ObjectId,
  "username": String,
  "email": String,
  "addresses": [
    { "type": String, "street": String, "city": String }
  ],
  "roles": [String],
  "created_at": Date
}
```

## Proposed PostgreSQL Schema

### Relational Mapping

```sql
-- Normalize embedded addresses
CREATE TABLE users (
    id BIGSERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL UNIQUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE user_addresses (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    type VARCHAR(20) NOT NULL,
    street VARCHAR(255),
    city VARCHAR(100),
    CONSTRAINT valid_type CHECK (type IN ('home', 'work', 'other'))
);

CREATE TABLE user_roles (
    user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    role VARCHAR(50) NOT NULL,
    PRIMARY KEY (user_id, role)
);
```

## Migration Complexity

| Aspect | Complexity | Notes |
|--------|------------|-------|
| Schema Mapping | Medium | Embedded arrays need separate tables |
| Data Types | Low | MongoDB types map cleanly to PostgreSQL |
| Indexes | Low | Can recreate with appropriate types |
| Query Migration | High | Aggregation pipelines → SQL JOINs |

## Migration Steps
1. Create PostgreSQL schema
2. Export MongoDB data to JSON
3. Transform embedded documents to relational
4. Load data with foreign key validation
5. Recreate indexes
6. Update application queries
7. Test thoroughly with production data sample

## Performance Comparison
- MongoDB: ~2ms for user lookups (indexed _id)
- PostgreSQL: ~1ms expected (B-tree index on id)
- MongoDB: Complex aggregations fast
- PostgreSQL: JOINs will require proper indexing
```

---

## Example 3: Index Optimization Analysis

### Scenario
Database performance degrading over time, need index analysis.

### User Request
```
skill:database-schema-analysis - Focus on index optimization for MySQL database
```

### Skill Workflow

**Step 2**: Clarifying Questions
```
For index optimization analysis:

1. Do you have query logs or slow query log enabled?
2. What are your top 5 slowest queries?
3. Current database size and growth rate?
4. Any specific tables with known issues?
```

**Step 3**: Extract Index Data
```sql
SELECT * FROM information_schema.statistics 
WHERE table_schema = 'myapp';

SHOW INDEX FROM users;
SHOW TABLE STATUS;
```

**Step 5**: Index Analysis Report
```markdown
# Index Optimization Analysis

## Current Index Inventory

### users table
| Index Name | Type | Columns | Cardinality | Size |
|------------|------|---------|-------------|------|
| PRIMARY | BTREE | id | 1,000,000 | 45 MB |
| idx_email | BTREE | email | 1,000,000 | 52 MB |
| idx_username | BTREE | username | 1,000,000 | 48 MB |
| idx_created_at | BTREE | created_at | 365 | 22 MB |
| idx_email_username | BTREE | email, username | 1,000,000 | 98 MB |

### Analysis

#### Redundant Indexes
1. **idx_email_username** - Redundant with idx_email
   - email alone has same cardinality
   - Wasting 98 MB
   - **Recommendation**: DROP

2. **idx_created_at** - Low cardinality (365 distinct values)
   - Only useful for date range queries
   - Consider partial index for recent dates
   - **Recommendation**: Replace with partial index

#### Missing Indexes
1. **Foreign Key**: posts.user_id
   ```sql
   CREATE INDEX idx_posts_user_id ON posts(user_id);
   ```
   - Used in 90% of JOIN queries
   - Expected performance improvement: 10x

2. **Composite**: posts(user_id, created_at)
   ```sql
   CREATE INDEX idx_posts_user_created ON posts(user_id, created_at DESC);
   ```
   - Covers common query pattern: user's recent posts
   - Will enable index-only scans

## Estimated Impact
- Disk space saved: 120 MB (redundant indexes removed)
- Query performance: 5-10x improvement on user/posts queries
- Write performance: 2-3% improvement (fewer indexes to maintain)

## Implementation Plan
1. Create missing indexes during off-peak hours
2. Monitor query performance for 1 week
3. Drop redundant indexes after confirming no regression
4. Update index hints in critical queries if needed
```

---

## Example 4: Neo4j Graph Database Analysis

### Scenario
Analyzing a Neo4j social graph for optimization.

### User Request
```
Analyze our Neo4j social graph database - users, posts, follows relationships
```

### Skill Workflow

**Step 3**: Extract Graph Schema
```cypher
// Get node labels
CALL db.labels() YIELD label;

// Get relationship types
CALL db.relationshipTypes() YIELD relationshipType;

// Sample node properties
MATCH (u:User) RETURN keys(u) LIMIT 1;
MATCH (p:Post) RETURN keys(p) LIMIT 1;

// Count relationships
MATCH ()-[r]->() RETURN type(r), count(r);
```

**Step 5**: Graph Analysis Report
```markdown
# Neo4j Social Graph Analysis

## Graph Statistics
- **Nodes**: 1.5M (Users: 1M, Posts: 500K)
- **Relationships**: 25M total
  - FOLLOWS: 10M
  - POSTED: 500K
  - LIKED: 12M
  - COMMENTED: 2.5M

## Schema Visualization

```
(User)
  ├─[:FOLLOWS]─>(User)
  ├─[:POSTED]─>(Post)
  ├─[:LIKED]─>(Post)
  └─[:COMMENTED]─>(Post)

(Post)
  ├─[:POSTED_BY]─>(User)
  └─[:TAGGED]─>(Tag)
```

## Index Analysis

### Existing Indexes
```cypher
CALL db.indexes() YIELD description, state;
```

| Index | Type | Properties | State |
|-------|------|------------|-------|
| User.id | BTREE | id | ONLINE |
| User.email | BTREE | email | ONLINE |
| Post.id | BTREE | id | ONLINE |

### Missing Indexes (RECOMMENDED)
```cypher
CREATE INDEX user_created_at FOR (u:User) ON (u.created_at);
CREATE INDEX post_created_at FOR (p:Post) ON (p.created_at);
CREATE CONSTRAINT user_username FOR (u:User) REQUIRE u.username IS UNIQUE;
```

## Query Pattern Analysis

### Common Queries
1. **User Feed** (friends' recent posts):
   ```cypher
   MATCH (u:User {id: $userId})-[:FOLLOWS]->(friend)-[:POSTED]->(post)
   WHERE post.created_at > datetime() - duration('P7D')
   RETURN post ORDER BY post.created_at DESC LIMIT 50
   ```
   - Performance: 150ms avg
   - **Optimization**: Add index on Post.created_at

2. **Mutual Friends**:
   ```cypher
   MATCH (u:User {id: $userId})-[:FOLLOWS]->(mutual)<-[:FOLLOWS]-(them:User {id: $theirId})
   RETURN mutual
   ```
   - Performance: 50ms avg
   - **Status**: Optimal

## Recommendations
1. Add temporal indexes for time-based queries
2. Consider caching user feeds in Redis
3. Implement relationship property for follow_date
4. Use query hints for complex traversals
5. Monitor query plan for full scans
```

---

## Example 5: Cross-Database Schema Comparison

### Scenario
Comparing development and production schemas to identify drift.

### User Request
```
Compare schema between dev and prod PostgreSQL databases
```

### Skill Workflow

**Steps 1-4**: Extract schemas from both databases

**Step 5**: Diff Report
```markdown
# Schema Drift Analysis: Dev vs Production

## Tables

### Only in Production
- **audit_logs** (missing in dev)
- **session_tokens** (missing in dev)

### Only in Dev
- **test_data** (should not be in dev)

### Different Column Definitions

#### users table
| Column | Dev Type | Prod Type | Impact |
|--------|----------|-----------|--------|
| phone | varchar(15) | varchar(20) | LOW - wider in prod |
| status | varchar(20) | enum('active','inactive','banned') | HIGH - type mismatch |

#### posts table
| Column | Dev | Prod | Impact |
|--------|-----|------|--------|
| view_count | Missing | integer DEFAULT 0 | MEDIUM - missing tracking |

## Indexes

### Missing in Dev
- `idx_posts_user_created` - composite index
- `idx_users_status` - enum index

### Different Definitions
- `idx_users_email` - UNIQUE in prod, not in dev

## Recommendations
1. Sync dev schema from prod using migration script
2. Add `audit_logs` table to dev (with sample data)
3. Update `users.status` to enum type in dev
4. Add missing indexes to dev
5. Remove `test_data` table from dev
6. Create schema validation CI check

## Migration Script
```sql
-- Add missing columns
ALTER TABLE posts ADD COLUMN view_count INTEGER DEFAULT 0;

-- Change type
ALTER TABLE users ALTER COLUMN status TYPE user_status USING status::user_status;

-- Add missing indexes
CREATE INDEX idx_posts_user_created ON posts(user_id, created_at DESC);
```
```

---

## Common Patterns

### Pattern: Performance Audit
```
Analyze database schema and provide performance optimization recommendations
```

### Pattern: Migration Preparation
```
Analyze current schema for migration from MySQL to PostgreSQL
```

### Pattern: Security Audit
```
Analyze database schema and identify PII fields, security issues, and compliance gaps
```

### Pattern: Documentation Generation
```
Generate comprehensive database documentation for onboarding new developers
```

---

**Last Updated**: 2025-02-06
**Maintained by**: The Forge
