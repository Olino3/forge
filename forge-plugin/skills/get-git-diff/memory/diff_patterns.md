# Common Diff Patterns

This file catalogs common patterns seen in git diffs and what they typically indicate. Use this as a reference when analyzing diffs to quickly identify change types and potential risks.

---

## Change Type Patterns

### Feature Addition

**Characteristics**:
- Multiple new files (`A` status)
- High insertion count relative to deletions
- New test files corresponding to new features
- Documentation updates (README, docs/)
- New dependencies in requirements/package files

**Example Indicators**:
```
A   src/features/new_feature.py
A   tests/test_new_feature.py
M   README.md
M   requirements.txt
```

**What to look for**:
- Are tests included?
- Is documentation updated?
- Are new dependencies necessary and vetted?
- Does it introduce new API endpoints or public interfaces?

**Risk Level**: Medium
- New code = new bugs
- Integration points need review
- Dependency security concerns

---

### Bug Fix

**Characteristics**:
- Small number of files (1-3 typically)
- Small number of changed lines (10-50 typically)
- Changes concentrated in specific functions/methods
- Often includes test additions to prevent regression
- Commit message contains "fix", "bug", "issue #123"

**Example Indicators**:
```diff
M   src/auth/login.py          (+5, -3)
A   tests/test_login_fix.py    (+15, -0)
```

**Diff Pattern**:
```diff
-    if user.password == password:
+    if user.check_password(password):
```

**What to look for**:
- Is there a test that would have caught this bug?
- Does the fix address the root cause or just symptoms?
- Are there similar patterns elsewhere that need fixing?
- Does it introduce breaking changes?

**Risk Level**: Low to Medium
- Isolated changes are lower risk
- But fixes can introduce new bugs

---

### Refactoring

**Characteristics**:
- High rename count (`R` status)
- Many files changed, but similar content
- Import statement updates throughout codebase
- File moves to new directory structure
- Function/class renames
- Similar insertion/deletion counts (restructuring, not adding features)

**Example Indicators**:
```
R100  src/utils.py → src/core/utils.py
R95   src/auth.py → src/auth/main.py
M     src/main.py                        (+12, -12)
M     tests/test_auth.py                 (+8, -8)
```

**Diff Pattern**:
```diff
-from src.utils import helper
+from src.core.utils import helper
```

**What to look for**:
- Are all imports updated consistently?
- Do tests still pass after restructuring?
- Is this breaking for external consumers?
- Are there circular dependency risks?

**Risk Level**: Medium to High
- Easy to miss an import update
- Can break external dependencies
- May introduce circular imports

---

### Dependency Update

**Characteristics**:
- Changes in dependency files (requirements.txt, package.json, Gemfile, etc.)
- Lock file updates (package-lock.json, poetry.lock, Gemfile.lock)
- Potential API usage changes if major version bump
- Changelog/release notes updates

**Example Indicators**:
```
M   requirements.txt      (+3, -3)
M   poetry.lock           (+150, -120)
```

**Diff Pattern**:
```diff
-django==4.1.0
+django==4.2.5
-requests==2.28.0
+requests==2.31.0
```

**What to look for**:
- Are these security updates? (check CVE databases)
- Are these major version changes? (breaking changes likely)
- Do tests pass with new versions?
- Are all transitive dependencies compatible?

**Risk Level**: Low to High
- Security patches: Low risk, high urgency
- Major version bumps: High risk, need thorough testing
- Always check for breaking changes in release notes

---

### Security Fix

**Characteristics**:
- Changes in authentication/authorization code
- Input validation additions
- SQL query parameterization
- Cryptographic function updates
- Removal of hardcoded credentials
- Security-related dependency updates
- Commit message contains "security", "CVE", "vulnerability"

**Example Indicators**:
```diff
# SQL Injection fix
-query = f"SELECT * FROM users WHERE id = {user_id}"
+query = "SELECT * FROM users WHERE id = %s"
+cursor.execute(query, (user_id,))

# XSS fix
-return f"<div>{user_input}</div>"
+return f"<div>{escape(user_input)}</div>"

# Auth bypass fix
-if user.is_admin:
+if user.is_authenticated and user.is_admin:
```

**What to look for**:
- Is this a complete fix or partial mitigation?
- Are there similar vulnerabilities elsewhere?
- Should this be coordinated disclosure?
- Are there tests to prevent regression?

**Risk Level**: Critical
- Security issues are high priority
- May need backporting to previous versions
- May require coordinated disclosure

---

### Database Migration

**Characteristics**:
- New files in migrations/ or db/migrate/
- Model file changes
- Schema definition updates
- Potential data migration scripts

**Example Indicators**:
```
A   migrations/0024_add_user_profiles.py
M   models/user.py
```

**Diff Pattern**:
```diff
# Model change
class User(models.Model):
    email = models.EmailField()
+   profile_image = models.URLField(null=True)
+   bio = models.TextField(blank=True)
```

**What to look for**:
- Is there a rollback/down migration?
- Will this work on existing data?
- Are there default values for new required fields?
- Is there a data backfill plan?
- Performance impact on large tables?

**Risk Level**: Medium to High
- Can cause downtime if not handled properly
- Data loss risk if rollback not tested
- Performance impact on large tables

---

### Configuration Change

**Characteristics**:
- Changes in config files (.env.example, config.yml, settings.py)
- Environment variable additions
- Feature flag toggles
- API endpoint URLs
- Resource limits (memory, timeout)

**Example Indicators**:
```
M   config/production.yml
M   .env.example
M   settings.py
```

**Diff Pattern**:
```diff
# New environment variable
+API_TIMEOUT=30
+ENABLE_FEATURE_X=false

# Changed resource limit
-MAX_UPLOAD_SIZE = 5 * 1024 * 1024  # 5MB
+MAX_UPLOAD_SIZE = 10 * 1024 * 1024  # 10MB
```

**What to look for**:
- Are new config values documented?
- Are there sensible defaults?
- Do all environments need this config?
- Security implications (exposing new services)?

**Risk Level**: Medium
- Can break deployments if config not updated
- May expose services unintentionally
- Requires coordination with DevOps

---

### Performance Optimization

**Characteristics**:
- Algorithm changes (loops to comprehensions, O(n²) to O(n))
- Caching additions
- Database query optimization
- Lazy loading implementations
- Index additions

**Example Indicators**:
```diff
# Algorithm optimization
-for user in users:
-    if user.email == email:
-        return user
+return next((u for u in users if u.email == email), None)

# Caching
+@lru_cache(maxsize=128)
 def get_user_permissions(user_id):

# Query optimization (N+1 fix)
-posts = Post.objects.all()
+posts = Post.objects.select_related('author').all()
```

**What to look for**:
- Is there benchmarking data?
- Does optimization improve real-world scenarios?
- Any correctness trade-offs?
- Cache invalidation strategy?

**Risk Level**: Low to Medium
- Premature optimization can add complexity
- Cache invalidation bugs are common

---

### Breaking Change

**Characteristics**:
- API signature changes (parameters added/removed/reordered)
- Public function/class renames or deletions
- Return type changes
- Exception type changes
- Major version bump in semantic versioning

**Example Indicators**:
```diff
# Parameter change
-def create_user(name, email):
+def create_user(email, name, verified=False):

# Return type change
-def get_users() -> List[User]:
+def get_users() -> Iterator[User]:

# Removed public API
-def legacy_function():
-    pass
```

**What to look for**:
- Is this versioned appropriately?
- Is there a deprecation period?
- Are consumers notified?
- Is there a migration guide?
- Are tests updated to reflect changes?

**Risk Level**: High
- Will break existing code
- Requires major version bump
- Needs clear communication

---

### Test Changes

**Characteristics**:
- Changes in tests/ or test_*.py files
- Test additions for new features
- Test updates for refactored code
- Mock/fixture updates

**Example Indicators**:
```
A   tests/test_new_feature.py
M   tests/test_auth.py
M   tests/fixtures/users.json
```

**What to look for**:
- Do tests cover new functionality?
- Are edge cases tested?
- Are error cases tested?
- Is test data realistic?
- Are tests deterministic (no flakiness)?

**Risk Level**: Low
- Test changes are generally low risk
- But missing tests increase risk elsewhere

---

### Documentation Update

**Characteristics**:
- Changes in .md files, docs/ directory
- README updates
- API documentation
- Changelog updates
- Comment additions

**Example Indicators**:
```
M   README.md
M   docs/api.md
M   CHANGELOG.md
A   docs/new-feature.md
```

**What to look for**:
- Does documentation match code changes?
- Are examples up to date?
- Is migration/upgrade guide included?
- Are breaking changes documented?

**Risk Level**: Very Low
- Documentation changes carry minimal risk
- But outdated docs can cause confusion

---

## Structural Patterns

### Large File Changes

**Pattern**: Single file with hundreds of lines changed

**Possible Causes**:
- Reformatting (entire file auto-formatted)
- Mass rename within file (variable/function rename)
- Generated code (API clients, migrations)
- Dependency vendoring

**What to check**:
```bash
# Ignore whitespace to see if it's formatting
git diff -w commit1 commit2 -- path/to/large_file.py

# Check for renames within file
git diff --word-diff commit1 commit2 -- path/to/large_file.py
```

**Risk Assessment**:
- Formatting changes: Low risk
- Mass renames: Medium risk (easy to introduce typos)
- Generated code: Low risk if generation is verified

---

### Many Small Changes Across Many Files

**Pattern**: 50+ files changed, 1-5 lines each

**Possible Causes**:
- Import path update after refactoring
- Global variable/constant rename
- Copyright year update
- Dependency API change propagation

**Example**:
```
M   src/module1.py    (+2, -2)
M   src/module2.py    (+2, -2)
M   src/module3.py    (+2, -2)
... (47 more files)
```

**What to check**:
- Is the change consistent across all files?
- Was this an automated refactor? (IDE refactoring tool)
- Are there any files that differ from the pattern?

**Risk Assessment**: Medium
- Easy to miss edge cases
- Automated refactors can have blind spots

---

### Binary File Changes

**Pattern**: `Binary files a/path b/path differ`

**File Types**:
- Images (.png, .jpg, .gif)
- Fonts (.ttf, .woff)
- PDFs (.pdf)
- Compiled files (.pyc, .class, .o)
- Archives (.zip, .tar.gz)

**What to check**:
- Are binary files necessary in the repo? (consider Git LFS)
- Are these generated files? (should be .gitignored)
- File size increase (large files bloat repo)

**Risk Assessment**: Varies
- Images/fonts: Low risk
- Compiled files: Should be in .gitignore
- Large binaries: Repo size concern

---

### Merge Conflict Resolutions

**Pattern**: Merge commit with unexpected changes

**Indicators**:
```bash
# Check if it's a merge commit
git log -1 --format="%P" <commit>  # Multiple parent hashes

# See conflict resolution
git diff <commit>^1...<commit>  # Against first parent
git diff <commit>^2...<commit>  # Against second parent
```

**What to look for**:
- Did the merge introduce new code? (not in either parent)
- Are there remnants of conflict markers?
- Does the resolution make sense?

**Risk Assessment**: Medium to High
- Manual conflict resolution can introduce bugs
- Test thoroughly after merge

---

## Anti-Patterns and Red Flags

### Suspicious Patterns

1. **Commented-out code additions**:
   ```diff
   +    # user = authenticate(username, password)
   +    # if not user:
   +    #     return None
   ```
   **Flag**: Why is code being added as comments?

2. **Debug/logging code in production**:
   ```diff
   +    print(f"DEBUG: user_id = {user_id}")
   +    import pdb; pdb.set_trace()
   ```
   **Flag**: Should not be in production code

3. **Hardcoded credentials added**:
   ```diff
   +    API_KEY = "sk-1234567890abcdef"
   +    PASSWORD = "admin123"
   ```
   **Flag**: Security violation

4. **TODO comments**:
   ```diff
   +    # TODO: Fix this properly later
   +    # HACK: Temporary workaround
   ```
   **Flag**: Technical debt being introduced

5. **Massive deletions without explanation**:
   ```
   D   src/important_module.py    (0, -500)
   D   tests/test_important.py    (0, -200)
   ```
   **Flag**: Why is substantial code being removed?

6. **Whitespace-only changes**:
   ```diff
   -    return True
   +    return True
   ```
   **Flag**: Likely formatting inconsistency or merge artifact

---

## Pattern Detection Checklist

When analyzing a diff, systematically check for:

### Change Scope
- [ ] How many files changed?
- [ ] Total lines added/removed?
- [ ] Are changes localized or spread throughout codebase?

### File Types
- [ ] Source code changes?
- [ ] Test changes?
- [ ] Configuration changes?
- [ ] Documentation changes?
- [ ] Database migrations?

### Operations
- [ ] Any new files?
- [ ] Any deleted files?
- [ ] Any renamed/moved files?
- [ ] Any binary files?

### Risk Indicators
- [ ] Security-sensitive code (auth, crypto, input validation)?
- [ ] Database schema changes?
- [ ] Breaking API changes?
- [ ] Dependency updates?
- [ ] Configuration changes?

### Quality Indicators
- [ ] Are tests included/updated?
- [ ] Is documentation updated?
- [ ] Are error cases handled?
- [ ] Is there commented-out code?
- [ ] Are there TODOs?

---

## Context-Specific Patterns

### Web Application

**Common patterns**:
- Route/endpoint additions (`@app.route`, `@api.get`)
- Template changes (HTML files)
- Static asset updates (CSS, JS)
- Middleware additions
- Authentication/authorization changes

**Risk areas**:
- CSRF protection
- XSS vulnerabilities
- SQL injection in queries
- Authentication bypasses

### Data Science / ML

**Common patterns**:
- Model file updates (.pkl, .h5, .pt)
- Data pipeline changes
- Feature engineering code
- Hyperparameter tuning
- Notebook changes (.ipynb)

**Risk areas**:
- Data leakage
- Reproducibility (random seeds)
- Model versioning
- Large file commits

### API Services

**Common patterns**:
- Endpoint additions/modifications
- Schema/model changes (Pydantic, OpenAPI)
- Serialization changes
- Error response updates

**Risk areas**:
- Breaking changes to contracts
- Backward compatibility
- API versioning
- Rate limiting

### DevOps / Infrastructure

**Common patterns**:
- Dockerfile changes
- CI/CD pipeline updates (.github/workflows, .gitlab-ci.yml)
- Infrastructure as Code (Terraform, CloudFormation)
- Kubernetes manifests

**Risk areas**:
- Deployment failures
- Resource limits
- Security group changes
- Secrets management

---

## Quick Reference

| Pattern | Indicators | Risk Level |
|---------|-----------|------------|
| Feature Addition | New files, high insertions, new tests | Medium |
| Bug Fix | Few files, small changes, focused | Low-Medium |
| Refactoring | Renames, moves, import updates | Medium-High |
| Dependency Update | Package file changes | Low-High (varies) |
| Security Fix | Auth/validation code, CVE refs | Critical |
| Database Migration | Migration files, model changes | Medium-High |
| Config Change | Config files, env vars | Medium |
| Breaking Change | API signature changes, deletions | High |
| Performance Opt | Algorithm changes, caching | Low-Medium |
| Test Changes | Test file updates | Low |
| Documentation | .md files, comments | Very Low |

---

## Further Reading

- **Code Review Best Practices**: https://google.github.io/eng-practices/review/
- **Semantic Versioning**: https://semver.org/
- **OWASP Secure Coding**: https://owasp.org/www-project-secure-coding-practices-quick-reference-guide/
- **Database Migration Best Practices**: https://www.mongodb.com/basics/database-migration
