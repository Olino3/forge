---
name: accessibility
version: "1.0.0"
description: "Build WCAG 2.1 AA compliant websites with semantic HTML, proper ARIA, focus management, and screen reader support. Includes color contrast (4.5:1 text), keyboard navigation, form labels, and live regions."
context:
  primary_domain: "engineering"
  always_load_files: []
  detection_required: false
  file_budget: 4
memory:
  scopes:
    - type: "skill-specific"
      files: [project_overview.md, common_patterns.md]
    - type: "shared-project"
      usage: "reference"
tags: [accessibility, wcag, aria, a11y, semantic-html, screen-reader, keyboard-navigation, focus-management]
---

# skill:accessibility - WCAG 2.1 AA Compliance

## Version: 1.0.0

## Purpose

Build accessible websites that meet WCAG 2.1 AA standards. This skill audits existing code and generates accessible patterns for semantic HTML, ARIA attributes, focus management, keyboard navigation, color contrast, form labeling, and live regions. Use when building new UI components, auditing existing pages for compliance, or fixing accessibility issues reported by automated tools or manual testing.

## File Structure

```
skills/accessibility/
├── SKILL.md (this file)
└── examples.md
```

## Interface References

- **Context**: Loaded via [ContextProvider Interface](../../interfaces/context_provider.md)
- **Memory**: Accessed via [MemoryStore Interface](../../interfaces/memory_store.md)
- **Shared Patterns**: [Shared Loading Patterns](../../interfaces/shared_loading_patterns.md)
- **Schemas**: Validated against [context_metadata.schema.json](../../interfaces/schemas/context_metadata.schema.json) and [memory_entry.schema.json](../../interfaces/schemas/memory_entry.schema.json)

## Accessibility Focus Areas

This skill evaluates 8 critical dimensions of web accessibility:

1. **Semantic HTML**: Correct element usage (`<nav>`, `<main>`, `<article>`, `<aside>`, `<header>`, `<footer>`, `<section>`), heading hierarchy, landmark regions
2. **ARIA Attributes**: Roles, states, and properties applied correctly — never overriding native semantics
3. **Keyboard Navigation**: All interactive elements reachable via Tab, operable via Enter/Space, escape closes modals, arrow keys for composite widgets
4. **Focus Management**: Visible focus indicators, focus trapping in modals, focus restoration on close, skip links
5. **Color Contrast**: Minimum 4.5:1 for normal text, 3:1 for large text (18px+ bold or 24px+), 3:1 for UI components and graphical objects
6. **Form Accessibility**: Visible labels associated via `for`/`id` or wrapping `<label>`, error messages linked via `aria-describedby`, required fields indicated
7. **Dynamic Content**: Live regions (`aria-live`), status messages, loading states announced to screen readers
8. **Media Accessibility**: Alt text for images, captions for video, transcripts for audio, no autoplay with sound

**Note**: Focus on issues that affect real users with disabilities. Automated tools catch ~30% of issues — this skill provides the manual judgment layer.

---

## MANDATORY WORKFLOW (MUST FOLLOW EXACTLY)

### Step 1: Initial Analysis

**YOU MUST:**
1. Determine the scope of the accessibility review or implementation:
   - Single component, page, or full application
   - New build vs. audit of existing code
   - Specific WCAG criteria to target (default: all AA criteria)
2. Identify the technology stack (React, Vue, plain HTML, etc.)
3. Detect any existing accessibility tooling (eslint-plugin-jsx-a11y, axe-core, pa11y, Lighthouse)
4. Ask clarifying questions:
   - What assistive technologies must be supported? (Screen readers: NVDA, JAWS, VoiceOver)
   - Are there specific WCAG criteria the team has been cited for?
   - What is the target compliance level? (A, AA, or AAA)

**DO NOT PROCEED WITHOUT A CLEAR SCOPE**

### Step 2: Load Memory

> Follow [Standard Memory Loading](../../interfaces/shared_loading_patterns.md#pattern-1-standard-memory-loading) with `skill="accessibility"` and `domain="engineering"`.

**YOU MUST:**
1. Use `memoryStore.getSkillMemory("accessibility", "{project-name}")` to load project-specific patterns
2. Use `memoryStore.getByProject("{project-name}")` for cross-skill insights (component patterns, design tokens)
3. If memory exists: Review previously documented component patterns, known exceptions, and remediation history
4. If no memory exists: Note this is the first accessibility pass

### Step 3: Load Context

> Follow [Standard Context Loading](../../interfaces/shared_loading_patterns.md#pattern-2-standard-context-loading) for the `engineering` domain. Stay within the file budget declared in frontmatter.

**YOU MUST:**
1. Use `contextProvider.getDomainIndex("engineering")` for general engineering context
2. Load framework-specific accessibility patterns if detected (React, Angular, Vue)
3. Reference WCAG 2.1 criteria directly when citing issues

### Step 4: Audit or Implement Accessible Patterns

**YOU MUST evaluate ALL categories below:**

**Semantic Structure**:
- Heading hierarchy is logical and sequential (no skipped levels)
- Landmark regions present: `<main>`, `<nav>`, `<header>`, `<footer>`
- Lists use `<ul>`/`<ol>`/`<dl>` — not styled `<div>` sequences
- Tables use `<th>`, `scope`, and `<caption>` for data tables
- No `<div>` or `<span>` used where a semantic element exists

**ARIA Correctness**:
- No ARIA role duplicates native HTML semantics (`<button role="button">` is redundant)
- Required ARIA attributes present for custom widgets (e.g., `aria-expanded` for accordions)
- `aria-label` or `aria-labelledby` on elements without visible text
- `aria-hidden="true"` not applied to focusable elements

**Keyboard & Focus**:
- All interactive elements in tab order (no positive `tabindex` values)
- Custom components handle Enter, Space, Escape, Arrow keys appropriately
- Focus indicator visible and meets 3:1 contrast ratio
- Modal dialogs trap focus and restore on close
- Skip-to-content link present as first focusable element

**Color & Contrast**:
- Text contrast meets 4.5:1 (normal) or 3:1 (large text)
- Information not conveyed by color alone (use icons, patterns, or text)
- Focus indicators meet 3:1 contrast against adjacent colors
- Disabled states still visually distinguishable

**Forms**:
- Every input has an associated `<label>` (visible, not `aria-label` only unless justified)
- Error messages use `aria-describedby` to link to input
- Required fields use `aria-required="true"` and visual indicator
- Form validation errors announced via `aria-live="assertive"` or focus management

**Dynamic Content**:
- Loading states use `aria-live="polite"` or `role="status"`
- Error alerts use `aria-live="assertive"` or `role="alert"`
- Route changes in SPAs manage focus (move to main content or `<h1>`)
- Toast notifications use `role="status"` with `aria-live="polite"`

**DO NOT SKIP ANY CATEGORY**

### Step 5: Generate Output

**YOU MUST ask the user for preferred output format:**
- **Option A**: Structured audit report with findings, WCAG criteria references, and remediation code
- **Option B**: Inline code patches with accessible implementations
- **Option C (Default)**: Both audit report and code patches

**For EVERY finding, YOU MUST provide:**
1. **Severity**: Critical / Important / Minor
2. **WCAG Criterion**: Specific criterion (e.g., 1.4.3 Contrast, 2.1.1 Keyboard, 4.1.2 Name Role Value)
3. **Description**: What is wrong and who it affects
4. **Fix**: Concrete code with the accessible implementation
5. **Testing**: How to verify the fix (screen reader, keyboard, automated tool)
6. **File:line**: Exact location

**Output to** `/claudedocs/accessibility_{project}_{YYYY-MM-DD}.md`

### Step 6: Update Memory

> Follow [Standard Memory Update](../../interfaces/shared_loading_patterns.md#pattern-3-standard-memory-update) for `skill="accessibility"`.

Use `memoryStore.update("accessibility", "{project-name}", ...)` to store:
1. **project_overview.md**: Framework, component library, a11y tooling, compliance target
2. **common_patterns.md**: Project-specific accessible component patterns discovered
3. **known_issues.md**: Documented exceptions, accepted limitations, and remediation timeline
4. **audit_history.md**: Summary of audits performed with dates and key findings

---

## Compliance Checklist

Before completing, verify:

- [ ] Step 1: Scope, stack, and compliance target identified
- [ ] Step 2: Standard Memory Loading pattern followed
- [ ] Step 3: Standard Context Loading pattern followed
- [ ] Step 4: All accessibility categories audited/implemented
- [ ] Step 5: Output saved with standard naming convention, all findings include WCAG criterion
- [ ] Step 6: Standard Memory Update pattern followed

**FAILURE TO COMPLETE ALL STEPS INVALIDATES THE REVIEW**

## Further Reading

- **WCAG 2.1**: https://www.w3.org/TR/WCAG21/
- **WAI-ARIA 1.2**: https://www.w3.org/TR/wai-aria-1.2/
- **ARIA Authoring Practices**: https://www.w3.org/WAI/ARIA/apg/
- **axe-core Rules**: https://dequeuniversity.com/rules/axe/
- **WebAIM Contrast Checker**: https://webaim.org/resources/contrastchecker/

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-02-12 | Initial release with interface-based architecture |
