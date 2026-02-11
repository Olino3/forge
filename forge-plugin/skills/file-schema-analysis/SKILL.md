---
name: file-schema-analysis
description: Analyze and document file-based data schemas across multiple formats (JSON Schema, XML/XSD, YAML, Protobuf, Avro, Parquet, GraphQL, OpenAPI). Extracts structure, constraints, relationships, and evolution patterns. Generates comprehensive schema documentation with field inventory, validation rules, and version history. Use for API contract analysis, data format validation, schema migration planning, and documentation generation.
---

# File Schema Analysis Expert

## ⚠️ MANDATORY COMPLIANCE ⚠️

**CRITICAL**: The 5-step workflow outlined in this document MUST be followed in exact order for EVERY schema analysis. Skipping steps or deviating from the procedure will result in incomplete and unreliable analysis. This is non-negotiable.

## File Structure

- **SKILL.md** (this file): Main instructions and MANDATORY workflow
- **examples.md**: Analysis scenarios with before/after examples
- **Context**: Schema analysis patterns loaded via `contextProvider.getDomainIndex("schema")`. See [ContextProvider Interface](../../interfaces/context_provider.md).
- **Memory**: Project-specific memory accessed via `memoryStore.getSkillMemory("file-schema-analysis", "{project-name}")`. See [MemoryStore Interface](../../interfaces/memory_store.md).
- **templates/**: `analysis_report.md`, `schema_visualization.md`
- **scripts/**: Helper utilities for schema extraction

## Interface References

- **Context**: Loaded via [ContextProvider Interface](../../interfaces/context_provider.md)
- **Memory**: Accessed via [MemoryStore Interface](../../interfaces/memory_store.md)
- **Schemas**: Validated against [context_metadata.schema.json](../../interfaces/schemas/context_metadata.schema.json) and [memory_entry.schema.json](../../interfaces/schemas/memory_entry.schema.json)

## Analysis Focus Areas

File schema analysis evaluates 7 critical dimensions:

1. **Structure Detection**: Format identification, field hierarchy, nesting levels
2. **Type System**: Data types, constraints, validation rules, formats
3. **Relationships**: References, dependencies, composition patterns
4. **Validation**: Required vs optional fields, constraints, patterns
5. **Documentation**: Inline comments, descriptions, examples
6. **Evolution**: Version tracking, compatibility analysis, breaking changes
7. **Quality**: Anti-patterns, best practices, performance implications

---

## MANDATORY WORKFLOW (MUST FOLLOW EXACTLY)

### ⚠️ STEP 1: Identify Target Files (REQUIRED)

**YOU MUST:**
1. Ask the user which files to analyze:
   - Specific file paths (e.g., `schema/user.json`, `api.proto`)
   - Directory patterns (e.g., `schemas/*.json`, `**/*.proto`)
   - File format types (JSON Schema, Protobuf, GraphQL, etc.)
2. If not specified, scan the current directory for common schema files:
   - JSON Schema: `*.schema.json`, `schemas/*.json`
   - Protobuf: `*.proto`
   - GraphQL: `*.graphql`, `*.gql`, `schema.graphql`
   - OpenAPI: `openapi.yaml`, `swagger.json`, `api.yaml`
   - Avro: `*.avsc`
   - XML Schema: `*.xsd`
3. Verify files exist and are readable
4. Identify file format for each file (by extension and content inspection)

**DO NOT PROCEED WITHOUT IDENTIFYING TARGET FILES**

### ⚠️ STEP 2: Load Project Memory & Context (REQUIRED)

**YOU MUST:**
1. **CHECK PROJECT MEMORY FIRST**:
   - Identify the project name from the repository root or ask the user
   - Use `memoryStore.getSkillMemory("file-schema-analysis", "{project-name}")` to load existing project memory. See [MemoryStore Interface](../../interfaces/memory_store.md).
   - If memory exists, review previously analyzed schemas, patterns, and project-specific context
   - If no memory exists, you will create it later in this process

2. **USE CONTEXT INDEXES FOR EFFICIENT LOADING**:
   - Use `contextProvider.getDomainIndex("schema")` to discover available schema context files. See [ContextProvider Interface](../../interfaces/context_provider.md).
   - Based on the file formats identified in Step 1, use `contextProvider.getConditionalContext("schema", detection)` to load relevant files
   - Always load `common_patterns.md` via `contextProvider.getAlwaysLoadFiles("schema")`
   - If analyzing security-sensitive schemas, use `contextProvider.getCrossDomainContext("schema", {"security": true})`

3. **Ask clarifying questions** in Socratic format:
   - What is the purpose of these schema files?
   - Are you planning a migration or evolution of the schema?
   - What documentation output format do you prefer?
   - Any specific concerns (validation, performance, compatibility)?
   - Target platforms or systems that consume these schemas?

**DO NOT PROCEED WITHOUT COMPLETING THIS STEP**

### ⚠️ STEP 3: Read and Parse Schema Files (REQUIRED)

**YOU MUST:**
1. **READ each identified file** using the view tool
2. **Detect format** if not already determined:
   - Check file extension
   - Inspect content structure (JSON, XML, Protobuf syntax, GraphQL SDL, YAML)
   - Identify schema definition keywords (`$schema`, `message`, `type`, etc.)
3. **Extract metadata**:
   - Schema version (if present)
   - Namespace/package information
   - Comments and documentation
   - Examples or default values
4. **Verify readability**: Ensure files are valid and parseable

**DO NOT PROCEED WITHOUT READING THE FILES**

### ⚠️ STEP 4: Analyze Schema Structure (REQUIRED)

**YOU MUST perform deep analysis covering ALL these aspects:**

#### 4.1 Structure Analysis
- **Identify all entities/types/messages**: Top-level definitions
- **Map field hierarchy**: Nested structures, composition patterns
- **Detect relationships**: References ($ref, foreign keys), dependencies
- **Analyze cardinality**: Single values, arrays, maps, repeated fields

#### 4.2 Type System Analysis
- **Extract field types**: Primitives, complex types, custom types
- **Identify constraints**:
  - Required vs optional fields
  - Validation rules (min/max, patterns, enums)
  - Default values
  - Formats (email, date, UUID, etc.)
- **Check for polymorphism**: Union types, discriminators, oneOf/anyOf

#### 4.3 Validation Rules
- **Field-level validations**: Length, range, pattern, format
- **Cross-field validations**: Dependencies, conditional requirements
- **Business rules**: Custom constraints, check constraints
- **Error conditions**: What makes data invalid?

#### 4.4 Documentation Extraction
- **Inline documentation**: Comments, description fields
- **Examples**: Sample valid data
- **Deprecated fields**: Marked for removal
- **Custom extensions**: Vendor-specific additions

#### 4.5 Evolution and Versioning
- **Version identification**: Current schema version
- **Change history**: If documented in comments or separate files
- **Compatibility markers**: Breaking vs non-breaking changes
- **Migration notes**: How to upgrade from previous versions

#### 4.6 Quality Assessment
- **Check for anti-patterns**:
  - Overly deep nesting (6+ levels)
  - Ambiguous field names
  - Missing validation on critical fields
  - Inconsistent naming conventions
  - Lack of documentation
- **Identify best practices**:
  - Clear, descriptive names
  - Appropriate use of types and constraints
  - Good documentation coverage
  - Logical structure organization

#### 4.7 Cross-References
- **External dependencies**: Imported schemas, shared definitions
- **Internal references**: Reused types, common patterns
- **Circular references**: Potential issues

**USE THE TEMPLATES** in `templates/` directory to structure your analysis

**DO NOT PROCEED WITHOUT COMPREHENSIVE ANALYSIS**

### ⚠️ STEP 5: Generate Analysis Report & Update Memory (REQUIRED)

**YOU MUST:**

1. **Generate comprehensive analysis report** using the template from `templates/analysis_report.md`:
   - Executive summary
   - File inventory
   - Field catalog (all fields with types, constraints, descriptions)
   - Relationship diagram (ASCII or Mermaid)
   - Validation rules summary
   - Quality assessment
   - Recommendations for improvement
   - Version history (if available)

2. **Create schema visualization** using `templates/schema_visualization.md`:
   - Entity-relationship diagram
   - Type hierarchy
   - Dependency graph

3. **UPDATE PROJECT MEMORY**:
   - Use `memoryStore.update(layer="skill-specific", skill="file-schema-analysis", project="{project-name}", ...)` to store:
   - Discovered patterns
   - Schema conventions and naming patterns
   - Format preferences
   - Dependencies and relationships
   - Metadata for future reference
   - Timestamps and staleness tracking are handled automatically by MemoryStore. See [MemoryStore Interface](../../interfaces/memory_store.md).

4. **Provide actionable recommendations**:
   - Suggest improvements for quality issues
   - Identify missing validations
   - Recommend documentation additions
   - Highlight breaking changes if comparing versions

**MEMORY UPDATE IS MANDATORY - DO NOT SKIP**

---

## Output Requirements

### Analysis Report Must Include:

1. **Schema Inventory**
   - File paths and formats
   - Version information
   - Size and complexity metrics

2. **Field Catalog**
   - Complete list of all fields/attributes
   - Types and constraints
   - Required/optional status
   - Default values
   - Documentation/descriptions

3. **Visual Representations**
   - Entity-relationship diagram
   - Type hierarchy diagram
   - Dependency graph

4. **Validation Summary**
   - All validation rules
   - Business constraints
   - Format requirements

5. **Quality Report**
   - Anti-patterns found
   - Best practices followed
   - Recommendations

6. **Evolution Analysis** (if multiple versions)
   - Changes between versions
   - Breaking changes
   - Migration guide

---

## Socratic Prompting Guidelines

When interacting with users, ask clarifying questions such as:

**Understanding Intent:**
- "What decisions are you trying to make with this schema analysis?"
- "Are you planning to modify, migrate, or document these schemas?"
- "Do you need this for technical documentation or API contracts?"

**Scope Definition:**
- "Should I analyze all schema files or focus on specific ones?"
- "Are there related schemas in other systems I should be aware of?"
- "Do you need cross-version comparison?"

**Output Preferences:**
- "What format would you prefer for the analysis report (Markdown, JSON, HTML)?"
- "Do you need visual diagrams (Mermaid, PlantUML, ASCII)?"
- "Should I prioritize depth (complete details) or breadth (overview)?"

**Context Understanding:**
- "What systems or languages consume these schemas?"
- "Are there known issues or pain points with the current schema?"
- "Any compliance or regulatory requirements for the data structure?"

---

## Quality Standards

### Your analysis MUST:
- ✅ Be **100% accurate** to the actual schema definition
- ✅ Cover **all fields and types** without omission
- ✅ Identify **all validation rules and constraints**
- ✅ Extract **all documentation** present in the files
- ✅ Detect **format-specific features** correctly
- ✅ Provide **actionable recommendations**
- ✅ Use **templates** for consistent output
- ✅ Update **project memory** for future reference

### Your analysis MUST NOT:
- ❌ Hallucinate fields or types not in the schema
- ❌ Miss required or optional markers
- ❌ Ignore validation constraints
- ❌ Skip documentation extraction
- ❌ Provide generic recommendations without analysis basis

---

## Integration with Other Skills

**Combine with:**
- `database-schema-analysis`: For schemas stored in database systems
- `python-code-review`: When analyzing Python Pydantic models or dataclasses
- `dotnet-code-review`: When analyzing C# data models
- `generate-python-unit-tests`: To create schema validation tests

---

## Version History

- **v1.1.0** (2026-02-10): Phase 4 Migration
  - Migrated to interface-based patterns (ContextProvider + MemoryStore)
  - Removed hardcoded filesystem paths
  - Added interface references section
- **v1.0.0** (2025-02-06): Initial release
  - Support for JSON Schema, Protobuf, GraphQL, OpenAPI, Avro, XML/XSD
  - Comprehensive analysis workflow
  - Template-based reporting
  - Project memory integration

---

**Last Updated**: 2025-02-06
**Maintained by**: The Forge
