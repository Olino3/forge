# Vercel Agent Skills Plugin

A Claude Code plugin providing Vercel's agent skills for React, React Native, composition patterns, and web design guidelines.

## Overview

This plugin is a wrapper for the [Vercel agent-skills](https://github.com/vercel/agent-skills) repository, making these high-quality skills discoverable through the Forge marketplace. The plugin uses a symlink architecture to keep the upstream Vercel code unmodified while providing seamless integration with Claude Code.

## Included Skills

### 1. **React Composition Patterns** (`vercel-skills:composition-patterns`)
React composition patterns that scale. Covers:
- Component architecture best practices
- Avoiding boolean prop proliferation
- Compound components with shared context
- State management patterns
- React 19 API updates

### 2. **React Best Practices** (`vercel-skills:react-best-practices`)
Comprehensive React development guidelines including:
- Component design principles
- Performance optimization
- State management
- Testing strategies
- Modern React patterns

### 3. **React Native Skills** (`vercel-skills:react-native-skills`)
React Native development best practices:
- Mobile-specific patterns
- Platform considerations
- Performance optimization
- Native module integration

### 4. **Web Design Guidelines** (`vercel-skills:web-design-guidelines`)
Design system and UI/UX patterns:
- Design system principles
- Accessibility guidelines
- Visual design patterns
- Component library design

### 5. **Claude.ai Patterns** (`vercel-skills:claude.ai`)
Patterns specific to Claude.ai integration and AI-assisted development.

## Installation

This plugin is available through the Forge marketplace:

```bash
# Add the Forge marketplace (if not already added)
/plugin marketplace add <forge-marketplace-url>

# Install the Vercel skills plugin
/plugin install vercel-skills@forge-marketplace
```

## Usage

Once installed, Claude Code will automatically use these skills when appropriate based on your task context. The skills are model-invoked, meaning Claude decides when to apply them.

To reference a specific skill in your conversation, you can mention it by name:
- "Use vercel composition patterns..."
- "Apply React best practices..."
- "Follow Vercel's design guidelines..."

## Architecture

This plugin uses a **symlink wrapper pattern**:

```
vercel-skills-plugin/
├── .claude-plugin/
│   └── plugin.json          # Plugin manifest
├── skills/                  # Symlink → ../agent-skills/skills
└── README.md
```

The `skills/` directory is a symlink to the Vercel agent-skills repository, allowing:
- ✅ No modification to upstream Vercel code
- ✅ Easy updates via `git pull` in the agent-skills repo
- ✅ Standard Claude Code plugin structure
- ✅ Seamless skill discovery

## Updating

To update the Vercel skills to the latest version:

```bash
cd /path/to/forge/vercel/agent-skills
git pull origin main
```

The plugin will automatically reflect the updated skills since it uses a symlink.

## License

MIT - This plugin wrapper follows the same license as the Vercel agent-skills repository.

## Credits

Skills authored and maintained by [Vercel](https://vercel.com).
Plugin wrapper created for the Forge marketplace.

## Links

- [Vercel agent-skills Repository](https://github.com/vercel/agent-skills)
- [Claude Code Documentation](https://code.claude.com/docs)
- [Forge Marketplace](https://github.com/your-org/forge)
