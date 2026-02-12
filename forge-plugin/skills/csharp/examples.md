# csharp Examples

Usage scenarios for the `csharp` skill.

---

## Example 1: .NET 8 Upgrade Plan

**User Request**: "Move our ASP.NET Core service from .NET 6 to .NET 8 and adopt new C# features."

**What the skill does**:
- Reviews runtime compatibility and analyzer settings
- Highlights required API changes and new language features (required members, primary constructors)
- Produces a migration checklist and sample updates

**Output**: `/claudedocs/csharp_checkout-api_2026-02-12.md`

---

## Example 2: LINQ Performance Tuning

**User Request**: "Our batch processor is slow. Optimize the LINQ-heavy code path."

**What the skill does**:
- Identifies allocation hotspots and multiple enumeration risks
- Suggests `Span<T>`, pooled collections, and iterative loops where needed
- Summarizes measurable optimizations

**Output**: `/claudedocs/csharp_batch-processor_2026-02-12.md`

---

## Example 3: Background Worker Reliability

**User Request**: "Design a reliable background worker with proper retries and cancellation."

**What the skill does**:
- Reviews hosted service patterns, DI lifetimes, and logging
- Recommends Polly retry policies and graceful shutdown hooks
- Provides a reference implementation outline

**Output**: `/claudedocs/csharp_worker-service_2026-02-12.md`
