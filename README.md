# ⚒️ The Forge ⚒️

> *"As Hephaestus crafted divine weapons for the gods, so too does the Forge craft tools for mortal developers."*

<div align="center">

🔥 **Welcome to the Forge** 🔥

*A divine marketplace where Claude Code plugins are forged in the fires of innovation*

[![Marketplace](https://img.shields.io/badge/Claude_Code-Marketplace-blueviolet?style=for-the-badge&logo=data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjQiIGhlaWdodD0iMjQiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PHBhdGggZD0iTTEyIDJMMiA3djEwbDEwIDVsMTAtNVY3TDEyIDJ6IiBmaWxsPSIjZmZmIi8+PC9zdmc+)](https://github.com/Olino3/forge)
[![Forged in Shell](https://img.shields.io/badge/Forged_in-Shell-success?style=for-the-badge&logo=gnu-bash)](https://github.com/Olino3/forge)
[![Open Source](https://img.shields.io/badge/Open-Source-orange?style=for-the-badge&logo=github)](https://github.com/Olino3/forge)

</div>

---

## 🏛️ The Legend

In the depths of Mount Olympus, Hephaestus toiled at his anvil, forging legendary artifacts that would shape the fate of gods and mortals alike. The **Forge** carries on this sacred tradition—a curated, versioned registry of plugins that you can discover and install directly from Claude Code.

⚡ **Forged in Shell** • Simple to host, inspect, and extend  
🔨 **Battle-tested** • Curated plugins ready for production  
✨ **Ever-evolving** • New tools added by the community

---

## 🛠️ Wielding the Divine Tools

Learn how to discover, install, and manage plugins to extend your Claude Code capabilities using the Forge as your marketplace.

### 📜 Prerequisites

Before entering the Forge, ensure you have:

- ✅ **Claude Code** installed and running  
- 🎯 **Basic CLI knowledge** to wield the command line  
- 🔗 **Repository access**: [Olino3/forge](https://github.com/Olino3/forge)

---

## 🔥 Ignite the Forge

Marketplaces are sacred catalogs where divine tools await discovery. Add the Forge to unlock its treasures.

### ⚡ Summon the Marketplace

Light the flames of the Forge in Claude Code:

```bash
/plugin marketplace add Olino3/forge
```

💡 **Alternative Invocation**: If your setup requires a direct registry path:

```bash
/plugin marketplace add https://raw.githubusercontent.com/Olino3/forge/main/registry.json
```

> ⚠️ **Note**: Adjust `registry.json` and path to match the actual manifest in this repository.

### 👁️ Behold the Arsenal

Once the Forge burns bright in your marketplaces, gaze upon its offerings:

```bash
/plugin
```

This invokes the sacred plugin management interface, where the Forge's divine creations await your selection alongside tools from other marketplaces.

📚 **Master's Grimoire**: For advanced forge mastery—including Git repositories, local development, and team distribution—consult the official Claude Code documentation on **Plugin Marketplaces**.

---

## ⚒️ Forge Your Toolkit

Choose your path: wander the halls of discovery or command the flames directly.

### 🗺️ Path of Discovery (Recommended for Exploration)

Enter the sacred halls:

```bash
/plugin
```

**Your Quest**:

1. 🔍 Select **"Browse Plugins"**  
2. 📖 Behold the artifacts with their divine descriptions and powers  
3. ⚡ Choose your tool and follow Hephaestus's guidance to claim it  

### ⚡ Path of Command (For Swift Forging)

Master smiths command the flames directly:

#### 🔨 Forge a Specific Tool

```bash
/plugin install forge-plugin@Olino3/forge
```

#### ✨ Rekindle a Dormant Tool

```bash
/plugin enable forge-plugin@Olino3/forge
```

#### 💤 Rest a Tool (Without Destroying)

```bash
/plugin disable forge-plugin@Olino3/forge
```

#### 🔥 Return to the Flames

```bash
/plugin uninstall forge-plugin@Olino3/forge
```

---

## ✅ Verify Your Craftsmanship

After forging a new tool, ensure it's tempered properly:

### 1. 📋 **Inspect Your New Powers**

Reveal what Hephaestus has bestowed:
```bash
/help
```

Seek new commands or abilities granted by your artifact.

### 2. 🧪 **Test in the Crucible**

Wield the tool as intended—consult its sacred scrolls (documentation) within the Forge or its own repository.

### 3. 🔍 **Divine Audit**

Survey your complete arsenal:

```bash
/plugin
```

Select **"Manage Plugins"** to witness:

- ⚔️ All installed artifacts  
- 🏛️ Their origin (Forge or other marketplaces)  
- ⚡ Power to enable/disable or banish them

---

## 🏗️ The Forge's Architecture

Behold the sacred structure where divine tools are born:

```text
🏛️ forge/
├─ 🔮 .claude/                    # Claude's divine configurations
│   └─ settings.local.json        # Local settings for the forge
├─ 📦 .claude-plugin/             # Marketplace registry
│   └─ marketplace.json           # Sacred catalog of available plugins
├─ ⚒️ forge-plugin/               # The main forge workshop
│   ├─ .claude-plugin/            # Plugin manifest
│   │   └─ plugin.json            # Plugin definition
│   └─ skills/                    # Arsenal of divine skills
│       ├─ get-git-diff/          # Git diff analysis tool
│       │   ├─ context/           # Knowledge scrolls
│       │   ├─ memory/            # Pattern libraries
│       │   ├─ scripts/           # Shell utilities
│       │   ├─ templates/         # Output templates
│       │   ├─ examples.md        # Usage examples
│       │   └─ SKILL.md           # Skill documentation
│       └─ python-code-review/    # Python review expert
│           ├─ context/           # Security & standards
│           ├─ memory/            # Framework patterns
│           ├─ templates/         # Review templates
│           ├─ examples.md        # Review scenarios
│           └─ SKILL.md           # Skill documentation
├─ 📜 CLAUDE.md                   # Divine instructions for Claude
├─ 🛡️ .gitignore                  # Protected artifacts
└─ � README.md                   # This divine manuscript
```

> 🔍 **Explore**: Each skill in the forge contains specialized knowledge and tools for specific tasks. The `.claude-plugin` directories define the marketplace and plugin structures for Claude Code.

---

## 🎁 Contribute to the Forge

Join Hephaestus's workshop! Forge new tools for the community:

### 📝 The Sacred Ritual

1. 🍴 **Fork** [Olino3/forge](https://github.com/Olino3/forge)  
2. ⚒️ **Add your plugin** to the `marketplace.json`  
3. 📤 **Open a pull request** with:
   - ✨ Plugin name and divine purpose  
   - 📖 Clear description of powers granted  
   - 💡 Example usage: `/plugin install ...`, commands, etc.

---

## 📜 License

The divine laws governing this forge can be found in the `LICENSE` scroll in the repository root. If no license is inscribed, consider all works protected until divine decree is made.

---

## 🆘 Seek Guidance

Should you encounter obstacles in your quest:

### 🐛 Report Issues

Open an issue in [Olino3/forge/issues](https://github.com/Olino3/forge/issues) with:

- ⚡ The exact `/plugin` incantations you used  
- 🔢 Your Claude Code version  
- 📋 Error messages or divine omens (logs)  

### 🤝 Contribute Solutions

Or become a fellow smith—contribute fixes via pull request!

---

<div align="center">

**⚒️ May your code be as strong as Hephaestus's hammer ⚒️**

*Forged with 🔥 by the community*

</div>
