---
name: animate
version: "1.0.0"
description: "Zero-config animations for React, Vue, Solid, Svelte, Preact with @formkit/auto-animate (3.28kb). Prevents 15 errors."
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
## tags: [animation, auto-animate, formkit, react, vue, svelte, solid, preact, transitions, motion]

# skill:animate - Zero-Config UI Animations

## Version: 1.0.0

## Purpose

Add smooth, automatic animations to web applications using @formkit/auto-animate and complementary animation libraries. This skill handles list reordering, element insertion/removal, layout shifts, and page transitions across React, Vue, Solid, Svelte, and Preact with minimal configuration. Use when adding motion to UI components, animating list changes, or implementing page transitions.

## File Structure

```
skills/animate/
├── SKILL.md (this file)
└── examples.md
```

## Interface References

- **Context**: Loaded via [ContextProvider Interface](../../interfaces/context_provider.md)
- **Memory**: Accessed via [MemoryStore Interface](../../interfaces/memory_store.md)
- **Shared Patterns**: [Shared Loading Patterns](../../interfaces/shared_loading_patterns.md)
- **Schemas**: Validated against [context_metadata.schema.json](../../interfaces/schemas/context_metadata.schema.json) and [memory_entry.schema.json](../../interfaces/schemas/memory_entry.schema.json)

## Animation Focus Areas

1. **Auto-Animate Integration**: @formkit/auto-animate setup per framework — one line to animate any parent element
2. **List Animations**: Smooth add, remove, and reorder for dynamic lists (todo apps, kanban boards, data tables)
3. **Layout Transitions**: Animate height/width changes, accordion expand/collapse, tab switching
4. **Page Transitions**: Route-level transitions for SPAs (View Transitions API, framework-specific)
5. **Micro-Interactions**: Hover effects, button feedback, loading state transitions
6. **Performance**: GPU-accelerated transforms, `will-change` hints, reduced motion preferences
7. **Accessibility**: `prefers-reduced-motion` media query respect, no seizure-inducing flashes

## Common Errors Prevented

1. Missing `key` props on animated list items
2. Animating `height: auto` directly (use max-height or grid technique)
3. Triggering layout thrashing with width/height animations (use `transform` instead)
4. Forgetting `prefers-reduced-motion` media query
5. Using `display: none` transitions (not animatable — use opacity + visibility)
6. Auto-animate on wrong parent element (must be direct parent of animated children)
7. Conflicting CSS transitions with auto-animate
8. Memory leaks from unregistered animation observers
9. Animating during SSR hydration mismatch
10. Z-index stacking issues during animations
11. Missing `position: relative` on animated containers
12. Overriding auto-animate's inline styles accidentally
13. Using `setTimeout` instead of `onAnimationEnd` for sequencing
14. Animating non-composited properties causing jank (margin, padding, top/left)
15. Not disabling animations during automated testing

---

## MANDATORY WORKFLOW (MUST FOLLOW EXACTLY)

### Step 1: Initial Analysis

**YOU MUST:**
1. Detect the frontend framework (React, Vue, Solid, Svelte, Preact, or vanilla JS)
2. Identify the animation scope:
   - List/collection animations
   - Layout transitions
   - Page/route transitions
   - Micro-interactions
3. Check existing animation libraries in the project (Framer Motion, GSAP, CSS transitions)
4. Determine if @formkit/auto-animate is appropriate vs. a more specific library
5. Ask clarifying questions if needed:
   - What elements need animation?
   - Performance constraints (mobile, low-end devices)?
   - Existing design system motion guidelines?

### Step 2: Load Memory

> Follow [Standard Memory Loading](../../interfaces/shared_loading_patterns.md#pattern-1-standard-memory-loading) with `skill="animate"` and `domain="engineering"`.

**YOU MUST:**
1. Use `memoryStore.getSkillMemory("animate", "{project-name}")` to load project-specific animation patterns
2. Use `memoryStore.getByProject("{project-name}")` for cross-skill context (design tokens, component library)
3. Review previously established animation conventions and duration standards

### Step 3: Load Context

> Follow [Standard Context Loading](../../interfaces/shared_loading_patterns.md#pattern-2-standard-context-loading) for the `engineering` domain. Stay within the file budget declared in frontmatter.

### Step 4: Implement Animations

**YOU MUST:**

**Framework Detection & Setup:**
- **React**: `useAutoAnimate` hook from `@formkit/auto-animate/react`
- **Vue**: `v-auto-animate` directive from `@formkit/auto-animate/vue`
- **Solid**: `createAutoAnimate` from `@formkit/auto-animate/solid`
- **Svelte**: Action-based integration
- **Preact**: `useAutoAnimate` from `@formkit/auto-animate/preact`

**Implementation Rules:**
1. Apply auto-animate to the **direct parent** of elements that will be added/removed/reordered
2. Ensure all list items have stable, unique `key` props
3. Use `transform` and `opacity` for custom animations (GPU-composited properties)
4. Always include `prefers-reduced-motion` handling:
   ```css
   @media (prefers-reduced-motion: reduce) {
     *, *::before, *::after {
       animation-duration: 0.01ms !important;
       transition-duration: 0.01ms !important;
     }
   }
   ```
5. Set consistent animation durations following design system (default: 200-300ms for UI, 400-600ms for page)
6. Never animate `height`, `width`, `top`, `left` directly — use transforms or the grid technique

**DO NOT introduce animations without reduced-motion handling**

### Step 5: Generate Output

- Save implementation to `/claudedocs/animate_{project}_{YYYY-MM-DD}.md`
- Follow naming conventions in `../OUTPUT_CONVENTIONS.md`
- Include installation commands, code changes, and testing instructions

### Step 6: Update Memory

> Follow [Standard Memory Update](../../interfaces/shared_loading_patterns.md#pattern-3-standard-memory-update) for `skill="animate"`.

Store animation conventions, duration scales, library choices, and component-specific patterns.

---

## Compliance Checklist

Before completing, verify:

- [ ] Step 1: Framework detected and animation scope identified
- [ ] Step 2: Standard Memory Loading pattern followed
- [ ] Step 3: Standard Context Loading pattern followed
- [ ] Step 4: Animations implemented with reduced-motion support
- [ ] Step 5: Output saved with standard naming convention
- [ ] Step 6: Standard Memory Update pattern followed

## Further Reading

- **@formkit/auto-animate**: https://auto-animate.formkit.com/
- **View Transitions API**: https://developer.mozilla.org/en-US/docs/Web/API/View_Transitions_API
- **prefers-reduced-motion**: https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-motion
- **Web Animations API**: https://developer.mozilla.org/en-US/docs/Web/API/Web_Animations_API

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-02-12 | Initial release with interface-based architecture |
