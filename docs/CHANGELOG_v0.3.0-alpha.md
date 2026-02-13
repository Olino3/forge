# Changelog — v0.3.0-alpha

**Release Date**: 2026-02-13

## Summary

This release introduces a centralized version management system for The Forge, making it easy to bump versions across all 184 files in the repository with a single command.

## New Features

### 1. Centralized Version Management

- **VERSION file** — Single source of truth for current version (located at repo root)
- **Automated version bumping** — Script that updates version across all files
- **Makefile integration** — Convenient Make targets for version management

### 2. Build System (Makefile)

A comprehensive Makefile with 15 targets:

| Target | Description |
|--------|-------------|
| `make help` | Show all available targets with descriptions |
| `make version` | Display current version |
| `make bump-version NEW_VERSION=x.y.z` | Bump to specific version |
| `make bump-major` | Increment major version |
| `make bump-minor` | Increment minor version |
| `make bump-patch` | Increment patch version |
| `make setup` | Initialize repository (submodules, symlinks, plugins) |
| `make test` | Run test suite (Layer 1) |
| `make test-full` | Run full test suite (Layer 1 + Layer 2) |
| `make test-e2e` | Run all tests including E2E |
| `make validate` | Validate plugins, symlinks, and hooks |
| `make fix-symlinks` | Fix broken symlinks |
| `make clean` | Clean generated files and runtime artifacts |
| `make install` | Install The Forge as a Claude Code plugin (local) |
| `make uninstall` | Uninstall The Forge plugin |
| `make status` | Show repository status |

### 3. Version Bump Script

`scripts/bump-version.sh` — Automated version bumping with:

- Version format validation (semantic versioning)
- Updates VERSION file
- Updates plugin.json (canonical plugin version)
- Scans and updates all text files in repository
- Excludes .git, node_modules, and build artifacts
- Provides colored output and next-step guidance

### 4. Documentation

- **docs/VERSION_MANAGEMENT.md** — Complete version management guide
  - Quick reference
  - Version format specification
  - Automated bump workflows
  - List of all files updated
  - Best practices
  - Troubleshooting guide
  - CI/CD integration notes

## Files Updated

This release bumped the version from `0.2.0-alpha` to `0.3.0-alpha` in **184 files**:

- `VERSION` — new file, canonical version source
- `forge-plugin/.claude-plugin/plugin.json`
- `CLAUDE.md`
- All 81 context files
- All 19 agent config files
- All interface adapter files
- All skill documentation files
- All hook scripts
- GitHub workflow files
- Memory index files
- Templates

## Breaking Changes

None. This is a purely additive release focused on developer experience improvements.

## Migration Guide

No migration required. The new version management system is opt-in and does not affect existing workflows.

## Developer Experience Improvements

1. **Single command version bumps** — `make bump-minor` instead of manual find/replace
2. **Semantic versioning shortcuts** — `bump-major`, `bump-minor`, `bump-patch`
3. **Validation before commit** — `make test` runs full test suite
4. **Status overview** — `make status` shows version, git branch, submodules, symlinks
5. **Consistent workflows** — All common operations now available via `make`

## Testing

All changes verified with:
- Layer 1 tests: ✅ Pass
- Version consistency check: ✅ 184 files updated to 0.3.0-alpha
- Makefile targets: ✅ All 15 targets functional
- Symlink validation: ✅ All symlinks healthy

## Next Steps

For the next release, consider:
1. Adding `make release` target that combines test + commit + tag + push
2. GitHub Actions workflow to validate VERSION file matches plugin.json
3. Automated changelog generation from commit messages
4. Version pinning for external skill submodules

## References

- [docs/VERSION_MANAGEMENT.md](VERSION_MANAGEMENT.md) — Version management guide
- [CLAUDE.md](../CLAUDE.md) — Updated to reflect v0.3.0-alpha
- [README.md](../README.md) — Added Build System section
- [Makefile](../Makefile) — New build system
- [scripts/bump-version.sh](../scripts/bump-version.sh) — Version bump script

---

**Contributors**: Olin Osborne III
**Commit**: `chore: bump version to 0.3.0-alpha`
**Tag**: `v0.3.0-alpha`
