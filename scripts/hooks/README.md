# Git Hook Templates

This directory contains template git hooks that automate dependency management and symlink verification.

## Available Hooks

### post-checkout
**Triggered after**: `git checkout`, `git clone`

**Actions**:
- Updates git submodules automatically
- Verifies symlink integrity
- Warns if symlinks are broken

### post-merge
**Triggered after**: `git pull`, `git merge`

**Actions**:
- Detects changes to `.gitmodules`
- Updates submodules when configuration changes
- Keeps dependencies in sync with remote

## Installation

Hooks are automatically installed when you run:
```bash
./scripts/setup.sh
```

Or manually:
```bash
cp scripts/hooks/* .git/hooks/
chmod +x .git/hooks/*
```

## Customization

You can disable symlink verification in `post-checkout` by commenting out the verification section if it slows down checkouts.

## Notes

- Git hooks are local and not tracked by git (they live in `.git/hooks/`)
- These templates must be copied to `.git/hooks/` to take effect
- Hooks will not run if they don't have execute permissions
