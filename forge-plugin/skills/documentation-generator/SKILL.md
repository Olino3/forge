---
name: documentation-generator
description: Generates comprehensive documentation for codebases, APIs, modules, README files, architecture docs, migration guides, and changelogs. Inscribes knowledge into permanence. Analyzes source code to extract structure, public interfaces, dependencies, and usage patterns, then produces clear, structured documentation with examples, cross-references, and diagrams. Supports any language or framework.
---

# Documentation Generator

## ⚠️ MANDATORY COMPLIANCE ⚠️

**CRITICAL**: The 5-step workflow outlined in this document MUST be followed in exact order for EVERY documentation generation task. Skipping steps or deviating from the procedure will result in incomplete and unreliable documentation. This is non-negotiable.

## File Structure

- **SKILL.md** (this file): Main instructions and MANDATORY workflow
- **examples.md**: Documentation scenarios with sample outputs
- **Memory**: Project-specific memory accessed via `memoryStore.getSkillMemory("documentation-generator", "{project-name}")`. See [MemoryStore Interface](../../interfaces/memory_store.md).
- **templates/**:
  - `api_doc_template.md`: Template for API reference documentation
  - `module_doc_template.md`: Template for module/package documentation

## Interface References

- **Context**: Loaded via [ContextProvider Interface](../../interfaces/context_provider.md)
- **Memory**: Accessed via [MemoryStore Interface](../../interfaces/memory_store.md)
- **Schemas**: Validated against [memory_entry.schema.json](../../interfaces/schemas/memory_entry.schema.json)

## Documentation Focus Areas

Comprehensive documentation evaluates 7 critical dimensions:

1. **Code Analysis**: Understand structure, control flow, data models, and design patterns
2. **API Surface Detection**: Identify public interfaces, endpoints, exported symbols, and contracts
3. **Architecture Mapping**: Trace module boundaries, dependency graphs, and layer interactions
4. **Usage Pattern Extraction**: Discover how components are consumed, invoked, and composed
5. **Example Generation**: Produce realistic, runnable examples for every public interface
6. **Cross-Reference Building**: Link related concepts, types, functions, and modules together
7. **Completeness Verification**: Ensure no public interface is undocumented and no section is hollow

**Note**: Focus on clarity and accuracy. Documentation must serve both newcomers and experienced developers. Every word inscribed must earn its place.

---

## MANDATORY WORKFLOW (MUST FOLLOW EXACTLY)

### ⚠️ STEP 1: Identify Documentation Scope (REQUIRED)

**YOU MUST:**
1. Determine **what** to document:
   - A single function or class
   - A module or package
   - An API (REST, GraphQL, RPC)
   - A full project (README / overview)
   - An architecture decision record (ADR)
   - A migration guide or changelog
2. Identify the **target audience**:
   - End users / consumers of the API
   - Internal developers / contributors
   - Operations / DevOps engineers
   - New team members onboarding
3. Determine the **documentation type** (see Documentation Types section below)
4. Ask clarifying questions if scope is ambiguous:
   - Which files, directories, or endpoints should be covered?
   - What level of detail is expected?
   - Are there existing docs to update rather than replace?

**DO NOT PROCEED WITHOUT A CLEAR SCOPE**

### ⚠️ STEP 2: Analyze Source Material (REQUIRED)

**YOU MUST:**
1. Read and parse all source files within the identified scope
2. Extract key structures:
   - Classes, functions, methods, and their signatures
   - Type annotations, return types, and parameter defaults
   - Constants, configuration values, and enumerations
3. Identify public interfaces vs. internal implementation details
4. Map dependencies — imports, inheritance, composition, and external packages
5. Trace data flow and control flow through critical paths
6. Note error handling patterns, edge cases, and invariants
7. Identify existing inline comments, docstrings, and annotations

**DO NOT PROCEED WITHOUT THOROUGH SOURCE ANALYSIS**

### ⚠️ STEP 3: Load Project Memory (REQUIRED)

**YOU MUST:**
1. **CHECK PROJECT MEMORY FIRST**:
   - Identify the project name from the repository root or ask the user
   - Use `memoryStore.getSkillMemory("documentation-generator", "{project-name}")` to load existing project memory. See [MemoryStore Interface](../../interfaces/memory_store.md).
   - **Cross-skill discovery**: Use `memoryStore.getByProject("{project-name}")` to gather insights from all previous skill executions for comprehensive documentation
   - If memory exists, review previously learned documentation conventions, style guides, and project-specific patterns
   - If no memory exists, you will create it later in this process
2. Check for existing documentation in the repository:
   - README files, CONTRIBUTING guides, API docs, wiki pages
   - Inline docstring conventions (Google style, NumPy style, JSDoc, etc.)
   - Documentation tooling (Sphinx, MkDocs, TypeDoc, Javadoc, etc.)
3. Adopt the project's existing documentation style if one is established
4. Note any documentation gaps that should be filled

**DO NOT PROCEED WITHOUT CHECKING PROJECT MEMORY AND EXISTING DOCS**

### ⚠️ STEP 4: Generate Documentation (REQUIRED)

**YOU MUST:**
1. Select the appropriate template from `templates/` based on the documentation type
2. Write structured documentation that includes:
   - **Overview**: Purpose, context, and high-level description
   - **Installation / Setup**: Prerequisites, dependencies, environment setup (if applicable)
   - **API Reference**: Every public interface with signature, description, parameters, return values, exceptions, and examples
   - **Examples**: Realistic, runnable code snippets for common use cases
   - **Configuration**: All configurable options with defaults and descriptions
   - **Error Handling**: Common errors, troubleshooting steps, and edge cases
   - **Cross-References**: Links to related modules, types, and external resources
3. Include diagrams or ASCII art for architecture and data flow where helpful
4. Use consistent formatting: headings, code blocks, tables, and lists
5. Write in the imperative mood for instructions, present tense for descriptions

**DO NOT GENERATE SHALLOW OR PLACEHOLDER DOCUMENTATION**

### ⚠️ STEP 5: Review & Output (REQUIRED)

**YOU MUST:**
1. **Validate completeness**: Every public interface must be documented
2. **Check cross-references**: All internal links and references must resolve
3. **Verify examples**: Code examples must be syntactically correct and representative
4. **Review tone and clarity**: Documentation must be accessible to the target audience
5. **Ask user for output destination**:
   - **Option A**: Write to file(s) in the repository (e.g., `docs/`, `README.md`)
   - **Option B**: Write to `/claudedocs/` directory
   - **Option C (Default)**: Output inline in the conversation
6. Save the generated documentation to the chosen destination
7. Confirm the output was written successfully

**DO NOT SKIP VALIDATION**

**After completing generation, UPDATE PROJECT MEMORY**:

Use `memoryStore.update(layer="skill-specific", skill="documentation-generator", project="{project-name}", ...)` to store:

1. **doc_conventions.md**: Documentation style, formatting rules, and tooling used
2. **generated_docs.md**: Log of documentation generated with dates and scope
3. **project_structure.md**: Key modules, APIs, and architecture notes discovered

Timestamps and staleness tracking are handled automatically by MemoryStore. See [MemoryStore Interface](../../interfaces/memory_store.md).

This memory will be consulted in future documentation tasks to maintain consistency.

---

## Compliance Checklist

Before completing ANY documentation generation, verify:
- [ ] Step 1: Documentation scope, target audience, and doc type identified
- [ ] Step 2: Source material analyzed — structures, interfaces, and dependencies extracted
- [ ] Step 3: Project memory checked via `memoryStore.getSkillMemory()` and existing docs reviewed
- [ ] Step 4: Documentation generated with overview, API reference, examples, and cross-references
- [ ] Step 5: Output validated for completeness, accuracy, and clarity AND project memory updated

**FAILURE TO COMPLETE ALL STEPS INVALIDATES THE DOCUMENTATION**

---

## Documentation Types

### API Reference
Complete reference for REST, GraphQL, or RPC APIs. Includes endpoints, methods, parameters, request/response schemas, authentication, rate limits, and error codes. Use `templates/api_doc_template.md`.

### Module Guide
In-depth guide for a library, package, or module. Covers installation, quick start, full API reference, configuration, and examples. Use `templates/module_doc_template.md`.

### README
Project overview for the repository root. Includes purpose, features, installation, quick start, contributing guidelines, and license.

### Architecture Doc
High-level architecture documentation. Covers system components, data flow, deployment topology, technology choices, and design rationale.

### Changelog
Chronological record of notable changes per version. Follows Keep a Changelog format: Added, Changed, Deprecated, Removed, Fixed, Security.

### Migration Guide
Step-by-step instructions for upgrading between breaking versions. Includes before/after comparisons, automated migration scripts, and rollback procedures.

---

## Further Reading

Refer to official documentation and standards:
- **Documentation Standards**:
  - Diátaxis Framework: https://diataxis.fr/
  - Write the Docs: https://www.writethedocs.org/guide/
- **API Documentation**:
  - OpenAPI Specification: https://swagger.io/specification/
  - API Style Guide: https://apistylebook.com/
- **Tools**:
  - Sphinx: https://www.sphinx-doc.org/
  - MkDocs: https://www.mkdocs.org/
  - TypeDoc: https://typedoc.org/

---

## Version History

- v1.1.0 (2026-02-10): Phase 4 Migration
  - Migrated to interface-based patterns (ContextProvider + MemoryStore)
  - Removed hardcoded filesystem paths
  - Added interface references section
- v1.0.0 (2025-01-XX): Initial release
  - Mandatory 5-step workflow
  - API and module documentation templates
  - Project memory system for documentation conventions
  - Support for 6 documentation types
  - Example scenarios for common documentation tasks
