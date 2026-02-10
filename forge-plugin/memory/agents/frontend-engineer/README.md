# Frontend Engineer Agent Memory

This directory stores project-specific memory for the @frontend-engineer agent.

## Memory Structure

### projects/
Track frontend projects, frameworks, and UI libraries:
- Angular version and configuration
- UI component library (PrimeNG, Material, etc.)
- Build tool configuration
- Target browsers and devices

### components/
Store reusable component patterns and designs:
- Component architecture patterns (smart/presentational)
- Common component implementations
- Component naming conventions
- Reusable component library

### state_management/
Record state management approaches:
- State management solution (NgRx, Signals, Services)
- Store structure and organization
- State access patterns
- Side effect management

### ui_patterns/
Maintain UI/UX patterns and design decisions:
- Design system tokens and guidelines
- Layout patterns and responsive strategies
- Accessibility implementations
- Animation and interaction patterns

## Usage

The agent will automatically create and update files in these subdirectories as it works on different projects. Each project gets its own subdirectory for isolated memory storage.
