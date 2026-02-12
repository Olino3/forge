# Icon Design - Usage Examples

This document provides 3 comprehensive examples demonstrating the `icon-design` skill in action across different icon libraries, frameworks, and project types.

---

## Example 1: Selecting Icons for a SaaS Dashboard Navigation (Lucide + React)

### Scenario

User is building a SaaS analytics dashboard with React and needs icons for the main sidebar navigation. No prior memory exists for this project.

### User Prompt

"I need icons for my dashboard sidebar: Dashboard, Analytics, Users, Settings, Notifications, Billing, and Help. We're using React with Tailwind CSS."

### Skill Execution

**Step 1: Initial Analysis**
- Concepts: Dashboard, Analytics, Users, Settings, Notifications, Billing, Help
- Framework: React with Tailwind CSS
- Icon library: Not specified — will recommend Lucide (tree-shakeable, React-native support, MIT license)
- Project name: "saas-dashboard"
- No existing icon conventions detected

**Step 2: Load Memory**
- No memory exists for "saas-dashboard" — first-time use
- Continue with empty memory

**Step 3: Load Context**
- Load engineering domain context for frontend patterns
- Note Lucide's named export convention for tree-shaking

**Step 4: Map Concepts to Icons**
- **Dashboard** → `LayoutDashboard` (primary), alternatives: `LayoutGrid`, `AppWindow`
  - Rationale: Grid-based layout icon universally represents dashboards
- **Analytics** → `BarChart3` (primary), alternatives: `TrendingUp`, `LineChart`
  - Rationale: Bar chart is the most recognizable data visualization symbol
- **Users** → `Users` (primary), alternatives: `UserCircle`, `Contact`
  - Rationale: Multi-person icon for user management sections
- **Settings** → `Settings` (primary), alternatives: `SlidersHorizontal`, `Wrench`
  - Rationale: Gear icon is the universal settings metaphor
- **Notifications** → `Bell` (primary), alternatives: `BellRing`, `Inbox`
  - Rationale: Bell is the standard notification indicator
- **Billing** → `CreditCard` (primary), alternatives: `Receipt`, `Wallet`
  - Rationale: Credit card clearly communicates payment/billing
- **Help** → `HelpCircle` (primary), alternatives: `LifeBuoy`, `MessageCircleQuestion`
  - Rationale: Question mark in circle is the universal help symbol

**Step 5: Generate Integration Code**
- Install: `npm install lucide-react`
- Generate named imports for tree-shaking:
  ```jsx
  import {
    LayoutDashboard,
    BarChart3,
    Users,
    Settings,
    Bell,
    CreditCard,
    HelpCircle,
  } from 'lucide-react';
  ```
- Generate navigation component with consistent sizing:
  ```jsx
  const navItems = [
    { label: 'Dashboard', icon: LayoutDashboard, href: '/' },
    { label: 'Analytics', icon: BarChart3, href: '/analytics' },
    { label: 'Users', icon: Users, href: '/users' },
    { label: 'Settings', icon: Settings, href: '/settings' },
    { label: 'Notifications', icon: Bell, href: '/notifications' },
    { label: 'Billing', icon: CreditCard, href: '/billing' },
    { label: 'Help', icon: HelpCircle, href: '/help' },
  ];

  function Sidebar() {
    return (
      <nav>
        {navItems.map(({ label, icon: Icon, href }) => (
          <a key={href} href={href} className="flex items-center gap-3 px-4 py-2">
            <Icon size={20} strokeWidth={1.75} className="text-gray-500" />
            <span>{label}</span>
          </a>
        ))}
      </nav>
    );
  }
  ```

**Step 6: Optimize for Production**
- Lucide's named exports enable automatic tree-shaking — only the 7 imported icons are bundled
- Estimated bundle addition: ~2.8 KB gzipped (7 icons × ~400 bytes each)
- No dynamic imports needed for this small set

**Step 7: Generate Output**
- Saved to `/claudedocs/icon-design_saas-dashboard_2025-07-15.md`

**Step 8: Update Memory**
- Created `memory/skills/icon-design/saas-dashboard/icon_mappings.md` with all 7 mappings
- Created `memory/skills/icon-design/saas-dashboard/library_preferences.md`:
  - Library: Lucide React
  - Size: 20px
  - Stroke width: 1.75
  - Color: Tailwind `text-gray-500`

### Sample Output

```
✓ Recommended Lucide React for tree-shaking and Tailwind compatibility
✓ Mapped 7 navigation concepts to icons with alternatives
✓ Generated React sidebar component with consistent styling
✓ Bundle impact: ~2.8 KB gzipped (7 icons)

Memory saved for project 'saas-dashboard' — future icon selections will reuse these conventions.
```

---

## Example 2: Designing Icon Set for an E-Commerce Product Page (Heroicons + HTML/Tailwind)

### Scenario

User is building a static e-commerce product page with HTML and Tailwind CSS. They want icons for product features, trust badges, and action buttons. Memory exists from a previous session with library preference for Heroicons.

### User Prompt

"Add icons to my product page for: Add to Cart, Wishlist, Free Shipping, 30-Day Returns, Secure Payment, Star Rating, and Share. Using plain HTML with Tailwind."

### Skill Execution

**Step 1: Initial Analysis**
- Concepts: Add to Cart, Wishlist, Free Shipping, 30-Day Returns, Secure Payment, Star Rating, Share
- Framework: Plain HTML with Tailwind CSS
- Icon library: Check memory for preference
- Project name: "ecom-storefront"

**Step 2: Load Memory**
- Found existing memory for "ecom-storefront"
- `library_preferences.md`: Heroicons, outline style, 24px, stroke-width 1.5
- `icon_mappings.md`: 3 previous mappings (Home → `HomeIcon`, Search → `MagnifyingGlassIcon`, Menu → `Bars3Icon`)

**Step 3: Load Context**
- Load engineering domain context
- Note Heroicons provides both React components and raw SVG files

**Step 4: Map Concepts to Icons**
- **Add to Cart** → `shopping-cart` (primary), alternatives: `shopping-bag`, `plus-circle`
  - Rationale: Shopping cart is the universal e-commerce add action
- **Wishlist** → `heart` (primary), alternatives: `bookmark`, `star`
  - Rationale: Heart universally represents favorites/wishlists
- **Free Shipping** → `truck` (primary), alternatives: `paper-airplane`, `globe-alt`
  - Rationale: Delivery truck directly communicates shipping
- **30-Day Returns** → `arrow-path` (primary), alternatives: `arrow-uturn-left`, `receipt-refund`
  - Rationale: Circular arrow conveys return/exchange cycle
- **Secure Payment** → `shield-check` (primary), alternatives: `lock-closed`, `key`
  - Rationale: Shield with check mark communicates verified security
- **Star Rating** → `star` (primary), alternatives: `sparkles`, `hand-thumb-up`
  - Rationale: Star is the standard rating symbol across all platforms
- **Share** → `share` (primary), alternatives: `arrow-up-on-square`, `link`
  - Rationale: Share icon is platform-standard for social sharing

**Step 5: Generate Integration Code**
- Using Heroicons SVG via CDN for HTML project:
  ```html
  <!-- Trust badges row -->
  <div class="flex gap-6 justify-center py-4">
    <div class="flex items-center gap-2 text-sm text-gray-600">
      <!-- Free Shipping: truck -->
      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"
           stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
        <path stroke-linecap="round" stroke-linejoin="round"
              d="M8.25 18.75a1.5 1.5 0 0 1-3 0m3 0a1.5 1.5 0 0 0-3 0m3 0h6m-9 0H3.375..." />
      </svg>
      <span>Free Shipping</span>
    </div>
  </div>

  <!-- Action buttons -->
  <button class="flex items-center gap-2 bg-blue-600 text-white px-6 py-3 rounded-lg">
    <!-- Add to Cart: shopping-cart -->
    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"
         stroke-width="1.5" stroke="currentColor" class="w-5 h-5">
      <path stroke-linecap="round" stroke-linejoin="round"
            d="M2.25 3h1.386c.51 0 .955.343 1.087.835l.383 1.437..." />
    </svg>
    Add to Cart
  </button>
  ```
- Consistent sizing: `w-6 h-6` for badges, `w-5 h-5` for button icons

**Step 6: Optimize for Production**
- Generated an SVG sprite sheet containing all 7 icons plus the 3 from memory:
  ```html
  <svg xmlns="http://www.w3.org/2000/svg" style="display:none">
    <symbol id="icon-shopping-cart" viewBox="0 0 24 24">...</symbol>
    <symbol id="icon-heart" viewBox="0 0 24 24">...</symbol>
    <!-- remaining icons -->
  </svg>
  ```
- Usage via `<use>` references reduces duplicate SVG markup:
  ```html
  <svg class="w-5 h-5"><use href="#icon-shopping-cart" /></svg>
  ```
- Single HTTP request for all icons vs 10 separate SVGs

**Step 7: Generate Output**
- Saved to `/claudedocs/icon-design_ecom-storefront_2025-07-15.md`

**Step 8: Update Memory**
- Updated `icon_mappings.md` with 7 new concept-to-icon mappings (total: 10)
- `library_preferences.md` unchanged — same conventions apply

### Sample Output

```
✓ Using Heroicons (outline, 24px) per project memory
✓ Mapped 7 product page concepts to icons with alternatives
✓ Generated HTML/Tailwind integration with inline SVGs
✓ Created SVG sprite sheet for 10 icons (3 existing + 7 new)

Memory updated for project 'ecom-storefront' — 10 icon mappings stored.
```

---

## Example 3: Creating a Consistent Icon System for a Mobile App (Phosphor + React Native)

### Scenario

User is building a React Native fitness tracking app and needs a consistent icon system across multiple screens. No memory exists. They specifically request Phosphor Icons for its weight variants.

### User Prompt

"Set up icons for my fitness app using Phosphor. I need: Home, Workouts, Progress, Profile, Timer, Heart Rate, Calories, and Steps. We need both tab bar icons and in-screen icons."

### Skill Execution

**Step 1: Initial Analysis**
- Concepts: Home, Workouts, Progress, Profile, Timer, Heart Rate, Calories, Steps
- Framework: React Native
- Icon library: Phosphor (user-specified) — supports 6 weight variants (thin, light, regular, bold, fill, duotone)
- Dual context: tab bar icons (filled for active, regular for inactive) and in-screen icons (regular weight)
- Project name: "fitness-tracker"

**Step 2: Load Memory**
- No memory exists for "fitness-tracker" — first-time use
- Continue with empty memory

**Step 3: Load Context**
- Load engineering domain context for React Native patterns
- Note Phosphor's weight variant system for active/inactive states

**Step 4: Map Concepts to Icons**
- **Home** → `House` (primary), alternatives: `HouseSimple`, `HouseLine`
  - Rationale: House is the universal home screen metaphor
- **Workouts** → `Barbell` (primary), alternatives: `PersonSimpleRun`, `Dumbbell`
  - Rationale: Barbell is immediately recognizable as exercise/fitness
- **Progress** → `ChartLineUp` (primary), alternatives: `TrendUp`, `ChartBar`
  - Rationale: Upward trend line communicates progress and improvement
- **Profile** → `UserCircle` (primary), alternatives: `User`, `IdentificationCard`
  - Rationale: Circle-framed user icon is the standard profile indicator
- **Timer** → `Timer` (primary), alternatives: `Clock`, `Stopwatch`
  - Rationale: Timer icon with indicator is specific to timed activities
- **Heart Rate** → `Heartbeat` (primary), alternatives: `Heart`, `Activity`
  - Rationale: Heart with pulse line directly represents heart rate monitoring
- **Calories** → `Fire` (primary), alternatives: `Lightning`, `Flame`
  - Rationale: Fire/flame is the universal symbol for calories burned
- **Steps** → `Footprints` (primary), alternatives: `PersonSimpleWalk`, `SneakerMove`
  - Rationale: Footprints directly represent step tracking

**Step 5: Generate Integration Code**
- Install: `npx expo install phosphor-react-native react-native-svg`
- Generate tab bar with weight variants for active/inactive states:
  ```jsx
  import {
    House,
    Barbell,
    ChartLineUp,
    UserCircle,
  } from 'phosphor-react-native';

  const tabs = [
    { name: 'Home', icon: House },
    { name: 'Workouts', icon: Barbell },
    { name: 'Progress', icon: ChartLineUp },
    { name: 'Profile', icon: UserCircle },
  ];

  function TabBar({ activeTab }) {
    return (
      <View style={styles.tabBar}>
        {tabs.map(({ name, icon: Icon }) => (
          <Pressable key={name} style={styles.tab}>
            <Icon
              size={24}
              weight={activeTab === name ? 'fill' : 'regular'}
              color={activeTab === name ? '#6366F1' : '#9CA3AF'}
            />
            <Text style={activeTab === name ? styles.activeLabel : styles.label}>
              {name}
            </Text>
          </Pressable>
        ))}
      </View>
    );
  }
  ```
- Generate in-screen stat cards with consistent styling:
  ```jsx
  import { Timer, Heartbeat, Fire, Footprints } from 'phosphor-react-native';

  const stats = [
    { label: 'Timer', icon: Timer, value: '32:15', unit: 'min' },
    { label: 'Heart Rate', icon: Heartbeat, value: '142', unit: 'bpm' },
    { label: 'Calories', icon: Fire, value: '487', unit: 'kcal' },
    { label: 'Steps', icon: Footprints, value: '8,432', unit: 'steps' },
  ];

  function StatCard({ label, icon: Icon, value, unit }) {
    return (
      <View style={styles.card}>
        <Icon size={28} weight="duotone" color="#6366F1" />
        <Text style={styles.value}>{value}</Text>
        <Text style={styles.unit}>{unit}</Text>
      </View>
    );
  }
  ```

**Step 6: Optimize for Production**
- Phosphor React Native uses named exports — tree-shaking eliminates unused icons automatically
- Only 8 icons imported across 2 files — estimated bundle addition: ~4 KB
- For larger icon sets, recommend dynamic imports with `React.lazy`:
  ```jsx
  const LazyIcon = React.lazy(() =>
    import('phosphor-react-native').then(mod => ({ default: mod.Barbell }))
  );
  ```
- Weight variants share the same SVG path data, so switching between `regular` and `fill` adds no extra bundle cost

**Step 7: Generate Output**
- Saved to `/claudedocs/icon-design_fitness-tracker_2025-07-15.md`

**Step 8: Update Memory**
- Created `memory/skills/icon-design/fitness-tracker/icon_mappings.md`:
  - 8 concept-to-icon mappings with weight variant usage notes
  - Tab bar icons: `fill` (active) / `regular` (inactive)
  - In-screen icons: `duotone` weight
- Created `memory/skills/icon-design/fitness-tracker/library_preferences.md`:
  - Library: Phosphor React Native
  - Tab bar size: 24px
  - In-screen size: 28px
  - Active color: `#6366F1` (indigo)
  - Inactive color: `#9CA3AF` (gray)
  - Weight system: fill/regular for navigation, duotone for stats

### Sample Output

```
✓ Set up Phosphor React Native with expo compatibility
✓ Mapped 8 fitness concepts to icons with alternatives
✓ Generated tab bar component with fill/regular weight toggling
✓ Generated stat card component with duotone weight
✓ Bundle impact: ~4 KB (8 icons, tree-shaken)

Memory saved for project 'fitness-tracker' — icon system documented for consistency.
```

---

## Common Patterns

Across all examples, the skill follows these patterns:

1. **Library recommendation**: When no preference exists, recommend based on framework compatibility and tree-shaking support
2. **Semantic mapping**: Every icon choice includes rationale for why it best represents the concept
3. **Alternatives**: 2–3 alternatives provided per concept for user choice
4. **Consistent styling**: Size, weight, and color conventions enforced across all icons in a project
5. **Production optimization**: Tree-shaking, sprite sheets, or dynamic imports based on project type
6. **Memory persistence**: Library preferences and icon mappings stored for future consistency
