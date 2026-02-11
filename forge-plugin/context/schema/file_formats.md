---
id: "schema/file_formats"
domain: schema
title: "File Format Schema Patterns"
type: reference
estimatedTokens: 1550
loadingStrategy: onDemand
version: "1.0.0"
lastUpdated: "2026-02-10"
sections:
  - name: "Overview"
    estimatedTokens: 11
    keywords: [overview]
  - name: "JSON Schema Detection"
    estimatedTokens: 98
    keywords: [json, schema, detection]
  - name: "XML Schema (XSD) Patterns"
    estimatedTokens: 43
    keywords: [xml, schema, xsd, patterns]
  - name: "YAML Schema Analysis"
    estimatedTokens: 42
    keywords: [yaml, schema, analysis]
  - name: "Protocol Buffers (Protobuf)"
    estimatedTokens: 71
    keywords: [protocol, buffers, protobuf]
  - name: "Apache Avro"
    estimatedTokens: 59
    keywords: [apache, avro]
  - name: "Apache Parquet"
    estimatedTokens: 47
    keywords: [apache, parquet]
  - name: "CSV/TSV Schema Inference"
    estimatedTokens: 38
    keywords: [csvtsv, schema, inference]
  - name: "GraphQL Schema"
    estimatedTokens: 61
    keywords: [graphql, schema]
  - name: "OpenAPI/Swagger"
    estimatedTokens: 60
    keywords: [openapiswagger]
  - name: "Schema Evolution Patterns"
    estimatedTokens: 42
    keywords: [schema, evolution, patterns]
  - name: "Common Anti-Patterns"
    estimatedTokens: 66
    keywords: [anti-patterns]
  - name: "Schema Documentation Extraction"
    estimatedTokens: 40
    keywords: [schema, documentation, extraction]
tags: [schema, json, xml, yaml, protobuf, avro, parquet, graphql, openapi]
---

# File Format Schema Patterns

## Overview

This document provides patterns for analyzing and understanding file-based data schemas across common formats.

---

## JSON Schema Detection

### Implicit Schema Analysis
```json
{
  "user": {
    "id": 12345,
    "name": "John Doe",
    "email": "john@example.com",
    "roles": ["admin", "user"],
    "metadata": {
      "created_at": "2024-01-01T00:00:00Z",
      "last_login": null
    }
  }
}
```

**Detected Structure**:
- Root object with nested `user` object
- Primitive types: number (id), string (name, email), array (roles), object (metadata), null
- Date string pattern detected (ISO 8601)
- Optional fields (last_login can be null)

### Explicit JSON Schema
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "name": {"type": "string", "minLength": 1},
    "age": {"type": "integer", "minimum": 0},
    "email": {"type": "string", "format": "email"}
  },
  "required": ["name", "email"]
}
```

**Key Elements to Extract**:
- Schema version ($schema)
- Type constraints (type, format)
- Validation rules (minLength, minimum, pattern)
- Required vs optional fields
- Default values
- Nested schemas and references ($ref)

---

## XML Schema (XSD) Patterns

### Basic XSD Structure
```xml
<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">
  <xs:element name="user">
    <xs:complexType>
      <xs:sequence>
        <xs:element name="name" type="xs:string"/>
        <xs:element name="age" type="xs:integer" minOccurs="0"/>
        <xs:element name="email" type="xs:string"/>
      </xs:sequence>
      <xs:attribute name="id" type="xs:ID" use="required"/>
    </xs:complexType>
  </xs:element>
</xs:schema>
```

**Key Patterns**:
- Elements vs Attributes
- Simple vs Complex types
- Occurrence constraints (minOccurs, maxOccurs)
- Sequences, choices, and all groups
- Type restrictions and extensions

---

## YAML Schema Analysis

### Implicit Structure
```yaml
database:
  host: localhost
  port: 5432
  credentials:
    username: admin
    password: ${DB_PASSWORD}  # Environment variable
  options:
    - ssl: true
    - pool_size: 10
```

**Patterns to Detect**:
- Nested mappings (dictionaries)
- Scalar types (string, number, boolean)
- Sequences (arrays/lists)
- Environment variable interpolation
- Anchors and aliases for reuse
- Multi-document files (---)

---

## Protocol Buffers (Protobuf)

```protobuf
syntax = "proto3";

message User {
  int64 id = 1;
  string name = 2;
  string email = 3;
  repeated string roles = 4;
  Metadata metadata = 5;
  
  message Metadata {
    int64 created_at = 1;
    optional int64 last_login = 2;
  }
}

enum Role {
  ROLE_UNSPECIFIED = 0;
  ROLE_USER = 1;
  ROLE_ADMIN = 2;
}
```

**Key Elements**:
- Syntax version (proto2 vs proto3)
- Message definitions (similar to classes)
- Field types and numbers (for wire format)
- Repeated fields (arrays)
- Optional fields (proto3)
- Nested messages
- Enumerations
- Import dependencies

---

## Apache Avro

```json
{
  "type": "record",
  "name": "User",
  "namespace": "com.example",
  "fields": [
    {"name": "id", "type": "long"},
    {"name": "name", "type": "string"},
    {"name": "email", "type": "string"},
    {"name": "roles", "type": {"type": "array", "items": "string"}},
    {"name": "last_login", "type": ["null", "long"], "default": null}
  ]
}
```

**Patterns**:
- Record types (similar to structs)
- Primitive types (null, boolean, int, long, float, double, bytes, string)
- Complex types (record, enum, array, map, union, fixed)
- Union types for optional fields
- Default values
- Namespace organization

---

## Apache Parquet

**Analysis Approach** (binary format):
- Extract schema from metadata
- Identify column names and types
- Analyze compression codecs
- Check for nested structures (groups)
- Review statistics (min, max, null counts)

**Schema Representation**:
```
message schema {
  required int64 id;
  required binary name (UTF8);
  required binary email (UTF8);
  optional group metadata {
    required int64 created_at;
    optional int64 last_login;
  }
}
```

---

## CSV/TSV Schema Inference

### Header-based Detection
```csv
user_id,name,email,age,created_date
1001,"John Doe",john@example.com,30,2024-01-01
1002,"Jane Smith",jane@example.com,25,2024-01-02
```

**Inference Strategy**:
1. Use first row as field names
2. Sample multiple rows to infer types
3. Detect patterns: dates, emails, numbers, booleans
4. Identify nullable columns (empty values)
5. Detect delimiters and quote characters
6. Check for multi-line values

---

## GraphQL Schema

```graphql
type User {
  id: ID!
  name: String!
  email: String!
  age: Int
  roles: [Role!]!
  metadata: Metadata
}

type Metadata {
  createdAt: DateTime!
  lastLogin: DateTime
}

enum Role {
  USER
  ADMIN
  GUEST
}

type Query {
  user(id: ID!): User
  users(limit: Int = 10): [User!]!
}
```

**Key Elements**:
- Types and fields
- Required vs optional (! modifier)
- Scalars (Int, Float, String, Boolean, ID)
- Custom scalars (DateTime)
- Lists and non-null lists
- Enums
- Input types
- Query/Mutation/Subscription definitions

---

## OpenAPI/Swagger

```yaml
openapi: 3.0.0
components:
  schemas:
    User:
      type: object
      required:
        - id
        - name
        - email
      properties:
        id:
          type: integer
          format: int64
        name:
          type: string
          minLength: 1
          maxLength: 100
        email:
          type: string
          format: email
        roles:
          type: array
          items:
            type: string
            enum: [user, admin]
```

**Analysis Points**:
- Schema definitions under components
- Type constraints and formats
- Required vs optional properties
- Array items and uniqueItems
- Discriminators for polymorphism
- References ($ref) for reusability
- Examples and default values

---

## Schema Evolution Patterns

### Versioning Strategies
1. **Inline Version Field**: `{"version": "1.0", ...}`
2. **Schema URI**: `{"$schema": "http://api.example.com/schemas/user/v2"}`
3. **Namespace**: `com.example.user.v2.User`
4. **File Name**: `user-schema-v2.json`

### Compatibility Rules
- **Forward Compatible**: Old code can read new data (add optional fields)
- **Backward Compatible**: New code can read old data (don't remove fields)
- **Full Compatible**: Both directions work

---

## Common Anti-Patterns

### 1. Stringly-Typed Data
❌ `{"status": "1"}` (should be integer or enum)
✅ `{"status": 1}` or `{"status": "active"}`

### 2. Implicit Nullability
❌ Field may or may not be present without documentation
✅ Explicit optional markers or null unions

### 3. Mixed Array Types
❌ `["string", 123, true]` (weak typing)
✅ Homogeneous arrays with clear types

### 4. Deeply Nested Structures
❌ 6+ levels of nesting (hard to query/validate)
✅ Flatten or use references

### 5. Ambiguous Field Names
❌ `date`, `timestamp`, `time` (unclear format)
✅ `created_at_iso8601`, `updated_timestamp_unix`

---

## Schema Documentation Extraction

### Auto-Generated Documentation Should Include:
1. **Field Inventory**: All fields with types
2. **Constraints**: Required, min/max, patterns, enums
3. **Relationships**: References, nested objects
4. **Examples**: Sample valid data
5. **Evolution History**: Version changes
6. **Validation Rules**: Custom business logic
7. **Performance Notes**: Indexed fields, large arrays

---

**Last Updated**: 2025-02-06
**Maintained by**: The Forge
