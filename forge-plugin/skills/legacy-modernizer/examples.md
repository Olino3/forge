# Legacy Modernizer Examples

This file contains example scenarios demonstrating how to use the legacy-modernizer skill to assess, plan, and execute legacy code modernization for various technology stacks and migration types.

---

## Example 1: Modernizing a jQuery + PHP Monolith to React + Node.js

### Scenario
A 10-year-old e-commerce application built with jQuery 1.x on the frontend and PHP 5.6 with a custom MVC framework on the backend. No automated tests, inline SQL queries, and a single 15,000-line `functions.php` utility file.

### User Prompt
```
Help me modernize our legacy e-commerce app. It's jQuery and PHP 5.6, we want to move to React and Node.js.
```

### Skill Execution

**Step 1 — Assess Legacy Codebase**:
- **Runtime**: PHP 5.6 (EOL since December 2018) — critical security risk
- **Frontend**: jQuery 1.11.3 — multiple known XSS vulnerabilities
- **Database**: Raw MySQL queries with string concatenation — SQL injection risk
- **Architecture**: Single-entry `index.php` routing to 47 controller files, god-class `functions.php` (15,200 lines, 340 functions)
- **Dependencies**: No Composer lockfile, 12 vendor libraries copied directly into `/lib/`
- **Tests**: Zero automated tests, manual QA checklist in a wiki page
- **Complexity**: Average cyclomatic complexity of 28 per function in `functions.php`

**Step 2 — Classify & Prioritize Debt**:

| Debt Item | Type | Risk | Effort | Value | Priority |
|-----------|------|------|--------|-------|----------|
| PHP 5.6 EOL runtime | Infrastructure | 5 | 4 | 5 | **Critical** |
| SQL injection in queries | Code | 5 | 3 | 5 | **Critical** |
| jQuery XSS vulnerabilities | Dependency | 4 | 4 | 4 | **High** |
| No automated tests | Test | 4 | 4 | 5 | **High** |
| God class functions.php | Code | 3 | 4 | 4 | **Medium** |
| No dependency management | Infrastructure | 3 | 2 | 3 | **Medium** |
| Missing documentation | Documentation | 2 | 3 | 3 | **Low** |

**Quick wins**: Add Composer for dependency management, parameterize SQL queries in most-critical paths.

**Step 3 — Load Project Memory**:
```
memoryStore.getSkillMemory("legacy-modernizer", "ecommerce-app")
→ No existing memory found. First-time assessment.

contextProvider.getIndex("php")
contextProvider.getIndex("javascript")
contextProvider.getIndex("react")
```

**Step 4 — Plan & Execute Modernization**:

**Pattern**: Strangler Fig — build React frontend alongside jQuery, migrate page by page.

**Phase 1 — Safety Nets (Weeks 1-3)**:
- Write characterization tests for critical paths (checkout, payment, user auth)
- Set up CI pipeline with PHPUnit and basic smoke tests
- Add Composer, pin all dependencies, audit for vulnerabilities
- Parameterize top-20 most dangerous SQL queries

**Phase 2 — API Extraction (Weeks 4-8)**:
- Build Node.js/Express API layer that proxies to PHP backend
- Extract product catalog, cart, and user endpoints as REST APIs
- Run both systems in parallel — API gateway routes to new endpoints progressively
- Validate parity with parallel run pattern on non-critical endpoints

**Phase 3 — Frontend Migration (Weeks 9-16)**:
- Build React app consuming the new API layer
- Migrate pages incrementally: product listing → product detail → cart → checkout
- Feature toggles control which pages serve React vs. jQuery
- Each page migration includes component tests with React Testing Library

**Phase 4 — Backend Cutover (Weeks 17-24)**:
- Migrate remaining PHP business logic to Node.js services
- Replace raw SQL with Prisma ORM, add database migrations
- Decommission PHP backend once all traffic routes through Node.js
- Remove jQuery and legacy assets

**Step 5 — Review & Output**:
- Characterization tests confirm checkout flow parity between old and new
- Output saved to `/claudedocs/legacy_mod_ecommerce_2026-02-12.md`
- Memory created:
  ```
  memoryStore.update("legacy-modernizer", "ecommerce-app", {
    debt_inventory: "47 items, 2 critical addressed in Phase 1",
    migration_phase: "Phase 1 complete",
    patterns_used: ["strangler-fig", "parallel-run", "feature-toggle"],
    lessons: "Characterization tests caught 3 undocumented discount rules"
  })
  ```

---

## Example 2: Python 2 to Python 3 Migration with Test Harness Creation

### Scenario
A data processing pipeline written in Python 2.7 with 85 modules, heavy use of `print` statements, `unicode`/`str` confusion, and `urllib2`. No test suite exists. The pipeline processes 2M records daily and cannot tolerate downtime.

### User Prompt
```
We need to migrate our data pipeline from Python 2.7 to Python 3. There are no tests and we can't afford downtime.
```

### Skill Execution

**Step 1 — Assess Legacy Codebase**:
- **Runtime**: Python 2.7 (EOL since January 2020) — no security patches
- **Modules**: 85 `.py` files, 23,000 LOC total
- **Key incompatibilities found**:
  - 142 `print` statements (not function calls)
  - 67 instances of `unicode()` / `basestring` usage
  - 31 `urllib2` imports
  - 18 `dict.has_key()` calls
  - 12 `except Exception, e:` syntax usages
  - 8 modules using `__cmp__` magic method
  - Mixed `str`/`bytes` handling in CSV parsing and HTTP responses
- **Dependencies**: `requirements.txt` with 34 packages, 6 have no Python 3 support
- **Tests**: Zero. No test directory, no test framework installed
- **Architecture**: ETL pipeline with clear stage separation (extract → transform → load) but shared global state via module-level variables

**Step 2 — Classify & Prioritize Debt**:

| Debt Item | Type | Risk | Effort | Value | Priority |
|-----------|------|------|--------|-------|----------|
| Python 2.7 EOL | Infrastructure | 5 | 5 | 5 | **Critical** |
| No test suite | Test | 5 | 4 | 5 | **Critical** |
| str/bytes confusion in I/O | Code | 4 | 4 | 5 | **High** |
| 6 Py2-only dependencies | Dependency | 4 | 3 | 4 | **High** |
| Print statement syntax | Code | 2 | 1 | 3 | **Quick Win** |
| dict.has_key() usage | Code | 2 | 1 | 2 | **Quick Win** |
| Global mutable state | Architecture | 3 | 4 | 3 | **Medium** |

**Step 3 — Load Project Memory**:
```
memoryStore.getSkillMemory("legacy-modernizer", "data-pipeline")
→ No existing memory found.

contextProvider.getIndex("python")
```

**Step 4 — Plan & Execute Modernization**:

**Pattern**: Branch by Abstraction for I/O layers + Parallel Run for validation.

**Phase 1 — Build Test Harness (Weeks 1-3)**:
- Install pytest and create test infrastructure
- Write characterization tests using recorded I/O:
  - Capture input/output pairs for each pipeline stage
  - Create fixture files from production data samples (anonymized)
  - Build snapshot tests: `assert transform(input_fixture) == expected_output`
- Achieve characterization test coverage on all 5 pipeline stages
- Target: 100% of critical path functions have at least one characterization test

**Phase 2 — Mechanical Fixes (Week 4)**:
- Run `2to3` tool for safe automatic transformations:
  - `print` statements → `print()` function calls (142 instances)
  - `dict.has_key(k)` → `k in dict` (18 instances)
  - `except Exception, e` → `except Exception as e` (12 instances)
- Run `futurize` for compatibility shims on ambiguous patterns
- Run characterization tests after each batch — all must pass

**Phase 3 — Dependency Migration (Weeks 5-6)**:
- Replace 6 Python 2-only packages with maintained alternatives:
  - `urllib2` → `requests` (31 call sites)
  - `ConfigParser` → `configparser` (standard lib rename)
  - `MySQLdb` → `mysqlclient` (drop-in compatible)
  - 3 internal libraries → forked and ported versions
- Pin all dependencies in `requirements.txt` with `>=` lower bounds
- Run full characterization suite after each dependency swap

**Phase 4 — String/Bytes Cleanup (Weeks 7-9)**:
- Introduce abstraction layer for all I/O boundaries:
  - File reads/writes: explicit encoding declaration (`encoding='utf-8'`)
  - HTTP responses: decode at boundary, work with `str` internally
  - CSV parsing: unified text-mode handling
- Replace `unicode()` with `str()`, remove `basestring` checks (67 instances)
- Parallel run: process 1 week of production data through both Py2 and Py3 pipelines, compare outputs record-by-record

**Phase 5 — Cutover (Week 10)**:
- Switch production to Python 3.11 runtime
- Monitor error rates and processing times for 48 hours
- Decommission Python 2.7 environment

**Step 5 — Review & Output**:
- Parallel run showed 100% output parity across 14M records
- 3 encoding edge cases caught and fixed during Phase 4
- Output saved to `/claudedocs/legacy_mod_pipeline_2026-02-12.md`
- Memory updated:
  ```
  memoryStore.update("legacy-modernizer", "data-pipeline", {
    debt_inventory: "Py2→Py3 migration complete, 8 architecture items remaining",
    migration_phase: "Phase 5 complete — running on Python 3.11",
    patterns_used: ["branch-by-abstraction", "parallel-run", "characterization-tests"],
    lessons: "Characterization tests with fixture data were essential — caught 3 encoding bugs that 2to3 missed"
  })
  ```

---

## Example 3: Refactoring a Tightly-Coupled Java Enterprise App to Clean Architecture

### Scenario
A Java 8 enterprise application using Spring Boot 1.5, with business logic embedded in 200+ REST controllers, direct JPA entity usage in API responses, circular dependencies between 14 service classes, and a single 3,000-line `ApplicationService.java` god class.

### User Prompt
```
Our Java app is a mess — business logic in controllers, circular dependencies everywhere, and one massive god class. Help us move to clean architecture.
```

### Skill Execution

**Step 1 — Assess Legacy Codebase**:
- **Runtime**: Java 8 (LTS but approaching EOL), Spring Boot 1.5 (EOL since August 2019)
- **Structure**: 214 REST controllers averaging 380 lines each, business logic mixed with HTTP handling
- **God class**: `ApplicationService.java` — 3,012 lines, 89 public methods, cyclomatic complexity of 156
- **Circular dependencies**: 14 service classes with bidirectional `@Autowired` injections
- **Data layer**: JPA entities exposed directly in API responses — 47 `@Entity` classes used as DTOs
- **Tests**: 340 integration tests (Spring context boot), 12 unit tests, average test time 8 minutes
- **Dependencies**: Spring Boot 1.5.22, Hibernate 5.0, Jackson 2.8 — all have known CVEs
- **Build**: Maven with 6-minute build time, no parallel execution configured

**Step 2 — Classify & Prioritize Debt**:

| Debt Item | Type | Risk | Effort | Value | Priority |
|-----------|------|------|--------|-------|----------|
| Spring Boot 1.5 EOL | Dependency | 5 | 4 | 5 | **Critical** |
| Business logic in controllers | Architecture | 4 | 5 | 5 | **Critical** |
| God class ApplicationService | Code | 4 | 4 | 5 | **High** |
| Circular dependencies | Architecture | 4 | 3 | 4 | **High** |
| JPA entities as DTOs | Architecture | 3 | 3 | 4 | **High** |
| No unit tests (only integration) | Test | 3 | 4 | 4 | **High** |
| Jackson CVEs | Dependency | 4 | 2 | 3 | **Quick Win** |
| Slow build time | Infrastructure | 2 | 2 | 3 | **Quick Win** |

**Step 3 — Load Project Memory**:
```
memoryStore.getSkillMemory("legacy-modernizer", "enterprise-app")
→ No existing memory found.

contextProvider.getIndex("java")
contextProvider.getIndex("spring")
```

**Step 4 — Plan & Execute Modernization**:

**Pattern**: Branch by Abstraction for architecture layers + incremental extraction.

**Phase 1 — Foundation & Safety Nets (Weeks 1-4)**:
- Upgrade Spring Boot 1.5 → 2.7 → 3.2 (two-hop migration for compatibility)
- Upgrade Java 8 → 17 (LTS), enable records and sealed classes
- Fix Jackson and Hibernate CVEs as part of the Spring Boot upgrade
- Enable Maven parallel builds (`-T 1C`), reducing build time to ~2 minutes
- Write characterization tests for `ApplicationService`'s 20 most critical methods
- Configure ArchUnit rules to prevent new architectural violations

**Phase 2 — Introduce Domain Layer (Weeks 5-10)**:
- Create package structure following hexagonal architecture:
  ```
  com.company.app/
  ├── domain/          # Entities, value objects, domain services
  │   ├── model/       # Pure domain objects (no JPA annotations)
  │   └── port/        # Interfaces for inbound and outbound
  ├── application/     # Use cases / application services
  ├── adapter/
  │   ├── in/web/      # REST controllers (thin, delegation only)
  │   └── out/persistence/  # JPA repositories, entity mappers
  └── config/          # Spring configuration
  ```
- Extract domain models from JPA entities — create pure POJOs for the domain layer
- Introduce mapper classes (MapStruct) between domain models, JPA entities, and DTOs
- Migrate 5 bounded contexts incrementally, starting with the least coupled

**Phase 3 — Break the God Class (Weeks 11-16)**:
- Decompose `ApplicationService.java` into focused application services:
  - Extract methods by domain concept (Order, User, Product, Payment, Inventory)
  - Each new service implements a port interface from the domain layer
  - Use the Branch by Abstraction pattern: `ApplicationService` delegates to new services behind interfaces
  - Remove methods from `ApplicationService` one group at a time
  - Target: `ApplicationService` reduced to a deprecated facade, then removed
- Resolve circular dependencies by introducing event-based communication:
  - Replace bidirectional `@Autowired` with domain events (`ApplicationEventPublisher`)
  - Each service publishes events, other services subscribe — no direct coupling

**Phase 4 — Controller Cleanup (Weeks 17-22)**:
- Extract business logic from controllers into application services:
  - Controllers become thin adapters: validate input → call use case → map response
  - Each controller method should be ≤15 lines
  - Introduce request/response DTOs separate from domain models
- Add unit tests for each new application service (mock ports)
- Target: 80%+ unit test coverage on domain and application layers, integration tests only for adapters

**Phase 5 — Validation & Stabilization (Weeks 23-24)**:
- Run full regression suite — all 340 existing integration tests must pass
- Run new unit test suite — target 500+ unit tests, <30 second execution
- ArchUnit tests enforce: no domain → adapter dependencies, no circular references
- Performance benchmark: API response times within 5% of pre-modernization baseline

**Step 5 — Review & Output**:
- All 340 integration tests pass, 523 new unit tests added (82% domain coverage)
- ArchUnit catches 0 violations in the new architecture
- API response times improved by 12% due to reduced object graph loading
- Output saved to `/claudedocs/legacy_mod_enterprise_2026-02-12.md`
- Memory created:
  ```
  memoryStore.update("legacy-modernizer", "enterprise-app", {
    debt_inventory: "God class eliminated, 14 circular deps resolved, Spring Boot 3.2 running",
    migration_phase: "Phase 5 complete — clean architecture in place",
    patterns_used: ["branch-by-abstraction", "hexagonal-architecture", "domain-events"],
    lessons: "ArchUnit rules were essential for preventing regression to old patterns. MapStruct saved weeks of manual mapping code. Two-hop Spring Boot upgrade (1.5→2.7→3.2) was safer than direct jump."
  })
  ```

---

## Summary of Modernization Types

1. **Full-stack migration** (jQuery+PHP → React+Node.js) — Strangler Fig with parallel run validation
2. **Language version migration** (Python 2 → 3) — Characterization tests + mechanical transforms + parallel run
3. **Architecture transformation** (Tightly-coupled → Clean Architecture) — Branch by Abstraction + incremental extraction

## Best Practices

- Always build safety nets (characterization tests) before modifying legacy code
- Migrate incrementally — never attempt a big-bang rewrite
- Keep the system deployable at every intermediate step
- Use parallel run to validate critical business logic during migration
- Document decisions as you go — future you will thank present you
- Measure before and after: performance, error rates, test coverage, build times
- Update project memory after each phase to track progress and lessons learned
