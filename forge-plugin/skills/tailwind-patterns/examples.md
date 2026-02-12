# Tailwind Patterns Skill — Examples

Usage scenarios demonstrating how `skill:tailwind-patterns` builds production components.

---

## Example 1: Responsive Dashboard Layout

### Problem

A dashboard needs a sidebar navigation on desktop that collapses to a bottom navigation on mobile.

### Implementation

```tsx
export function DashboardLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex min-h-screen flex-col md:flex-row">
      {/* Sidebar: hidden on mobile, shown on md+ */}
      <aside className="hidden w-64 shrink-0 border-r bg-card md:block">
        <nav className="flex flex-col gap-1 p-4" aria-label="Dashboard navigation">
          <NavLink href="/dashboard" icon="home">Overview</NavLink>
          <NavLink href="/dashboard/analytics" icon="chart">Analytics</NavLink>
          <NavLink href="/dashboard/settings" icon="gear">Settings</NavLink>
        </nav>
      </aside>

      {/* Main content */}
      <main className="flex-1 overflow-auto p-4 pb-20 md:p-8 md:pb-8">
        {children}
      </main>

      {/* Bottom nav: shown on mobile, hidden on md+ */}
      <nav
        className="fixed inset-x-0 bottom-0 z-50 flex border-t bg-card md:hidden"
        aria-label="Mobile navigation"
      >
        <BottomNavItem href="/dashboard" icon="home" label="Home" />
        <BottomNavItem href="/dashboard/analytics" icon="chart" label="Analytics" />
        <BottomNavItem href="/dashboard/settings" icon="gear" label="Settings" />
      </nav>
    </div>
  )
}

function NavLink({ href, icon, children }: { href: string; icon: string; children: React.ReactNode }) {
  return (
    <a
      href={href}
      className="
        flex items-center gap-3 rounded-md px-3 py-2 text-sm font-medium
        text-muted-foreground
        hover:bg-accent hover:text-accent-foreground
        focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring
        transition-colors
      "
    >
      <Icon name={icon} className="h-4 w-4" />
      {children}
    </a>
  )
}

function BottomNavItem({ href, icon, label }: { href: string; icon: string; label: string }) {
  return (
    <a
      href={href}
      className="
        flex flex-1 flex-col items-center gap-1 py-3 text-xs
        text-muted-foreground
        hover:text-foreground
        transition-colors
      "
    >
      <Icon name={icon} className="h-5 w-5" />
      {label}
    </a>
  )
}
```

**Key points:**
- `hidden md:block` / `md:hidden` for device-appropriate navigation
- `pb-20 md:pb-8` accounts for bottom nav height on mobile
- Semantic `<nav>` with `aria-label` for screen readers
- `focus-visible:` for keyboard-only focus indicators

---

## Example 2: Card Component with Variants (cva)

### Problem

The design system needs a reusable card with size, variant, and interactive states that stays consistent.

### Implementation

```tsx
// components/ui/card.tsx
import { cva, type VariantProps } from "class-variance-authority"
import { cn } from "@/lib/utils"

const cardVariants = cva(
  // Base styles
  "rounded-xl border bg-card text-card-foreground transition-shadow",
  {
    variants: {
      variant: {
        default: "border-border shadow-sm",
        outlined: "border-2 border-primary/20 shadow-none",
        elevated: "border-transparent shadow-lg",
        ghost: "border-transparent shadow-none bg-transparent",
      },
      size: {
        sm: "p-4",
        md: "p-6",
        lg: "p-8",
      },
      interactive: {
        true: "cursor-pointer hover:shadow-md active:scale-[0.98]",
        false: "",
      },
    },
    defaultVariants: {
      variant: "default",
      size: "md",
      interactive: false,
    },
  }
)

interface CardProps
  extends React.HTMLAttributes<HTMLDivElement>,
    VariantProps<typeof cardVariants> {}

export function Card({ className, variant, size, interactive, ...props }: CardProps) {
  return (
    <div
      className={cn(cardVariants({ variant, size, interactive }), className)}
      {...props}
    />
  )
}

export function CardHeader({ className, ...props }: React.HTMLAttributes<HTMLDivElement>) {
  return <div className={cn("flex flex-col gap-1.5", className)} {...props} />
}

export function CardTitle({ className, ...props }: React.HTMLAttributes<HTMLHeadingElement>) {
  return <h3 className={cn("text-lg font-semibold leading-none tracking-tight", className)} {...props} />
}

export function CardDescription({ className, ...props }: React.HTMLAttributes<HTMLParagraphElement>) {
  return <p className={cn("text-sm text-muted-foreground", className)} {...props} />
}

export function CardContent({ className, ...props }: React.HTMLAttributes<HTMLDivElement>) {
  return <div className={cn("pt-4", className)} {...props} />
}

export function CardFooter({ className, ...props }: React.HTMLAttributes<HTMLDivElement>) {
  return <div className={cn("flex items-center gap-2 pt-4", className)} {...props} />
}
```

**Usage:**

```tsx
<Card variant="elevated" size="lg" interactive>
  <CardHeader>
    <CardTitle>Pro Plan</CardTitle>
    <CardDescription>For growing teams</CardDescription>
  </CardHeader>
  <CardContent>
    <p className="text-3xl font-bold">$29<span className="text-sm font-normal text-muted-foreground">/mo</span></p>
  </CardContent>
  <CardFooter>
    <Button className="w-full">Get Started</Button>
  </CardFooter>
</Card>
```

**Key points:**
- `cva` (class-variance-authority) defines typed variants
- `cn()` utility merges classes, allowing override via `className` prop
- Compound components (`CardHeader`, `CardContent`, etc.) for flexible composition
- Design token colors (`bg-card`, `text-card-foreground`) for theme support

---

## Example 3: Form with Dark Mode Support

### Problem

A settings form needs to work in both light and dark mode with proper contrast and visual feedback.

### Implementation

```tsx
export function SettingsForm() {
  return (
    <form className="mx-auto max-w-2xl space-y-8">
      <fieldset className="space-y-4">
        <legend className="text-lg font-semibold text-foreground">
          Profile Settings
        </legend>

        <div className="space-y-2">
          <label htmlFor="displayName" className="text-sm font-medium leading-none text-foreground">
            Display Name
          </label>
          <input
            id="displayName"
            type="text"
            className="
              flex h-10 w-full rounded-md border border-input
              bg-background px-3 py-2 text-sm text-foreground
              ring-offset-background
              placeholder:text-muted-foreground
              focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2
              disabled:cursor-not-allowed disabled:opacity-50
            "
            placeholder="Enter your name"
          />
        </div>

        <div className="space-y-2">
          <label htmlFor="bio" className="text-sm font-medium leading-none text-foreground">
            Bio
          </label>
          <textarea
            id="bio"
            rows={4}
            className="
              flex min-h-[80px] w-full rounded-md border border-input
              bg-background px-3 py-2 text-sm text-foreground
              ring-offset-background
              placeholder:text-muted-foreground
              focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2
              disabled:cursor-not-allowed disabled:opacity-50
              resize-y
            "
            placeholder="Tell us about yourself"
          />
          <p className="text-xs text-muted-foreground">
            Maximum 160 characters.
          </p>
        </div>

        <div className="flex items-center gap-3">
          <input
            id="notifications"
            type="checkbox"
            className="
              h-4 w-4 rounded border border-primary
              text-primary
              focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2
            "
          />
          <label htmlFor="notifications" className="text-sm font-medium leading-none text-foreground">
            Enable email notifications
          </label>
        </div>
      </fieldset>

      <div className="flex justify-end gap-3">
        <button
          type="button"
          className="
            inline-flex h-10 items-center justify-center rounded-md
            border border-input bg-background px-4 py-2
            text-sm font-medium text-foreground
            hover:bg-accent hover:text-accent-foreground
            focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2
            transition-colors
          "
        >
          Cancel
        </button>
        <button
          type="submit"
          className="
            inline-flex h-10 items-center justify-center rounded-md
            bg-primary px-4 py-2
            text-sm font-medium text-primary-foreground
            hover:bg-primary/90
            focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2
            disabled:pointer-events-none disabled:opacity-50
            transition-colors
          "
        >
          Save Changes
        </button>
      </div>
    </form>
  )
}
```

**Key points:**
- All colors use design tokens (`foreground`, `background`, `muted-foreground`, `primary`)
- Dark mode works automatically — tokens resolve to different values based on `dark` class
- `ring-offset-background` ensures focus ring offset matches current theme
- `focus-visible:` (not `focus:`) for keyboard-only focus indicators
- `disabled:pointer-events-none disabled:opacity-50` for consistent disabled states

---

## Example 4: Responsive Grid with Container Queries

### Problem

A component rendered in both a sidebar (narrow) and main content area (wide) needs to adapt to its container width, not the viewport.

### Implementation

```tsx
export function StatsGrid({ stats }: { stats: Stat[] }) {
  return (
    <div className="@container">
      <div className="grid grid-cols-1 gap-4 @sm:grid-cols-2 @lg:grid-cols-4">
        {stats.map((stat) => (
          <div
            key={stat.label}
            className="rounded-lg border bg-card p-4 @sm:p-6"
          >
            <p className="text-sm text-muted-foreground">{stat.label}</p>
            <p className="text-2xl font-bold @lg:text-3xl">{stat.value}</p>
            <p className={cn(
              "mt-1 text-xs",
              stat.trend > 0 ? "text-green-600 dark:text-green-400" : "text-red-600 dark:text-red-400"
            )}>
              {stat.trend > 0 ? "↑" : "↓"} {Math.abs(stat.trend)}% from last month
            </p>
          </div>
        ))}
      </div>
    </div>
  )
}
```

**Key points:**
- `@container` on the parent enables container queries
- `@sm:`, `@lg:` breakpoints respond to container width, not viewport
- Same component works in sidebar (1-col), main area (2-col), and full-width (4-col)
- Requires Tailwind v3.2+ with container queries plugin or Tailwind v4
