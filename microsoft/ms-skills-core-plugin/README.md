# Microsoft Core Skills Plugin

A Claude Code plugin providing Microsoft's core skills for Azure deployment, MCP server development, GitHub integration, and skill creation. Language-agnostic tooling and infrastructure skills.

## Overview

This plugin is a wrapper for the core (language-agnostic) skills from the [Microsoft skills repository](https://github.com/microsoft/skills), making these essential infrastructure and tooling skills discoverable through the Forge marketplace.

## Included Skills

### 1. **Azure Developer CLI Deployment** (`ms-skills-core:azd-deployment`)
Deploy to Azure Container Apps with Azure Developer CLI (azd). Bicep infrastructure, remote builds, multi-service deployments.

**Use when**: Deploying applications to Azure, setting up infrastructure, container deployments

---

### 2. **Copilot SDK** (`ms-skills-core:copilot-sdk`)
Build applications powered by GitHub Copilot using the Copilot SDK. Session management, custom tools, streaming, hooks, MCP servers, BYOK.

**Use when**: Building Copilot-powered applications, creating custom tools, integrating MCP servers

---

### 3. **GitHub Issue Creator** (`ms-skills-core:github-issue-creator`)
Convert raw notes, error logs, or screenshots into structured GitHub issues.

**Use when**: Creating issues from logs, converting notes to issues, automating issue creation

---

### 4. **MCP Builder** (`ms-skills-core:mcp-builder`)
Build MCP servers for LLM tool integration. Python (FastMCP), Node/TypeScript, or C#/.NET.

**Use when**: Creating MCP servers, building custom tools, extending LLM capabilities

---

### 5. **Podcast Generation** (`ms-skills-core:podcast-generation`)
Generate podcast-style audio with Azure OpenAI Realtime API. Full-stack React + FastAPI + WebSocket.

**Use when**: Creating audio content, building podcast features, using Realtime API

---

### 6. **Skill Creator** (`ms-skills-core:skill-creator`)
Guide for creating effective skills for AI coding agents.

**Use when**: Creating new skills, documenting patterns, designing agent capabilities

---

## Installation

This plugin is available through the Forge marketplace:

```bash
# Install the Microsoft core skills plugin
/plugin install ms-skills-core@forge-marketplace
```

## Recommended Companion Plugins

Pair with language-specific Microsoft skills for full Azure SDK coverage:

- **ms-skills-python** - Azure SDK for Python (41 skills)
- **ms-skills-dotnet** - Azure SDK for .NET (29 skills)
- **ms-skills-typescript** - Azure SDK for TypeScript (24 skills)
- **ms-skills-java** - Azure SDK for Java (26 skills)
- **ms-skills-rust** - Azure SDK for Rust (7 skills)
- **ms-agents** - Microsoft custom agents and deep-wiki plugin

## Usage

Once installed, Claude Code will automatically use these skills when appropriate based on task context.

### Manual Skill Reference

You can explicitly reference skills in your conversation:

```
"Use azd to deploy this to Azure"
"Create an MCP server for this tool"
"Convert these notes into a GitHub issue"
```

### Skill Namespacing

Skills are namespaced to prevent conflicts:

- `ms-skills-core:azd-deployment`
- `ms-skills-core:copilot-sdk`
- `ms-skills-core:github-issue-creator`
- `ms-skills-core:mcp-builder`
- `ms-skills-core:podcast-generation`
- `ms-skills-core:skill-creator`

## Architecture

This plugin uses a **symlink wrapper pattern**:

```
ms-skills-core-plugin/
├── .claude-plugin/
│   └── plugin.json          # Plugin manifest
├── skills/                  # Symlinks → ../skills/.github/skills
│   ├── azd-deployment
│   ├── copilot-sdk
│   ├── github-issue-creator
│   ├── mcp-builder
│   ├── podcast-generation
│   └── skill-creator
└── README.md
```

The `skills/` directory contains symlinks to individual skills in the Microsoft repository, allowing:
- ✅ No modification to upstream Microsoft code
- ✅ Easy updates via `git pull` in the skills repo
- ✅ Standard Claude Code plugin structure
- ✅ Seamless skill discovery

## Updating

To update the Microsoft skills to the latest version:

```bash
cd /path/to/forge/microsoft/skills
git pull origin main
```

The plugin will automatically reflect the updated skills since it uses symlinks.

## License

MIT - This plugin wrapper follows the same license as the Microsoft skills repository.

## Credits

Skills authored and maintained by [Microsoft](https://github.com/microsoft).
Plugin wrapper created for the Forge marketplace.

## Links

- [Microsoft Skills Repository](https://github.com/microsoft/skills)
- [Microsoft Skills Documentation](https://microsoft.github.io/skills/)
- [Azure Developer CLI](https://learn.microsoft.com/azure/developer/azure-developer-cli/)
- [Claude Code Documentation](https://code.claude.com/docs)
- [Forge Marketplace](https://github.com/your-org/forge)

## Support

For issues with:
- **Skill content**: Report to [microsoft/skills](https://github.com/microsoft/skills/issues)
- **Plugin integration**: Report to the Forge marketplace maintainers
- **Azure services**: See [Azure Documentation](https://learn.microsoft.com/azure/)
