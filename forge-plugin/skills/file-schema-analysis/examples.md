# file-schema-analysis Examples

## Usage Scenarios

This document provides practical examples of using the `file-schema-analysis` skill in various contexts.

---

## Example 1: JSON Schema Analysis

### Scenario
You have a JSON Schema file defining an API request/response format and need comprehensive documentation.

### User Request
```
Please use skill:file-schema-analysis to analyze api/schemas/user-schema.json
```

### Skill Workflow

**Step 1**: File Identification
- Identifies `api/schemas/user-schema.json`
- Detects format as JSON Schema (Draft 7)
- Verifies file exists and is readable

**Step 2**: Context Loading
```
I'll analyze the user schema file. Before I proceed, a few questions:

1. Is this schema actively used in production APIs, or is it for documentation purposes?
2. Are you planning any schema evolution or migration?
3. Do you need the analysis for API documentation, validation logic, or both?
4. Should I check for OpenAPI compatibility?
```

**User Response**:
```
1. Production API (REST endpoints)
2. Planning v2 migration
3. Both documentation and validation
4. Yes, we use OpenAPI 3.0
```

**Step 3-4**: Parse and Analyze
- Reads the JSON Schema file
- Extracts all field definitions, types, and constraints
- Identifies validation rules (minLength, pattern, format)
- Maps required vs optional fields
- Detects nested objects and arrays

**Step 5**: Generate Report
Creates comprehensive analysis including:
- Field inventory table with all properties
- Validation rules summary
- Mermaid diagram showing object relationships
- OpenAPI compatibility notes
- Recommendations for v2 improvements
- Updates project memory with schema patterns

### Sample Output

```markdown
# User Schema Analysis Report

## Executive Summary
- **File**: api/schemas/user-schema.json
- **Format**: JSON Schema Draft 7
- **Complexity**: Medium (12 fields, 2 nested objects)
- **Version**: 0.1.0-alpha

## Field Catalog

| Field Path | Type | Required | Constraints | Description |
|------------|------|----------|-------------|-------------|
| id | integer | Yes | minimum: 1 | Unique user identifier |
| username | string | Yes | minLength: 3, maxLength: 50, pattern: ^[a-zA-Z0-9_]+$ | Login username |
| email | string | Yes | format: email | Contact email |
| profile.firstName | string | No | minLength: 1 | First name |
| profile.lastName | string | No | minLength: 1 | Last name |
| roles | array[string] | Yes | minItems: 1, enum: [user, admin, guest] | User roles |

## Validation Rules
- Email must be valid format (RFC 5322)
- Username allows only alphanumeric and underscore
- At least one role required
- All dates in ISO 8601 format

## Recommendations
1. Add `additionalProperties: false` to prevent unknown fields
2. Consider UUID for `id` instead of integer for distributed systems
3. Add `maxItems` constraint on `roles` array
4. Document the enum values in description fields
```

---

## Example 2: GraphQL Schema Analysis

### Scenario
Analyzing a GraphQL schema for a microservice API.

### User Request
```
Analyze our GraphQL schema at services/user-service/schema.graphql. We need to understand the type system and relationships.
```

### Skill Workflow

**Step 1**: File Identification
- Locates `services/user-service/schema.graphql`
- Detects GraphQL SDL format
- Verifies syntax

**Step 2**: Socratic Questions
```
I found your GraphQL schema. To provide the most useful analysis:

1. Are you using this with any specific GraphQL server (Apollo, Relay)?
2. Do you need federation compatibility analysis?
3. Should I analyze resolver complexity (N+1 query potential)?
4. Any specific performance or security concerns?
```

**Step 5**: Generates report with:
- Type hierarchy diagram
- Query/Mutation/Subscription inventory
- Relationship graph (showing foreign key patterns)
- N+1 query warnings
- Federation readiness assessment

---

## Example 3: Protocol Buffers Multi-File Analysis

### Scenario
Analyzing multiple .proto files for a gRPC service.

### User Request
```
skill:file-schema-analysis for all proto files in protos/v1/*.proto
```

### Skill Workflow

**Step 1**: File Identification
- Scans `protos/v1/` directory
- Finds: `user.proto`, `order.proto`, `common.proto`
- Detects proto3 syntax

**Step 2**: Context Loading
- Loads protobuf patterns from context
- Checks for existing proto analysis in memory

**Step 3-4**: Cross-File Analysis
- Identifies imported dependencies
- Maps message relationships across files
- Detects common types in `common.proto`
- Analyzes field numbering consistency
- Checks for reserved fields

**Step 5**: Comprehensive Report
```markdown
# gRPC Service Schema Analysis

## File Inventory
1. common.proto (3 messages, 2 enums)
2. user.proto (5 messages, imports common.proto)
3. order.proto (7 messages, imports common.proto, user.proto)

## Dependency Graph
```
common.proto
  ├── user.proto
  │   └── order.proto
  └── order.proto
```

## Cross-File Type Usage
- `common.Money` used in 5 messages across files
- `common.Status` enum referenced 8 times
- `user.UserId` used in order.proto

## Recommendations
1. Field numbers 1-15 are single-byte encoded - good usage
2. Consider using `optional` for backward compatibility
3. Add more descriptive comments for generated documentation
4. Version the package names (e.g., `com.company.api.v1`)
```

---

## Example 4: OpenAPI/Swagger Schema Extraction

### Scenario
Extracting and documenting schemas from an OpenAPI specification.

### User Request
```
Extract all data schemas from our OpenAPI spec at docs/openapi.yaml
```

### Skill Workflow

**Step 1**: File Identification
- Locates `docs/openapi.yaml`
- Detects OpenAPI 3.0.x format

**Step 2**: Clarification
```
I found your OpenAPI specification. Some questions:

1. Do you want just the schema components, or also path/operation analysis?
2. Should I extract request vs response schemas separately?
3. Need validation for any specific OpenAPI linters/validators?
4. Planning to generate client SDKs from this?
```

**Step 3-4**: Schema Extraction
- Extracts all schemas from `components.schemas`
- Identifies `$ref` references and resolves them
- Maps which endpoints use which schemas
- Analyzes discriminators for polymorphism

**Step 5**: Detailed Documentation
- Creates separate documentation for each schema
- Shows request/response usage matrix
- Generates code examples in multiple languages
- Provides JSON Schema extraction for validation

---

## Example 5: Schema Evolution Analysis (Version Comparison)

### Scenario
Comparing two versions of a schema to identify breaking changes.

### User Request
```
Compare schemas/user-v1.json and schemas/user-v2.json. What are the breaking changes?
```

### Skill Workflow

**Step 1**: File Identification
- Identifies both v1 and v2 schemas
- Confirms both are same format

**Step 2**: Questions
```
I'll compare the two schema versions. To guide the analysis:

1. What's your backward compatibility requirement?
2. Do you have existing clients on v1?
3. Need a migration guide for upgrading?
4. Should I check for forward compatibility too?
```

**Step 3-4**: Differential Analysis
- Loads both schemas
- Compares field by field
- Identifies additions, deletions, modifications
- Categorizes as breaking vs non-breaking
- Checks constraint changes

**Step 5**: Migration Report
```markdown
# Schema Migration Report: v1 → v2

## Breaking Changes ⚠️
1. **Removed field**: `profile.middleName` (was optional)
   - Impact: HIGH - Existing data will be lost
   - Recommendation: Migrate to `profile.fullName` or keep as deprecated
   
2. **Type change**: `id` from `integer` to `string` (UUID)
   - Impact: CRITICAL - All client code must update
   - Migration: Provide integer→UUID mapping

3. **New required field**: `email_verified` (boolean)
   - Impact: HIGH - Existing records need default value
   - Recommendation: Set default `false` for existing users

## Non-Breaking Changes ✅
1. **Added optional field**: `profile.phoneNumber`
2. **Relaxed constraint**: `username` maxLength 50→100
3. **Added enum value**: roles enum includes "moderator"

## Compatibility Score
- **Forward Compatible**: NO (removed field)
- **Backward Compatible**: NO (type change, new required field)
- **Recommendation**: Use API versioning (/v1 and /v2 endpoints)

## Migration Checklist
- [ ] Create UUID mapping for existing integer IDs
- [ ] Backfill `email_verified` with default false
- [ ] Update client libraries for type changes
- [ ] Provide migration script for data transformation
- [ ] Maintain /v1 endpoint for 6 months
```

---

## Example 6: Avro Schema for Data Pipeline

### Scenario
Analyzing Avro schema for a data pipeline to ensure compatibility with Kafka/Spark.

### User Request
```
Analyze data/schemas/events.avsc for our Kafka pipeline
```

### Skill Workflow

**Step 1**: Identifies Avro schema file

**Step 2**: Pipeline Context Questions
```
I'll analyze the Avro schema. For pipeline compatibility:

1. Which Kafka version and compatibility mode (BACKWARD, FORWARD, FULL)?
2. Are you using Schema Registry?
3. Need Spark/Hive schema mapping?
4. Any compression requirements?
```

**Step 3-4**: Avro-Specific Analysis
- Analyzes record structure
- Checks union types for null handling
- Identifies logical types (timestamp-millis, decimal)
- Reviews default values
- Checks for schema evolution compatibility

**Step 5**: Pipeline Compatibility Report
- Schema Registry compatibility check
- Spark DataFrame mapping
- Hive table DDL generation
- Parquet conversion notes
- Evolution best practices for the pipeline

---

## Common Patterns

### Pattern: Batch Analysis
```
Analyze all schema files in my project: **/*.schema.json, **/*.proto, **/*.graphql
```

### Pattern: Security Audit
```
Analyze api/schema.json and flag any security concerns (PII fields, missing constraints)
```

### Pattern: Documentation Generation
```
Generate API documentation from schemas/*.json in Markdown format
```

### Pattern: Validation Test Generation
```
Analyze user-schema.json and suggest validation test cases
```

---

**Last Updated**: 2025-02-06
**Maintained by**: The Forge
