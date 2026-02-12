# Animate Skill — Examples

Usage scenarios demonstrating how `skill:animate` adds smooth animations across frameworks.

---

## Example 1: Animated Todo List with React

### Problem

A todo list adds and removes items without visual feedback, making it hard to track changes.

### Implementation

```bash
npm install @formkit/auto-animate
```

```tsx
"use client"
import { useState } from "react"
import { useAutoAnimate } from "@formkit/auto-animate/react"

interface Todo {
  id: string
  text: string
  done: boolean
}

export function TodoList() {
  const [todos, setTodos] = useState<Todo[]>([])
  const [parent] = useAutoAnimate() // One line — animates add/remove/reorder

  function addTodo(text: string) {
    setTodos(prev => [...prev, { id: crypto.randomUUID(), text, done: false }])
  }

  function removeTodo(id: string) {
    setTodos(prev => prev.filter(t => t.id !== id))
  }

  function toggleTodo(id: string) {
    setTodos(prev =>
      prev.map(t => (t.id === id ? { ...t, done: !t.done } : t))
    )
  }

  return (
    <ul ref={parent} className="space-y-2">
      {todos.map(todo => (
        <li key={todo.id} className="flex items-center gap-3 rounded-lg border p-3">
          <input
            type="checkbox"
            checked={todo.done}
            onChange={() => toggleTodo(todo.id)}
          />
          <span className={todo.done ? "line-through opacity-50" : ""}>
            {todo.text}
          </span>
          <button onClick={() => removeTodo(todo.id)} className="ml-auto">
            Remove
          </button>
        </li>
      ))}
    </ul>
  )
}
```

**Key points:**
- `useAutoAnimate()` returns a ref — attach it to the direct parent of animated children
- Each child must have a unique `key` prop
- Animations happen automatically on add, remove, and reorder

---

## Example 2: Vue Accordion with Auto-Animate

### Problem

An FAQ accordion expands and collapses content abruptly with no visual transition.

### Implementation

```bash
npm install @formkit/auto-animate
```

```vue
<script setup lang="ts">
import { ref } from "vue"
import { vAutoAnimate } from "@formkit/auto-animate/vue"

const faqs = ref([
  { id: 1, question: "What is your return policy?", answer: "30-day returns...", open: false },
  { id: 2, question: "How long does shipping take?", answer: "3-5 business days...", open: false },
  { id: 3, question: "Do you offer support?", answer: "24/7 email support...", open: false },
])

function toggle(id: number) {
  const faq = faqs.value.find(f => f.id === id)
  if (faq) faq.open = !faq.open
}
</script>

<template>
  <div class="space-y-4">
    <div
      v-for="faq in faqs"
      :key="faq.id"
      v-auto-animate
      class="rounded-lg border"
    >
      <button
        class="flex w-full items-center justify-between p-4 text-left font-medium"
        :aria-expanded="faq.open"
        @click="toggle(faq.id)"
      >
        {{ faq.question }}
        <span :class="{ 'rotate-180': faq.open }" class="transition-transform">▼</span>
      </button>
      <div v-if="faq.open" class="px-4 pb-4 text-muted-foreground">
        {{ faq.answer }}
      </div>
    </div>
  </div>
</template>
```

**Key points:**
- `v-auto-animate` directive applied to the parent of conditionally rendered content
- Works with `v-if` / `v-show` toggling
- Chevron rotation uses standard CSS transition (separate from auto-animate)

---

## Example 3: Custom Animation Duration and Easing

### Problem

Default auto-animate timing doesn't match the project's motion design guidelines (400ms ease-out).

### Implementation

```tsx
"use client"
import { useAutoAnimate } from "@formkit/auto-animate/react"

export function NotificationList({ notifications }: { notifications: Notification[] }) {
  const [parent] = useAutoAnimate({
    duration: 400,
    easing: "ease-out",
    // Custom animation function for full control:
    // disableAnimations: false,
  })

  return (
    <div ref={parent} className="space-y-3">
      {notifications.map(n => (
        <div key={n.id} className="rounded-lg border p-4 shadow-sm">
          <p className="font-medium">{n.title}</p>
          <p className="text-sm text-muted-foreground">{n.message}</p>
        </div>
      ))}
    </div>
  )
}
```

**With reduced motion support:**

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

```tsx
// Programmatic check
const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches

const [parent] = useAutoAnimate(
  prefersReducedMotion ? { duration: 0 } : { duration: 400, easing: "ease-out" }
)
```

**Key points:**
- Pass options object to customize duration (ms) and easing
- Always respect `prefers-reduced-motion` — either via CSS or JavaScript
- For complex animations beyond auto-animate's scope, consider Framer Motion or GSAP

---

## Example 4: Disabling Animations for Testing

### Problem

E2E tests are flaky because animations cause timing issues with element visibility assertions.

### Implementation

```tsx
"use client"
import { useAutoAnimate } from "@formkit/auto-animate/react"

const DISABLE_ANIMATIONS = process.env.NEXT_PUBLIC_DISABLE_ANIMATIONS === "true"

export function AnimatedList({ items }: { items: Item[] }) {
  const [parent, enable] = useAutoAnimate()

  // Disable in test environments
  if (DISABLE_ANIMATIONS) {
    enable(false)
  }

  return (
    <ul ref={parent}>
      {items.map(item => (
        <li key={item.id}>{item.name}</li>
      ))}
    </ul>
  )
}
```

```bash
# In Playwright/Cypress test config
NEXT_PUBLIC_DISABLE_ANIMATIONS=true npx playwright test
```

**Key points:**
- `useAutoAnimate` returns `[ref, enable]` — call `enable(false)` to disable
- Use environment variable to disable globally during testing
- Prevents flaky tests caused by animation timing
