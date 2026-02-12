# tailwind-patterns Memory

Project-specific memory for Tailwind CSS patterns, design tokens, and component conventions.

## Purpose

This memory helps `skill:tailwind-patterns` remember:
- Tailwind version and configuration customizations
- Design token definitions (colors, spacing, typography)
- Component library integration (shadcn/ui, DaisyUI, custom)
- Dark mode strategy and implementation
- Custom utility classes and plugins

## Memory Files Per Project

Each project gets its own directory: `{project-name}/`

### Required Files

#### `project_overview.md`
- Tailwind CSS version (v3.x or v4.x)
- Component library (shadcn/ui, Radix, Headless UI, DaisyUI)
- Dark mode strategy (class-based, media query, system preference)
- Custom theme extensions (colors, fonts, breakpoints, spacing)
- CSS variable / design token structure

#### `common_patterns.md`
- Layout patterns (grid configurations, flex patterns)
- Component variant definitions (cva configurations)
- Responsive breakpoint conventions
- State variant patterns (hover, focus, disabled)
- Animation and transition conventions
- Custom utility classes

## Related Documentation

- **Skill**: `../../skills/tailwind-patterns/SKILL.md`
- **Memory System**: `../index.md`
