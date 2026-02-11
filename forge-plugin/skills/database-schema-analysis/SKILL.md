---
name: database-schema-analysis
description: Analyze and document database schemas across SQL and NoSQL systems (PostgreSQL, MySQL, SQL Server, MongoDB, Cassandra, Neo4j, Redis). Extracts tables, relationships, indexes, constraints, and performance patterns. Generates comprehensive schema documentation with ERDs, normalization analysis, index recommendations, and migration guidance. Use for database reverse engineering, migration planning, optimization analysis, and documentation generation.
---

# Database Schema Analysis Expert

## ⚠️ MANDATORY COMPLIANCE ⚠️

**CRITICAL**: The 5-step workflow outlined in this document MUST be followed in exact order for EVERY database schema analysis. Skipping steps or deviating from the procedure will result in incomplete and unreliable analysis. This is non-negotiable.

## File Structure

- **SKILL.md** (this file): Main instructions and MANDATORY workflow
- **examples.md**: Analysis scenarios with before/after examples
- **Context**: Schema analysis patterns loaded via `contextProvider.getDomainIndex("schema")`. See [ContextProvider Interface](../../interfaces/context_provider.md).
- **Memory**: Project-specific memory accessed via `memoryStore.getSkillMemory("database-schema-analysis", "{project-name}")`. See [MemoryStore Interface](../../interfaces/memory_store.md).
- **templates/**: `db_schema_report.md`, `er_diagram.md`, `index_analysis.md`
- **scripts/**: Helper utilities for database introspection

## Interface References

- **Context**: Loaded via [ContextProvider Interface](../../interfaces/context_provider.md)
- **Memory**: Accessed via [MemoryStore Interface](../../interfaces/memory_store.md)
- **Schemas**: Validated against [context_metadata.schema.json](../../interfaces/schemas/context_metadata.schema.json) and [memory_entry.schema.json](../../interfaces/schemas/memory_entry.schema.json)

## Analysis Focus Areas

Database schema analysis evaluates 8 critical dimensions:

1. **Structure Analysis**: Tables/collections, columns/fields, data types
2. **Relationships**: Foreign keys, references, joins, graph edges
3. **Constraints**: Primary keys, unique constraints, checks, not null
4. **Indexes**: Single-column, composite, full-text, spatial, performance impact
5. **Normalization**: 1NF, 2NF, 3NF, BCNF compliance, denormalization patterns
6. **Performance**: Query patterns, index coverage, partitioning, sharding
7. **Evolution**: Version tracking, migration history, compatibility
8. **Security**: PII detection, encryption requirements, access patterns

---

## MANDATORY WORKFLOW (MUST FOLLOW EXACTLY)

### ⚠️ STEP 1: Identify Target Database (REQUIRED)

**YOU MUST:**
1. Ask the user about the database system:
   - Database type (PostgreSQL, MySQL, MongoDB, Cassandra, etc.)
   - Connection details or schema dump files
   - Specific schemas/databases to analyze
   - Access method (live connection, SQL dump, DDL scripts, ORM models)
2. Verify access to schema information:
   - For live databases: Test connection credentials
   - For dumps: Locate and verify SQL/DDL files
   - For ORM models: Find model definition files (Python models, Entity Framework, etc.)
3. Identify scope:
   - Specific tables/collections or entire database?
   - Include system tables/metadata?
   - Focus areas (performance, normalization, security)?

**DO NOT PROCEED WITHOUT IDENTIFYING TARGET**

### ⚠️ STEP 2: Load Project Memory & Context (REQUIRED)

**YOU MUST:**
1. **CHECK PROJECT MEMORY FIRST**:
   - Identify the project name from the repository root or ask the user
   - Use `memoryStore.getSkillMemory("database-schema-analysis", "{project-name}")` to load existing project memory. See [MemoryStore Interface](../../interfaces/memory_store.md).
   - If memory exists, review previously analyzed schemas, patterns, and project-specific context
   - If no memory exists, you will create it later in this process

2. **USE CONTEXT INDEXES FOR EFFICIENT LOADING**:
   - Use `contextProvider.getDomainIndex("schema")` to discover available schema context files. See [ContextProvider Interface](../../interfaces/context_provider.md).
   - Use `contextProvider.getAlwaysLoadFiles("schema")` to load foundational concepts (common_patterns.md)
   - Use `contextProvider.getConditionalContext("schema", detection)` to load database-specific patterns
   - If analyzing security aspects, use `contextProvider.getCrossDomainContext("schema", {"security": true})` for security context

3. **Ask clarifying questions** in Socratic format:
   - What is the purpose of this database analysis?
   - Planning a migration to a different database system?
   - Performance optimization goals?
   - Documentation for new team members?
   - Compliance or security audit?
   - Known pain points or issues with current schema?

**DO NOT PROCEED WITHOUT COMPLETING THIS STEP**

### ⚠️ STEP 3: Extract Schema Metadata (REQUIRED)

**YOU MUST:**
1. **Extract schema information** using appropriate method:
   
   **For SQL Databases (PostgreSQL, MySQL, SQL Server)**:
   - Query information_schema tables or system catalogs
   - Extract table definitions (DDL)
   - Retrieve indexes, constraints, foreign keys
   - Get column types, defaults, nullable status
   - Identify views, stored procedures, triggers
   
   **For NoSQL Databases**:
   - MongoDB: Sample documents, infer schema, check indexes
   - Cassandra: Extract keyspace, table definitions, clustering keys
   - Neo4j: Identify node labels, relationship types, properties
   - Redis: Analyze key patterns, data structures

2. **Organize extracted metadata**:
   - Group by schema/database/keyspace
   - Categorize by entity type (tables, views, collections)
   - Map relationships and dependencies
   - Identify data volumes if available

3. **Document extraction method**:
   - SQL queries used
   - Tools employed (pg_dump, mysqldump, mongodump)
   - Sampling strategy for NoSQL
   - Timestamp of extraction

**DO NOT PROCEED WITHOUT EXTRACTING METADATA**

### ⚠️ STEP 4: Analyze Schema Structure (REQUIRED)

**YOU MUST perform deep analysis covering ALL these aspects:**

#### 4.1 Entity Analysis
- **Identify all entities**: Tables, collections, node types
- **Catalog fields/columns**: Name, type, constraints, defaults
- **Analyze data types**: Precision, size, appropriateness
- **Check naming conventions**: Consistency, clarity, standards compliance

#### 4.2 Relationship Analysis
- **Map foreign keys**: Source and target tables, referential actions
- **Identify implicit relationships**: Naming patterns, join patterns
- **Analyze cardinality**: One-to-one, one-to-many, many-to-many
- **Document junction tables**: Many-to-many relationships
- **Check referential integrity**: Orphaned records, circular dependencies

#### 4.3 Constraint Analysis
- **Primary keys**: Single vs composite, type, uniqueness
- **Unique constraints**: Business keys, natural keys
- **Check constraints**: Validation rules, business logic
- **Not null constraints**: Required vs optional fields
- **Default values**: Appropriateness, consistency

#### 4.4 Index Analysis
- **Catalog all indexes**: Type, columns, uniqueness
- **Evaluate coverage**: Query patterns vs indexes
- **Identify redundant indexes**: Duplicate or overlapping
- **Check missing indexes**: Foreign keys, WHERE clause columns
- **Analyze index types**: B-tree, hash, GiST, GIN, full-text
- **Assess performance impact**: Size, selectivity, usage statistics

#### 4.5 Normalization Assessment
- **Check normal forms**: 1NF, 2NF, 3NF, BCNF
- **Identify violations**: Repeating groups, partial dependencies, transitive dependencies
- **Evaluate denormalization**: Justified vs premature
- **Recommend improvements**: Normalization or strategic denormalization

#### 4.6 Performance Analysis
- **Query patterns**: Common joins, aggregations, filters
- **Partitioning strategy**: Range, list, hash partitioning
- **Sharding approach**: Distribution key, replication
- **Connection pooling**: Configuration recommendations
- **Table sizes**: Large tables, growth projections
- **Slow query patterns**: N+1 queries, missing indexes

#### 4.7 Security and Compliance
- **PII field detection**: Identify sensitive data (emails, SSNs, addresses)
- **Encryption requirements**: At-rest and in-transit
- **Access control**: Role-based access, row-level security
- **Audit capabilities**: Logging, temporal tables, event sourcing

#### 4.8 Quality Assessment
- **Anti-patterns**: EAV, polymorphic associations, metadata tribbles
- **Best practices**: Proper use of constraints, indexes, types
- **Code smells**: Generic names, missing documentation, inconsistent patterns
- **Technical debt**: Legacy patterns, workarounds, deprecated features

**USE THE TEMPLATES** in `templates/` directory to structure your analysis

**DO NOT PROCEED WITHOUT COMPREHENSIVE ANALYSIS**

### ⚠️ STEP 5: Generate Analysis Report & Update Memory (REQUIRED)

**YOU MUST:**

1. **Generate comprehensive analysis report** using the template from `templates/db_schema_report.md`:
   - Executive summary
   - Database inventory
   - Entity catalog (all tables/collections with fields)
   - Relationship diagram (ERD)
   - Index analysis and recommendations
   - Normalization assessment
   - Performance optimization opportunities
   - Security and compliance notes
   - Quality assessment

2. **Create ER diagram** using `templates/er_diagram.md`:
   - Visual representation of entities and relationships
   - Cardinality indicators
   - Key constraints

3. **Generate index analysis** using `templates/index_analysis.md`:
   - Index inventory
   - Coverage analysis
   - Recommendations for additions/removals
   - Performance impact assessment

4. **UPDATE PROJECT MEMORY**:
   - Use `memoryStore.update(layer="skill-specific", skill="database-schema-analysis", project="{project-name}", ...)` to store:
   - Database type and version
   - Naming conventions and patterns
   - Performance characteristics
   - Migration history if available
   - Common query patterns
   - Timestamps and staleness tracking are handled automatically by MemoryStore. See [MemoryStore Interface](../../interfaces/memory_store.md).

5. **Provide actionable recommendations**:
   - Prioritized list of improvements
   - Migration strategies if changing platforms
   - Index optimization plan
   - Normalization/denormalization guidance
   - Security hardening steps

**MEMORY UPDATE IS MANDATORY - DO NOT SKIP**

---

## Output Requirements

### Analysis Report Must Include:

1. **Database Overview**
   - Type and version
   - Size and complexity metrics
   - Number of entities, relationships, indexes

2. **Entity Catalog**
   - Complete list of tables/collections
   - All fields with types, constraints, defaults
   - Primary and foreign keys
   - Indexes

3. **Visual Representations**
   - Entity-relationship diagram (ERD)
   - Dependency graph
   - Normalization level diagram

4. **Index Analysis**
   - All indexes with types and columns
   - Usage statistics (if available)
   - Recommendations for optimization

5. **Relationship Mapping**
   - Foreign key relationships
   - Cardinality
   - Referential actions

6. **Quality Report**
   - Normalization violations
   - Anti-patterns
   - Missing indexes
   - Best practices compliance

7. **Performance Assessment**
   - Partitioning strategy
   - Query pattern analysis
   - Optimization recommendations

8. **Security Analysis**
   - PII fields
   - Encryption status
   - Access control notes

---

## Socratic Prompting Guidelines

When interacting with users, ask clarifying questions such as:

**Understanding Intent:**
- "What decisions are you trying to make with this database analysis?"
- "Are you planning a migration, optimization, or documentation?"
- "Who is the audience for this analysis (developers, DBAs, auditors)?"

**Scope Definition:**
- "Should I analyze all schemas or focus on specific ones?"
- "Do you want performance analysis or just structural documentation?"
- "Should I include stored procedures, triggers, and views?"

**Context Understanding:**
- "What is your current database load (queries/sec, data volume)?"
- "Are there known performance issues or slow queries?"
- "Any compliance requirements (GDPR, HIPAA, SOC2)?"
- "What is your migration strategy or timeline?"

**Technical Details:**
- "Do you have access to query logs for usage analysis?"
- "Can I connect to a live database or work from dumps?"
- "Are there ORM models I should cross-reference?"

---

## Quality Standards

### Your analysis MUST:
- ✅ Be **100% accurate** to the actual database schema
- ✅ Catalog **all tables/collections and fields**
- ✅ Map **all relationships and constraints**
- ✅ Identify **all indexes** with recommendations
- ✅ Assess **normalization level** correctly
- ✅ Provide **specific, actionable recommendations**
- ✅ Use **templates** for consistent output
- ✅ Update **project memory** for future reference

### Your analysis MUST NOT:
- ❌ Hallucinate tables or columns not in the database
- ❌ Miss foreign key relationships
- ❌ Overlook indexes or constraints
- ❌ Provide generic recommendations without basis
- ❌ Ignore security or compliance considerations

---

## Integration with Other Skills

**Combine with:**
- `file-schema-analysis`: For API schemas that mirror database structure
- `python-code-review`: When analyzing SQLAlchemy or Django models
- `dotnet-code-review`: When analyzing Entity Framework models
- `generate-python-unit-tests`: To create database migration tests

---

## Supported Database Systems

### SQL Databases
- ✅ PostgreSQL (all versions)
- ✅ MySQL / MariaDB
- ✅ Microsoft SQL Server
- ✅ SQLite
- ✅ Oracle Database
- ✅ Amazon Aurora

### NoSQL Databases
- ✅ MongoDB (document store)
- ✅ Cassandra (column-family)
- ✅ Neo4j (graph)
- ✅ Redis (key-value)
- ✅ DynamoDB
- ✅ Couchbase

---

## Version History

- **v1.1.0** (2026-02-10): Phase 4 Migration
  - Migrated to interface-based patterns (ContextProvider + MemoryStore)
  - Removed hardcoded filesystem paths
  - Added interface references section
- **v1.0.0** (2025-02-06): Initial release
  - Support for major SQL and NoSQL databases
  - Comprehensive analysis workflow
  - Template-based reporting
  - Project memory integration
  - Index and performance analysis

---

**Last Updated**: 2025-02-06
**Maintained by**: The Forge
