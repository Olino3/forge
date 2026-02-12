# Stitch Skills Plugin

A Claude Code plugin providing Google Labs' Stitch agent skills for design-to-code workflows, React component generation, and UI development.

## Overview

This plugin is a wrapper for the [Google Labs stitch-skills](https://github.com/google-labs-code/stitch-skills) repository, making these powerful design-to-code skills discoverable through the Forge marketplace. The plugin uses a symlink architecture to keep the upstream Google Labs code unmodified while providing seamless integration with Claude Code.

## Included Skills

### 1. **DESIGN.md Generation** (`stitch-skills:design-md`)
Analyze Stitch projects and synthesize a semantic design system into DESIGN.md files.

**Key Features**:
- Extract design tokens and patterns from Stitch projects
- Generate semantic design documentation
- Create source-of-truth for consistent screen generation

**Required Tools**: `stitch*:*`, Read, Write, web_fetch

**Use when**: Creating design systems, documenting visual language, generating new screens aligned with existing designs

---

### 2. **Prompt Enhancement** (`stitch-skills:enhance-prompt`)
Transform vague UI ideas into polished, Stitch-optimized prompts with enhanced specificity and design context.

**Key Features**:
- Enhance prompt specificity for better results
- Add UI/UX vocabulary and keywords
- Inject design system context
- Structure output for optimal generation

**Required Tools**: `stitch*:*`, Read, Write

**Use when**: Refining UI ideas, improving generation quality, preparing design prompts

---

### 3. **React Component Conversion** (`stitch-skills:react-components`)
Convert Stitch designs into modular Vite and React components using system-level networking and AST-based validation.

**Key Features**:
- Automated Stitch-to-React conversion
- Modular component structure
- Design token consistency validation
- AST-based code analysis

**Required Tools**: `stitch*:*`, Read, Write, Bash

**Use when**: Converting designs to code, building component libraries, ensuring design-code consistency

---

### 4. **Walkthrough Video Generation** (`stitch-skills:remotion`)
Generate professional walkthrough videos from Stitch projects using Remotion with smooth transitions, zooming, and text overlays.

**Key Features**:
- Automated video generation from Stitch screens
- Smooth transitions and animations
- Professional text overlays and zooming
- Showcase app flows effectively

**Required Tools**: `stitch*:*`, Read, Write, Bash

**Use when**: Creating product demos, showcasing designs, generating marketing materials

---

### 5. **shadcn/ui Integration** (`stitch-skills:shadcn-ui`)
Expert guidance for integrating and building applications with shadcn/ui components, including discovery, installation, and customization.

**Key Features**:
- Component discovery and selection
- Installation and setup guidance
- Customization best practices
- Radix UI and Base UI integration
- Tailwind CSS configuration

**Required Tools**: `shadcn*:*`, `mcp_shadcn*`, Read, Write, Bash, web_fetch

**Use when**: Building with shadcn/ui, integrating accessible components, customizing design systems

**Note**: Requires shadcn MCP server for full component discovery functionality

---

### 6. **Stitch Loop Workflow** (`stitch-skills:stitch-loop`)
Generate complete multi-page websites from a single prompt using an autonomous baton-passing loop pattern.

**Key Features**:
- Iterative website generation
- Automated file organization
- Multi-page coordination
- Validation and consistency checks

**Required Tools**: `stitch*:*`, Read, Write, Bash

**Use when**: Rapid prototyping, generating full websites, automated design-to-deployment workflows

---

## Installation

This plugin is available through the Forge marketplace:

```bash
# Add the Forge marketplace (if not already added)
/plugin marketplace add <forge-marketplace-url>

# Install the Stitch skills plugin
/plugin install stitch-skills@forge-marketplace
```

## Prerequisites

### Stitch MCP Server (Recommended)

Most skills are designed to work with the **Stitch MCP server** for optimal functionality. While skills can provide expert guidance without MCP integration, full automation requires the MCP server.

**Setup Stitch MCP Server**:
1. Install Stitch MCP server following [Google Labs documentation](https://github.com/google-labs-code/stitch-skills)
2. Configure in your `.claude/settings.json` or Claude Code MCP settings
3. Restart Claude Code to load the MCP connection

**Skills requiring Stitch MCP**: design-md, enhance-prompt, react-components, remotion, stitch-loop

### shadcn MCP Server (Optional)

The `shadcn-ui` skill benefits from the **shadcn MCP server** for component discovery and installation automation.

**Setup shadcn MCP Server**:
1. Install shadcn MCP server
2. Configure in your MCP settings
3. Skills will automatically use MCP tools when available

## Usage

Once installed, Claude Code will automatically invoke these skills based on task context. The skills are model-invoked, meaning Claude decides when to apply them.

### Manual Skill Reference

You can explicitly reference skills in your conversation:

```
"Use stitch skills to generate a DESIGN.md from my project"
"Apply shadcn-ui skill to integrate these components"
"Use stitch-loop to build a multi-page website"
```

### Skill Namespacing

Skills are namespaced to prevent conflicts:

- `stitch-skills:design-md`
- `stitch-skills:enhance-prompt`
- `stitch-skills:react-components`
- `stitch-skills:remotion`
- `stitch-skills:shadcn-ui`
- `stitch-skills:stitch-loop`

## Tool Requirements

Skills declare `allowed-tools` in their frontmatter to restrict which Claude Code tools they can use:

| Skill | Allowed Tools |
|-------|---------------|
| design-md | `stitch*:*`, Read, Write, web_fetch |
| enhance-prompt | `stitch*:*`, Read, Write |
| react-components | `stitch*:*`, Read, Write, Bash |
| remotion | `stitch*:*`, Read, Write, Bash |
| shadcn-ui | `shadcn*:*`, `mcp_shadcn*`, Read, Write, Bash, web_fetch |
| stitch-loop | `stitch*:*`, Read, Write, Bash |

These restrictions ensure skills operate within their intended scope and dependencies.

## Architecture

This plugin uses a **symlink wrapper pattern**:

```
stitch-skills-plugin/
├── .claude-plugin/
│   └── plugin.json          # Plugin manifest
├── skills/                  # Symlink → ../stitch-skills/skills
└── README.md
```

The `skills/` directory is a symlink to the Google Labs stitch-skills repository, allowing:
- ✅ No modification to upstream Google Labs code
- ✅ Easy updates via `git pull` in the stitch-skills repo
- ✅ Standard Claude Code plugin structure
- ✅ Seamless skill discovery

## Updating

To update the Stitch skills to the latest version:

```bash
cd /path/to/forge/google-labs-code/stitch-skills
git pull origin main
```

The plugin will automatically reflect the updated skills since it uses a symlink.

## Degraded Mode (Without MCP)

Skills can operate in **degraded mode** when MCP servers are not available:

- **With MCP**: Full automation, direct tool invocation, streamlined workflows
- **Without MCP**: Expert guidance, manual steps, best practices documentation

Skills will adapt based on available tools and provide the best possible assistance.

## License

Apache-2.0 - This plugin wrapper follows the same license as the Google Labs stitch-skills repository.

## Credits

Skills authored and maintained by [Google Labs](https://labs.google/).
Plugin wrapper created for the Forge marketplace.

## Links

- [Google Labs stitch-skills Repository](https://github.com/google-labs-code/stitch-skills)
- [Stitch Documentation](https://github.com/google-labs-code/stitch-skills)
- [Claude Code Documentation](https://code.claude.com/docs)
- [Forge Marketplace](https://github.com/your-org/forge)

## Related Skills

If you're working with React, also check out:
- **vercel-skills** - Vercel's React composition patterns and best practices
- **forge-plugin** - The Forge's core agent skills and commands

## Support

For issues with:
- **Stitch skills content**: Report to [google-labs-code/stitch-skills](https://github.com/google-labs-code/stitch-skills/issues)
- **Plugin integration**: Report to the Forge marketplace maintainers
- **MCP server setup**: See [MCP documentation](https://code.claude.com/docs/en/mcp)
