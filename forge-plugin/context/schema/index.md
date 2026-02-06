# Schema Analysis Context Files

## Overview

This directory contains reference material for schema analysis tasks across file formats and database systems. Use these files to understand common patterns, anti-patterns, and best practices when analyzing data structures.

## File Guide

### 📁 **file_formats.md**
**When to use**: Analyzing file-based schemas (JSON, XML, YAML, Protobuf, Avro, Parquet, etc.)

**Contains**:
- Common file format patterns and structures
- Schema detection techniques for various formats
- Validation patterns and constraint identification
- Version evolution tracking
- Documentation extraction methods

**Best for**: File schema analysis, data interchange format validation, API contract analysis

---

### 🗄️ **database_patterns.md**
**When to use**: Analyzing database schemas (SQL and NoSQL)

**Contains**:
- Relational database patterns (tables, relationships, constraints)
- NoSQL patterns (document, key-value, column-family, graph)
- Index analysis and optimization patterns
- Normalization and denormalization patterns
- Data type mapping across database systems
- Performance implications of schema design

**Best for**: Database schema reverse engineering, migration planning, schema optimization

---

### 🔗 **common_patterns.md**
**When to use**: Understanding universal schema concepts applicable to both files and databases

**Contains**:
- Universal schema patterns (hierarchies, relationships, constraints)
- Data modeling principles (entities, attributes, associations)
- Schema versioning and evolution strategies
- Documentation and metadata standards
- Anti-patterns and code smells in schema design
- Cross-platform compatibility considerations

**Best for**: High-level schema design analysis, cross-system schema comparison, documentation generation

---

## Loading Strategy

### For File Schema Analysis
```
1. Read index.md (this file)
2. Load file_formats.md
3. Load common_patterns.md if analyzing complex structures
```

### For Database Schema Analysis
```
1. Read index.md (this file)
2. Load database_patterns.md
3. Load common_patterns.md if analyzing design patterns
```

### For Comprehensive Schema Work
```
1. Read index.md (this file)
2. Load common_patterns.md first (foundation)
3. Load specific format files as needed
```

---

## Related Context

- **../security/**: Security considerations for schema design (SQL injection, data exposure)
- **../python/**, **../dotnet/**, **../angular/**: Language-specific schema handling patterns
- **../azure/**: Cloud database and storage schema patterns

---

## Best Practices

1. **Always start with index.md** to understand which files are relevant
2. **Don't load all files** - select only what you need for the current task
3. **Cross-reference** with language-specific contexts when implementing schema handlers
4. **Update memory** with project-specific schema patterns you discover

---

**Last Updated**: 2025-02-06
**Maintained by**: The Forge
