---
name: tailwind-patterns
version: "1.0.0"
description: "Production-ready Tailwind CSS patterns for common website components: responsive layouts, cards, navigation, forms, buttons, and typography. Includes spacing scale, breakpoints, mobile-first patterns."
context:
  primary_domain: "engineering"
  always_load_files: []
  detection_required: true
  file_budget: 4
memory:
  scopes:
    - type: "skill-specific"
      files: [project_overview.md, common_patterns.md]
    - type: "shared-project"
      usage: "reference"
## tags: [tailwind, css, utility-classes, responsive, mobile-first, shadcn, components, layout, typography]

# skill:tailwind-patterns - Production Tailwind CSS Patterns

## Version: 1.0.0

## Purpose

Provide production-ready Tailwind CSS patterns for common website components. This skill covers responsive layouts, cards, navigation, forms, buttons, typography, spacing, and dark mode with mobile-first approach. It integrates with shadcn/ui, Radix, and Headless UI component libraries. Use when building UI components with Tailwind, setting up a design system, or converting designs to responsive Tailwind markup.

## File Structure

```
skills/tailwind-patterns/
├── SKILL.md (this file)
└── examples.md
```

## Interface References

- **Context**: Loaded via [ContextProvider Interface](../../interfaces/context_provider.md)
- **Memory**: Accessed via [MemoryStore Interface](../../interfaces/memory_store.md)
- **Shared Patterns**: [Shared Loading Patterns](../../interfaces/shared_loading_patterns.md)
- **Schemas**: Validated against [context_metadata.schema.json](../../interfaces/schemas/context_metadata.schema.json) and [memory_entry.schema.json](../../interfaces/schemas/memory_entry.schema.json)

## Tailwind Pattern Focus Areas

1. **Responsive Layouts**: Flexbox and Grid patterns with mobile-first breakpoints (`sm:`, `md:`, `lg:`, `xl:`, `2xl:`)
2. **Component Patterns**: Cards, navigation bars, sidebars, modals, dropdowns, tables, and forms
3. **Typography System**: Font scale, line heights, letter spacing, prose for content
4. **Spacing & Sizing**: Consistent use of the spacing scale (`p-4`, `m-6`, `gap-8`), avoiding arbitrary values
5. **Color System**: Design tokens via CSS custom properties, semantic colors (`primary`, `muted`, `destructive`)
6. **Dark Mode**: `dark:` variant with class-based toggling, smooth transitions
7. **State Variants**: Hover, focus, active, disabled, group-hover, peer states
8. **shadcn/ui Integration**: Component composition, variant props via `cva`, `cn()` utility

## Tailwind Core Rules

1. **Mobile-first**: Write base styles for mobile, then add breakpoint prefixes for larger screens
2. **Spacing scale**: Use Tailwind's spacing scale — avoid arbitrary values (`p-[13px]`) unless necessary
3. **Semantic classes**: Use `text-foreground`, `bg-background`, `border-border` from design tokens
4. **No `@apply` abuse**: Prefer utility classes in markup; use `@apply` only for base styles or third-party overrides
5. **Component extraction**: Extract repeated patterns into React components, not `@apply` classes
6. **Container queries**: Use `@container` for component-level responsive design
7. **Logical properties**: Prefer `ps-4`/`pe-4` over `pl-4`/`pr-4` for RTL support

---

## MANDATORY WORKFLOW (MUST FOLLOW EXACTLY)

### Step 1: Initial Analysis

**YOU MUST:**
1. Identify the Tailwind version (v3.x or v4.x) and configuration
2. Detect the component library (shadcn/ui, Radix, Headless UI, DaisyUI, or custom)
3. Determine the scope:
   - Single component implementation
   - Page layout
   - Design system setup
   - Responsive refactoring
4. Check for existing `tailwind.config.ts` customizations (colors, fonts, breakpoints)
5. Identify if dark mode is required and the strategy (class-based, media query, or system)
6. Ask clarifying questions:
   - Design reference or mockup available?
   - Breakpoint requirements?
   - RTL support needed?

### Step 2: Load Memory

> Follow [Standard Memory Loading](../../interfaces/shared_loading_patterns.md#pattern-1-standard-memory-loading) with `skill="tailwind-patterns"` and `domain="engineering"`.

**YOU MUST:**
1. Use `memoryStore.getSkillMemory("tailwind-patterns", "{project-name}")` to load project patterns
2. Use `memoryStore.getByProject("{project-name}")` for cross-skill context (design tokens, color palette)
3. Review previously documented component patterns, custom utilities, and design decisions

### Step 3: Load Context

> Follow [Standard Context Loading](../../interfaces/shared_loading_patterns.md#pattern-2-standard-context-loading) for the `engineering` domain. Stay within the file budget declared in frontmatter.

### Step 4: Implement Tailwind Patterns

**YOU MUST follow these patterns:**

**Responsive Layout (Mobile-First):**
```tsx
<div className="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-3">
  {items.map(item => (
    <Card key={item.id} className="p-6" />
  ))}
</div>
```

**Card Component with Variants (cva + cn):**
```tsx
import { cva, type VariantProps } from "class-variance-authority"
import { cn } from "@/lib/utils"

const cardVariants = cva(
  "rounded-lg border bg-card text-card-foreground shadow-sm",
  {
    variants: {
      size: {
        sm: "p-4",
        md: "p-6",
        lg: "p-8",
      },
    },
    defaultVariants: { size: "md" },
  }
)

interface CardProps extends React.HTMLAttributes<HTMLDivElement>,
  VariantProps<typeof cardVariants> {}

export function Card({ className, size, ...props }: CardProps) {
  return <div className={cn(cardVariants({ size }), className)} {...props} />
}
```

**Button with States:**
```tsx
<button className="
  inline-flex items-center justify-center rounded-md
  bg-primary px-4 py-2 text-sm font-medium text-primary-foreground
  hover:bg-primary/90
  focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2
  disabled:pointer-events-none disabled:opacity-50
  transition-colors
">
  Submit
</button>
```

**Dark Mode:**
```tsx
<div className="bg-white text-gray-900 dark:bg-gray-950 dark:text-gray-50">
  <p className="text-gray-600 dark:text-gray-400">Subtitle text</p>
</div>
```

**Form Input:**
```tsx
<div className="space-y-2">
  <label htmlFor="email" className="text-sm font-medium leading-none">
    Email
  </label>
  <input
    id="email"
    type="email"
    className="
      flex h-10 w-full rounded-md border border-input bg-background
      px-3 py-2 text-sm
      placeholder:text-muted-foreground
      focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2
      disabled:cursor-not-allowed disabled:opacity-50
    "
    placeholder="you@example.com"
  />
</div>
```

**Rules:**
- Mobile-first: Base classes for mobile, add `md:`, `lg:` for larger screens
- Use design token colors (`primary`, `muted`, `destructive`) not raw colors in components
- Use `focus-visible:` not `focus:` for keyboard-only focus indicators
- Use `transition-colors` or `transition-all` for smooth state changes
- Group related utility classes logically (layout → spacing → typography → colors → states)

**DO NOT use arbitrary values when a Tailwind scale value exists**

### Step 5: Generate Output

- Save to `/claudedocs/tailwind-patterns_{project}_{YYYY-MM-DD}.md`
- Follow naming conventions in `../OUTPUT_CONVENTIONS.md`
- Include component code, Tailwind config changes, and utility setup

### Step 6: Update Memory

> Follow [Standard Memory Update](../../interfaces/shared_loading_patterns.md#pattern-3-standard-memory-update) for `skill="tailwind-patterns"`.

Store design tokens, component patterns, custom utilities, breakpoint decisions, and dark mode strategy.

---

## Compliance Checklist

Before completing, verify:

- [ ] Step 1: Tailwind version, component library, and scope identified
- [ ] Step 2: Standard Memory Loading pattern followed
- [ ] Step 3: Standard Context Loading pattern followed
- [ ] Step 4: Tailwind patterns implemented with mobile-first, design tokens, and proper state variants
- [ ] Step 5: Output saved with standard naming convention
- [ ] Step 6: Standard Memory Update pattern followed

## Further Reading

- **Tailwind CSS Docs**: https://tailwindcss.com/docs
- **shadcn/ui**: https://ui.shadcn.com/
- **Class Variance Authority**: https://cva.style/docs
- **Tailwind v4**: https://tailwindcss.com/blog/tailwindcss-v4

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-02-12 | Initial release with interface-based architecture |
