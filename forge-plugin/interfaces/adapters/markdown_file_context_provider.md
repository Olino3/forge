# MarkdownFileContextProvider Adapter

Version: 0.3.0-alpha
Status: Specification
Last Updated: 2026-02-10

---

## Overview

The `MarkdownFileContextProvider` is the filesystem-backed adapter that implements the [`ContextProvider`](../context_provider.md) interface. It maps every interface method to concrete file read operations against the `forge-plugin/context/` directory tree.

---

## Path Resolution

All paths are resolved relative to `forge-plugin/context/`.

| Interface Concept | Filesystem Path |
|---|---|
| Domain root | `forge-plugin/context/{domain}/` |
| Domain index | `forge-plugin/context/{domain}/index.md` |
| Context file | `forge-plugin/context/{domain}/{filename}.md` |
| Loading protocol | `forge-plugin/context/loading_protocol.md` |
| Cross-domain matrix | `forge-plugin/context/cross_domain.md` |
| Main index | `forge-plugin/context/index.md` |

---

## Method-to-File Mapping

### getCatalog(domain?)

**File operations**:
1. If `domain` is provided: list files in `context/{domain}/`.
2. If `domain` is omitted: list files in all 9 domain directories.
3. For each file, read YAML frontmatter (between `---` delimiters) to extract metadata.
4. Return structured catalog without loading file body content.

**Filesystem call**: `ls context/{domain}/*.md` + read first N lines of each file for frontmatter.

### getDomainIndex(domain)

**File operations**:
1. Read `context/{domain}/index.md` in full.
2. Parse structured content: file descriptions, loading workflows, detection hints.
3. If frontmatter is present, merge frontmatter metadata into the result.

**Filesystem call**: `Read context/{domain}/index.md`

### getLoadingProtocol()

**File operations**:
1. Read `context/loading_protocol.md` in full.
2. Parse the 5-step protocol into structured data.

**Filesystem call**: `Read context/loading_protocol.md`

### getAlwaysLoadFiles(domain)

**File operations**:
1. Read `context/{domain}/index.md` to identify "always-load" files (or use frontmatter `loadingStrategy: "always"` from catalog).
2. Read full content of each always-load file.
3. Strip YAML frontmatter from returned content.

**Filesystem calls**:
- `Read context/{domain}/index.md` (to identify files)
- `Read context/{domain}/{file}.md` for each always-load file

**Per-domain always-load files**:

| Domain | Always-Load Files |
|---|---|
| python | `context_detection.md`, `common_issues.md` |
| dotnet | `context_detection.md`, `common_issues.md` |
| angular | `context_detection.md`, `common_issues.md` |
| schema | `common_patterns.md` |
| engineering | (none -- all reference/onDemand) |
| git | (none -- all reference/onDemand) |
| azure | (none -- all reference/onDemand) |
| commands | (none -- all reference/onDemand) |
| security | (none -- all reference/onDemand) |

### detectProjectType(domain, signals)

**File operations**:
1. Read `context/{domain}/context_detection.md`.
2. Match provided signals against detection patterns in the file.

**Filesystem call**: `Read context/{domain}/context_detection.md`

**Domains with detection files**: `python`, `dotnet`, `angular`.

**Domains without detection files**: `engineering`, `git`, `azure`, `commands`, `schema`, `security`. For these domains, the method returns an empty `DetectionResult` and skills should use the domain index decision matrix directly.

### getConditionalContext(domain, detection)

**File operations**:
1. For each file ID in `detection.recommendedFiles`, read the full file from `context/{domain}/{filename}.md`.
2. Strip YAML frontmatter from returned content.
3. Enforce token budget (4-6 files total including always-load files).

**Filesystem calls**: `Read context/{domain}/{file}.md` for each recommended file.

### getCrossDomainContext(domain, triggers)

**File operations**:
1. Read `context/cross_domain.md`.
2. Match triggers against the cross-domain trigger matrix.
3. For each matched secondary file, read from `context/{secondary_domain}/{file}.md`.

**Filesystem calls**:
- `Read context/cross_domain.md`
- `Read context/{secondary_domain}/{file}.md` for each triggered file

### getReference(domain, file)

**File operations**:
1. Read only the YAML frontmatter from `context/{domain}/{file}.md` (lines between the opening and closing `---` delimiters).
2. Parse frontmatter into a `ContextReference` object.
3. Do NOT read the file body.

**Filesystem call**: `Read context/{domain}/{file}.md` (first ~30 lines only, to extract frontmatter).

### materialize(reference)

**File operations**:
1. Read `context/{reference.domain}/{filename}.md` in full.
2. Strip YAML frontmatter.
3. Return body content.

**Filesystem call**: `Read context/{domain}/{file}.md`

### materializeSections(reference, sections[])

**File operations**:
1. Read `context/{reference.domain}/{filename}.md` in full.
2. Strip YAML frontmatter.
3. Parse markdown headings to identify section boundaries.
4. Extract only the requested sections by matching heading text to section names from frontmatter.
5. Return partial content.

**Filesystem call**: `Read context/{domain}/{file}.md` (full read, then filter in-memory).

**Section boundary rules**:
- Sections start at a `## {Section Name}` heading.
- Sections end at the next heading of equal or higher level, or at end-of-file.
- Section names in frontmatter must match heading text exactly (case-insensitive).

### search(query, domain?)

**File operations**:
1. If `domain` is provided, scope to `context/{domain}/`. Otherwise, scan all domains.
2. For each file, read YAML frontmatter.
3. Match query against: `tags`, section `keywords`, `title`, `detectionTriggers`.
4. Score and rank matches.
5. Return `ContextReference` objects (no content loaded).

**Filesystem calls**: Read frontmatter of all files in scope (first ~30 lines each).

---

## Fallback: Files Without YAML Frontmatter

Not all context files have YAML frontmatter yet. For files without frontmatter, metadata is derived from the file footer and filename:

### Footer-Based Metadata Extraction

Many context files end with a footer block like:

```
**Version**: 0.3.0-alpha (Compacted)
**Last Updated**: 2025-11-14
**Maintained For**: python-code-review skill
```

Or in italic format:

```
*Last Updated: 2026-02-10*
```

### Derivation Rules

| Metadata Field | Derivation Source |
|---|---|
| `id` | `{domain}/{filename}` from filesystem path |
| `domain` | Parent directory name |
| `title` | First `#` heading in the file |
| `type` | `"index"` if filename is `index.md`; `"detection"` if filename is `context_detection.md`; otherwise `"reference"` |
| `estimatedTokens` | `word_count / 0.75` (approximate) |
| `loadingStrategy` | `"always"` if `type` is `"always"` or `"detection"` or `"index"`; otherwise `"onDemand"` |
| `version` | Extracted from `**Version**: X.Y.Z` footer line |
| `lastUpdated` | Extracted from `**Last Updated**: YYYY-MM-DD` or `*Last Updated: YYYY-MM-DD*` footer line |
| `maintainedFor` | Extracted from `**Maintained For**: {skill}` footer line |
| `tags` | Derived from domain name and filename |
| `sections` | Derived from `##` headings in the file |

### Precedence

If a file has both YAML frontmatter and a footer block, the YAML frontmatter takes precedence for all fields.

---

## Before/After: SKILL_TEMPLATE.md Steps 2-3

### Step 2: Load Memory (unchanged by this adapter)

Memory loading is handled by the `MemoryStore` interface, not `ContextProvider`.

### Step 3: Load Context

**BEFORE** (hardcoded paths in SKILL_TEMPLATE.md):

```markdown
### Step 3: Load Context
- Follow `context/loading_protocol.md` for the `{domain}` domain
- Read `context/{domain}/index.md`
- Load always-load files: `context/{domain}/common_issues.md`
- Run detection: `context/{domain}/context_detection.md`
- Load framework files based on detection
- Check `context/cross_domain.md` for secondary context
```

**AFTER** (interface-based):

```markdown
### Step 3: Load Context
- Call `ContextProvider.getDomainIndex("{domain}")` to understand available context
- Call `ContextProvider.getAlwaysLoadFiles("{domain}")` to load mandatory files
- Call `ContextProvider.detectProjectType("{domain}", signals)` with gathered code signals
- Call `ContextProvider.getConditionalContext("{domain}", detection)` to load framework-specific files
- Call `ContextProvider.getCrossDomainContext("{domain}", triggers)` for secondary context
- Total loaded files should stay within the 4-6 file budget
```

---

## Directory Listing: All 9 Domains

### angular/ (17 files)

```
context/angular/
  index.md
  context_detection.md
  common_issues.md
  component_patterns.md
  component_testing_patterns.md
  jest_testing_standards.md
  ngrx_patterns.md
  performance_patterns.md
  primeng_patterns.md
  rxjs_patterns.md
  security_patterns.md
  service_patterns.md
  service_testing_patterns.md
  tailwind_patterns.md
  test_antipatterns.md
  testing_utilities.md
  typescript_patterns.md
```

### azure/ (11 files)

```
context/azure/
  index.md
  azure_bicep_overview.md
  azure_functions_overview.md
  azure_pipelines_cicd_patterns.md
  azure_pipelines_overview.md
  azure_verified_modules.md
  azurite_setup.md
  docker_compose_reference.md
  dockerfile_reference.md
  local_development_setup.md
  tiltfile_reference.md
```

### commands/ (8 files)

```
context/commands/
  index.md
  analysis_patterns.md
  brainstorming_patterns.md
  build_patterns.md
  documentation_standards.md
  implementation_strategies.md
  refactoring_patterns.md
  testing_strategies.md
```

### dotnet/ (12 files)

```
context/dotnet/
  index.md
  context_detection.md
  common_issues.md
  aspnet_patterns.md
  async_patterns.md
  blazor_patterns.md
  csharp_patterns.md
  di_patterns.md
  ef_patterns.md
  linq_patterns.md
  performance_patterns.md
  security_patterns.md
```

### engineering/ (6 files)

```
context/engineering/
  index.md
  api_design_patterns.md
  architecture_patterns.md
  code_review_principles.md
  error_recovery.md
  testing_principles.md
```

### git/ (3 files)

```
context/git/
  index.md
  diff_patterns.md
  git_diff_reference.md
```

### python/ (14 files)

```
context/python/
  index.md
  context_detection.md
  common_issues.md
  datascience_patterns.md
  dependency_management.md
  django_patterns.md
  fastapi_patterns.md
  flask_patterns.md
  ml_patterns.md
  mocking_patterns.md
  test_antipatterns.md
  testing_frameworks.md
  unit_testing_standards.md
  virtual_environments.md
```

### schema/ (4 files)

```
context/schema/
  index.md
  common_patterns.md
  database_patterns.md
  file_formats.md
```

### security/ (3 files)

```
context/security/
  index.md
  owasp_python.md
  security_guidelines.md
```

### Top-Level Files (3 files)

```
context/
  index.md
  loading_protocol.md
  cross_domain.md
```

**Total**: 81 context files across 9 domains + 3 top-level files.

---

*Last Updated: 2026-02-10*
