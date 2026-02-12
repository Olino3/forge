# office Memory

Project-specific memory for Office document generation, including reusable document templates and library API patterns.

## Purpose

This memory helps the `skill:office` remember:
- Document structures and layouts that have been generated for each project
- Library-specific API patterns, workarounds, and configuration snippets
- Styling conventions: fonts, colors, margins, and branding per project
- Data binding patterns that map project data to document elements
- Runtime-specific considerations (Node.js vs. Cloudflare Workers vs. browser)

## Memory Files Per Project

Each project gets its own directory: `{project-name}/`

### `document_templates.md`

**Purpose**: Store reusable document structures and layouts so future documents maintain consistency and avoid rebuilding from scratch.

**Should contain**:
- **Document structures**: Section layouts, page configurations, slide orders
- **Table templates**: Column definitions, header styles, row formatting patterns
- **Header/footer configurations**: Logo placement, page number format, branding elements
- **Page layouts**: Margins, orientation, page sizes used for each document type
- **Reusable components**: Cover pages, signature blocks, disclaimer sections, table of contents patterns
- **Data schemas**: TypeScript interfaces used for document data binding

**Example entry**:
```markdown
## Quarterly Report — DOCX Template

- **Library**: docx
- **Page setup**: A4, portrait, 1-inch margins
- **Sections**: Cover page → Executive Summary → KPI Table → Charts → Appendix
- **Header**: Company logo (left), report title (right)
- **Footer**: Page X of Y (centered), confidentiality notice (left)
- **KPI table**: 5 columns, header row with #2B579A background, alternating row shading #F2F2F2
- **Data interface**: `QuarterlyReportData { title, author, date, kpis: KpiRow[], chartImagePath }`
```

**When to update**:
- First generation: Create with the document structure and layout decisions made
- Subsequent documents: Add new templates or refine existing ones based on feedback
- Rebranding: Update colors, fonts, and logo references when project branding changes

---

### `library_patterns.md`

**Purpose**: Catalog proven API usage patterns, workarounds, and configuration snippets for each library to avoid re-discovering solutions.

**Should contain**:
- **API patterns**: Correct usage of library APIs that are non-obvious or poorly documented
- **Workarounds**: Known bugs or limitations and how to work around them
- **Configuration snippets**: Reusable setup code for common scenarios (e.g., font embedding, page numbering)
- **Performance tips**: Optimizations for large documents (streaming, chunked writes)
- **Runtime compatibility**: Patterns that differ between Node.js, Cloudflare Workers, and browser environments
- **Version-specific notes**: API changes between library versions that affect generated code

**Example patterns**:
```markdown
## docx: Table Cell Vertical Alignment

The `verticalAlign` property on `TableCell` must use `VerticalAlign.CENTER` enum,
not a string. Strings silently fail and default to top alignment.

## pdf-lib: Coordinate System

Origin is bottom-left. Y increases upward. To position text 100pt from the top
of an A4 page: y = 841.89 - 100 = 741.89

## xlsx: Styling Requires Fork

SheetJS community edition (`xlsx`) does not support cell styling.
Use `xlsx-js-style` (drop-in replacement) for background colors, font formatting,
and border styling. Import as `import XLSX from "xlsx-js-style"`.

## pptxgenjs: Image Sizing

Images specified in inches. To fill a 10×7.5 slide with an image:
`slide.addImage({ path: "bg.png", x: 0, y: 0, w: 10, h: 7.5 })`
```

**When to update**: After every generation — save new API discoveries, workarounds, and patterns that required investigation.

---

## Why This Skill Needs Memory

### Document Consistency Across Sessions

**Without memory**: Each document generation starts from scratch. The user must re-specify layouts, styles, fonts, and branding every time, risking visual inconsistency between documents.

**With memory**: Document templates are loaded automatically. Every report, invoice, or presentation matches the project's established style without repetitive input.

### Library Pattern Reuse

**Without memory**: Non-obvious API patterns and workarounds are re-discovered through trial and error every session. The same coordinate math mistakes, styling quirks, and configuration issues recur.

**With memory**: Proven patterns are reused immediately. Known pitfalls are avoided. Document generation is faster and more reliable.

### Cross-Document Consistency

**Without memory**: Generating a new invoice 3 months after the first one produces a different layout, font, or color scheme because the original decisions are lost.

**With memory**: The original template structure, branding, and data interfaces are preserved and reapplied, ensuring all project documents share a cohesive visual identity.

---

## Memory Growth Pattern

### First Generation (New Project)

1. User specifies document type, content, and styling requirements
2. Generate the document following the full workflow
3. Create both memory files:
   - `document_templates.md` — save the document structure, layout, and data interface
   - `library_patterns.md` — record any API patterns, workarounds, or configuration discoveries

### Subsequent Generations

1. Load both memory files before generating the document
2. Apply saved templates and patterns — only ask the user for new or changed requirements
3. Reuse proven library patterns from `library_patterns.md`
4. Check `document_templates.md` for similar past documents to use as a starting point
5. After generation, update both files with new learnings

### Ongoing Refinement

- `document_templates.md` grows as new document types are generated; existing templates are refined based on user feedback
- `library_patterns.md` accumulates API knowledge over time; entries are updated when library versions change

---

## Related Documentation

- **Skill Documentation**: `../../skills/office/SKILL.md` for the full generation workflow
- **Skill Examples**: `../../skills/office/examples.md` for practical scenarios
- **Main Memory Index**: `../index.md` for memory system overview
- **Memory Lifecycle**: `../lifecycle.md` for freshness, pruning, and archival rules
- **Memory Quality**: `../quality_guidance.md` for validation standards
