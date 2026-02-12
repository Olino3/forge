# cpp Memory

Project-specific memory for the `cpp` skill. Store per-project conventions, toolchain details, and performance notes.

## Directory Structure

```
cpp/
└── {project-name}/
    ├── project_overview.md
    ├── toolchain_profile.md
    ├── performance_notes.md
    └── known_issues.md
```

## Memory Files

### `project_overview.md`

- Project purpose, domain, and architecture
- Target platforms, compilers, and supported C++ standard

### `toolchain_profile.md`

- Build system details (CMake/Bazel), compiler flags, sanitizers
- CI/CD notes, formatting, and static analysis tooling

### `performance_notes.md`

- Hot paths, allocation strategies, and benchmarking baselines
- Concurrency model and known contention points

### `known_issues.md`

- Documented technical debt, unsafe patterns, and migration goals
