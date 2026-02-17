---
name: code-documenter
## description: Technical documentation, API docs, and code comments. Generates inline code comments, function/method docstrings, API documentation, module and package docs, architecture documentation, and README/guides. Follows language-specific conventions (PEP 257, JSDoc, XML docs, GoDoc) and adapts to project style. Use for improving code readability, onboarding new developers, and maintaining living documentation alongside code.

# Code Documenter

## ⚠️ MANDATORY COMPLIANCE ⚠️

**CRITICAL**: The 5-step workflow outlined in this document MUST be followed in exact order for EVERY documentation task. Skipping steps or deviating from the procedure will result in incomplete and unreliable documentation. This is non-negotiable.

## File Structure

- **SKILL.md** (this file): Main instructions and MANDATORY workflow
- **examples.md**: Documentation scenarios with sample outputs
- **Context**: Relevant domain context loaded via `contextProvider`. See [ContextProvider Interface](../../interfaces/context_provider.md).
- **Memory**: Project-specific memory accessed via `memoryStore.getSkillMemory("code-documenter", "{project-name}")`. See [MemoryStore Interface](../../interfaces/memory_store.md).

## Documentation Focus Areas

Comprehensive code documentation covers 6 critical dimensions:

1. **Inline Code Comments**: Clarify complex logic, algorithms, edge cases, and non-obvious decisions within source code
2. **Function/Method Documentation**: Docstrings with descriptions, parameters, return values, exceptions, and usage examples
3. **API Documentation**: Endpoint references, request/response schemas, authentication, error codes, and rate limits
4. **Module/Package Documentation**: Package-level overviews, public interface summaries, dependency explanations, and quick-start guides
5. **Architecture Documentation**: System overviews, component interactions, data flow diagrams, and design rationale
6. **README & Guides**: Project introductions, installation instructions, usage examples, contributing guidelines, and onboarding material

**Note**: Follow language-specific conventions (PEP 257 for Python, JSDoc for JavaScript/TypeScript, XML docs for C#, GoDoc for Go). Adapt to the project's existing documentation style when one is established.

---

## Purpose

[TODO: Add purpose description]


## MANDATORY WORKFLOW (MUST FOLLOW EXACTLY)

### ⚠️ STEP 1: Identify Documentation Scope (REQUIRED)

**YOU MUST:**
1. Determine **what code** to document:
   - A single function, method, or class
   - A module, package, or library
   - REST/GraphQL/RPC API endpoints
   - An entire project or subsystem
   - Architecture decisions or design documents
   - README, onboarding guides, or contributor docs
2. Identify the **target audience**:
   - End users / API consumers
   - Internal developers / contributors
   - New team members onboarding
   - Operations / DevOps engineers
3. Determine the **documentation type**:
   - Inline comments and docstrings
   - API reference documentation
   - Module/package guide
   - Architecture overview
   - README or contributor guide
4. Ask clarifying questions if scope is ambiguous:
   - Which files, directories, or endpoints should be documented?
   - What level of detail is expected (summary vs. comprehensive)?
   - Are there existing docs to update rather than replace?
   - What docstring convention does the project use?

**DO NOT PROCEED WITHOUT A CLEAR SCOPE**

### ⚠️ STEP 2: Load Project Memory (REQUIRED)

**YOU MUST:**
1. **CHECK PROJECT MEMORY FIRST**:
   - Identify the project name from the repository root or ask the user
   - Use `memoryStore.getSkillMemory("code-documenter", "{project-name}")` to load project-specific patterns
   - **Cross-skill discovery**: Use `memoryStore.getByProject("{project-name}")` to check for code review findings, test insights, schema analysis, or other skill results that inform documentation
   - If memory exists: Review previously learned documentation conventions, docstring style, and project-specific patterns
   - If no memory exists (empty result): Note this is the first documentation task; you will create memory later
2. Check for existing documentation in the repository:
   - Inline docstring conventions (Google style, NumPy style, JSDoc, XML docs, etc.)
   - Documentation tooling (Sphinx, MkDocs, TypeDoc, Javadoc, Doxygen, etc.)
   - Existing README files, API docs, and contributor guides
3. Adopt the project's existing documentation style if one is established
4. Note any documentation gaps that should be filled

See [ContextProvider](../../interfaces/context_provider.md) and [MemoryStore](../../interfaces/memory_store.md) interfaces.

**DO NOT PROCEED WITHOUT COMPLETING THIS STEP**

### ⚠️ STEP 3: Load Context (REQUIRED)

**YOU MUST use contextProvider to load relevant domain context**:

1. **Identify relevant domains** based on the code being documented:
   - Use `contextProvider.getDomainIndex("{language}")` for language-specific conventions (e.g., `"python"`, `"typescript"`, `"dotnet"`)
   - Use `contextProvider.getDomainIndex("security")` if documenting security-sensitive code
   - Use `contextProvider.getDomainIndex("architecture")` if documenting system design
2. **Load always-required files**: Use `contextProvider.getAlwaysLoadFiles("{language}")` for universal patterns and conventions
3. **Load conditional context**: Use `contextProvider.getConditionalContext("{language}", detection)` for framework-specific patterns:
   - If Django/Flask/FastAPI detected: Load framework-specific documentation conventions
   - If React/Angular/Vue detected: Load component documentation patterns
   - If API endpoints detected: Load API documentation standards (OpenAPI, etc.)
4. **Load cross-domain context** if applicable: Use `contextProvider.getCrossDomainContext("{language}", triggers)` for security documentation, testing documentation, etc.

**Progressive loading**: Only load files relevant to the detected language, framework, and documentation type. The ContextProvider respects the 4-6 file token budget automatically.

**DO NOT SKIP LOADING RELEVANT CONTEXT FILES**

### ⚠️ STEP 4: Generate Documentation (REQUIRED)

**YOU MUST:**
1. **Write inline comments** for complex logic:
   - Explain *why*, not *what* — the code shows what, comments explain reasoning
   - Annotate non-obvious algorithms, edge cases, and workarounds
   - Mark TODO/FIXME/HACK with context and ticket references where applicable
2. **Write docstrings** following language conventions:
   - **Python**: PEP 257, Google style or NumPy style (match project convention)
   - **TypeScript/JavaScript**: JSDoc with `@param`, `@returns`, `@throws`, `@example`
   - **C#**: XML documentation comments with `<summary>`, `<param>`, `<returns>`, `<exception>`
   - **Go**: GoDoc conventions with package-level and function-level comments
   - **Java**: Javadoc with `@param`, `@return`, `@throws`
3. **Write API documentation** for endpoints:
   - HTTP method, path, and description
   - Request parameters (path, query, header, body) with types and constraints
   - Response schemas with examples for success and error cases
   - Authentication requirements and rate limits
4. **Write module/package documentation**:
   - Overview paragraph describing purpose and usage context
   - Public interface summary with brief descriptions
   - Quick-start example showing typical usage
   - Cross-references to related modules
5. Ensure documentation is:
   - **Accurate**: Matches actual code behavior
   - **Complete**: All public interfaces documented
   - **Consistent**: Same style and depth throughout
   - **Concise**: No unnecessary repetition or filler

**DO NOT GENERATE SHALLOW OR PLACEHOLDER DOCUMENTATION**

### ⚠️ STEP 5: Output & Update Memory (REQUIRED)

**YOU MUST ask user for preferred output format**:

- **Option A**: Inline — add documentation directly to source files (docstrings, comments)
- **Option B**: Standalone files — write to `docs/` directory or `/claudedocs/`
- **Option C (Default)**: Both inline documentation and standalone reference docs

**DO NOT CHOOSE FORMAT WITHOUT USER INPUT**

**For generated documentation, YOU MUST ensure**:
1. **Accuracy**: All documented parameters, return types, and behaviors match the actual code
2. **Completeness**: Every public function, class, method, and endpoint is documented
3. **Examples**: At least one usage example per public interface
4. **Cross-references**: Links between related components and external resources
5. Save output to the chosen destination and confirm successful write

**After completing documentation, UPDATE PROJECT MEMORY**:

Use `memoryStore.update("code-documenter", "{project-name}", ...)` to create or update memory files:

1. **doc_conventions.md**: Documentation style (Google/NumPy/JSDoc), formatting rules, tooling
2. **documented_components.md**: Log of components documented with dates and scope
3. **project_patterns.md**: Coding patterns, naming conventions, and architecture notes discovered

Timestamps and staleness tracking are managed automatically by MemoryStore. See [MemoryStore Interface](../../interfaces/memory_store.md) for `update()` and `append()` method details.

---

### Step 6: Generate Output

Create deliverables and save to `/claudedocs/`:
- Follow OUTPUT_CONVENTIONS.md naming: `code-documenter_{project}_{YYYY-MM-DD}.md`
- Include all required sections
- Provide clear, actionable recommendations

## Interface References

- **Context**: Loaded via [ContextProvider Interface](../../interfaces/context_provider.md)
- **Memory**: Accessed via [MemoryStore Interface](../../interfaces/memory_store.md)
- **Schemas**: Validated against [memory_entry.schema.json](../../interfaces/schemas/memory_entry.schema.json)

## Compliance Checklist

Before completing ANY documentation task, verify:
- [ ] Step 1: Documentation scope, target audience, and documentation type identified
- [ ] Step 2: Project memory loaded via `memoryStore.getSkillMemory()` and existing docs reviewed
- [ ] Step 3: Relevant context files loaded via `contextProvider`
- [ ] Step 4: Documentation generated with inline comments, docstrings, API docs, and cross-references as applicable
- [ ] Step 5: Output saved to chosen destination AND project memory updated via `memoryStore.update()`

**FAILURE TO COMPLETE ALL STEPS INVALIDATES THE DOCUMENTATION**

## Further Reading

Refer to official documentation and standards:
- **Documentation Standards**:
  - Diátaxis Framework: https://diataxis.fr/
  - Write the Docs: https://www.writethedocs.org/guide/
- **Language-Specific Conventions**:
  - PEP 257 — Python Docstring Conventions: https://peps.python.org/pep-0257/
  - JSDoc: https://jsdoc.app/
  - XML Documentation Comments (C#): https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/xmldoc/
  - GoDoc: https://go.dev/blog/godoc
- **API Documentation**:
  - OpenAPI Specification: https://swagger.io/specification/
  - API Style Guide: https://apistylebook.com/

---

## Version History

- v1.0.0 (2026-02-12): Initial release
  - Mandatory 5-step workflow
  - Support for inline comments, docstrings, API docs, module docs, architecture docs, and guides
  - Multi-language convention support (Python, TypeScript, C#, Go, Java)
  - Interface-based context and memory access
