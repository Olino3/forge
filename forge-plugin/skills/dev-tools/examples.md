# Dev Tools Examples

This file contains example scenarios demonstrating how to use the dev-tools skill to orchestrate multi-step developer workflows.

---

## Example 1: Review Pipeline — Python API Changes

### Scenario
A developer has made changes to a FastAPI application and wants a full review before committing.

### User Prompt
```
step — review my changes before I commit
```

### Skill Execution

**Step 1 - Identify Workflow**:
- **Pipeline**: Review Pipeline
- **Steps planned**:
  1. `get-git-diff` → Capture staged changes
  2. `python-code-review` → Review Python code (detected via `contextProvider.detectProjectType()`)
  3. `commit-helper` → Generate commit message
- **User confirmation**: "I'll review your staged Python changes and help with the commit message. Proceed?"

**Step 2 - Load Memory**:
- `memoryStore.getSkillMemory("dev-tools", "order-api")` → Found workflow preferences
- Previous review used `python-code-review` with FastAPI context
- Tool preferences: `pytest` for testing, `black` for formatting

**Step 3 - Load Context**:
- `contextProvider.detectProjectType()` → Python 3.11, FastAPI, PostgreSQL
- Loaded engineering domain context
- Verified `get-git-diff`, `python-code-review`, `commit-helper` skills exist

**Step 4 - Execute Pipeline**:

**Step 1/3 — Git Diff** (via `skillInvoker.invoke("get-git-diff")`):
```
✓ Captured diff: 4 files changed, 45 insertions, 12 deletions
  - src/api/orders.py (M)
  - src/services/order_service.py (M)
  - tests/api/test_orders.py (A)
  - src/schemas/order.py (M)
```

**Step 2/3 — Code Review** (via `skillInvoker.invoke("python-code-review")`):
```
✓ Review complete:
  - ✅ Async patterns followed correctly
  - ✅ Pydantic v2 schemas used properly
  - ⚠️ Missing input validation on order quantity (could be negative)
  - ⚠️ New endpoint missing rate limiting
  - ✅ Tests cover happy path and error cases
```

**Step 3/3 — Commit Message** (via `skillInvoker.invoke("commit-helper")`):
```
✓ Generated commit message:
  feat(orders): add bulk order creation endpoint

  Add POST /api/orders/bulk endpoint for creating multiple orders
  in a single request. Includes input validation, transaction
  management, and partial failure handling.

  Includes unit tests for bulk creation, validation errors,
  and transaction rollback scenarios.
```

**Step 5 - Output**:
- Saved to `/claudedocs/dev-tools_order-api_2026-02-12_review-pipeline.md`

**Step 6 - Update Memory**:
- Updated workflow pattern: Review → Python Review → Commit works well for this project
- Stored: Rate limiting is frequently missed on new endpoints

---

## Example 2: Ship Pipeline — Full Pre-Merge Checklist

### Scenario
A developer has completed a feature branch and wants to ensure everything is ready for merge.

### User Prompt
```
step — ship it, make sure everything is ready for merge
```

### Skill Execution

**Step 1 - Identify Workflow**:
- **Pipeline**: Ship Pipeline
- **Steps planned**:
  1. `get-git-diff` → Review all changes on branch
  2. `angular-code-review` → Review Angular code (detected)
  3. `generate-jest-unit-tests` → Generate missing tests
  4. Run test suite
  5. `documentation-generator` → Update docs if needed
  6. `commit-helper` → Final commit message
- **User confirmation**: "I'll run the full ship pipeline for your Angular project. This includes review, tests, docs, and commit. Proceed?"

**Step 2 - Load Memory**:
- `memoryStore.getSkillMemory("dev-tools", "dashboard-app")` → Found preferences
- Previous ships always run linting before commit

**Step 3 - Load Context**:
- `contextProvider.detectProjectType()` → Angular 17, TypeScript, Jest
- All required skills verified available

**Step 4 - Execute Pipeline**:

**Step 1/6 — Git Diff**:
```
✓ Branch diff: 12 files changed, 340 insertions, 45 deletions
  Feature: User dashboard redesign
```

**Step 2/6 — Code Review**:
```
✓ Review complete: 2 warnings, 0 critical
  - ⚠️ Component not using OnPush change detection
  - ⚠️ Missing unsubscribe in ngOnDestroy
```

**Step 3/6 — Test Generation**:
```
✓ Generated 8 new test cases for UserDashboardComponent
✓ Generated 4 new test cases for DashboardService
```

**Step 4/6 — Run Tests**:
```
✓ 47 tests passed, 0 failed
✓ Coverage: 87% (above 80% threshold)
```

**Step 5/6 — Documentation**:
```
✓ No documentation updates needed (internal component change)
```

**Step 6/6 — Commit Message**:
```
✓ Generated:
  feat(dashboard): redesign user dashboard with responsive layout

  Redesign the user dashboard component with responsive grid layout,
  real-time data updates via WebSocket, and improved loading states.
```

**Pipeline Summary**:
```
Ship Pipeline Complete ✅
  ✓ Code Review: 2 warnings (non-blocking)
  ✓ Tests: 47 passed, 12 new tests added
  ✓ Coverage: 87%
  ✓ Docs: No updates needed
  ✓ Commit message ready
  
  Merge readiness: READY (with minor warnings)
```

**Step 5 - Output**:
- Saved to `/claudedocs/dev-tools_dashboard-app_2026-02-12_ship-pipeline.md`

**Step 6 - Update Memory**:
- Stored: Ship pipeline successful with Angular + Jest stack
- Updated tool preferences

---

## Example 3: Debug Pipeline — Investigating Test Failure

### Scenario
A developer's tests are failing intermittently and they can't figure out why.

### User Prompt
```
step — help me debug these flaky tests, I've been going in circles
```

### Skill Execution

**Step 1 - Identify Workflow**:
- **Pipeline**: Debug Pipeline
- **Steps planned**:
  1. `power-debug` → Investigate flaky test root cause
  2. Implement fix
  3. Run tests to verify fix
  4. `commit-helper` → Commit the fix
- **User confirmation**: "I'll use the debug pipeline to investigate your flaky tests. Proceed?"

**Step 2 - Load Memory**:
- `memoryStore.getSkillMemory("dev-tools", "payment-service")` → Found history
- Previous debug session found shared state issue in test fixtures

**Step 3 - Load Context**:
- `contextProvider.detectProjectType()` → Python 3.12, pytest, PostgreSQL
- Loaded engineering context

**Step 4 - Execute Pipeline**:

**Step 1/4 — Power Debug** (via `skillInvoker.invoke("power-debug")`):
```
✓ Investigation complete:
  Root cause: Tests share database state — no transaction rollback between tests
  Evidence: Tests pass individually, fail when run together
  Fix: Add pytest fixture with transaction rollback
```

**Step 2/4 — Implement Fix**:
```
✓ Added conftest.py fixture:
  @pytest.fixture(autouse=True)
  def db_session(db):
      yield db
      db.rollback()
```

**Step 3/4 — Verify Fix**:
```
✓ Ran test suite 5 times — all passed consistently
✓ No more flaky failures
```

**Step 4/4 — Commit** (via `skillInvoker.invoke("commit-helper")`):
```
✓ Generated:
  fix(tests): add transaction rollback fixture to prevent test pollution

  Tests were sharing database state across test functions, causing
  intermittent failures when run in certain orders. Add autouse
  fixture that rolls back transactions after each test.
```

**Step 5 - Output**:
- Saved to `/claudedocs/dev-tools_payment-service_2026-02-12_debug-pipeline.md`

**Step 6 - Update Memory**:
- Stored: "Test isolation via transaction rollback" as standard pattern
- Documented: Shared DB state as common flaky test cause

---

## Summary of Pipelines

| Pipeline | Trigger | Steps | Best For |
|----------|---------|-------|----------|
| Review | "review", "check" | diff → review → commit | Pre-commit quality check |
| Test | "test", "add tests" | detect → generate → run | Test coverage improvement |
| Document | "document", "docs" | analyze → generate → commit | Documentation maintenance |
| Debug | "debug", "investigate" | investigate → fix → verify → commit | Stubborn bug resolution |
| Ship | "ship", "merge" | diff → review → test → docs → commit | Full pre-merge checklist |

## Best Practices

- Always confirm the pipeline plan before execution
- Handle step failures gracefully — offer retry, skip, or abort
- Pass context between steps to avoid redundant work
- Store workflow preferences in memory for faster future executions
- Use the Ship pipeline before every merge for consistent quality
- Compose custom pipelines when predefined ones don't fit
