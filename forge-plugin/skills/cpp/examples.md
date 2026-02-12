# cpp Examples

Practical scenarios for the `cpp` skill.

---

## Example 1: Modernize Legacy C++14 Module

**User Request**: "Upgrade our C++14 utilities to C++20 with safer memory handling and clearer APIs."

**What the skill does**:
- Confirms compiler targets (GCC 13, Clang 17) and C++20 enablement
- Recommends migrating raw pointers to `std::unique_ptr` and `std::span`
- Outputs a modernization plan and example refactor snippet

**Output**: `/claudedocs/cpp_utilities_2026-02-12.md`

---

## Example 2: Low-Latency Trading Pipeline Review

**User Request**: "Audit our market data pipeline for latency bottlenecks and lock contention."

**What the skill does**:
- Loads project memory for build flags and threading model
- Reviews allocator usage, queue designs, and cache-line alignment
- Suggests lock-free ring buffer patterns and measurable metrics

**Output**: `/claudedocs/cpp_trading-pipeline_2026-02-12.md`

---

## Example 3: Public SDK API Design

**User Request**: "Design a stable C++ SDK API for partners with ABI compatibility guarantees."

**What the skill does**:
- Clarifies ABI policy (Itanium vs MSVC) and release cadence
- Provides guidance on pimpl usage, symbol visibility, and versioning
- Produces a checklist for binary compatibility and upgrade paths

**Output**: `/claudedocs/cpp_partner-sdk_2026-02-12.md`
