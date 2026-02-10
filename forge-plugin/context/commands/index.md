# Commands Context Index

This directory contains **shared contextual knowledge** for commands. These files provide patterns, strategies, and best practices that commands reference during execution.

## Purpose

Command context files provide:
- **Analysis Patterns**: Methodologies for code analysis and assessment
- **Implementation Strategies**: Approaches for feature development
- **Refactoring Patterns**: Safe improvement techniques
- **Documentation Standards**: Format and style guidelines
- **Testing Strategies**: Test pyramid, coverage, and debugging
- **Build Patterns**: Build system and artifact optimization
- **Brainstorming Patterns**: Requirements discovery techniques

## Available Context Files

| File | Used By | Key Topics |
|------|---------|------------|
| [`analysis_patterns.md`](analysis_patterns.md) | `/analyze` | Static analysis, severity classification, multi-language strategies |
| [`implementation_strategies.md`](implementation_strategies.md) | `/implement` | TDD/BDD, incremental development, testing integration |
| [`refactoring_patterns.md`](refactoring_patterns.md) | `/improve` | Safe refactoring, code smell identification, technical debt |
| [`documentation_standards.md`](documentation_standards.md) | `/document` | API docs, inline comments, architecture docs, README standards |
| [`testing_strategies.md`](testing_strategies.md) | `/test` | Test pyramid, coverage targets, failure debugging |
| [`build_patterns.md`](build_patterns.md) | `/build` | Build systems, Docker builds, caching, artifact optimization |
| [`brainstorming_patterns.md`](brainstorming_patterns.md) | `/brainstorm` | Socratic questioning, requirements elicitation, prioritization |

## Loading Patterns

### For `/analyze`
1. Load `analysis_patterns.md` (always)
2. Load domain-specific context from `../python/`, `../dotnet/`, or `../angular/` based on detected language
3. Load `../security/security_guidelines.md` if security focus

### For `/implement`
1. Load `implementation_strategies.md` (always)
2. Load domain-specific context based on target framework
3. Load `testing_strategies.md` if `--with-tests` flag

### For `/improve`
1. Load `refactoring_patterns.md` (always)
2. Load domain-specific context based on code language
3. Load `analysis_patterns.md` for pre-improvement assessment

### For `/document`
1. Load `documentation_standards.md` (always)
2. Load domain-specific context for language-specific doc conventions

### For `/test`
1. Load `testing_strategies.md` (always)
2. Load domain-specific testing context (`../python/testing_frameworks.md`, `../angular/jest_testing_standards.md`)

### For `/build`
1. Load `build_patterns.md` (always)
2. Load `../azure/` context if Azure-related build

### For `/brainstorm`
1. Load `brainstorming_patterns.md` (always)
2. Load `../schema/` context if data modeling is involved

## Context vs Domain Context

| Aspect | Command Context (this directory) | Domain Context (`../python/`, etc.) |
|--------|----------------------------------|--------------------------------------|
| **Scope** | Cross-cutting command patterns | Language/framework-specific knowledge |
| **Used by** | Commands | Commands and Skills |
| **Content** | Methodologies and strategies | Standards and best practices |
| **Example** | "How to do code analysis" | "Python PEP8 standards" |

Commands should load **both** command context and relevant domain context for comprehensive guidance.

---

## Related Documentation

- **Commands**: See `../../commands/index.md` for command documentation
- **Domain Context**: See `../index.md` for all context domains
- **Memory**: See `../../memory/commands/index.md` for command memory
