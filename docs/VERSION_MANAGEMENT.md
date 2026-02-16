# Version Management System

The Forge uses a centralized version management system built around a `VERSION` file and automated by Make.

## Quick Reference

```bash
# Show current version
make version

# Bump to specific version
make bump-version NEW_VERSION=0.3.0-alpha

# Bump major version (x.0.0)
make bump-major

# Bump minor version (x.y.0)
make bump-minor

# Bump patch version (x.y.z)
make bump-patch
```

## Version File

**Location**: `/VERSION` (repo root)

This is the single source of truth for the current version. It contains only the version number (e.g., `0.3.0-alpha`).

## Version Format

The Forge uses semantic versioning with an optional pre-release suffix:

```
MAJOR.MINOR.PATCH[-PRERELEASE]
```

Examples:
- `0.3.0-alpha` — Alpha release
- `0.3.0-beta` — Beta release
- `1.0.0` — Production release

## Automated Version Bumping

### Script: `scripts/bump-version.sh`

This script updates the version across all files in the repository:

1. Updates `VERSION` file
2. Updates `forge-plugin/.claude-plugin/plugin.json` (canonical plugin version)
3. Scans all text files and replaces old version with new version
4. Excludes `.git`, `node_modules`, and other build artifacts

### Usage

```bash
# Direct script usage
./scripts/bump-version.sh 0.3.0-alpha

# Via Makefile (recommended)
make bump-version NEW_VERSION=0.3.0-alpha
```

### Automatic Semantic Bumps

The Makefile provides convenience targets for standard semantic version bumps:

```bash
# Bump major version (0.2.0-alpha → 1.0.0-alpha)
make bump-major

# Bump minor version (0.2.0-alpha → 0.3.0-alpha)
make bump-minor

# Bump patch version (0.2.0-alpha → 0.2.1-alpha)
make bump-patch
```

## Files Updated

The version bump script updates all occurrences of the version string in:

- `VERSION` — canonical version file
- `forge-plugin/.claude-plugin/plugin.json` — plugin manifest
- All context files (`.md`)
- All agent config files (`.json`)
- All interface files (`.md`)
- All skill files (`.md`)
- All hook scripts (`.sh`)
- GitHub workflow files (`.md`)

## Workflow

### 1. Bump Version

```bash
make bump-version NEW_VERSION=0.3.0-alpha
```

### 2. Review Changes

```bash
git diff
```

### 3. Run Tests

```bash
make test
```

### 4. Commit Changes

```bash
git add -A
git commit -m "chore: bump version to 0.3.0-alpha"
```

### 5. Tag Release

```bash
git tag v0.3.0-alpha
```

### 6. Push

```bash
git push && git push --tags
```

## Makefile Targets

| Target | Description |
|--------|-------------|
| `make help` | Show all available targets |
| `make version` | Show current version |
| `make bump-version NEW_VERSION=x.y.z` | Bump to specific version |
| `make bump-major` | Increment major version |
| `make bump-minor` | Increment minor version |
| `make bump-patch` | Increment patch version |
| `make setup` | Initialize repository (submodules, symlinks) |
| `make test` | Run test suite (Layer 1) |
| `make test-full` | Run full test suite (Layer 1 + Layer 2) |
| `make test-e2e` | Run all tests including E2E |
| `make validate` | Validate plugins and symlinks |
| `make fix-symlinks` | Fix broken symlinks |
| `make clean` | Clean generated files |
| `make install` | Install plugin locally |
| `make uninstall` | Uninstall plugin |
| `make status` | Show repo status |

## Version History

| Version | Date | Notes |
|---------|------|-------|
| 0.3.0-alpha | 2026-02-13 | Added version management system, Makefile |
| 0.2.0-alpha | 2026-02-XX | Interface-driven architecture, comprehensive hooks |
| 0.1.0-alpha | 2026-01-XX | Initial release |

## Best Practices

1. **Always use the Makefile** — don't edit `VERSION` file manually
2. **Test before committing** — run `make test` after version bumps
3. **Tag releases** — every version bump should get a git tag
4. **Semantic versioning** — follow semver principles:
   - **Major** — breaking changes
   - **Minor** — new features, backwards compatible
   - **Patch** — bug fixes, no API changes
5. **Pre-release suffixes** — use `-alpha`, `-beta`, `-rc1` for pre-releases

## Troubleshooting

### Version mismatch after bump

If some files weren't updated:

```bash
# Re-run the bump script
./scripts/bump-version.sh 0.3.0-alpha

# Or manually search for old version
grep -r "0.2.0-alpha" . --exclude-dir=.git
```

### Makefile not working

Ensure you're in the repo root:

```bash
cd /path/to/forge
make help
```

### Script permission denied

Make the script executable:

```bash
chmod +x scripts/bump-version.sh
```

## Integration with CI/CD

The version management system integrates with:

- **GitHub Actions** — version checks in CI
- **Agentic Workflows** — release note generation based on version tags
- **Plugin Marketplace** — version validation for marketplace.json

See [AGENTIC_FORGE.md](../AGENTIC_FORGE.md) for release automation workflows.
