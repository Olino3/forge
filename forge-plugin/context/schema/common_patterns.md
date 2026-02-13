---
id: "schema/common_patterns"
domain: schema
title: "Common Schema Patterns"
type: always
estimatedTokens: 1700
loadingStrategy: always
version: "0.3.0-alpha"
lastUpdated: "2026-02-10"
sections:
  - name: "Overview"
    estimatedTokens: 11
    keywords: [overview]
  - name: "Core Schema Elements"
    estimatedTokens: 233
    keywords: [core, schema, elements]
  - name: "Schema Versioning Strategies"
    estimatedTokens: 46
    keywords: [schema, versioning, strategies]
  - name: "Schema Evolution Patterns"
    estimatedTokens: 61
    keywords: [schema, evolution, patterns]
  - name: "Documentation Patterns"
    estimatedTokens: 129
    keywords: [documentation, patterns]
  - name: "Schema Design Principles"
    estimatedTokens: 139
    keywords: [schema, design, principles]
  - name: "Anti-Patterns to Avoid"
    estimatedTokens: 118
    keywords: [anti-patterns, avoid]
  - name: "Schema Quality Checklist"
    estimatedTokens: 138
    keywords: [schema, quality, checklist]
  - name: "Cross-Platform Considerations"
    estimatedTokens: 76
    keywords: [cross-platform, considerations]
  - name: "Schema Testing Strategies"
    estimatedTokens: 69
    keywords: [schema, testing, strategies]
tags: [schema, patterns, entities, relationships, constraints, versioning, antipatterns]
---

# Common Schema Patterns

## Overview

This document covers universal schema design principles applicable across file formats and database systems.

---

## Core Schema Elements

### 1. Entities and Attributes

**Entity**: A distinct object or concept (User, Product, Order)
**Attribute**: A property of an entity (name, price, quantity)

```
User Entity:
- id (identifier)
- username (unique attribute)
- email (contact attribute)
- created_at (temporal attribute)
- roles (multi-valued attribute)
```

**Attribute Types**:
- **Simple**: Atomic value (name, age)
- **Composite**: Multiple parts (address = street + city + zip)
- **Derived**: Calculated from others (age from birthdate)
- **Multi-valued**: Multiple values allowed (phone numbers, tags)

---

### 2. Relationships and Cardinality

**One-to-One (1:1)**
- Each entity instance relates to exactly one instance of another
- Example: User ↔ UserProfile
- Implementation: Foreign key with UNIQUE constraint

**One-to-Many (1:N)**
- One entity instance relates to many instances of another
- Example: User → Posts (one user has many posts)
- Implementation: Foreign key in "many" side

**Many-to-Many (M:N)**
- Multiple instances on both sides
- Example: Students ↔ Courses
- Implementation: Junction/link table

**Hierarchical (Tree)**
- Parent-child relationships
- Example: Categories with subcategories
- Implementations:
  - Adjacency List (parent_id column)
  - Nested Sets (left/right boundaries)
  - Closure Table (all ancestor-descendant pairs)
  - Materialized Path (path stored as string)

---

### 3. Constraints and Validation

**Primary Key Constraints**
- Uniquely identifies each record
- Cannot be NULL
- Single column or composite

**Unique Constraints**
- Ensures no duplicate values
- Can be NULL (unless combined with NOT NULL)
- Multiple allowed per table

**Foreign Key Constraints**
- Maintains referential integrity
- Points to primary/unique key in another table
- Cascading actions on update/delete

**Check Constraints**
- Custom validation logic
- Range checks, format validation, business rules
```sql
CHECK (age >= 18)
CHECK (email LIKE '%@%.%')
CHECK (end_date > start_date)
```

**Not Null Constraints**
- Prevents NULL values
- Essential for required fields

**Default Values**
- Automatic value when not provided
- Simplifies inserts, documents expected values

---

## Schema Versioning Strategies

### 1. Semantic Versioning
```
v1.0.0 → v1.1.0 (backward compatible addition)
v1.1.0 → v2.0.0 (breaking change)
```

### 2. Version Field in Data
```json
{
  "schema_version": "2.1.0",
  "data": {...}
}
```

### 3. Namespace/Package Versioning
```
com.example.api.v1.User
com.example.api.v2.User
```

### 4. Evolutionary Database Design
- Small, reversible changes
- Parallel change pattern (old + new coexist)
- Deprecation period before removal

---

## Schema Evolution Patterns

### Additive Changes (Safe)
✅ Add optional fields/columns
✅ Add new entities/tables
✅ Add indexes
✅ Widen data types (VARCHAR(50) → VARCHAR(100))
✅ Relax constraints (remove CHECK, make nullable)

### Destructive Changes (Risky)
⚠️ Remove fields/columns
⚠️ Rename fields/columns
⚠️ Change data types
⚠️ Add required constraints (NOT NULL, CHECK)
⚠️ Narrow data types

### Safe Evolution Workflow
1. **Expand**: Add new schema elements alongside old
2. **Migrate**: Dual-write to old and new
3. **Contract**: Remove old schema elements after migration

---

## Documentation Patterns

### Essential Schema Documentation

**1. Schema Diagram**
- Entity-relationship diagrams (ERD)
- Class diagrams (UML)
- Graph visualizations

**2. Field Inventory**
```
Field Name    | Type          | Required | Constraints        | Description
------------- | ------------- | -------- | ------------------ | -----------
user_id       | INTEGER       | Yes      | PRIMARY KEY        | Unique identifier
username      | VARCHAR(50)   | Yes      | UNIQUE, NOT NULL   | Login name
email         | VARCHAR(255)  | Yes      | UNIQUE, NOT NULL   | Contact email
created_at    | TIMESTAMP     | Yes      | DEFAULT NOW()      | Registration date
```

**3. Relationship Documentation**
- Cardinality (1:1, 1:N, M:N)
- Referential actions (CASCADE, RESTRICT)
- Business rules governing relationships

**4. Version History**
```
Version | Date       | Changes                    | Migration Required
------- | ---------- | -------------------------- | ------------------
2.0.0   | 2024-02-01 | Added user_roles table     | Yes
1.1.0   | 2024-01-15 | Added email_verified field | No
```

**5. Example Data**
- Valid samples
- Edge cases
- Invalid samples (with reasons)

**6. Performance Notes**
- Index strategy
- Expected data volumes
- Query patterns

---

## Schema Design Principles

### 1. Clarity Over Cleverness
- Use descriptive names
- Avoid abbreviations unless domain-standard
- Consistent naming conventions

**Good Names**:
- `user_id`, `created_at`, `order_total`
- `is_active`, `has_permission` (boolean prefixes)
- `get_user_by_id()` (verb + object)

**Bad Names**:
- `usr_id`, `crtd`, `tot`
- `flag1`, `status` (ambiguous)
- `data`, `info`, `temp` (too generic)

### 2. Consistency
- **Naming**: Same pattern for similar concepts (created_at, updated_at, deleted_at)
- **Types**: Same type for similar data (all IDs as BIGINT, all timestamps with timezone)
- **Structure**: Similar entities follow similar patterns

### 3. Atomicity
- **One fact per field**: Don't store multiple values in single field
- ❌ `name` = "John Doe" (should split to first_name, last_name)
- ❌ `address` = "123 Main St, Springfield, 12345"
- ✅ Separate fields for each atomic piece

### 4. Don't Repeat Yourself (DRY)
- **Avoid Redundancy**: Don't store calculated values unless performance critical
- **Use Relationships**: Don't duplicate data across tables
- **Normalize First**: Then denormalize strategically for performance

### 5. Design for Change
- **Extensibility**: Leave room for growth
- **Versioning**: Plan for schema evolution
- **Backward Compatibility**: Support old clients during transitions

---

## Anti-Patterns to Avoid

### 1. God Object/Table
**Problem**: Single entity with 50+ attributes
**Impact**: Hard to maintain, query, optimize
**Solution**: Decompose into focused entities

### 2. Metadata Tribbles
**Problem**: Creating schema elements dynamically at runtime
**Impact**: Uncontrolled growth, hard to maintain
**Solution**: Use flexible schemas (JSON) or configuration tables

### 3. Boolean Trap
**Problem**: Multiple related booleans
```sql
is_active BOOLEAN
is_deleted BOOLEAN
is_archived BOOLEAN
is_hidden BOOLEAN
```
**Solution**: Use ENUM or status column
```sql
status ENUM('active', 'deleted', 'archived', 'hidden')
```

### 4. Fear of NULL
**Problem**: Using empty strings, -1, or magic values instead of NULL
**Impact**: Inconsistent data, harder queries
**Solution**: Embrace NULL for "unknown" or "not applicable"

### 5. Premature Optimization
**Problem**: Complex denormalization before proven need
**Impact**: Complexity without benefits
**Solution**: Start normalized, optimize based on measurements

### 6. CSV in Database
**Problem**: Storing delimited values in fields
```sql
tags VARCHAR(255) -- "tag1,tag2,tag3"
```
**Impact**: Can't query efficiently, integrity issues
**Solution**: Use proper relationships or JSON arrays

---

## Schema Quality Checklist

### ✅ Correctness
- [ ] All entities and relationships accurately model domain
- [ ] Constraints properly enforce business rules
- [ ] Data types appropriate for data ranges
- [ ] No data loss in conversions

### ✅ Completeness
- [ ] All required entities and relationships present
- [ ] All necessary constraints defined
- [ ] Documentation covers all elements
- [ ] Migration path documented

### ✅ Consistency
- [ ] Naming conventions followed throughout
- [ ] Similar entities use similar patterns
- [ ] Types consistent across similar fields

### ✅ Performance
- [ ] Appropriate indexes on query patterns
- [ ] No over-indexing
- [ ] Partitioning strategy for large tables
- [ ] Denormalization justified and documented

### ✅ Maintainability
- [ ] Clear, descriptive names
- [ ] Proper documentation
- [ ] Schema versioning in place
- [ ] Migration strategy defined

### ✅ Security
- [ ] Sensitive data identified
- [ ] Encryption requirements specified
- [ ] Access control considered
- [ ] Audit trails for sensitive operations

---

## Cross-Platform Considerations

### Data Type Portability
Different systems, different types:
- **Integers**: INT, INTEGER, BIGINT, INT64, Long
- **Decimals**: DECIMAL, NUMERIC, DOUBLE, Float64
- **Strings**: VARCHAR, TEXT, String, NVARCHAR
- **Dates**: TIMESTAMP, DATETIME, Date, DateTime
- **Binary**: BLOB, BYTEA, VARBINARY, Binary

**Best Practice**: Document expected precision and range, not just type name

### Identifier Strategies
- **Auto-increment**: Database-specific, not distributed
- **UUID**: Portable, distributed, larger storage
- **Snowflake ID**: Time-ordered, distributed, sortable
- **ULID**: UUID-compatible, sortable, timestamp-prefixed

### JSON Portability
- **PostgreSQL**: JSONB (binary, indexed, functions)
- **MySQL**: JSON (text-based, some functions)
- **MongoDB**: Native BSON (binary JSON)
- **SQLite**: JSON1 extension (text-based)

---

## Schema Testing Strategies

### 1. Constraint Testing
- Verify required fields reject NULL
- Test unique constraints prevent duplicates
- Check foreign keys enforce referential integrity
- Validate CHECK constraints catch invalid data

### 2. Migration Testing
- Test forward migration (v1 → v2)
- Test rollback (v2 → v1) if supported
- Verify data integrity after migration
- Performance test on production-scale data

### 3. Load Testing
- Insert performance with various data volumes
- Query performance on indexes
- Update/delete performance
- Concurrent access patterns

---

**Last Updated**: 2025-02-06
**Maintained by**: The Forge
