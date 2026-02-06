# Commit Helper Examples

This file contains example scenarios demonstrating how to use the commit-helper skill to craft meaningful commit messages for various types of changes.

---

## Example 1: Simple Bug Fix

### Scenario
Developer fixed a null pointer exception when looking up users by email.

### User Prompt
```
Help me write a commit message for my staged changes
```

### Skill Execution

**Step 1 - Analyze Changes**:
```bash
git diff --staged --stat
# src/auth/user_lookup.py | 5 +++--
# 1 file changed, 3 insertions(+), 2 deletions(-)

git diff --staged --name-status
# M    src/auth/user_lookup.py
```

Diff content shows a null check added before accessing `user.email` on line 42.

**Step 2 - Determine Context**:
- **Type**: `fix` — corrects a bug (null pointer exception)
- **Scope**: `auth` — change is in the authentication module
- **Breaking changes**: None — behavior is corrected, not altered
- **Motivation**: Application crashed when querying non-existent users

**Step 3 - Craft Message**:
```
fix(auth): add null check before accessing user email

The user lookup function crashed with a NullPointerError when
querying an email address that had no matching user record.
Add a guard clause to return None early when the query yields
no results.

Fixes #1042
```

**Step 4 - Review**:
- ✅ Type: `fix` — correct for bug fix
- ✅ Scope: `auth` — matches affected module
- ✅ Subject: imperative mood, 47 chars, specific
- ✅ Body: explains what and why, wrapped at 72 chars
- ✅ Footer: references the issue

---

## Example 2: Feature Addition

### Scenario
Developer added a new endpoint for exporting user data as CSV.

### User Prompt
```
Generate a commit message for the CSV export feature I just implemented
```

### Skill Execution

**Step 1 - Analyze Changes**:
```bash
git diff --staged --stat
# src/api/exports.py       | 78 ++++++++++++++++++++++++++++++++++++++
# src/api/router.py        |  3 ++
# tests/api/test_exports.py | 45 ++++++++++++++++++++++
# 3 files changed, 126 insertions(+)

git diff --staged --name-status
# A    src/api/exports.py
# M    src/api/router.py
# A    tests/api/test_exports.py
```

New file `exports.py` contains a `/users/export` endpoint that streams CSV data. Router updated to include the new route. Tests cover CSV generation and streaming.

**Step 2 - Determine Context**:
- **Type**: `feat` — new functionality added
- **Scope**: `api` — new API endpoint
- **Breaking changes**: None — additive change only
- **Details**: Supports filtering by date range, streams large datasets

**Step 3 - Craft Message**:
```
feat(api): add CSV export endpoint for user data

Add GET /users/export endpoint that generates and streams user
data as CSV. Supports optional date range filtering via query
parameters `from` and `to`. Uses streaming response to handle
large datasets without excessive memory consumption.

Includes unit tests for CSV generation, date filtering, and
streaming behavior.
```

**Step 4 - Review**:
- ✅ Type: `feat` — correct for new feature
- ✅ Scope: `api` — matches affected area
- ✅ Subject: imperative mood, 43 chars, descriptive
- ✅ Body: covers what, why, and key design decisions
- ✅ No breaking changes, no issue reference needed

---

## Example 3: Breaking Change

### Scenario
Developer renamed the configuration keys and changed the config file format from INI to YAML.

### User Prompt
```
Write a commit message — I changed the config format from INI to YAML
```

### Skill Execution

**Step 1 - Analyze Changes**:
```bash
git diff --staged --stat
# src/config/loader.py     | 34 ++++++++++++--------
# src/config/schema.py     | 18 +++++------
# config.example.yaml      | 25 ++++++++++++++++
# config.example.ini       | 20 ----------------
# docs/configuration.md    | 42 ++++++++++++++-----------
# 5 files changed, 72 insertions(+), 67 deletions(-)

git diff --staged --name-status
# M    src/config/loader.py
# M    src/config/schema.py
# A    config.example.yaml
# D    config.example.ini
# M    docs/configuration.md
```

**Step 2 - Determine Context**:
- **Type**: `feat` — new configuration format capability (could also be `build` or `chore`, but the config format is user-facing)
- **Scope**: `config` — configuration subsystem
- **Breaking changes**: **YES** — existing INI config files will no longer be parsed; users must migrate to YAML format
- **Migration**: Documentation updated with migration guide

**Step 3 - Craft Message**:
```
feat(config)!: migrate configuration format from INI to YAML

Replace INI-based configuration with YAML format for improved
readability, nested value support, and consistency with modern
tooling conventions.

The configuration loader now uses PyYAML to parse config files.
Key names have been restructured to use nested hierarchies
instead of flat dot-notation (e.g., `database.host` becomes a
nested `database:` section with `host:` key).

Migration guide added to docs/configuration.md.

BREAKING CHANGE: Configuration files must be converted from INI
to YAML format. The old config.ini format is no longer supported.
See docs/configuration.md for migration instructions.
```

**Step 4 - Review**:
- ✅ Type: `feat!` — exclamation mark signals breaking change
- ✅ Scope: `config` — matches affected subsystem
- ✅ Subject: imperative mood, 52 chars
- ✅ Body: explains motivation and key details
- ✅ Footer: `BREAKING CHANGE:` with clear migration path
- ✅ Documentation reference included

---

## Example 4: Refactoring

### Scenario
Developer extracted duplicated validation logic into a shared utility module.

### User Prompt
```
I refactored the validation code, need a good commit message
```

### Skill Execution

**Step 1 - Analyze Changes**:
```bash
git diff --staged --stat
# src/api/users.py         | 15 ++------
# src/api/orders.py        | 18 +++-------
# src/api/products.py      | 12 ++-----
# src/utils/validators.py  | 45 ++++++++++++++++++++++++++++
# tests/utils/test_validators.py | 38 +++++++++++++++++++++++
# 5 files changed, 89 insertions(+), 39 deletions(-)

git diff --staged --name-status
# M    src/api/users.py
# M    src/api/orders.py
# M    src/api/products.py
# A    src/utils/validators.py
# A    tests/utils/test_validators.py
```

Duplicated email, phone, and address validation removed from three API modules and consolidated into `validators.py`.

**Step 2 - Determine Context**:
- **Type**: `refactor` — code restructuring, no behavior change
- **Scope**: `validation` — cross-cutting validation concern
- **Breaking changes**: None — internal restructuring only, public API unchanged

**Step 3 - Craft Message**:
```
refactor(validation): extract shared validation logic into utility module

Consolidate duplicated email, phone number, and address
validation from users, orders, and products API modules into
a shared src/utils/validators.py module.

Reduces code duplication across three modules and provides a
single source of truth for validation rules. No behavioral
changes — all existing validation logic preserved exactly.

Adds dedicated unit tests for the extracted validators.
```

**Step 4 - Review**:
- ✅ Type: `refactor` — correct, no behavior change
- ✅ Scope: `validation` — describes the cross-cutting concern
- ✅ Subject: imperative mood, 56 chars
- ✅ Body: explains what was consolidated and why
- ✅ Explicitly states no behavioral changes

**Alternative message** (narrower scope):
```
refactor(api): deduplicate validation logic across API modules
```

---

## Example 5: Multi-File Change with Mixed Concerns

### Scenario
Developer updated the database schema, added a migration, updated the ORM model, and modified the API to expose new fields.

### User Prompt
```
Commit message for adding the user preferences feature
```

### Skill Execution

**Step 1 - Analyze Changes**:
```bash
git diff --staged --stat
# migrations/0024_add_user_preferences.py | 32 +++++++++++++++++
# src/models/user.py                      | 14 ++++++--
# src/api/users.py                        | 23 ++++++++----
# src/api/schemas.py                      |  8 +++++
# tests/api/test_users.py                 | 35 ++++++++++++++++++
# tests/models/test_user.py               | 18 ++++++++++
# docs/api.md                             | 15 ++++++++
# 7 files changed, 139 insertions(+), 6 deletions(-)

git diff --staged --name-status
# A    migrations/0024_add_user_preferences.py
# M    src/models/user.py
# M    src/api/users.py
# M    src/api/schemas.py
# A    tests/api/test_users.py
# A    tests/models/test_user.py
# M    docs/api.md
```

**Step 2 - Determine Context**:
- **Type**: `feat` — new user-facing feature
- **Scope**: `users` — the user domain is the primary affected area
- **Breaking changes**: None — new fields are optional with defaults
- **Note**: Spans multiple layers (DB, model, API, docs) but represents a single cohesive feature

**Step 3 - Craft Message**:
```
feat(users): add user preferences with theme and locale support

Introduce user preferences system allowing users to configure
their preferred theme (light/dark/system) and locale settings.

Changes span the full stack:
- Database migration adding preferences columns with defaults
- User model extended with preference fields and validation
- API endpoints updated to accept and return preferences
- Response schemas updated with new optional fields
- API documentation updated with preference endpoints

All new fields have sensible defaults (theme: "system",
locale: "en-US") ensuring backward compatibility with existing
clients.

Refs #892
```

**Step 4 - Review**:
- ✅ Type: `feat` — correct for new feature
- ✅ Scope: `users` — primary domain, even though changes span layers
- ✅ Subject: imperative mood, 55 chars
- ✅ Body: enumerates all layers touched, explains defaults
- ✅ Backward compatibility explicitly noted

---

## Example 6: Documentation Update

### Scenario
Developer rewrote the getting started guide and added API reference docs.

### User Prompt
```
Need a commit message for the documentation overhaul
```

### Skill Execution

**Step 1 - Analyze Changes**:
```bash
git diff --staged --stat
# docs/getting-started.md     | 145 +++++++++++++++++++++--------
# docs/api-reference.md       | 234 +++++++++++++++++++++++++++++++++++
# docs/README.md               |  12 ++-
# docs/images/architecture.png |  Bin 0 -> 45032 bytes
# 4 files changed, 352 insertions(+), 39 deletions(-)

git diff --staged --name-status
# M    docs/getting-started.md
# A    docs/api-reference.md
# M    docs/README.md
# A    docs/images/architecture.png
```

Getting started guide rewritten with clearer step-by-step instructions. New API reference document covers all endpoints. Architecture diagram added.

**Step 2 - Determine Context**:
- **Type**: `docs` — exclusively documentation changes
- **Scope**: none needed (or `guide` if project convention requires scope)
- **Breaking changes**: None — documentation only

**Step 3 - Craft Message**:
```
docs: rewrite getting started guide and add API reference

Overhaul the getting started guide with clearer step-by-step
instructions, prerequisites section, and troubleshooting tips.

Add comprehensive API reference documenting all endpoints with
request/response examples, authentication requirements, and
error codes.

Include architecture diagram showing system component
relationships.
```

**Step 4 - Review**:
- ✅ Type: `docs` — correct for documentation-only changes
- ✅ No scope — acceptable for broad documentation changes
- ✅ Subject: imperative mood, 51 chars
- ✅ Body: summarizes each major documentation change

---

## Example 7: Performance Improvement

### Scenario
Developer optimized a database query that was causing slow page loads.

### User Prompt
```
Commit message for the query optimization
```

### Skill Execution

**Step 1 - Analyze Changes**:
```bash
git diff --staged --stat
# src/repositories/orders.py | 18 +++++----
# migrations/0025_add_order_indexes.py | 14 +++++++
# 2 files changed, 24 insertions(+), 8 deletions(-)
```

Query rewritten to use JOIN instead of subquery. Composite index added on `(user_id, created_at)`.

**Step 2 - Determine Context**:
- **Type**: `perf` — performance optimization
- **Scope**: `orders` — order repository affected
- **Breaking changes**: None

**Step 3 - Craft Message**:
```
perf(orders): optimize order listing query with JOIN and index

Replace correlated subquery with JOIN for order listing,
reducing query time from ~800ms to ~15ms on production dataset.

Add composite index on (user_id, created_at) to support the
optimized query pattern and common sort operations.
```

**Step 4 - Review**:
- ✅ Type: `perf` — correct for performance improvement
- ✅ Scope: `orders` — matches affected module
- ✅ Body: includes measurable performance improvement
- ✅ Mentions the index migration

---

## Example 8: Revert Commit

### Scenario
Developer needs to revert a previous commit that introduced a regression.

### User Prompt
```
I need to revert commit abc1234, it broke the login flow
```

### Skill Execution

**Step 1 - Analyze Changes**:
```bash
git log -1 --format="%s" abc1234
# feat(auth): add rate limiting to login endpoint

git diff abc1234^..abc1234 --stat
# src/auth/login.py     | 23 +++++++++++++++++
# src/middleware/rate.py | 45 +++++++++++++++++++++++++++++
# 2 files changed, 68 insertions(+)
```

**Step 2 - Determine Context**:
- **Type**: `revert` — undoing a previous commit
- **Scope**: `auth` — same scope as original commit
- **Breaking changes**: None — restoring previous behavior

**Step 3 - Craft Message**:
```
revert(auth): undo rate limiting on login endpoint

This reverts commit abc1234.

The rate limiting implementation caused false positives for
users behind shared NAT gateways, blocking legitimate login
attempts. Reverting until a more granular rate limiting
strategy (per-account rather than per-IP) is implemented.

Refs #1108
```

**Step 4 - Review**:
- ✅ Type: `revert` — correct for reverting
- ✅ References the original commit hash
- ✅ Explains *why* the revert is necessary
- ✅ Mentions the intended follow-up approach

---

## Summary of Commit Types

1. **Bug fix** (`fix`) — Corrects incorrect behavior
2. **Feature** (`feat`) — Adds new capability
3. **Breaking change** (`feat!`/`fix!`) — Incompatible changes requiring migration
4. **Refactoring** (`refactor`) — Restructures without changing behavior
5. **Multi-layer feature** (`feat`) — Single feature spanning multiple system layers
6. **Documentation** (`docs`) — Documentation-only changes
7. **Performance** (`perf`) — Measurable performance improvements
8. **Revert** (`revert`) — Undoes a previous commit with explanation

## Best Practices

- Always use imperative mood in the subject line ("add" not "added")
- Keep the subject line under 72 characters
- Separate subject from body with a blank line
- Explain *why* in the body, not *how* — the diff shows how
- Reference issues in the footer, not the subject
- Use `BREAKING CHANGE:` footer for any backward-incompatible changes
- When in doubt about type, consider the primary intent of the change
- One commit should represent one logical change — split unrelated changes
- Include measurable impact for performance changes
- For reverts, always explain why the original change is being undone
