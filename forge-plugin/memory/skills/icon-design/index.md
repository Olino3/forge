# Memory Structure: icon-design

## Purpose

This directory stores **project-specific** icon mappings, library preferences, and styling conventions learned during icon selection sessions. Each project gets its own subdirectory to maintain consistent icon usage across multiple sessions.

## Conceptual Overview

### Memory vs Context

- **Context** (`../../../context/engineering/`): **Shared, static** frontend engineering knowledge (frameworks, patterns, best practices)
- **Memory** (this directory): **Project-specific, dynamic** icon selections (which icons map to which concepts, library choice, sizing conventions)

**Example**:
- Context says: "Use named imports from Lucide for tree-shaking"
- Memory records: "In this project, Dashboard maps to `LayoutDashboard`, icons are 20px with stroke-width 1.75, using Tailwind `text-gray-500`"

## Directory Structure

```
icon-design/
├── index.md                      # This file - explains memory structure
└── {project-name}/               # Per-project memory (created on first use)
    ├── icon_mappings.md          # Concept-to-icon associations
    └── library_preferences.md   # Library choice, sizing, and styling
```

## Memory Files

### 1. `icon_mappings.md`

**What to store**:
- UI concept to icon name mappings
- The library each icon comes from
- Import path or component name
- Rationale for the selection
- Date the mapping was established

**When created**: First time icons are selected for a project

**When updated**: Each time new icons are added or existing mappings are changed

**Example content**:
```markdown
# Icon Mappings for saas-dashboard

## Active Mappings

| Concept | Icon | Library | Import | Date |
|---------|------|---------|--------|------|
| Dashboard | LayoutDashboard | Lucide | lucide-react | 2025-07-15 |
| Analytics | BarChart3 | Lucide | lucide-react | 2025-07-15 |
| Users | Users | Lucide | lucide-react | 2025-07-15 |
| Settings | Settings | Lucide | lucide-react | 2025-07-15 |
| Notifications | Bell | Lucide | lucide-react | 2025-07-15 |
| Billing | CreditCard | Lucide | lucide-react | 2025-07-15 |
| Help | HelpCircle | Lucide | lucide-react | 2025-07-15 |

## Replaced Mappings

| Concept | Old Icon | New Icon | Reason | Date |
|---------|----------|----------|--------|------|
```

### 2. `library_preferences.md`

**What to store**:
- Chosen icon library and version
- Default icon size (px)
- Stroke width or weight variant
- Color scheme (active, inactive, disabled states)
- Style variant (outline, solid, duotone)
- Framework integration approach (named imports, SVG sprites, CDN)

**When created**: First time an icon library is chosen for a project

**When updated**: When styling conventions change or new contexts are established (e.g., dark mode)

**Example content**:
```markdown
# Library Preferences for fitness-tracker

## Library
- **Name**: Phosphor React Native
- **Package**: phosphor-react-native
- **Version**: ^2.0.0

## Sizing
- **Tab bar icons**: 24px
- **In-screen icons**: 28px
- **Small inline icons**: 16px

## Weight / Style
- **Navigation active**: fill
- **Navigation inactive**: regular
- **Stats / dashboard**: duotone
- **Form labels**: light

## Colors
- **Active**: #6366F1 (indigo-500)
- **Inactive**: #9CA3AF (gray-400)
- **Disabled**: #D1D5DB (gray-300)
- **Destructive**: #EF4444 (red-500)

## Integration
- Named imports for tree-shaking
- Expo-compatible via react-native-svg
```

## Why This Skill Needs Memory

Icon consistency is critical for user experience. Without memory:
- The same concept could get different icons across sessions
- Sizing and color conventions would need to be re-specified every time
- Library choices would be re-evaluated unnecessarily
- Visual inconsistencies would accumulate as the project grows

With memory:
- **Consistency**: Every session reuses established icon mappings
- **Speed**: Library preferences are loaded instantly without re-detection
- **Growth**: New icon selections are additive, building a complete icon system
- **Auditability**: The full history of icon choices and replacements is tracked

## Memory Growth Pattern

### First Session
- Choose icon library based on project framework
- Map initial set of concepts to icons
- Establish sizing, weight, and color conventions

### Subsequent Sessions
- Load existing mappings to avoid conflicts
- Add new concept-to-icon mappings
- Reuse established conventions for consistency
- Update any mappings that the user wants to change

### Maintenance
- Archive replaced mappings with rationale
- Update library version when upgraded
- Add new style contexts (dark mode, compact view) as they emerge

## Related Files

- `../../../skills/icon-design/SKILL.md` - Skill definition and workflow
- `../../../skills/icon-design/examples.md` - Usage examples
- `/claudedocs/icon-design_{project}_{date}.md` - Session output reports
- `../../index.md` - Overall memory system explanation
