# Firebase Firestore - Project Memory System

## Purpose

This directory stores project-specific knowledge learned during Firebase Firestore implementation sessions. Each project gets its own subdirectory containing collection structures, security rules, query patterns, and configuration discovered during implementation.

## Directory Structure

```
memory/skills/firebase-firestore/
├── index.md (this file)
└── {project-name}/
    ├── collection_structure.md
    ├── security_rules.md
    ├── query_patterns.md
    ├── data_model.md
    └── performance_config.md
```

## Project Memory Contents

### collection_structure.md
- Collection hierarchy and subcollections
- Document schemas with field types and constraints
- Document ID strategy (auto-generated vs custom)
- Subcollection depth and relationships
- Document size estimates

### security_rules.md
- Current security rules (firestore.rules)
- Authentication requirements per collection
- Role-based access control patterns
- Field-level validation logic
- Custom functions and reusable helpers
- Rule testing results and edge cases

### query_patterns.md
- Implemented query patterns (simple, compound, collection group)
- Composite index definitions (firestore.indexes.json)
- Pagination strategies (cursor-based, limit/offset)
- Real-time listener scopes and lifecycle
- Aggregation query usage (count, sum, average)

### data_model.md
- Embedding vs referencing decisions with rationale
- Denormalization strategy and duplicated fields
- Fan-out write patterns
- Relationship modeling (one-to-many, many-to-many)
- Aggregation fields and distributed counters
- Data migration history

### performance_config.md
- Offline persistence configuration (cache size, multi-tab)
- Index optimization notes
- Read/write cost distribution
- SDK configuration settings
- Cost optimization strategies
- Rate limiting and quota management

## Memory Lifecycle

### Creation
Memory is created the FIRST time a project's Firestore is designed or analyzed. The project name is either:
1. Extracted from the Firebase project ID
2. Specified by the user
3. Derived from the repository name

### Updates
Memory is UPDATED every time the skill works on the project's Firestore:
- Collection structure changes are tracked
- New security rules are recorded
- Query patterns and indexes are updated
- Data model decisions are appended
- Performance configurations are refined

### Usage
Memory is READ at the START of every Firestore session:
- Provides existing collection context
- Shows security rule evolution
- Guides query optimization focus
- Informs data modeling decisions
- Ensures consistency across sessions

## Best Practices

### DO:
- ✅ Update memory after every Firestore change
- ✅ Track collection structure evolution over time
- ✅ Document security rule changes and rationale
- ✅ Record index additions and the queries they support
- ✅ Note data modeling trade-offs and decisions

### DON'T:
- ❌ Store actual document data or PII
- ❌ Include Firebase service account keys or credentials
- ❌ Copy entire security rules verbatim (summarize patterns instead)
- ❌ Store temporary query results
- ❌ Include environment-specific configuration (project IDs, API keys)

## Memory vs Context

### Context (`../../context/schema/`)
- **Universal knowledge**: Applies to ALL Firestore projects
- **NoSQL patterns**: Document modeling, denormalization strategies
- **Best practices**: Firestore limits, pricing considerations, indexing rules
- **Static**: Updated by Forge maintainers

### Memory (this directory)
- **Project-specific**: Only for ONE Firestore project
- **Learned patterns**: Discovered during implementation
- **Historical tracking**: Changes over time
- **Dynamic**: Updated by the skill automatically

## Example Memory Structure

```
ecommerce-app/
├── collection_structure.md
│   - 5 top-level collections: products, categories, orders, users, reviews
│   - orders/{orderId}/items subcollection for order line items
│   - Auto-generated IDs for all collections
│   - Max document size: ~15 KiB (products with embedded variants)
│   - Last updated: 2025-07-14
│
├── security_rules.md
│   - Products: public read, admin-only write
│   - Orders: owner read/create, admin read all
│   - Users: owner read/write only
│   - Custom claims: role ('admin', 'customer')
│   - Helper functions: isAuthenticated(), isAdmin(), isOwner()
│
├── query_patterns.md
│   - Products by category with rating sort (composite index)
│   - Orders by user with date desc (composite index)
│   - Real-time listener on product inventory
│   - Cursor-based pagination (20 items per page)
│   - Collection group query on order items for analytics
│
├── data_model.md
│   - categoryName denormalized into products (avoids extra read)
│   - Order items store price snapshot (price at time of purchase)
│   - Review count/average rating aggregated on product document
│   - Distributed counter for product view counts (10 shards)
│
└── performance_config.md
    - Offline persistence enabled (100 MB cache)
    - 3 composite indexes defined
    - Read-heavy workload (~90% reads)
    - Estimated cost: ~$15/month at 10K DAU
    - Index exemptions on 'description' fields (no queries)
```

## Security Considerations

### DO Store:
- Collection structures and schemas
- Security rule patterns (summarized)
- Query patterns (anonymized)
- Index definitions
- Performance characteristics
- Data modeling decisions

### DON'T Store:
- Actual document data
- Firebase project IDs or API keys
- Service account credentials
- PII or sensitive user information
- Production data samples
- Access tokens or secrets

## Integration with Tools

Memory can inform:
- **Firebase Emulator**: Provide context for local testing setup
- **Security audits**: Historical rule changes and access patterns
- **Cost monitoring**: Expected read/write patterns for budget planning
- **Migration tools**: Collection structure for data migration scripts
- **Code generators**: Schema types for TypeScript interfaces or Dart classes

---

**Memory System Version**: 1.0.0
**Last Updated**: 2025-07-14
**Maintained by**: firebase-firestore skill
