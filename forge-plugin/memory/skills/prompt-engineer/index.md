# prompt-engineer Memory

Project-specific memory for LLM prompt patterns, evaluation results, and model-specific optimization notes.

## Purpose

This memory helps the `skill:prompt-engineer` remember:
- Which prompt techniques and patterns work best for each project
- Evaluation results and accuracy metrics across prompt iterations
- Model-specific quirks, limitations, and optimization notes
- Known edge cases and failure modes for project-specific prompts
- Successful patterns that can be reused or adapted for new tasks

## Memory Files Per Project

Each project gets its own directory: `{project-name}/`

### Recommended Files

#### `prompt_patterns.md`
Stores successful prompt templates and techniques used in the project.
- Prompt architecture decisions (zero-shot, few-shot, CoT, etc.)
- System message conventions and role definitions
- Output schema patterns that parse reliably
- Few-shot example selection strategies that proved effective
- Guardrail and safety instruction patterns

#### `evaluation_results.md`
Tracks quality metrics and test results for prompt iterations.
- Accuracy, consistency, and hallucination rates per prompt version
- A/B test results comparing prompt variants
- Regression tracking across model updates
- Edge cases discovered during testing
- Performance benchmarks (latency, token usage, cost)

#### `model_specific_notes.md`
Documents model-specific behaviors and optimization strategies.
- Known quirks or limitations for specific model versions
- Token budget strategies tailored to model context windows
- Format compliance differences between models
- Temperature and sampling parameter recommendations
- Model migration notes when switching between providers

## Usage

Access via the MemoryStore interface:

```
# Load project memory
memoryStore.getSkillMemory("prompt-engineer", "{project-name}")

# Update after successful prompt engineering
memoryStore.update("prompt-engineer", "{project-name}", ...)

# Append new patterns or evaluation results
memoryStore.append("prompt-engineer", "{project-name}", ...)
```

See [MemoryStore Interface](../../../interfaces/memory_store.md) for full method documentation.

## Evolution

Memory accumulates over time as prompts are designed, tested, and refined:
1. **First session**: Basic patterns and initial evaluation results recorded
2. **Subsequent sessions**: Patterns refined, new edge cases documented, model notes expanded
3. **Mature memory**: Comprehensive pattern library with proven techniques, detailed evaluation history, and model-specific playbooks

## Related Documentation

- [Prompt Engineer SKILL.md](../../../skills/prompt-engineer/SKILL.md) — Main skill instructions and workflow
- [Prompt Engineer examples.md](../../../skills/prompt-engineer/examples.md) — Usage scenarios and demonstrations
- [MemoryStore Interface](../../../interfaces/memory_store.md) — Memory access patterns
- [Memory Lifecycle](../../lifecycle.md) — Memory freshness, pruning, and archival policies
- [Memory Quality Guidance](../../quality_guidance.md) — Memory validation standards
