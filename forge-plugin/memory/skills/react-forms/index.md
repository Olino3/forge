# react-forms Memory

Project-specific memory for form patterns, validation schemas, and UI integration.

## Purpose

This memory helps `skill:react-forms` remember:
- Form library and validation library versions
- Schema conventions and naming patterns
- UI component integration (shadcn/ui, MUI, Radix, native)
- Error display and feedback patterns
- Server-side validation approach

## Memory Files Per Project

Each project gets its own directory: `{project-name}/`

### Required Files

#### `project_overview.md`
- React Hook Form version
- Zod version (v3 vs. v4)
- UI component library for form elements
- Form submission target (Server Actions, API routes, client-side)
- Validation mode preference (onSubmit, onBlur, onChange)

#### `common_patterns.md`
- Schema organization and file structure
- Reusable field component patterns
- Error message display conventions
- Multi-step form patterns
- Dynamic field array patterns
- Server error mapping approach

## Related Documentation

- **Skill**: `../../skills/react-forms/SKILL.md`
- **Memory System**: `../index.md`
