# Troubleshooting Guide

Common issues and solutions for The Forge dependency management system.

---

## Broken Symlinks After Clone

**Symptom**: Plugins fail to load, symlink errors in logs

**Cause**: Cloned without `--recursive` flag, external repositories missing

**Solution**:
```bash
# Initialize submodules and fix symlinks
./scripts/setup.sh

# Or manually:
git submodule update --init --recursive
./scripts/fix-symlinks.sh
```

---

## Submodules Not Initializing

**Symptom**: `git submodule update` fails or does nothing

**Solution 1** - Force update:
```bash
git submodule update --init --recursive --force
```

**Solution 2** - Clean and reinitialize:
```bash
git submodule foreach --recursive git clean -xfd
git submodule update --init --recursive
```

**Solution 3** - Manual clone (if all else fails):
```bash
# Remove broken submodules
rm -rf vercel/ google-labs-code/ microsoft/ sentry-team/ trailofbits/

# Re-run setup
./scripts/setup.sh
```

---

## Plugins Not Loading in Claude Code

**Symptom**: Installed plugins don't appear in Claude Code

**Check 1** - Validate marketplace:
```bash
claude plugin validate .
```

**Check 2** - Verify symlinks:
```bash
./scripts/verify-symlinks.sh
```

**Check 3** - Check plugin paths:
```bash
# Ensure submodules exist
git submodule status

# Should show 5 submodules with commit hashes
```

**Solution** - Rebuild symlinks:
```bash
./scripts/fix-symlinks.sh
```

---

## Permission Denied on Scripts

**Symptom**: `./scripts/setup.sh: Permission denied`

**Solution**:
```bash
# Make scripts executable
chmod +x scripts/*.sh
chmod +x scripts/hooks/*

# Run setup
./scripts/setup.sh
```

---

## Git Submodule Shows "no submodule mapping found"

**Symptom**: Error when running `git submodule update`

**Cause**: `.gitmodules` file corrupted or missing

**Solution**:
```bash
# Check .gitmodules exists and is valid
cat .gitmodules

# Should show 5 submodule entries
# If missing, you need to re-clone the repository:
cd ..
git clone --recursive https://github.com/Olino3/forge.git
```

---

## Symlinks Show as Modified in Git

**Symptom**: `git status` shows symlinks as modified

**Cause**: Git treating symlinks as files (Windows or misconfigured Git)

**Solution**:
```bash
# Configure Git to track symlinks properly
git config core.symlinks true

# Reset repository
git reset --hard HEAD
```

---

## Submodule Update Says "Already up to date"

**Symptom**: External repos not updating even after upstream changes

**Explanation**: Submodules are pinned to specific commits by design

**To Update External Repos**:
```bash
# Update all submodules to their latest main branch
git submodule update --remote

# Commit the updated submodule references
git add vercel/ google-labs-code/ microsoft/ sentry-team/ trailofbits/
git commit -m "chore: update external skill repositories"
```

---

## Claude Code Says Plugin Invalid

**Symptom**: `claude plugin validate .` fails

**Common Causes**:
1. Broken symlinks → Run `./scripts/fix-symlinks.sh`
2. Missing plugin.json → Check wrapper plugin directories exist
3. Invalid JSON → Validate JSON syntax in marketplace.json

**Debug Steps**:
```bash
# 1. Verify submodules
git submodule status

# 2. Verify symlinks
./scripts/verify-symlinks.sh

# 3. Check individual plugin
cd vercel/vercel-skills-plugin
claude plugin validate .

# 4. Validate marketplace
cd /root/forge
claude plugin validate .
```

---

## Microsoft Plugin Symlinks Incomplete

**Symptom**: Only some Microsoft skills load

**Cause**: Incomplete symlink creation for language-specific plugins

**Solution**:
```bash
# Recreate all Microsoft symlinks
./scripts/fix-symlinks.sh

# Verify count
find microsoft/ -type l | wc -l
# Should show ~258 symlinks across 7 plugins
```

---

## Getting Help

If none of these solutions work:

1. **Check logs**: Look for error messages in Claude Code
2. **Verify environment**: Ensure you're on Linux/macOS (Windows requires WSL)
3. **Clean slate**: Delete forge directory, re-clone with `--recursive`
4. **Report issue**: Open GitHub issue with error output

---

## Prevention

To avoid issues in the future:

✅ **Always clone with `--recursive`**:
```bash
git clone --recursive https://github.com/Olino3/forge.git
```

✅ **Run setup after clone**:
```bash
cd forge && ./scripts/setup.sh
```

✅ **Install git hooks** (automated via setup.sh):
```bash
# Hooks auto-update submodules on checkout/merge
cp scripts/hooks/* .git/hooks/
chmod +x .git/hooks/*
```

---

*For setup instructions, see [SETUP.md](SETUP.md)*
