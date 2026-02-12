# accessibility Memory

Project-specific memory for accessibility audits and accessible component implementations.

## Purpose

This memory helps `skill:accessibility` remember:
- Project-specific component accessibility patterns
- Known accessibility exceptions and accepted limitations
- WCAG compliance target and current audit status
- Assistive technology requirements and testing results
- Remediation history and recurring issues

## Memory Files Per Project

Each project gets its own directory: `{project-name}/`

### Required Files

#### `project_overview.md`
- Framework and UI component library
- Target compliance level (A, AA, AAA)
- Assistive technologies to support
- Accessibility tooling (axe-core, eslint-plugin-jsx-a11y, pa11y)
- Design system accessibility guidelines

#### `common_patterns.md`
- Project-specific accessible component patterns
- ARIA attribute conventions
- Focus management patterns
- Color contrast requirements and design tokens
- Keyboard navigation patterns for custom widgets

### Optional Files

#### `known_issues.md`
- Documented accessibility exceptions
- Third-party component limitations
- Remediation timeline for known issues

#### `audit_history.md`
- Summary of audits performed with dates and WCAG criteria tested
- Key findings and resolution status
- Compliance trends over time

## Related Documentation

- **Skill**: `../../skills/accessibility/SKILL.md`
- **Memory System**: `../index.md`
