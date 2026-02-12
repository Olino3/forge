# Open Source Contributions Examples

This file contains example scenarios demonstrating how to use the open-source-contributions skill to prepare maintainer-friendly pull requests across different languages, project types, and contribution categories.

---

## Example 1: Contributing a Bug Fix to a Popular React Library

### Scenario

A developer discovers a bug in a popular React UI component library where the `<DatePicker>` component crashes when the `locale` prop is changed dynamically. The issue is tracked as #4821 in the project's GitHub repository. The project uses Conventional Commits, Jest for testing, and requires a CLA signature.

### User Prompt
```
I want to fix the DatePicker locale crash in react-awesome-ui. The issue is #4821 — the component throws a TypeError when switching locale from "en-US" to "ja-JP" at runtime.
```

### Skill Execution

**Step 1 - Initial Analysis**:
- Target project: `react-awesome-ui` (MIT license, 15k stars)
- Issue #4821: `<DatePicker>` throws `TypeError: Cannot read properties of undefined (reading 'months')` when `locale` prop changes after initial render
- `CONTRIBUTING.md` found: requires fork workflow, Conventional Commits, test coverage, CLA
- Issue is open, labeled `bug` and `good first issue`, unassigned
- Maintainer comment on issue: "This is likely in `useDateFormatter` hook — the locale cache isn't invalidated on prop change"

**Step 2 - Load Memory**:
```
memoryStore.getSkillMemory("open-source-contributions", "react-awesome-ui")
```
No prior memory found — first contribution to this project.

**Step 3 - Load Context**:
```
contextProvider.getIndex("engineering")
```
Load relevant engineering context for React component patterns and testing.

**Step 4 - Analyze Project Conventions**:
- **Commit format**: Conventional Commits with scopes matching component names (e.g., `fix(datepicker): ...`)
- **Branch naming**: `fix/issue-{number}` pattern observed in merged PRs
- **Code style**: ESLint + Prettier, 2-space indent, single quotes, semicolons
- **Test framework**: Jest + React Testing Library, tests colocated in `__tests__/` directories
- **CI pipeline**: GitHub Actions — lint, typecheck, unit tests, visual regression tests
- **PR template**: Requires issue reference, description, test plan, and checklist

**Step 5 - Prepare Clean Contribution**:

Fork and create branch:
```bash
gh repo fork awesome-org/react-awesome-ui --clone
cd react-awesome-ui
git checkout -b fix/issue-4821
```

Identify the bug in `src/components/DatePicker/useDateFormatter.ts`:
```typescript
// Bug: locale cache is initialized once and never updated
const formatterCache = useRef(createFormatter(locale));

// Fix: invalidate cache when locale changes
const formatterCache = useRef(createFormatter(locale));
useEffect(() => {
  formatterCache.current = createFormatter(locale);
}, [locale]);
```

Add test in `src/components/DatePicker/__tests__/DatePicker.test.tsx`:
```typescript
it('should handle dynamic locale changes without crashing', () => {
  const { rerender } = render(<DatePicker locale="en-US" />);
  expect(screen.getByRole('textbox')).toBeInTheDocument();

  rerender(<DatePicker locale="ja-JP" />);
  expect(screen.getByRole('textbox')).toBeInTheDocument();
  expect(screen.getByText('月')).toBeInTheDocument();
});
```

Commit:
```
fix(datepicker): invalidate locale cache on dynamic prop change

The useDateFormatter hook cached the date formatter on initial render
but never updated it when the locale prop changed. This caused a
TypeError when accessing locale-specific month names after a locale
switch.

Add a useEffect to rebuild the formatter cache whenever the locale
prop changes.

Fixes #4821
```

**Step 6 - Craft PR Description**:
```markdown
## Fix: DatePicker crashes on dynamic locale change

Fixes #4821

### Problem
The `<DatePicker>` component throws a `TypeError` when the `locale` prop
is changed after initial render. The `useDateFormatter` hook caches the
formatter on mount but never invalidates the cache on prop changes.

### Solution
Add a `useEffect` in `useDateFormatter` that rebuilds the formatter
cache whenever the `locale` dependency changes. This ensures the
component always uses a formatter matching the current locale.

### Testing
- Added unit test for dynamic locale switching (en-US → ja-JP)
- All existing tests pass (`npm test` — 347 passed, 0 failed)
- Manual testing confirmed no crash on rapid locale toggling

### Checklist
- [x] Code follows project style guidelines
- [x] Tests added for the fix
- [x] All CI checks pass locally
- [x] CLA signed
```

**Step 7 - Pre-Submission Checklist**:
- ✅ `npm run lint` — no errors
- ✅ `npm run typecheck` — no type errors
- ✅ `npm test` — 348 tests passed (347 existing + 1 new)
- ✅ Single commit, focused on one fix
- ✅ Branch rebased on latest `main`
- ✅ CLA signed via bot

---

## Example 2: Adding a New Feature to a Python CLI Tool

### Scenario

A developer wants to add CSV export functionality to an open-source Python CLI tool for database management. The feature was requested in issue #256. The project uses `pyproject.toml` for configuration, `pytest` for testing, `ruff` for linting, and follows the fork-and-branch contribution model with detailed documentation requirements.

### User Prompt
```
I want to add CSV export to the db-toolkit CLI. Issue #256 requests a `db-toolkit export --format csv` command. The project is well-documented and expects thorough docs with any new feature.
```

### Skill Execution

**Step 1 - Initial Analysis**:
- Target project: `db-toolkit` (Apache-2.0 license, CLI tool for database operations)
- Issue #256: Feature request for CSV export via `db-toolkit export --format csv`
- `CONTRIBUTING.md`: Fork workflow, feature branches named `feature/{description}`, requires docs update, changelog entry, and 90%+ test coverage on new code
- Maintainer comment: "Happy to accept this. Please add it as a new format handler in the exporter module. Don't forget to update the man page."

**Step 2 - Load Memory**:
```
memoryStore.getSkillMemory("open-source-contributions", "db-toolkit")
```
No prior memory found — first contribution.

**Step 3 - Load Context**:
```
contextProvider.getIndex("engineering")
```
Load relevant Python engineering context.

**Step 4 - Analyze Project Conventions**:
- **Commit format**: Conventional Commits, scopes match module names (e.g., `feat(exporter): ...`)
- **Branch naming**: `feature/{short-description}` for features
- **Code style**: `ruff` linter + `ruff format`, line length 88, type hints required on all public functions
- **Test framework**: `pytest` with fixtures in `conftest.py`, coverage enforced at 90%
- **CI pipeline**: GitHub Actions — ruff check, mypy, pytest with coverage, doc build
- **Documentation**: Sphinx docs in `docs/`, man pages auto-generated, changelog in `CHANGELOG.md`
- **Architecture**: Format handlers implement `BaseExporter` abstract class

**Step 5 - Prepare Clean Contribution**:

Fork and create branch:
```bash
gh repo fork db-org/db-toolkit --clone
cd db-toolkit
git checkout -b feature/csv-export
```

Create `src/db_toolkit/exporters/csv_exporter.py`:
```python
"""CSV format exporter for database query results."""

import csv
import io
from typing import TextIO

from db_toolkit.exporters.base import BaseExporter, ExportResult


class CsvExporter(BaseExporter):
    """Export query results to CSV format."""

    format_name = "csv"

    def export(self, rows: list[dict], output: TextIO) -> ExportResult:
        if not rows:
            return ExportResult(rows_written=0, format="csv")

        writer = csv.DictWriter(output, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

        return ExportResult(rows_written=len(rows), format="csv")
```

Register the exporter in `src/db_toolkit/exporters/__init__.py`:
```python
from db_toolkit.exporters.csv_exporter import CsvExporter

EXPORTERS = {
    "json": JsonExporter,
    "csv": CsvExporter,  # new
}
```

Add comprehensive tests in `tests/exporters/test_csv_exporter.py`:
```python
class TestCsvExporter:
    def test_export_basic_rows(self, sample_rows, tmp_path):
        output_file = tmp_path / "output.csv"
        with open(output_file, "w") as f:
            result = CsvExporter().export(sample_rows, f)
        assert result.rows_written == 3
        assert "name,email,age" in output_file.read_text()

    def test_export_empty_rows(self, tmp_path):
        output_file = tmp_path / "output.csv"
        with open(output_file, "w") as f:
            result = CsvExporter().export([], f)
        assert result.rows_written == 0

    def test_export_special_characters(self, tmp_path):
        rows = [{"name": 'O\'Brien, "Jim"', "note": "line1\nline2"}]
        output_file = tmp_path / "output.csv"
        with open(output_file, "w") as f:
            CsvExporter().export(rows, f)
        content = output_file.read_text()
        assert "O'Brien" in content

    def test_export_unicode(self, tmp_path):
        rows = [{"name": "日本語テスト", "city": "東京"}]
        output_file = tmp_path / "output.csv"
        with open(output_file, "w", encoding="utf-8") as f:
            CsvExporter().export(rows, f)
        assert "日本語テスト" in output_file.read_text(encoding="utf-8")
```

Update `docs/usage.rst` with CSV export documentation. Add changelog entry. Update man page source.

Commits (atomic):
```
feat(exporter): add CSV format handler

Implement CsvExporter extending BaseExporter to support CSV output
format. Handles header generation, special character escaping, and
Unicode content.

Refs #256
```
```
test(exporter): add comprehensive tests for CSV exporter

Cover basic export, empty input, special characters, and Unicode
content. All tests use pytest tmp_path fixture for isolated output.
```
```
docs: add CSV export usage guide and changelog entry

Document the --format csv option in usage guide with examples.
Add entry to CHANGELOG.md under Unreleased section. Update man
page source with new format option.

Closes #256
```

**Step 6 - Craft PR Description**:
```markdown
## Feature: Add CSV Export Format

Closes #256

### Summary
Add CSV as a supported export format for the `db-toolkit export` command.
Users can now run `db-toolkit export --format csv` to export query results
as comma-separated values.

### Changes
- **New**: `CsvExporter` class in `src/db_toolkit/exporters/csv_exporter.py`
  implementing `BaseExporter` interface
- **Modified**: Exporter registry to include CSV format
- **Tests**: 4 test cases covering basic rows, empty input, special
  characters, and Unicode content (100% coverage on new code)
- **Docs**: Usage guide updated, changelog entry added, man page updated

### Design Decisions
- Used stdlib `csv.DictWriter` — no new dependencies required
- Follows the same `BaseExporter` pattern as `JsonExporter`
- Header row is always included (consistent with common CSV conventions)

### Testing
```
$ pytest tests/exporters/test_csv_exporter.py -v
4 passed in 0.12s

$ pytest --cov=src/db_toolkit/exporters/csv_exporter
Coverage: 100%
```

### Checklist
- [x] Follows `BaseExporter` interface pattern
- [x] Code passes `ruff check` and `mypy`
- [x] Test coverage ≥90% on new code (100%)
- [x] Documentation updated (usage guide, changelog, man page)
- [x] Commits follow Conventional Commits format
```

**Step 7 - Pre-Submission Checklist**:
- ✅ `ruff check .` — no errors
- ✅ `mypy src/` — no type errors
- ✅ `pytest` — all tests pass, coverage 100% on new code
- ✅ Three atomic commits, each focused on one concern
- ✅ Branch rebased on latest `main`
- ✅ No unrelated changes in diff

---

## Example 3: Submitting a Performance Improvement to a Go Microservice

### Scenario

A developer identifies a performance bottleneck in an open-source Go microservice where the JSON serialization in a hot path is causing excessive allocations. The project tracks issues in GitHub, uses `golangci-lint`, requires benchmarks for performance PRs, and follows a squash-merge strategy. Issue #189 describes the slow response times.

### User Prompt
```
I want to submit a performance fix for the user-api Go microservice. Issue #189 reports that the /users/search endpoint is slow under load. I've profiled it and the bottleneck is in JSON serialization — encoding/json is allocating heavily. I want to switch the hot path to use jsoniter for zero-allocation encoding.
```

### Skill Execution

**Step 1 - Initial Analysis**:
- Target project: `user-api` (BSD-3-Clause license, Go microservice)
- Issue #189: `/users/search` P99 latency spikes to 200ms under load, expected <50ms
- `CONTRIBUTING.md`: Fork workflow, performance PRs require before/after benchmarks, squash merge on merge
- Maintainer comment: "We're open to alternative JSON encoders if benchmarks show clear improvement. Please ensure backward compatibility — output must be byte-identical."

**Step 2 - Load Memory**:
```
memoryStore.getSkillMemory("open-source-contributions", "user-api")
```
No prior memory found — first contribution.

**Step 3 - Load Context**:
```
contextProvider.getIndex("engineering")
```
Load relevant Go engineering context.

**Step 4 - Analyze Project Conventions**:
- **Commit format**: Conventional Commits with Go package as scope (e.g., `perf(handler): ...`)
- **Branch naming**: `perf/{description}` for performance improvements
- **Code style**: `golangci-lint` with strict config, `gofmt` enforced, error wrapping with `fmt.Errorf("...: %w", err)`
- **Test framework**: Standard `testing` package, table-driven tests, benchmarks in `_test.go` files
- **CI pipeline**: GitHub Actions — golangci-lint, go test -race, go vet, benchmark comparison
- **Performance PRs**: Must include benchmark results comparing before/after, use `benchstat` for statistical comparison
- **Dependencies**: New dependencies require justification; prefer stdlib unless significant benefit shown

**Step 5 - Prepare Clean Contribution**:

Fork and create branch:
```bash
gh repo fork microservices-org/user-api --clone
cd user-api
git checkout -b perf/json-serialization-189
```

Add benchmark first to establish baseline in `internal/handler/search_bench_test.go`:
```go
func BenchmarkSearchHandler_Serialize(b *testing.B) {
    users := generateTestUsers(1000)
    b.ResetTimer()
    b.ReportAllocs()
    for i := 0; i < b.N; i++ {
        var buf bytes.Buffer
        if err := serializeUsers(users, &buf); err != nil {
            b.Fatal(err)
        }
        buf.Reset()
    }
}
```

Run baseline benchmarks:
```bash
go test -bench=BenchmarkSearchHandler_Serialize -benchmem -count=10 \
  ./internal/handler/ > bench_before.txt
```

Optimize `internal/handler/serialize.go`:
```go
import jsoniter "github.com/json-iterator/go"

var json = jsoniter.ConfigCompatibleWithStandardLibrary

func serializeUsers(users []User, w io.Writer) error {
    encoder := json.NewEncoder(w)
    return encoder.Encode(users)
}
```

Run optimized benchmarks and compare:
```bash
go test -bench=BenchmarkSearchHandler_Serialize -benchmem -count=10 \
  ./internal/handler/ > bench_after.txt
benchstat bench_before.txt bench_after.txt
```

Results:
```
name                              old time/op    new time/op    delta
SearchHandler_Serialize-8          4.52ms ± 2%    1.23ms ± 1%   -72.8%  (p=0.000)

name                              old alloc/op   new alloc/op   delta
SearchHandler_Serialize-8          2.34MB ± 0%    0.12MB ± 0%   -94.9%  (p=0.000)

name                              old allocs/op  new allocs/op  delta
SearchHandler_Serialize-8          15.2k ± 0%      1.2k ± 0%   -92.1%  (p=0.000)
```

Verify output compatibility:
```go
func TestSerializeUsers_OutputCompatibility(t *testing.T) {
    users := []User{{ID: 1, Name: "Alice", Email: "alice@example.com"}}

    var stdBuf, optBuf bytes.Buffer
    stdEncoder := stdjson.NewEncoder(&stdBuf)
    stdEncoder.Encode(users)

    serializeUsers(users, &optBuf)

    if stdBuf.String() != optBuf.String() {
        t.Errorf("output mismatch:\nstd: %s\nopt: %s", stdBuf.String(), optBuf.String())
    }
}
```

Commit:
```
perf(handler): replace encoding/json with jsoniter for search serialization

Switch the /users/search response serialization from encoding/json to
json-iterator/go using ConfigCompatibleWithStandardLibrary for
byte-identical output.

Benchmarks show 72.8% reduction in latency and 94.9% reduction in
allocations for serializing 1000 user records.

Fixes #189
```

**Step 6 - Craft PR Description**:
```markdown
## Perf: Optimize JSON Serialization in Search Endpoint

Fixes #189

### Problem
The `/users/search` endpoint exhibits P99 latency spikes to ~200ms under
load. Profiling (`go tool pprof`) shows 68% of CPU time spent in
`encoding/json.Marshal` with excessive heap allocations causing GC
pressure.

### Solution
Replace `encoding/json` with `github.com/json-iterator/go` using
`ConfigCompatibleWithStandardLibrary` to ensure byte-identical output
while dramatically reducing allocations.

### Benchmark Results (10 runs, `benchstat`)
| Metric | Before | After | Delta |
|--------|--------|-------|-------|
| Time/op | 4.52ms | 1.23ms | **-72.8%** |
| Alloc/op | 2.34MB | 0.12MB | **-94.9%** |
| Allocs/op | 15,200 | 1,200 | **-92.1%** |

### Output Compatibility
Added `TestSerializeUsers_OutputCompatibility` to verify the optimized
encoder produces byte-identical output to `encoding/json`. This test
runs in CI to prevent regressions.

### New Dependency
- `github.com/json-iterator/go` v1.1.12
- Justification: 73% latency reduction, stdlib-compatible API, widely
  adopted (used by Kubernetes, Docker, Istio)

### Testing
- All existing tests pass (`go test -race ./...`)
- Benchmark added for serialization path
- Output compatibility test added
- Manual load test: P99 dropped from 200ms to 48ms

### Checklist
- [x] Benchmarks included with `benchstat` comparison
- [x] Output byte-identical to encoding/json
- [x] `golangci-lint` passes
- [x] `go test -race` passes
- [x] New dependency justified
- [x] Single focused change
```

**Step 7 - Pre-Submission Checklist**:
- ✅ `golangci-lint run` — no issues
- ✅ `go test -race ./...` — all tests pass
- ✅ `go vet ./...` — no issues
- ✅ Benchmark results included with statistical significance
- ✅ Output compatibility verified by test
- ✅ Single commit, squash-merge ready
- ✅ Branch rebased on latest `main`

---

## Summary of Contribution Types

1. **Bug fix** — Fork, isolate the bug, write a failing test, fix it, verify CI
2. **New feature** — Fork, implement following project patterns, document thoroughly, test comprehensively
3. **Performance improvement** — Fork, benchmark before/after, optimize, prove improvement statistically

## Best Practices

- Always read `CONTRIBUTING.md` before writing a single line of code
- Match the project's code style exactly — don't impose your preferences
- One PR = one concern — never bundle unrelated changes
- Write the PR description for someone who has never seen the codebase
- Include measurable evidence for performance claims
- Respond promptly and graciously to reviewer feedback
- Sign the CLA if required — don't make the maintainer ask
- Thank the maintainers — they're volunteering their time
