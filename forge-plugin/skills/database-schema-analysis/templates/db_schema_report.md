# Database Schema Analysis Report

## Executive Summary

**Database Type**: [PostgreSQL | MySQL | MongoDB | Cassandra | Neo4j | Redis | etc.]
**Version**: [version]
**Analyzed**: [date]
**Environment**: [Development | Production | Staging]

### Database Statistics
- **Schemas/Databases**: [number]
- **Tables/Collections**: [number]
- **Total Columns/Fields**: [number]
- **Relationships**: [number]
- **Indexes**: [number]
- **Constraints**: [number]
- **Data Volume**: [size] ([rows] total rows)

### Health Score
**Overall**: [score/10]
- Structure: [score/10]
- Performance: [score/10]
- Security: [score/10]
- Normalization: [score/10]

### Key Findings
- ✅ [Positive finding 1]
- ✅ [Positive finding 2]
- ⚠️ [Warning/issue 1]
- ⚠️ [Warning/issue 2]
- ❌ [Critical issue 1]

---

## Database Overview

### System Information
- **Database Type**: [type]
- **Version**: [version]
- **Character Set**: [UTF-8, etc.]
- **Collation**: [collation]
- **Default Schema**: [schema name]
- **Total Size**: [size on disk]

### Schema Inventory

| Schema/Database | Tables | Views | Size | Description |
|-----------------|--------|-------|------|-------------|
| | | | | |

---

## Entity Catalog

### [Schema Name]

#### [Table/Collection 1]

**Purpose**: [What this entity represents]
**Row Count**: [count]
**Size**: [size]
**Growth Rate**: [rows/day or % per month]

##### Columns/Fields

| Column | Type | Nullable | Default | Constraints | Description |
|--------|------|----------|---------|-------------|-------------|
| | | | | | |

##### Indexes

| Index Name | Type | Columns | Unique | Size | Cardinality |
|------------|------|---------|--------|------|-------------|
| | | | | | |

##### Foreign Keys

| FK Name | Columns | References | On Delete | On Update |
|---------|---------|------------|-----------|-----------|
| | | | | |

##### Triggers/Procedures
[List any triggers or stored procedures associated with this table]

---

#### [Table/Collection 2]
[Repeat structure above]

---

## Relationships

### Entity-Relationship Diagram

[See separate ER diagram document or include Mermaid/ASCII diagram]

### Relationship Summary

| Parent Table | Child Table | Relationship | Type | Referential Action |
|--------------|-------------|--------------|------|-------------------|
| | | Foreign Key | 1:N | CASCADE |
| | | Foreign Key | 1:1 | RESTRICT |

### Implicit Relationships
[Relationships not enforced by foreign keys but exist in application logic]

| Table 1 | Table 2 | Relationship Type | Evidence |
|---------|---------|-------------------|----------|
| | | | Naming pattern, JOIN queries |

---

## Index Analysis

### Index Inventory

#### [Table Name]

| Index Name | Type | Columns | Unique | Partial | Size | Est. Usage |
|------------|------|---------|--------|---------|------|-----------|
| | B-tree | | Yes/No | | | High/Medium/Low |

### Index Coverage Analysis

**Well-Indexed Tables**:
- ✅ [Table]: All foreign keys indexed, composite indexes for common queries

**Under-Indexed Tables**:
- ⚠️ [Table]: Missing indexes on [column names]

**Over-Indexed Tables**:
- ⚠️ [Table]: [number] redundant indexes consuming [size]

### Missing Indexes (Recommendations)

#### High Priority
1. **[Table].[Column(s)]**
   - **Reason**: Foreign key without index, used in 80% of JOINs
   - **Impact**: HIGH - Expected 10x performance improvement
   - **DDL**:
     ```sql
     CREATE INDEX idx_table_column ON table(column);
     ```

2. **[Table].[Composite columns]**
   - **Reason**: Common WHERE + ORDER BY pattern
   - **Impact**: MEDIUM - Will enable index-only scans
   - **DDL**:
     ```sql
     CREATE INDEX idx_table_col1_col2 ON table(col1, col2 DESC);
     ```

#### Medium Priority
[Additional recommendations]

### Redundant Indexes (Removal Candidates)

1. **[Index Name]** on [Table]
   - **Reason**: Duplicate of [other index] or covered by composite index
   - **Savings**: [size]
   - **DDL**:
     ```sql
     DROP INDEX index_name;
     ```

### Index Statistics

```
Total Indexes:        [number]
Unique Indexes:       [number]
Composite Indexes:    [number]
Partial Indexes:      [number]
Full-Text Indexes:    [number]
Spatial Indexes:      [number]
Total Index Size:     [size]
```

---

## Normalization Analysis

### Normal Form Compliance

| Table | 1NF | 2NF | 3NF | BCNF | Notes |
|-------|-----|-----|-----|------|-------|
| [table1] | ✅ | ✅ | ✅ | ✅ | Fully normalized |
| [table2] | ✅ | ✅ | ❌ | ❌ | Transitive dependency |

### Normalization Violations

#### [Table Name] - 3NF Violation
- **Issue**: [Column] depends on [non-key column] instead of primary key
- **Example**: City depends on ZipCode instead of primary key
- **Impact**: Update anomalies, data redundancy
- **Recommendation**: 
  ```sql
  -- Normalize into separate table
  CREATE TABLE zip_codes (
      zip_code VARCHAR(10) PRIMARY KEY,
      city VARCHAR(100),
      state VARCHAR(2)
  );
  ```

### Denormalization Patterns

#### Justified Denormalization
1. **[Table].[Redundant Column]**
   - **Reason**: Performance - Avoids expensive JOIN for common read pattern
   - **Trade-off**: Additional [size], update overhead acceptable
   - **Maintenance**: Trigger ensures consistency

#### Questionable Denormalization
1. **[Table].[Column]**
   - **Reason**: [Unclear or premature optimization]
   - **Recommendation**: Consider normalizing unless proven performance need

---

## Performance Analysis

### Query Performance Patterns

#### Common Query Types
| Query Pattern | Frequency | Avg Duration | Tables Involved |
|---------------|-----------|--------------|-----------------|
| User lookup by ID | 45% | 2ms | users |
| User posts with JOIN | 30% | 50ms | users, posts |
| Dashboard aggregation | 10% | 200ms | orders, order_items |

#### Slow Query Patterns
1. **[Query Type]**
   - **Example**:
     ```sql
     SELECT * FROM orders o
     JOIN order_items oi ON oi.order_id = o.id
     WHERE o.user_id = ?
     ```
   - **Duration**: [avg time]
   - **Issue**: Full table scan on order_items
   - **Fix**: Add index on order_items.order_id

### Partitioning Strategy

#### Current Partitioning

| Table | Partitioning Type | Key | Partitions | Benefits |
|-------|------------------|-----|------------|----------|
| [table] | RANGE | created_at | Monthly (24) | Query pruning, faster archival |

#### Recommended Partitioning

**[Table]** ([size], [rows]):
- **Type**: RANGE partitioning by [column]
- **Strategy**: [Monthly/Weekly/etc.]
- **Benefit**: Query performance improvement, easier archival
- **Implementation**:
  ```sql
  ALTER TABLE table_name PARTITION BY RANGE (column_name);
  ```

### Table Sizes and Growth

| Table | Current Size | Row Count | Growth Rate | Projected Size (1 year) |
|-------|--------------|-----------|-------------|------------------------|
| | | | | |

### Connection and Resource Usage

- **Max Connections**: [number]
- **Typical Active**: [number]
- **Connection Pool**: [configured size]
- **Recommendation**: [Increase pool size / Add read replicas / etc.]

---

## Data Types and Constraints

### Data Type Usage

```
String Types:     ████████████████░░░░  60% ([number] columns)
Integer Types:    ██████░░░░░░░░░░░░░░  25%
Timestamp Types:  ████░░░░░░░░░░░░░░░░  10%
Boolean Types:    ██░░░░░░░░░░░░░░░░░░   3%
JSON Types:       █░░░░░░░░░░░░░░░░░░░   2%
```

### Constraint Summary

| Constraint Type | Count | Tables Covered |
|-----------------|-------|----------------|
| PRIMARY KEY | [count] | [percentage]% |
| FOREIGN KEY | [count] | - |
| UNIQUE | [count] | - |
| CHECK | [count] | - |
| NOT NULL | [count] | - |

### Missing Constraints (Recommendations)

1. **[Table]** - Missing PRIMARY KEY
   - Impact: Unable to uniquely identify rows
   - Recommendation: Add surrogate key

2. **[Table].[Column]** - Should be NOT NULL
   - Reason: Business logic requires this field
   - Current: [percentage]% of rows are NULL

3. **[Table]** - Missing FOREIGN KEY to [Parent Table]
   - Evidence: JOIN pattern suggests relationship
   - Recommendation: Add FK constraint for referential integrity

---

## Security and Compliance

### PII Detection

| Table | Column | Data Type | Classification | Recommendation |
|-------|--------|-----------|----------------|----------------|
| users | email | varchar | PII | Encrypt at rest, mask in non-prod |
| users | phone | varchar | PII | Encrypt at rest |
| users | ssn | varchar | Sensitive PII | Encrypt + tokenize |
| addresses | street | text | PII | Consider anonymization |

### Encryption Status

- **At-Rest Encryption**: [Enabled/Disabled]
- **In-Transit Encryption**: [TLS/SSL version]
- **Column-Level Encryption**: [columns using encryption]

### Access Control

- **User Roles**: [count] roles defined
- **Row-Level Security**: [Enabled/Disabled]
- **Audit Logging**: [Enabled/Disabled]
- **Recommendations**:
  1. [Security recommendation 1]
  2. [Security recommendation 2]

### Compliance Notes

#### GDPR Compliance
- [ ] PII fields identified and documented
- [ ] Encryption implemented for sensitive data
- [ ] Data retention policies defined
- [ ] Right to erasure procedures established
- [ ] Audit logging for PII access

#### HIPAA Compliance (if applicable)
- [ ] PHI fields identified
- [ ] Encryption at rest and in transit
- [ ] Access controls and audit trails
- [ ] Backup and recovery procedures

---

## Quality Assessment

### Anti-Patterns Detected

#### 1. [Anti-Pattern Name]
- **Location**: [Table/Column]
- **Description**: [What it is]
- **Impact**: [Why it's problematic]
- **Recommendation**: [How to fix]
- **Priority**: [HIGH/MEDIUM/LOW]

#### 2. Entity-Attribute-Value (EAV) Pattern
- **Location**: [Table]
- **Impact**: Performance, type safety, query complexity
- **Recommendation**: Normalize into proper columns or use JSON columns

### Best Practices Followed

1. ✅ **Proper Use of Foreign Keys**: Referential integrity enforced
2. ✅ **Appropriate Indexes**: All foreign keys indexed
3. ✅ **Consistent Naming**: snake_case for all identifiers
4. ✅ **Timestamp Tracking**: created_at/updated_at on all tables

### Code Smells

- ⚠️ Generic column names: `data`, `value`, `info`
- ⚠️ Inconsistent naming: Some tables plural, some singular
- ⚠️ Magic values: Status codes as integers without ENUM/CHECK
- ⚠️ Missing documentation: No comments on tables or columns

---

## Recommendations

### High Priority

#### 1. [Recommendation]
- **Issue**: [Current problem]
- **Impact**: [How it affects system]
- **Solution**: [Detailed fix]
- **Effort**: [HIGH/MEDIUM/LOW]
- **Expected Benefit**: [Quantified improvement]
- **Implementation**:
  ```sql
  [DDL statements]
  ```

### Medium Priority

#### 1. [Recommendation]
[Similar structure]

### Low Priority / Nice to Have

1. [Improvement]
2. [Enhancement]

---

## Migration Guidance

### Schema Evolution Strategy

**Recommended Approach**: [Blue-green deployment / Rolling updates / etc.]

### Breaking Changes

| Change | Impact | Mitigation |
|--------|--------|------------|
| [Change description] | [Impact on app] | [How to handle] |

### Migration Checklist

- [ ] Backup database before migration
- [ ] Test migration on staging environment
- [ ] Verify application compatibility
- [ ] Create rollback procedure
- [ ] Update ORM models
- [ ] Update documentation
- [ ] Notify stakeholders

---

## Monitoring and Maintenance

### Recommended Monitoring

1. **Query Performance**
   - Monitor slow query log
   - Track query execution times
   - Alert on queries > [threshold]

2. **Index Usage**
   - Track index scan vs sequential scan ratio
   - Identify unused indexes
   - Monitor index bloat

3. **Table Growth**
   - Monitor table sizes
   - Track row count growth
   - Alert on unexpected growth

4. **Connection Pool**
   - Monitor active connections
   - Track connection wait times
   - Alert on pool exhaustion

### Maintenance Tasks

| Task | Frequency | Purpose |
|------|-----------|---------|
| VACUUM/ANALYZE | Daily | Update statistics, reclaim space |
| Reindex | Monthly | Reduce index bloat |
| Partition maintenance | Monthly | Archive old partitions |
| Backup verification | Weekly | Ensure backups are valid |

---

## Appendix

### DDL Export

[Link to full DDL dump or include selected CREATE statements]

### Query Samples

[Common queries with EXPLAIN plans]

### Tools Used

- **Schema extraction**: [pg_dump, mysqldump, mongodump, etc.]
- **Analysis tools**: [Custom scripts, pgAdmin, etc.]
- **Validation**: [sqlfluff, schema comparison tools]

### Related Documentation

- [Link to application documentation]
- [Link to API documentation]
- [Link to runbooks]

---

**Report Generated**: [timestamp]
**Analyzed by**: database-schema-analysis skill v1.0.0
**Project**: [project-name]
**Next Review**: [recommended date]
