# Next.js Skill — Examples

Usage scenarios demonstrating how `skill:nextjs` builds production Next.js 16 applications.

---

## Example 1: Server Component with Async Params (Next.js 16)

### Problem

A product detail page needs to fetch data using the route slug, but Next.js 16 changed `params` to be a Promise.

### Implementation

```typescript
// app/products/[slug]/page.tsx
import { notFound } from "next/navigation"
import { Metadata } from "next"

interface PageProps {
  params: Promise<{ slug: string }>
}

// Dynamic metadata
export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  const { slug } = await params
  const product = await getProduct(slug)
  if (!product) return { title: "Not Found" }
  return {
    title: product.name,
    description: product.description,
    openGraph: { images: [product.imageUrl] },
  }
}

// Server Component — no "use client" needed
export default async function ProductPage({ params }: PageProps) {
  const { slug } = await params
  const product = await getProduct(slug)

  if (!product) notFound()

  return (
    <main>
      <h1>{product.name}</h1>
      <p>{product.description}</p>
      <span>${product.price}</span>
      <AddToCartButton productId={product.id} />
    </main>
  )
}

// Static generation for known products
export async function generateStaticParams() {
  const products = await getAllProductSlugs()
  return products.map((slug) => ({ slug }))
}
```

**Key points:**
- `params` is a `Promise` in Next.js 16 — must `await` before accessing properties
- Server Components can directly call database functions
- `generateStaticParams` enables ISR (Incremental Static Regeneration)

---

## Example 2: Server Action with Form Validation

### Problem

A contact form needs server-side validation, mutation, and page revalidation — without a separate API route.

### Implementation

```typescript
// app/contact/actions.ts
"use server"

import { z } from "zod"
import { revalidatePath } from "next/cache"

const contactSchema = z.object({
  name: z.string().min(2, "Name must be at least 2 characters"),
  email: z.string().email("Invalid email address"),
  message: z.string().min(10, "Message must be at least 10 characters"),
})

export type ContactState = {
  errors?: Record<string, string[]>
  success?: boolean
}

export async function submitContact(
  prevState: ContactState,
  formData: FormData
): Promise<ContactState> {
  const result = contactSchema.safeParse({
    name: formData.get("name"),
    email: formData.get("email"),
    message: formData.get("message"),
  })

  if (!result.success) {
    return { errors: result.error.flatten().fieldErrors }
  }

  await db.contacts.create({ data: result.data })
  revalidatePath("/contact")

  return { success: true }
}
```

```tsx
// app/contact/page.tsx
"use client"

import { useActionState } from "react"
import { submitContact, type ContactState } from "./actions"

const initialState: ContactState = {}

export default function ContactPage() {
  const [state, formAction, isPending] = useActionState(submitContact, initialState)

  if (state.success) {
    return <p role="status">Thank you! We will be in touch.</p>
  }

  return (
    <form action={formAction}>
      <div>
        <label htmlFor="name">Name</label>
        <input id="name" name="name" required />
        {state.errors?.name && (
          <p role="alert" className="text-red-500">{state.errors.name[0]}</p>
        )}
      </div>

      <div>
        <label htmlFor="email">Email</label>
        <input id="email" name="email" type="email" required />
        {state.errors?.email && (
          <p role="alert" className="text-red-500">{state.errors.email[0]}</p>
        )}
      </div>

      <div>
        <label htmlFor="message">Message</label>
        <textarea id="message" name="message" rows={5} required />
        {state.errors?.message && (
          <p role="alert" className="text-red-500">{state.errors.message[0]}</p>
        )}
      </div>

      <button type="submit" disabled={isPending}>
        {isPending ? "Sending..." : "Send Message"}
      </button>
    </form>
  )
}
```

**Key points:**
- `"use server"` marks the function as a Server Action
- `useActionState` (React 19) manages form state, pending state, and progressive enhancement
- Zod schema validates on the server — same schema can be reused client-side
- `revalidatePath` refreshes cached data after mutation

---

## Example 3: Cache Component with "use cache" Directive

### Problem

A product listing page queries the database on every request, causing unnecessary load. The data changes infrequently and can be cached.

### Implementation

```typescript
// app/products/page.tsx
"use cache"

import { Suspense } from "react"
import { ProductGrid } from "./product-grid"
import { ProductGridSkeleton } from "./product-grid-skeleton"

// This entire component is cached — the DB query runs once and result is reused
export default async function ProductsPage() {
  const products = await db.products.findMany({
    where: { active: true },
    orderBy: { createdAt: "desc" },
  })

  return (
    <main>
      <h1>Our Products</h1>
      <Suspense fallback={<ProductGridSkeleton />}>
        <ProductGrid products={products} />
      </Suspense>
    </main>
  )
}
```

```typescript
// app/products/actions.ts
"use server"

import { revalidateTag } from "next/cache"

export async function createProduct(formData: FormData) {
  await db.products.create({ data: parseFormData(formData) })
  // Invalidate the cached product list
  revalidateTag("products")
}
```

**Key points:**
- `"use cache"` at the top of the file caches the entire component's output
- Cannot access cookies, headers, or other dynamic APIs inside cached components
- Use `revalidateTag()` or `revalidatePath()` to invalidate when data changes
- Unlike `fetch` cache, this works with any data source (ORM, SDK, file system)

---

## Example 4: Client/Server Component Boundary

### Problem

An interactive product card needs a "Like" button with state, but the product data should be fetched on the server.

### Implementation

```typescript
// app/products/product-card.tsx (Server Component — no directive needed)
import { LikeButton } from "./like-button"

interface Product {
  id: string
  name: string
  price: number
  imageUrl: string
}

export function ProductCard({ product }: { product: Product }) {
  return (
    <article className="rounded-lg border p-4">
      <img src={product.imageUrl} alt={product.name} width={300} height={200} />
      <h3>{product.name}</h3>
      <p>${product.price}</p>
      {/* Client Component boundary — only this ships JS to browser */}
      <LikeButton productId={product.id} />
    </article>
  )
}
```

```tsx
// app/products/like-button.tsx
"use client"

import { useState, useOptimistic } from "react"
import { toggleLike } from "./actions"

export function LikeButton({ productId }: { productId: string }) {
  const [liked, setLiked] = useState(false)
  const [optimisticLiked, setOptimisticLiked] = useOptimistic(liked)

  async function handleLike() {
    setOptimisticLiked(!optimisticLiked)
    const result = await toggleLike(productId)
    setLiked(result.liked)
  }

  return (
    <button onClick={handleLike} aria-pressed={optimisticLiked}>
      {optimisticLiked ? "♥ Liked" : "♡ Like"}
    </button>
  )
}
```

**Key points:**
- Push `"use client"` as deep as possible — only the `LikeButton` ships JS
- `ProductCard` is a Server Component — fetched data never hits the client bundle
- `useOptimistic` (React 19) provides instant UI feedback before server confirms
- Props from Server to Client must be serializable (strings, numbers, booleans, arrays, plain objects)
