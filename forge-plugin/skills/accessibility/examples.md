# Accessibility Skill — Examples

Usage scenarios demonstrating how `skill:accessibility` solves real-world accessibility problems.

---

## Example 1: Navigation Menu Missing Keyboard Support

### Problem

A custom dropdown navigation menu built with `<div>` elements is inaccessible to keyboard users and screen readers.

### Before (Inaccessible)

```html
<div class="nav">
  <div class="nav-item" onclick="toggleMenu('products')">
    Products
    <div class="dropdown" id="products-menu">
      <div class="dropdown-item" onclick="navigate('/widgets')">Widgets</div>
      <div class="dropdown-item" onclick="navigate('/gadgets')">Gadgets</div>
    </div>
  </div>
</div>
```

**Issues:**
- No semantic structure — screen readers see generic `<div>` elements
- Not keyboard accessible — `onclick` only responds to mouse clicks
- No ARIA attributes — expanded/collapsed state not communicated
- No focus management — dropdown items unreachable via Tab

### After (Accessible)

```html
<nav aria-label="Main navigation">
  <ul role="menubar">
    <li role="none">
      <button
        role="menuitem"
        aria-haspopup="true"
        aria-expanded="false"
        aria-controls="products-menu"
      >
        Products
      </button>
      <ul role="menu" id="products-menu" hidden>
        <li role="none">
          <a role="menuitem" href="/widgets">Widgets</a>
        </li>
        <li role="none">
          <a role="menuitem" href="/gadgets">Gadgets</a>
        </li>
      </ul>
    </li>
  </ul>
</nav>
```

```javascript
// Keyboard handling
button.addEventListener("keydown", (e) => {
  switch (e.key) {
    case "Enter":
    case " ":
    case "ArrowDown":
      e.preventDefault()
      openMenu()
      menu.querySelector('[role="menuitem"]').focus()
      break
    case "Escape":
      closeMenu()
      button.focus()
      break
  }
})
```

**WCAG Criteria**: 2.1.1 Keyboard, 4.1.2 Name Role Value, 1.3.1 Info and Relationships

---

## Example 2: Form with Missing Labels and Error Handling

### Problem

A registration form uses placeholder text as labels and provides no accessible error feedback.

### Before (Inaccessible)

```html
<form>
  <input type="text" placeholder="Full Name" />
  <input type="email" placeholder="Email Address" />
  <input type="password" placeholder="Password" />
  <span class="error" style="color: red;">Password too short</span>
  <button type="submit">Sign Up</button>
</form>
```

**Issues:**
- Placeholder text disappears on input — user loses context
- No `<label>` elements — screen readers cannot identify fields
- Error message not linked to input — screen reader users don't know which field has the error
- Error identified by color only — invisible to color-blind users

### After (Accessible)

```html
<form novalidate>
  <div class="field">
    <label for="name">Full Name</label>
    <input
      id="name"
      type="text"
      autocomplete="name"
      aria-required="true"
      placeholder="Jane Doe"
    />
  </div>

  <div class="field">
    <label for="email">Email Address</label>
    <input
      id="email"
      type="email"
      autocomplete="email"
      aria-required="true"
      placeholder="jane@example.com"
    />
  </div>

  <div class="field">
    <label for="password">
      Password <span aria-hidden="true">*</span>
    </label>
    <input
      id="password"
      type="password"
      autocomplete="new-password"
      aria-required="true"
      aria-invalid="true"
      aria-describedby="password-error password-hint"
    />
    <p id="password-hint" class="hint">Must be at least 8 characters</p>
    <p id="password-error" class="error" role="alert">
      <span class="error-icon" aria-hidden="true">⚠</span>
      Password must be at least 8 characters
    </p>
  </div>

  <button type="submit">Sign Up</button>
</form>
```

**WCAG Criteria**: 1.3.1 Info and Relationships, 3.3.2 Labels or Instructions, 3.3.1 Error Identification, 1.4.1 Use of Color

---

## Example 3: Modal Dialog Without Focus Trapping

### Problem

A confirmation modal opens but keyboard focus escapes behind it, and there is no way to close it via keyboard.

### Before (Inaccessible)

```html
<div class="modal" style="display: block;">
  <div class="modal-content">
    <h2>Confirm Delete</h2>
    <p>Are you sure you want to delete this item?</p>
    <button onclick="deleteItem()">Delete</button>
    <button onclick="closeModal()">Cancel</button>
  </div>
</div>
```

### After (Accessible)

```html
<div
  role="dialog"
  aria-modal="true"
  aria-labelledby="modal-title"
  aria-describedby="modal-desc"
>
  <h2 id="modal-title">Confirm Delete</h2>
  <p id="modal-desc">Are you sure you want to delete this item? This action cannot be undone.</p>
  <div class="modal-actions">
    <button type="button" data-action="delete">Delete</button>
    <button type="button" data-action="cancel" autofocus>Cancel</button>
  </div>
</div>
```

```javascript
// Focus trap implementation
function trapFocus(modal) {
  const focusableElements = modal.querySelectorAll(
    'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
  )
  const first = focusableElements[0]
  const last = focusableElements[focusableElements.length - 1]

  modal.addEventListener("keydown", (e) => {
    if (e.key === "Escape") {
      closeModal()
      triggerElement.focus() // Restore focus to element that opened modal
      return
    }
    if (e.key !== "Tab") return

    if (e.shiftKey) {
      if (document.activeElement === first) {
        e.preventDefault()
        last.focus()
      }
    } else {
      if (document.activeElement === last) {
        e.preventDefault()
        first.focus()
      }
    }
  })

  first.focus()
}
```

**WCAG Criteria**: 2.1.2 No Keyboard Trap, 2.4.3 Focus Order, 1.3.1 Info and Relationships

---

## Example 4: Color Contrast Failure on Buttons

### Problem

Light gray text on a white button fails WCAG contrast requirements, and disabled state is indistinguishable.

### Before (Inaccessible)

```css
.btn-secondary {
  background: #f0f0f0;
  color: #999;       /* Contrast ratio: 2.85:1 — FAILS AA */
  border: none;
}
.btn-secondary:disabled {
  color: #ccc;       /* Contrast ratio: 1.61:1 — FAILS */
}
```

### After (Accessible)

```css
.btn-secondary {
  background: #f0f0f0;
  color: #595959;       /* Contrast ratio: 5.92:1 — PASSES AA */
  border: 1px solid #767676;  /* 4.54:1 contrast for UI component */
}
.btn-secondary:disabled {
  background: #f5f5f5;
  color: #767676;       /* Contrast ratio: 4.54:1 — PASSES AA */
  border-style: dashed; /* Visual distinction beyond color */
  cursor: not-allowed;
}
```

**WCAG Criteria**: 1.4.3 Contrast (Minimum), 1.4.11 Non-text Contrast

---

## Example 5: SPA Route Change Without Focus Management

### Problem

In a React SPA, clicking a navigation link changes the page content but screen reader users are not informed of the route change and focus remains on the clicked link.

### Before (Inaccessible)

```tsx
function App() {
  return (
    <Router>
      <nav><Link to="/dashboard">Dashboard</Link></nav>
      <Routes>
        <Route path="/dashboard" element={<Dashboard />} />
      </Routes>
    </Router>
  )
}
```

### After (Accessible)

```tsx
import { useEffect, useRef } from "react"
import { useLocation } from "react-router-dom"

function RouteAnnouncer() {
  const location = useLocation()
  const announcerRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    // Move focus to main content heading on route change
    const heading = document.querySelector("main h1")
    if (heading instanceof HTMLElement) {
      heading.setAttribute("tabindex", "-1")
      heading.focus()
    }
  }, [location.pathname])

  return (
    <div
      ref={announcerRef}
      role="status"
      aria-live="polite"
      aria-atomic="true"
      className="sr-only"
    >
      {`Navigated to ${document.title}`}
    </div>
  )
}

function App() {
  return (
    <Router>
      <a href="#main-content" className="sr-only focus:not-sr-only focus:absolute focus:z-50 focus:p-4">
        Skip to main content
      </a>
      <RouteAnnouncer />
      <nav aria-label="Main navigation">
        <Link to="/dashboard">Dashboard</Link>
      </nav>
      <main id="main-content">
        <Routes>
          <Route path="/dashboard" element={<Dashboard />} />
        </Routes>
      </main>
    </Router>
  )
}
```

**WCAG Criteria**: 2.4.1 Bypass Blocks (skip link), 2.4.3 Focus Order, 4.1.3 Status Messages
