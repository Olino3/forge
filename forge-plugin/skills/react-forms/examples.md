# React Forms Skill — Examples

Usage scenarios demonstrating how `skill:react-forms` builds type-safe validated forms.

---

## Example 1: Registration Form with Zod + React Hook Form

### Problem

A user registration form needs email validation, password confirmation, and type-safe submission.

### Implementation

```typescript
// schemas/auth.ts — Single source of truth for types and validation
import { z } from "zod"

export const registerSchema = z
  .object({
    name: z.string().min(2, "Name must be at least 2 characters"),
    email: z.string().email("Please enter a valid email"),
    password: z
      .string()
      .min(8, "Password must be at least 8 characters")
      .regex(/[A-Z]/, "Must contain at least one uppercase letter")
      .regex(/[0-9]/, "Must contain at least one number"),
    confirmPassword: z.string(),
    acceptTerms: z.literal(true, {
      errorMap: () => ({ message: "You must accept the terms" }),
    }),
  })
  .refine((data) => data.password === data.confirmPassword, {
    message: "Passwords don't match",
    path: ["confirmPassword"],
  })

// Inferred type — never define manually
export type RegisterFormData = z.infer<typeof registerSchema>
```

```tsx
// components/register-form.tsx
"use client"
import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import { registerSchema, type RegisterFormData } from "@/schemas/auth"
import { registerUser } from "@/app/actions"

export function RegisterForm() {
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
    setError,
  } = useForm<RegisterFormData>({
    resolver: zodResolver(registerSchema),
    defaultValues: {
      name: "",
      email: "",
      password: "",
      confirmPassword: "",
      acceptTerms: false as unknown as true,
    },
  })

  async function onSubmit(data: RegisterFormData) {
    const result = await registerUser(data)
    if (result?.errors) {
      // Map server errors back to form fields
      Object.entries(result.errors).forEach(([field, messages]) => {
        setError(field as keyof RegisterFormData, {
          message: messages[0],
        })
      })
    }
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)} noValidate className="space-y-4">
      <div>
        <label htmlFor="name">Full Name</label>
        <input id="name" {...register("name")} aria-invalid={!!errors.name} />
        {errors.name && <p role="alert">{errors.name.message}</p>}
      </div>

      <div>
        <label htmlFor="email">Email</label>
        <input id="email" type="email" {...register("email")} aria-invalid={!!errors.email} />
        {errors.email && <p role="alert">{errors.email.message}</p>}
      </div>

      <div>
        <label htmlFor="password">Password</label>
        <input id="password" type="password" {...register("password")} aria-invalid={!!errors.password} />
        {errors.password && <p role="alert">{errors.password.message}</p>}
      </div>

      <div>
        <label htmlFor="confirmPassword">Confirm Password</label>
        <input id="confirmPassword" type="password" {...register("confirmPassword")} aria-invalid={!!errors.confirmPassword} />
        {errors.confirmPassword && <p role="alert">{errors.confirmPassword.message}</p>}
      </div>

      <div>
        <label>
          <input type="checkbox" {...register("acceptTerms")} />
          I accept the terms and conditions
        </label>
        {errors.acceptTerms && <p role="alert">{errors.acceptTerms.message}</p>}
      </div>

      <button type="submit" disabled={isSubmitting}>
        {isSubmitting ? "Creating account..." : "Register"}
      </button>
    </form>
  )
}
```

**Key points:**
- `.refine()` handles cross-field validation (password confirmation)
- `z.literal(true)` enforces checkbox must be checked
- Server errors mapped back via `setError`
- `aria-invalid` for accessibility

---

## Example 2: Multi-Step Wizard Form

### Problem

A checkout form needs to be split across multiple steps with validation per step and shared state.

### Implementation

```typescript
// schemas/checkout.ts
import { z } from "zod"

export const shippingSchema = z.object({
  address: z.string().min(5, "Address is required"),
  city: z.string().min(2, "City is required"),
  zip: z.string().regex(/^\d{5}(-\d{4})?$/, "Invalid ZIP code"),
  country: z.string().min(2, "Country is required"),
})

export const paymentSchema = z.object({
  cardNumber: z.string().regex(/^\d{16}$/, "Card number must be 16 digits"),
  expiry: z.string().regex(/^\d{2}\/\d{2}$/, "Format: MM/YY"),
  cvv: z.string().regex(/^\d{3,4}$/, "CVV must be 3-4 digits"),
})

// Combined for final submission
export const checkoutSchema = shippingSchema.merge(paymentSchema)
export type CheckoutFormData = z.infer<typeof checkoutSchema>
```

```tsx
// components/checkout-wizard.tsx
"use client"
import { useState } from "react"
import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import {
  shippingSchema,
  paymentSchema,
  checkoutSchema,
  type CheckoutFormData,
} from "@/schemas/checkout"

const steps = [
  { schema: shippingSchema, fields: ["address", "city", "zip", "country"] as const },
  { schema: paymentSchema, fields: ["cardNumber", "expiry", "cvv"] as const },
]

export function CheckoutWizard() {
  const [step, setStep] = useState(0)
  const currentStep = steps[step]

  const {
    register,
    handleSubmit,
    trigger,
    formState: { errors, isSubmitting },
  } = useForm<CheckoutFormData>({
    resolver: zodResolver(checkoutSchema),
    mode: "onBlur",
  })

  async function handleNext() {
    // Validate only current step's fields
    const valid = await trigger(currentStep.fields as unknown as (keyof CheckoutFormData)[])
    if (valid) setStep((s) => s + 1)
  }

  async function onSubmit(data: CheckoutFormData) {
    await processCheckout(data)
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <div aria-label={`Step ${step + 1} of ${steps.length}`}>
        {step === 0 && (
          <>
            <h2>Shipping Address</h2>
            <input {...register("address")} placeholder="Street address" />
            {errors.address && <p role="alert">{errors.address.message}</p>}
            <input {...register("city")} placeholder="City" />
            {errors.city && <p role="alert">{errors.city.message}</p>}
            <input {...register("zip")} placeholder="ZIP code" />
            {errors.zip && <p role="alert">{errors.zip.message}</p>}
            <input {...register("country")} placeholder="Country" />
            {errors.country && <p role="alert">{errors.country.message}</p>}
          </>
        )}

        {step === 1 && (
          <>
            <h2>Payment Details</h2>
            <input {...register("cardNumber")} placeholder="Card number" />
            {errors.cardNumber && <p role="alert">{errors.cardNumber.message}</p>}
            <input {...register("expiry")} placeholder="MM/YY" />
            {errors.expiry && <p role="alert">{errors.expiry.message}</p>}
            <input {...register("cvv")} placeholder="CVV" />
            {errors.cvv && <p role="alert">{errors.cvv.message}</p>}
          </>
        )}
      </div>

      <div className="flex gap-4">
        {step > 0 && (
          <button type="button" onClick={() => setStep((s) => s - 1)}>
            Back
          </button>
        )}
        {step < steps.length - 1 ? (
          <button type="button" onClick={handleNext}>
            Next
          </button>
        ) : (
          <button type="submit" disabled={isSubmitting}>
            {isSubmitting ? "Processing..." : "Place Order"}
          </button>
        )}
      </div>
    </form>
  )
}
```

**Key points:**
- Separate schemas per step, merged for final validation
- `trigger()` validates specific fields for per-step validation
- Single `useForm` instance preserves state across steps
- `mode: "onBlur"` validates when user leaves a field

---

## Example 3: Dynamic Field Array (Invoice Line Items)

### Problem

An invoice form needs to dynamically add and remove line items with per-row validation.

### Implementation

```typescript
// schemas/invoice.ts
import { z } from "zod"

export const lineItemSchema = z.object({
  description: z.string().min(1, "Description required"),
  quantity: z.coerce.number().min(1, "Must be at least 1"),
  unitPrice: z.coerce.number().min(0.01, "Must be greater than 0"),
})

export const invoiceSchema = z.object({
  clientName: z.string().min(2, "Client name required"),
  dueDate: z.string().min(1, "Due date required"),
  items: z.array(lineItemSchema).min(1, "At least one line item required"),
})

export type InvoiceFormData = z.infer<typeof invoiceSchema>
```

```tsx
// components/invoice-form.tsx
"use client"
import { useForm, useFieldArray } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import { invoiceSchema, type InvoiceFormData } from "@/schemas/invoice"

export function InvoiceForm() {
  const {
    register,
    control,
    handleSubmit,
    watch,
    formState: { errors },
  } = useForm<InvoiceFormData>({
    resolver: zodResolver(invoiceSchema),
    defaultValues: {
      clientName: "",
      dueDate: "",
      items: [{ description: "", quantity: 1, unitPrice: 0 }],
    },
  })

  const { fields, append, remove } = useFieldArray({
    control,
    name: "items",
  })

  const watchedItems = watch("items")
  const total = watchedItems?.reduce(
    (sum, item) => sum + (item.quantity || 0) * (item.unitPrice || 0),
    0
  ) ?? 0

  async function onSubmit(data: InvoiceFormData) {
    await createInvoice(data)
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
      <input {...register("clientName")} placeholder="Client name" />
      <input {...register("dueDate")} type="date" />

      <table>
        <thead>
          <tr>
            <th>Description</th>
            <th>Qty</th>
            <th>Unit Price</th>
            <th>Total</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          {fields.map((field, index) => (
            <tr key={field.id}>
              <td>
                <input {...register(`items.${index}.description`)} />
                {errors.items?.[index]?.description && (
                  <p role="alert">{errors.items[index].description.message}</p>
                )}
              </td>
              <td>
                <input {...register(`items.${index}.quantity`)} type="number" min="1" />
              </td>
              <td>
                <input {...register(`items.${index}.unitPrice`)} type="number" step="0.01" />
              </td>
              <td>
                ${((watchedItems?.[index]?.quantity || 0) * (watchedItems?.[index]?.unitPrice || 0)).toFixed(2)}
              </td>
              <td>
                {fields.length > 1 && (
                  <button type="button" onClick={() => remove(index)}>Remove</button>
                )}
              </td>
            </tr>
          ))}
        </tbody>
        <tfoot>
          <tr>
            <td colSpan={3}><strong>Total</strong></td>
            <td><strong>${total.toFixed(2)}</strong></td>
          </tr>
        </tfoot>
      </table>

      <button type="button" onClick={() => append({ description: "", quantity: 1, unitPrice: 0 })}>
        + Add Line Item
      </button>

      <button type="submit">Create Invoice</button>
    </form>
  )
}
```

**Key points:**
- `useFieldArray` manages dynamic arrays with proper key tracking
- `z.coerce.number()` converts string form values to numbers
- `watch("items")` for live total calculation
- Each field uses `items.${index}.fieldName` path for registration
