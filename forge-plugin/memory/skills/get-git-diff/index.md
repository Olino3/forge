# get-git-diff Memory

Project-specific memory for git diff analysis patterns, commit conventions, and change history.

## Purpose

This memory helps the `skill:get-git-diff` remember:
- Which files/areas change frequently in each project
- Project-specific commit message conventions
- Typical merge and branch strategies
- Common change patterns and groupings

## Memory Files Per Project

Each project gets its own directory: `{project-name}/`

### Recommended Files

#### `common_patterns.md`

**Purpose**: Track recurring change patterns specific to this project

**Should contain**:
- **Hotspot files**: Files that appear in most commits (>50%)
- **Change groupings**: Files typically modified together
- **Change sizes**: Typical commit sizes and what they indicate
- **Active areas**: Current focus areas of development
- **File categories**: How the project groups related files

**Example structure**:
```markdown
# Common Patterns - MyProject

## Hotspot Files
- `src/api/routes.py` - Modified in 85% of commits
- `tests/test_api.py` - Always updated with route changes
- `CHANGELOG.md` - Updated with each release

## Typical Change Groups
Backend feature commits usually include:
- Route definition file
- Service layer file
- Schema/model file
- Test file
- Documentation update

Frontend commits typically include:
- Component file
- Styles file
- Test file

## Change Size Patterns
- **Small** (1-5 files, <100 lines): Bug fixes, minor features (70%)
- **Medium** (5-15 files, 100-500 lines): Features, refactoring (25%)
- **Large** (15+ files, 500+ lines): Major features, migrations (5%)

## Active Development Areas (Last 30 days)
- `/src/api/v2/` - New API version being built
- `/src/integrations/` - Third-party integrations
- `/tests/integration/` - Test coverage improvements
```

**When to update**: After each diff analysis, if new patterns emerge

---

#### `commit_conventions.md`

**Purpose**: Document project's commit message format and conventions

**Should contain**:
- **Message format**: Structure (Conventional Commits, custom, free-form)
- **Type prefixes**: Common types (feat, fix, docs, etc.) and their meanings
- **Scope usage**: How scopes are defined and used
- **Issue references**: Format for linking commits to issues/tickets
- **Breaking changes**: How breaking changes are indicated
- **Co-authorship**: How multiple authors are credited

**Example structure**:
```markdown
# Commit Conventions - MyProject

## Message Format
Project uses Conventional Commits with custom scopes:

```
<type>(<scope>): <subject>

[optional body]

[optional footer]
```

## Common Types
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `style`: Code style changes (no logic change)
- `refactor`: Code restructuring
- `perf`: Performance improvement
- `test`: Adding/updating tests
- `chore`: Build process, dependencies, tooling

## Scopes
- `api`: API endpoints and routes
- `db`: Database models and migrations
- `auth`: Authentication/authorization
- `ui`: User interface components
- `tests`: Test infrastructure

## Issue References
Always reference issue in footer:
```
Closes #123
Relates to #456
```

## Breaking Changes
Indicated in footer:
```
BREAKING CHANGE: API endpoint /users now requires authentication
```

## Recent Examples
- `feat(api): add pagination to users endpoint`
- `fix(auth): resolve token expiration bug (#789)`
- `docs: update API documentation for v2`
```

**When to update**: When new conventions are observed or old ones change

---

#### `merge_patterns.md`

**Purpose**: Track merge strategies and branch patterns

**Should contain**:
- **Merge strategy**: Merge commits, squash, rebase
- **Branch naming**: Conventions for feature/fix/release branches
- **Conflict patterns**: Common conflict areas
- **Release process**: How releases are prepared and tagged
- **Branch lifecycle**: How branches are created, merged, deleted

**Example structure**:
```markdown
# Merge Patterns - MyProject

## Merge Strategy
- **Feature branches**: Squash merge to `main`
- **Hotfix branches**: Merge commit to `main` and backport to `release/*`
- **Release branches**: Merge commit to `main`, tag, then delete

## Branch Naming
- `feature/ABC-123-short-description` - Feature branches (ticket-based)
- `fix/issue-456-bug-description` - Bug fix branches
- `release/v1.2.0` - Release preparation branches
- `hotfix/critical-security-patch` - Emergency fixes

## Common Conflict Areas
- `src/config/settings.py` - Often has conflicts due to parallel features
- `package.json` / `requirements.txt` - Dependency conflicts common
- Database migration files - Sequential numbering causes conflicts

## Release Process
1. Create `release/vX.Y.Z` branch from `main`
2. Update version numbers and CHANGELOG
3. Run full test suite and QA
4. Merge to `main` with merge commit
5. Tag as `vX.Y.Z`
6. Delete release branch

## Typical Merge Commit Messages
- `Merge pull request #123 from user/feature/new-api`
- `Merge branch 'release/v1.2.0'`
- `Merge hotfix/security-patch into main`

## Branch Lifecycle Stats
- Average feature branch lifespan: 3-5 days
- Average PRs per branch: 1 (no force-push after review)
- Stale branch cleanup: Automated after 30 days
```

**When to update**: When merge patterns change or new strategies adopted

---

#### `repository_info.md` (Optional)

**Purpose**: General repository metadata and context

**Should contain**:
- Repository name and primary purpose
- Main branches and their roles
- Key contributors and team structure
- Release schedule and versioning
- CI/CD pipeline overview

**Example structure**:
```markdown
# Repository Info - MyProject

## Repository
- **Name**: `mycompany/myproject`
- **Purpose**: RESTful API for customer management
- **Language**: Python 3.11+
- **Framework**: FastAPI

## Branch Structure
- `main`: Production-ready code, protected
- `develop`: Integration branch (if using GitFlow)
- `release/*`: Release preparation branches
- `hotfix/*`: Emergency fixes for production

## Team
- **Team Size**: 5 developers
- **Active Contributors**: 3 primary, 2 rotating
- **Code Review**: Required, minimum 1 approval

## Release Cadence
- **Minor releases**: Every 2 weeks (sprint releases)
- **Patch releases**: As needed for bugs
- **Major releases**: Quarterly

## CI/CD
- GitHub Actions runs on every PR
- Tests, linting, security scan required
- Auto-deploy to staging on merge to `main`
- Manual approval for production deploy
```

**When to update**: When repository structure or team changes

---

## Usage in skill:get-git-diff

### Loading Memory

```markdown
# In skill workflow Step 1 or Step 2

project_name = detect_project_name()
memory_path = f"../../memory/skills/get-git-diff/{project_name}/"

if exists(memory_path):
    common_patterns = read_file(f"{memory_path}/common_patterns.md")
    commit_conventions = read_file(f"{memory_path}/commit_conventions.md")
    merge_patterns = read_file(f"{memory_path}/merge_patterns.md")
    
    # Use for analysis
    - Identify hotspot files from common_patterns
    - Validate commit messages against commit_conventions
    - Understand branch strategy from merge_patterns
```

### Updating Memory

```markdown
# In skill workflow Step 4 (optional)

After generating diff analysis:

1. Check if new patterns emerged:
   - Are there new hotspot files?
   - Did commit message format change?
   - New branch naming pattern?

2. If yes, update relevant memory file:
   append_to_file(f"{memory_path}/common_patterns.md", new_pattern)

3. If first time analyzing project:
   - Create directory and all memory files
   - Populate with observations from this analysis
```

---

## Memory Benefits for Diff Analysis

### Enhanced Summaries

**Without memory**:
> "Modified 3 files with 150 lines changed"

**With memory**:
> "Modified typical backend feature group (routes + service + test). Change size is consistent with medium features (150 lines, project average 100-200). Hotspot file `routes.py` included as expected."

### Better Change Classification

**Without memory**:
> "Multiple file changes detected"

**With memory**:
> "Standard feature commit pattern: updated all related files in typical grouping. Follows project convention of keeping route/service/test together."

### Commit Validation

**Without memory**:
> "Commit message: 'fix stuff'"

**With memory**:
> "⚠️ Commit message doesn't follow project convention (Conventional Commits format expected)"

### Context for Reviewers

**Without memory**:
> "Large diff with 50 files changed"

**With memory**:
> "Large diff (50 files) but consistent with project's database migration pattern. Last 3 migrations had similar scope."

---

## Memory Lifecycle

### Creation (First Diff Analysis)

1. Skill runs on project for first time
2. Analyzes diff without memory
3. Creates `{project-name}/` directory
4. Generates initial memory files based on observations
5. Saves for future use

### Growth (Ongoing Analysis)

1. Skill runs on subsequent diffs
2. Loads existing memory
3. Uses memory to enhance analysis
4. Updates memory if new patterns observed
5. Memory becomes more accurate over time

### Maintenance (Periodic Review)

1. Review memory files every few months
2. Remove outdated patterns
3. Consolidate similar entries
4. Verify patterns still match current project state

---

## Example: Memory Evolution

### After 1st Analysis
```markdown
# common_patterns.md

## Hotspot Files
- src/main.py (observed in this commit)
- README.md (observed in this commit)
```

### After 10 Analyses
```markdown
# common_patterns.md

## Hotspot Files (Frequency)
- src/api/routes.py (8/10 commits - 80%)
- tests/test_api.py (7/10 commits - 70%)
- README.md (6/10 commits - 60%)
- src/models.py (5/10 commits - 50%)

## Change Groupings
Backend feature commits (6 observed):
- Route + Service + Test (pattern: 100%)
- Usually includes model change (pattern: 66%)
```

### After 50 Analyses
```markdown
# Detailed patterns, accurate statistics, reliable predictions
# Memory now provides high-value project-specific insights
```

---

## Related Documentation

- **Main Memory Index**: `../index.md` for memory system overview
- **Skill Documentation**: `../../skills/get-git-diff/SKILL.md` for skill workflow
- **Context Files**: `../../context/git/` for general diff knowledge
