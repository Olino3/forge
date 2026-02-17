---
name: prompt-engineer
## description: Masters the art and science of LLM prompt design, optimization, and evaluation. Specializes in chain-of-thought engineering, few-shot optimization, evaluation frameworks, and systematic prompt iteration. Like Hephaestus calibrating the heat of the forge to produce the finest alloys, this skill tunes every token and instruction to extract maximum quality, reliability, and consistency from language model interactions.

# Prompt Engineer

## ⚠️ MANDATORY COMPLIANCE ⚠️

**CRITICAL**: The 5-step workflow outlined in this document MUST be followed in exact order for EVERY prompt engineering task. Skipping steps or deviating from the procedure will result in suboptimal, unreliable, or insecure prompts. This is non-negotiable.

## File Structure

- **SKILL.md** (this file): Main instructions and MANDATORY workflow
- **examples.md**: Usage scenarios with different prompt engineering techniques and outputs
- **Memory**: Project-specific memory accessed via `memoryStore.getSkillMemory("prompt-engineer", "{project-name}")`. See [MemoryStore Interface](../../interfaces/memory_store.md).

## Interface References

- **ContextProvider**: Load domain knowledge via `contextProvider.getIndex("{domain}")`. See [ContextProvider Interface](../../interfaces/context_provider.md).
- **MemoryStore**: Read/write project-specific prompt patterns and evaluation results via `memoryStore`. See [MemoryStore Interface](../../interfaces/memory_store.md).
- **Schemas**: Validate configuration against [agent_config.schema.json](../../interfaces/schemas/agent_config.schema.json) and [memory_entry.schema.json](../../interfaces/schemas/memory_entry.schema.json).

## Focus Areas

Prompt engineering evaluates 7 critical dimensions:

1. **Prompt Architecture**: Design system/user/assistant role assignments, maximize instruction clarity, and specify constraints precisely to guide model behavior
2. **Few-Shot Design**: Select diverse, representative examples with consistent formatting, optimal ordering, and appropriate quantity for the task
3. **Chain-of-Thought Engineering**: Build reasoning scaffolds, decompose complex tasks into verifiable steps, and construct verification chains that catch errors
4. **Output Formatting**: Enforce structured output (JSON, XML, Markdown) through schema specification, format examples, and parsing-reliable patterns
5. **Evaluation & Metrics**: Measure accuracy, consistency, and hallucination rates; design A/B testing frameworks for prompt variants and track quality regressions
6. **Context Window Management**: Budget tokens across system instructions, examples, and user content; implement chunking strategies and priority ordering for long inputs
7. **Prompt Security**: Prevent injection attacks, establish guardrails against misuse, sanitize inputs, and validate outputs against expected schemas and content policies

**Note**: The skill designs and optimizes prompts. It does not deploy prompts to production systems unless explicitly requested.

---

## Purpose

[TODO: Add purpose description]


## MANDATORY WORKFLOW (MUST FOLLOW EXACTLY)

### ⚠️ STEP 1: Analyze Prompt Requirements (REQUIRED)

**YOU MUST:**
1. Identify the target task — what the prompt needs to accomplish
2. Determine the target model and its constraints (context window size, supported features, known strengths/weaknesses)
3. Define quality criteria — what constitutes a successful output (accuracy, format, tone, completeness)
4. Identify input variability — what range of inputs the prompt must handle robustly
5. Clarify constraints — latency requirements, token budget limits, cost considerations, safety requirements

**DO NOT PROCEED WITHOUT UNDERSTANDING THE REQUIREMENTS**

### ⚠️ STEP 2: Design Prompt Architecture (REQUIRED)

**YOU MUST:**
1. **Select the technique**: Choose the appropriate prompting strategy based on task complexity:
   - Zero-shot for simple, well-defined tasks
   - Few-shot for tasks requiring pattern demonstration
   - Chain-of-thought for multi-step reasoning
   - ReAct for tasks requiring tool use or external information
   - Tree of Thought for tasks requiring exploration of multiple solution paths
2. **Structure the template**: Define the system message, user message format, and expected assistant response format
3. **Plan examples**: If using few-shot, select examples that cover edge cases, demonstrate desired output format, and represent input diversity
4. **Define output schema**: Specify the exact output format (JSON schema, Markdown structure, XML DTD) the prompt must produce
5. **Establish guardrails**: Add safety instructions, refusal conditions, and output validation rules

**DO NOT PROCEED WITHOUT A CLEAR ARCHITECTURE**

### ⚠️ STEP 3: Load Project Memory (REQUIRED)

**YOU MUST:**
1. Load project-specific prompt patterns and conventions:
   ```
   memoryStore.getSkillMemory("prompt-engineer", "{project-name}")
   ```
   See [MemoryStore Interface](../../interfaces/memory_store.md) for method details.
2. Review previously successful prompt patterns for this project
3. Check known model-specific quirks or limitations documented in memory
4. Load relevant evaluation results from past iterations
5. If no project memory exists, proceed with general best practices and note that memory should be initialized

**DO NOT PROCEED WITHOUT CHECKING PROJECT MEMORY**

### ⚠️ STEP 4: Craft & Optimize Prompt (REQUIRED)

**YOU MUST:**
1. **Write the initial prompt** following the architecture from Step 2
2. **Apply optimization techniques**:
   - Use precise, unambiguous language — avoid vague instructions
   - Place critical instructions at the beginning and end of the prompt (primacy and recency effects)
   - Use delimiters (```, """, XML tags) to clearly separate sections
   - Include negative examples or explicit "do not" instructions for common failure modes
3. **Test with representative inputs**: Run the prompt against diverse inputs to verify quality
4. **Iterate on failures**: Analyze any incorrect outputs, identify root causes, and refine the prompt
5. **Evaluate against quality criteria**: Verify the prompt meets all criteria defined in Step 1

**DO NOT USE VAGUE OR UNTESTED PROMPTS**

### ⚠️ STEP 5: Review & Output (REQUIRED)

**YOU MUST validate the prompt against these criteria:**
1. **Clarity check**:
   - [ ] Instructions are unambiguous and self-contained
   - [ ] Role assignments are clear and consistent
   - [ ] Output format is explicitly specified with examples
2. **Robustness check**:
   - [ ] Handles edge cases and unexpected inputs gracefully
   - [ ] Includes fallback instructions for ambiguous situations
   - [ ] Tested against adversarial or malformed inputs
3. **Security check**:
   - [ ] Resistant to prompt injection attempts
   - [ ] Output validation rules prevent data leakage
   - [ ] Guardrails prevent harmful or off-topic outputs
4. **Output the final prompt** to `/claudedocs/` following output naming conventions
5. **Update project memory** with successful patterns:
   ```
   memoryStore.update("prompt-engineer", "{project-name}", ...)
   ```
   See [MemoryStore Interface](../../interfaces/memory_store.md) for `update()` and `append()` method details.

**DO NOT SKIP VALIDATION**

---

### Step 6: Generate Output

Create deliverables and save to `/claudedocs/`:
- Follow OUTPUT_CONVENTIONS.md naming: `prompt-engineer_{project}_{YYYY-MM-DD}.md`
- Include all required sections
- Provide clear, actionable recommendations

## Compliance Checklist

Before completing ANY prompt engineering task, verify:
- [ ] Step 1: Requirements analyzed — task, model, quality criteria, and constraints defined
- [ ] Step 2: Architecture designed — technique selected, template structured, examples planned
- [ ] Step 3: Project memory loaded — prior patterns and evaluation results reviewed
- [ ] Step 4: Prompt crafted and tested — iterations completed, quality criteria met
- [ ] Step 5: Prompt validated against clarity, robustness, and security checks; output saved and memory updated

**FAILURE TO COMPLETE ALL STEPS INVALIDATES THE PROMPT**

---

## Output File Naming Convention

**Format**: `prompt_{task_name}_{version}.md`

Where:
- `{task_name}` = Descriptive name of the prompt's purpose (snake_case)
- `{version}` = Version identifier (e.g., `v1`, `v2`)

**Examples**:
- `prompt_code_review_v1.md`
- `prompt_ticket_classifier_v2.md`
- `prompt_math_reasoning_v1.md`

---

## Prompt Techniques Reference

| Technique | Best For | Complexity |
|-----------|----------|------------|
| **Zero-shot** | Simple, well-defined tasks with clear instructions | Low |
| **Few-shot** | Pattern-based tasks requiring format demonstration | Medium |
| **Chain-of-Thought (CoT)** | Multi-step reasoning, math, logic problems | Medium |
| **Zero-shot CoT** | Reasoning tasks without example overhead ("Let's think step by step") | Low-Medium |
| **ReAct** | Tasks requiring tool use, search, or external data retrieval | High |
| **Tree of Thought** | Complex problems requiring exploration of multiple solution paths | High |
| **Self-Consistency** | Improving reliability by sampling multiple reasoning paths and voting | Medium |
| **Reflexion** | Iterative self-improvement through reflection on prior outputs | High |
| **Least-to-Most** | Complex tasks that can be decomposed into simpler sub-problems | Medium |
| **Directional Stimulus** | Guiding generation with hints or keywords toward desired output | Low-Medium |

---

## Further Reading

Refer to official documentation and research:
- **Prompting Guides**:
  - OpenAI Prompt Engineering Guide: https://platform.openai.com/docs/guides/prompt-engineering
  - Anthropic Prompt Engineering Guide: https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview
- **Research**:
  - Chain-of-Thought Prompting (Wei et al., 2022): https://arxiv.org/abs/2201.11903
  - ReAct: Synergizing Reasoning and Acting (Yao et al., 2022): https://arxiv.org/abs/2210.03629
  - Tree of Thoughts (Yao et al., 2023): https://arxiv.org/abs/2305.10601

---

## Version History

- v1.0.0 (2026-02-12): Initial release
  - Mandatory 5-step workflow for prompt engineering
  - 7 focus areas covering architecture through security
  - Prompt techniques reference table
  - Interface-based memory and context access
  - Output naming conventions and compliance checklist
