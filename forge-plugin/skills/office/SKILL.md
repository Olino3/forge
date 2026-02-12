---
name: "office"
description: "Generate Office documents (DOCX, XLSX, PDF, PPTX) with TypeScript. Pure JavaScript libraries that work everywhere: Claude Code CLI, Cloudflare Workers, browsers. Uses docx (Word), xlsx/SheetJS (Excel), pdf-lib (PDF), and pptxgenjs (PowerPoint)."
version: "1.0.0"
context:
  primary_domain: "engineering"
  always_load_files: []
  detection_required: false
  file_budget: 4
memory:
  scopes:
    - type: "skill-specific"
      files: [document_templates.md, library_patterns.md]
    - type: "shared-project"
      usage: "reference"
tags: [office, docx, xlsx, pdf, pptx, typescript, word, excel, powerpoint, document-generation]
---

# skill:office - Generate Office Documents with TypeScript

## Version: 1.0.0

## Purpose

Generate professional Office documents (DOCX, XLSX, PDF, PPTX) using pure JavaScript libraries in TypeScript. This skill produces TypeScript code that creates documents programmatically — suitable for Node.js, Cloudflare Workers, and browser environments. Use it when you need to generate reports, spreadsheets, invoices, presentations, or any structured document from code.

**Supported libraries**:

| Format | Library | Package |
|--------|---------|---------|
| Word (.docx) | docx | `docx` |
| Excel (.xlsx) | SheetJS | `xlsx` |
| PDF (.pdf) | pdf-lib | `pdf-lib` |
| PowerPoint (.pptx) | PptxGenJS | `pptxgenjs` |

## File Structure

```
skills/office/
├── SKILL.md (this file)
└── examples.md
```

## Interface References

- **Context**: Loaded via [ContextProvider Interface](../../interfaces/context_provider.md)
- **Memory**: Accessed via [MemoryStore Interface](../../interfaces/memory_store.md)
- **Shared Patterns**: [Shared Loading Patterns](../../interfaces/shared_loading_patterns.md)
- **Schemas**: Validated against [context_metadata.schema.json](../../interfaces/schemas/context_metadata.schema.json) and [memory_entry.schema.json](../../interfaces/schemas/memory_entry.schema.json)

## Mandatory Workflow

> **IMPORTANT**: Execute ALL steps in order. Do not skip any step.

### Step 1: Initial Analysis

- Determine the target document type: DOCX, XLSX, PDF, or PPTX
- Identify content structure: sections, tables, charts, images, headers/footers
- Identify styling requirements: fonts, colors, margins, page layout, branding
- Determine the runtime environment: Node.js, Cloudflare Workers, or browser
- Note any constraints: file size limits, accessibility requirements, template compatibility

### Step 2: Load Memory

> Follow [Standard Memory Loading](../../interfaces/shared_loading_patterns.md#pattern-1-standard-memory-loading) with `skill="office"` and `domain="engineering"`.

Load from memory:
- `document_templates.md` — previously generated document structures and reusable patterns
- `library_patterns.md` — proven API usage patterns, workarounds, and configuration snippets

### Step 3: Load Context

> Follow [Standard Context Loading](../../interfaces/shared_loading_patterns.md#pattern-2-standard-context-loading) for the `engineering` domain. Stay within the file budget declared in frontmatter.

### Step 4: Select Library and Configure

- Choose the appropriate library based on document type:
  - **DOCX** → `docx` — paragraph-based document model with styles, numbering, tables, images, headers/footers
  - **XLSX** → `xlsx` (SheetJS) — workbook/sheet model with cell references, formulas, styling, charts
  - **PDF** → `pdf-lib` — low-level page drawing with precise coordinate-based layout, font embedding, form fields
  - **PPTX** → `pptxgenjs` — slide-based model with text boxes, shapes, charts, images, transitions
- Set up TypeScript types and imports
- Configure document-level settings: page size, orientation, margins, metadata (author, title, subject)

### Step 5: Generate Document Code

- Produce TypeScript code that creates the document:
  - Define document structure (sections, pages, slides, sheets)
  - Add content: headings, paragraphs, tables, lists, images, charts
  - Apply styles: fonts, colors, borders, alignment, spacing
  - Handle images: embed from buffers, URLs, or base64
  - Configure page layout: margins, orientation, headers, footers, page numbers
- Ensure code is self-contained and runnable with a single `npx tsx` command or equivalent
- Add inline comments for complex API calls

### Step 6: Add Data Binding

- If the document uses dynamic data:
  - Implement template variables for text substitution
  - Add data iteration for tables and lists (e.g., invoice line items, report rows)
  - Add conditional sections (e.g., show/hide based on data presence)
  - Handle image placeholders (e.g., company logo from URL or file path)
- If the document is static, skip this step

### Step 7: Generate Output

- Save output to `/claudedocs/office_{project}_{YYYY-MM-DD}.md`
- Follow naming conventions in `../OUTPUT_CONVENTIONS.md`
- Output should include:
  - Complete TypeScript source code
  - Package dependencies (`npm install` command)
  - Build/run instructions
  - Sample output description

### Step 8: Update Memory

> Follow [Standard Memory Update](../../interfaces/shared_loading_patterns.md#pattern-3-standard-memory-update) for `skill="office"`. Store any newly learned patterns, library quirks, or reusable document templates.

Update:
- `document_templates.md` — save reusable document structures for this project
- `library_patterns.md` — record any new API patterns, workarounds, or configuration discoveries

## Compliance Checklist

Before completing, verify:

- [ ] All mandatory workflow steps executed in order
- [ ] Standard Memory Loading pattern followed (Step 2)
- [ ] Standard Context Loading pattern followed (Step 3)
- [ ] Correct library selected for the target document type (Step 4)
- [ ] Generated code is self-contained and runnable (Step 5)
- [ ] Output saved with standard naming convention (Step 7)
- [ ] Standard Memory Update pattern followed (Step 8)

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-07-21 | Initial release — DOCX, XLSX, PDF, PPTX generation with TypeScript |
