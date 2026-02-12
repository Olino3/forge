# Commands Documentation Directory

This directory contains usage examples for all Forge slash commands.

## Purpose

While command definitions live as flat `.md` files in the parent directory (following Claude Code plugin conventions), this directory preserves the detailed usage examples for documentation purposes.

## Structure

Each command has a corresponding `-examples.md` file:

- `analyze-examples.md` - Examples for `/analyze` command
- `implement-examples.md` - Examples for `/implement` command
- `improve-examples.md` - Examples for `/improve` command
- etc.

## Why This Structure?

Claude Code auto-discovers slash commands from flat `.md` files in the `commands/` directory:

- `commands/analyze.md` → `/analyze` command
- `commands/implement.md` → `/implement` command

Subdirectories in `commands/` would be treated as namespaces (e.g., `commands/analyze/COMMAND.md` → `/commands:analyze` or `/forge-plugin:command:analyze`), which creates duplicate/unwanted commands.

This `_docs/` directory (prefixed with underscore) is ignored by Claude Code's command discovery mechanism, allowing us to maintain organized documentation without interfering with command registration.

## Related Files

- Main command definitions: `../analyze.md`, `../implement.md`, etc.
- Command index: `../index.md`
