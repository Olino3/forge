---
name: react-forms
version: "1.0.0"
description: "Build type-safe validated forms using React Hook Form v7 and Zod v4. Single schema works on client and server with full TypeScript inference via z.infer."
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
tags: [react, forms, react-hook-form, zod, validation, typescript, type-safe, schema-validation]
---

# skill:react-forms - Type-Safe Forms with React Hook Form + Zod

## Version: 1.0.0

## Purpose

Build type-safe, validated forms using React Hook Form v7 and Zod v4. A single Zod schema provides client-side validation, server-side validation, and full TypeScript inference via `z.infer`. This skill covers form setup, field registration, custom validation, error display, multi-step forms, dynamic fields, and Server Action integration. Use when building any form in React/Next.js that needs validation, type safety, or complex field interactions.

## File Structure

```
skills/react-forms/
├── SKILL.md (this file)
└── examples.md
```

## Interface References

- **Context**: Loaded via [ContextProvider Interface](../../interfaces/context_provider.md)
- **Memory**: Accessed via [MemoryStore Interface](../../interfaces/memory_store.md)
- **Shared Patterns**: [Shared Loading Patterns](../../interfaces/shared_loading_patterns.md)
- **Schemas**: Validated against [context_metadata.schema.json](../../interfaces/schemas/context_metadata.schema.json) and [memory_entry.schema.json](../../interfaces/schemas/memory_entry.schema.json)

## Form Development Focus Areas

1. **Schema Definition**: Zod v4 schemas with transforms, refinements, and custom error messages
2. **Hook Form Integration**: `useForm` with `zodResolver`, register patterns, controlled vs. uncontrolled
3. **Type Inference**: `z.infer<typeof schema>` for form data types — no manual type definitions
4. **Error Handling**: Field-level errors, form-level errors, server errors, async validation
5. **Complex Forms**: Multi-step wizards, dynamic field arrays, conditional fields, dependent validation
6. **Server Integration**: Zod schema reuse in Server Actions, API routes, and middleware
7. **Performance**: Uncontrolled components by default, selective re-renders via `watch`, form state isolation
8. **Accessibility**: Labels, error announcements, required indicators, focus management on errors

## Common Errors Prevented

1. Defining form types manually instead of using `z.infer<typeof schema>`
2. Using `onChange` mode when `onBlur` or `onSubmit` is sufficient (causes unnecessary re-renders)
3. Forgetting `zodResolver` in `useForm` config — validation silently skipped
4. Not handling async default values (use `reset()` after fetch, not `defaultValues`)
5. Using `register` with controlled components (MUI, Radix) — use `Controller` instead
6. Missing `name` prop mismatch between schema and register
7. Zod schema not matching form field names exactly (case-sensitive)
8. Not calling `handleSubmit` on the form's `onSubmit` — raw form data instead of validated
9. Forgetting to disable submit button during `isSubmitting` state
10. Using `watch()` at form level instead of `useWatch` for individual fields (performance)

---

## MANDATORY WORKFLOW (MUST FOLLOW EXACTLY)

### Step 1: Initial Analysis

**YOU MUST:**
1. Identify the form requirements:
   - Fields, types, and validation rules
   - Submission target (Server Action, API route, client-side)
   - UI library (native HTML, MUI, Radix, shadcn/ui)
2. Determine form complexity:
   - Simple (single page, flat fields)
   - Multi-step wizard
   - Dynamic field arrays
   - Dependent/conditional fields
3. Check existing form patterns in the project
4. Ask clarifying questions if needed

### Step 2: Load Memory

> Follow [Standard Memory Loading](../../interfaces/shared_loading_patterns.md#pattern-1-standard-memory-loading) with `skill="react-forms"` and `domain="engineering"`.

**YOU MUST:**
1. Use `memoryStore.getSkillMemory("react-forms", "{project-name}")` to load project patterns
2. Use `memoryStore.getByProject("{project-name}")` for cross-skill context (design system, component lib)
3. Review existing form conventions, validation patterns, and error display styles

### Step 3: Load Context

> Follow [Standard Context Loading](../../interfaces/shared_loading_patterns.md#pattern-2-standard-context-loading) for the `engineering` domain. Stay within the file budget declared in frontmatter.

### Step 4: Implement Forms

**YOU MUST follow this pattern:**

**1. Define Zod Schema (single source of truth):**
```typescript
import { z } from "zod"

export const userSchema = z.object({
  name: z.string().min(2, "Name must be at least 2 characters"),
  email: z.string().email("Invalid email address"),
  age: z.coerce.number().min(18, "Must be 18 or older"),
  role: z.enum(["admin", "user", "moderator"]),
})

// Type is inferred — never define manually
export type UserFormData = z.infer<typeof userSchema>
```

**2. Wire React Hook Form:**
```typescript
"use client"
import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import { userSchema, type UserFormData } from "./schema"

export function UserForm() {
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<UserFormData>({
    resolver: zodResolver(userSchema),
    defaultValues: { name: "", email: "", role: "user" },
  })

  async function onSubmit(data: UserFormData) {
    // data is fully typed and validated
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      {/* Fields with error display */}
    </form>
  )
}
```

**3. Reuse Schema on Server:**
```typescript
"use server"
import { userSchema } from "./schema"

export async function createUser(formData: FormData) {
  const result = userSchema.safeParse(Object.fromEntries(formData))
  if (!result.success) {
    return { errors: result.error.flatten().fieldErrors }
  }
  // result.data is typed as UserFormData
  await db.users.create({ data: result.data })
}
```

**Rules:**
- Always use `zodResolver` — never skip client-side validation
- Always validate on the server too — client validation is a UX convenience, not a security layer
- Use `z.coerce` for form fields that come as strings but need other types
- Prefer `onSubmit` validation mode for most forms
- Use `Controller` for third-party controlled components
- Use `useFieldArray` for dynamic field lists

**DO NOT define form types manually — always use `z.infer`**

### Step 5: Generate Output

- Save to `/claudedocs/react-forms_{project}_{YYYY-MM-DD}.md`
- Follow naming conventions in `../OUTPUT_CONVENTIONS.md`
- Include schema file, form component, and server validation code

### Step 6: Update Memory

> Follow [Standard Memory Update](../../interfaces/shared_loading_patterns.md#pattern-3-standard-memory-update) for `skill="react-forms"`.

Store form patterns, validation conventions, UI component integration patterns, and error display styles.

---

## Compliance Checklist

Before completing, verify:

- [ ] Step 1: Form requirements and complexity identified
- [ ] Step 2: Standard Memory Loading pattern followed
- [ ] Step 3: Standard Context Loading pattern followed
- [ ] Step 4: Schema-first approach with Zod + React Hook Form implemented
- [ ] Step 5: Output saved with standard naming convention
- [ ] Step 6: Standard Memory Update pattern followed

## Further Reading

- **React Hook Form**: https://react-hook-form.com/
- **Zod**: https://zod.dev/
- **@hookform/resolvers**: https://github.com/react-hook-form/resolvers
- **Zod v4**: https://v4.zod.dev/

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-02-12 | Initial release with interface-based architecture |
