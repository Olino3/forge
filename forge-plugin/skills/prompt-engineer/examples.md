# Prompt Engineer Examples

This file contains example scenarios demonstrating how to use the prompt-engineer skill to design, optimize, and evaluate LLM prompts for various tasks.

---

## Example 1: Designing a Code Review Prompt with Structured JSON Output

### Scenario
A development team needs an LLM prompt that reviews pull request diffs and returns structured JSON feedback with severity ratings, affected files, and actionable suggestions.

### User Prompt
```
Design a prompt that reviews code diffs and outputs structured JSON with findings
```

### Skill Execution

**Step 1 - Analyze Prompt Requirements**:
- **Task**: Automated code review producing machine-parseable output
- **Target model**: Claude 3.5 Sonnet (200K context window)
- **Quality criteria**: Accurate issue detection, consistent JSON schema, no false positives on style-only issues
- **Input variability**: Diffs range from 5 lines to 2000+ lines, multiple languages (Python, TypeScript, Go)
- **Constraints**: Output must conform to a strict JSON schema for integration with CI pipeline

**Step 2 - Design Prompt Architecture**:
- **Technique**: Zero-shot with structured output specification
- **Template structure**: System message defines reviewer persona and JSON schema; user message contains the diff
- **Output schema**: JSON array of findings, each with `file`, `line`, `severity`, `category`, `message`, and `suggestion` fields
- **Guardrails**: Instruct model to return empty array if no issues found; never fabricate line numbers

**Step 3 - Load Project Memory**:
```
memoryStore.getSkillMemory("prompt-engineer", "ci-review-bot")
```
- Previous iterations showed the model sometimes invents line numbers for large diffs — added explicit instruction to only reference lines present in the diff
- Project uses ESLint for style, so prompt should skip style-only issues

**Step 4 - Craft & Optimize Prompt**:

```markdown
## System Message

You are an expert code reviewer. Analyze the provided code diff and identify bugs,
security vulnerabilities, performance issues, and logic errors.

Return your findings as a JSON array conforming to this exact schema:

{
  "findings": [
    {
      "file": "string — exact file path from the diff header",
      "line": "number — line number from the diff, must exist in the provided diff",
      "severity": "critical | high | medium | low",
      "category": "bug | security | performance | logic | maintainability",
      "message": "string — concise description of the issue",
      "suggestion": "string — specific actionable fix"
    }
  ]
}

Rules:
- ONLY reference line numbers that appear in the diff. Never fabricate line numbers.
- Skip style and formatting issues — those are handled by linters.
- If no issues are found, return: {"findings": []}
- Focus on correctness and security over subjective preferences.
- Each finding must include a concrete, actionable suggestion.

## User Message

Review the following diff:

```diff
{diff_content}
```​
```

**Testing**: Ran against 5 representative diffs:
- ✅ Small Python fix (3 lines) — correctly returned empty findings
- ✅ TypeScript API endpoint (80 lines) — caught missing input validation (severity: high)
- ✅ Go concurrency code (120 lines) — identified race condition (severity: critical)
- ✅ Large refactor (500 lines) — correctly flagged 2 issues, no fabricated line numbers
- ✅ Empty diff — returned `{"findings": []}`

**Step 5 - Review & Output**:
- ✅ Instructions are unambiguous — JSON schema explicitly defined
- ✅ Handles edge cases — empty diff, no issues, large diffs
- ✅ Security — no injection surface, output constrained to JSON schema
- ✅ Line number fabrication addressed with explicit rule

Output saved to `/claudedocs/prompt_code_review_v1.md`

---

## Example 2: Creating a Few-Shot Classification Prompt for Customer Support Tickets

### Scenario
A support team needs a prompt that classifies incoming customer tickets into categories and priority levels to route them to the correct team.

### User Prompt
```
Build a few-shot prompt to classify customer support tickets by category and priority
```

### Skill Execution

**Step 1 - Analyze Prompt Requirements**:
- **Task**: Multi-label classification — assign category and priority to support tickets
- **Target model**: GPT-4o (128K context)
- **Quality criteria**: >95% accuracy on known categories, consistent format, graceful handling of ambiguous tickets
- **Input variability**: Tickets range from one-line complaints to multi-paragraph technical descriptions; some include screenshots (text-only for now)
- **Constraints**: Must classify into exactly 6 categories and 3 priority levels; response under 100 tokens

**Step 2 - Design Prompt Architecture**:
- **Technique**: Few-shot with 6 diverse examples (one per category)
- **Template structure**: System message defines categories and priorities; few-shot examples demonstrate classification; user message contains the new ticket
- **Output schema**: JSON with `category`, `priority`, and `confidence` fields
- **Example selection strategy**: One example per category, varying priority levels, mix of short and detailed tickets
- **Guardrails**: If ticket doesn't fit any category, classify as "general" with low confidence

**Step 3 - Load Project Memory**:
```
memoryStore.getSkillMemory("prompt-engineer", "support-classifier")
```
- No existing memory — initializing for first use
- Noted: Will store evaluation results after deployment

**Step 4 - Craft & Optimize Prompt**:

```markdown
## System Message

You are a customer support ticket classifier. Classify each ticket into exactly one
category and one priority level.

Categories:
- billing: Payment issues, invoices, refunds, subscription changes
- technical: Bugs, errors, crashes, integration failures
- account: Login problems, password resets, account settings, permissions
- feature_request: New feature suggestions, enhancement requests
- onboarding: Setup help, getting started questions, documentation
- general: Anything that doesn't fit the above categories

Priority levels:
- urgent: Service is down, data loss, security breach, payment failure
- normal: Feature broken but workaround exists, non-critical bugs
- low: Questions, suggestions, minor cosmetic issues

Respond with JSON only. No additional text.

## Examples

Ticket: "I've been charged twice for my Pro subscription this month. Order #88412."
{"category": "billing", "priority": "urgent", "confidence": 0.97}

Ticket: "The export to CSV button gives a 500 error when I select more than 100 rows."
{"category": "technical", "priority": "normal", "confidence": 0.95}

Ticket: "I can't log in after changing my email address yesterday. Password reset doesn't send to my new email."
{"category": "account", "priority": "urgent", "confidence": 0.93}

Ticket: "It would be great if the dashboard supported dark mode."
{"category": "feature_request", "priority": "low", "confidence": 0.98}

Ticket: "Just signed up — where do I find the API docs for the webhook integration?"
{"category": "onboarding", "priority": "low", "confidence": 0.92}

Ticket: "Your product is amazing, just wanted to say thanks to the team!"
{"category": "general", "priority": "low", "confidence": 0.90}

## User Message

Ticket: "{ticket_text}"
```

**Testing**: Ran against 20 held-out tickets:
- ✅ 19/20 classified correctly (95% accuracy)
- ✅ 1 ambiguous ticket ("billing + technical") classified as billing — acceptable since payment was the primary concern
- ✅ All outputs valid JSON with correct schema
- ✅ Confidence scores correlate with classification difficulty

**Step 5 - Review & Output**:
- ✅ Clarity — categories and priorities explicitly defined with descriptions
- ✅ Robustness — examples cover all 6 categories, "general" acts as fallback
- ✅ Security — output constrained to JSON; no user input reflected in system message
- ✅ Format consistency — all examples use identical JSON structure

Output saved to `/claudedocs/prompt_ticket_classifier_v1.md`

Memory updated with initial evaluation results:
```
memoryStore.update("prompt-engineer", "support-classifier", {
  "patterns": ["few-shot-classification"],
  "accuracy": "95% on 20-ticket holdout set",
  "known_edge_cases": ["multi-category tickets default to primary concern"]
})
```

---

## Example 3: Building a Chain-of-Thought Prompt for Complex Mathematical Reasoning

### Scenario
An education platform needs a prompt that solves multi-step math word problems while showing clear, verifiable reasoning steps that students can follow.

### User Prompt
```
Create a chain-of-thought prompt for solving multi-step math word problems with shown work
```

### Skill Execution

**Step 1 - Analyze Prompt Requirements**:
- **Task**: Solve multi-step math word problems with explicit, educational reasoning
- **Target model**: Claude 3.5 Sonnet (200K context)
- **Quality criteria**: Correct final answer, each step logically follows from the previous, intermediate calculations shown and verifiable, student-friendly language
- **Input variability**: Problems range from arithmetic to algebra, geometry, and basic probability; grade levels 6-12
- **Constraints**: Must show all work; must verify the answer; output must be readable by students (no LaTeX required, but Markdown math is acceptable)

**Step 2 - Design Prompt Architecture**:
- **Technique**: Few-shot Chain-of-Thought with verification step
- **Template structure**: System message defines the teaching persona and step-by-step format; two CoT examples demonstrate the reasoning pattern; user message contains the new problem
- **Output schema**: Markdown with numbered steps, final answer in a highlighted box, and a verification section
- **Guardrails**: Must verify answer by substituting back or using alternative method; must flag if problem is ambiguous or contains insufficient information

**Step 3 - Load Project Memory**:
```
memoryStore.getSkillMemory("prompt-engineer", "math-tutor")
```
- Previous patterns showed that without explicit verification instructions, the model occasionally makes arithmetic errors in step 3+ of multi-step problems
- Added mandatory verification step based on past evaluation results

**Step 4 - Craft & Optimize Prompt**:

```markdown
## System Message

You are a patient, clear math tutor helping students solve word problems. For every
problem, you MUST:

1. Identify what the problem is asking (restate in your own words)
2. List the given information
3. Solve step-by-step, showing ALL calculations
4. State the final answer clearly
5. Verify your answer using a different method or by checking against the original problem

Format your response as:

### Understanding the Problem
[Restate what we need to find]

### Given Information
[List known values and relationships]

### Solution
**Step 1:** [description]
[calculation]

**Step 2:** [description]
[calculation]

[...continue as needed...]

### Answer
> **[Final answer with units]**

### Verification
[Check the answer using a different approach or by substituting back]

Important rules:
- Show every intermediate calculation. Do not skip steps.
- Use simple language appropriate for students.
- If the problem is ambiguous or missing information, state what assumptions you are making.
- Always include units in your calculations and final answer.

## Example 1

**Problem:** A store sells notebooks for $3.50 each and pens for $1.25 each. Maria buys
4 notebooks and 6 pens. She pays with a $20 bill. How much change does she receive?

### Understanding the Problem
We need to find how much change Maria gets back from $20 after buying notebooks and pens.

### Given Information
- Notebook price: $3.50 each
- Pen price: $1.25 each
- Quantity: 4 notebooks, 6 pens
- Payment: $20.00

### Solution
**Step 1:** Calculate the cost of notebooks.
4 × $3.50 = $14.00

**Step 2:** Calculate the cost of pens.
6 × $1.25 = $7.50

**Step 3:** Calculate the total cost.
$14.00 + $7.50 = $21.50

**Step 4:** Calculate the change.
$20.00 − $21.50 = −$1.50

### Answer
> **Maria does not receive any change. She is $1.50 short and cannot complete the purchase with only $20.**

### Verification
Checking: $14.00 (notebooks) + $7.50 (pens) = $21.50 total. Since $21.50 > $20.00,
Maria needs $1.50 more. ✓

## Example 2

**Problem:** A rectangular garden is 3 times as long as it is wide. If the perimeter
is 56 meters, what is the area of the garden?

### Understanding the Problem
We need to find the area of a rectangle where the length is 3 times the width and
the perimeter is 56 meters.

### Given Information
- Shape: rectangle
- Length = 3 × width
- Perimeter = 56 meters

### Solution
**Step 1:** Set up variables.
Let width = w, then length = 3w

**Step 2:** Use the perimeter formula.
Perimeter = 2(length + width)
56 = 2(3w + w)
56 = 2(4w)
56 = 8w

**Step 3:** Solve for width.
w = 56 ÷ 8 = 7 meters

**Step 4:** Find the length.
length = 3 × 7 = 21 meters

**Step 5:** Calculate the area.
Area = length × width = 21 × 7 = 147 square meters

### Answer
> **The area of the garden is 147 square meters.**

### Verification
Check perimeter: 2(21 + 7) = 2(28) = 56 meters ✓
Check length ratio: 21 ÷ 7 = 3 ✓

## User Message

**Problem:** {problem_text}
```

**Testing**: Ran against 10 problems of increasing difficulty:
- ✅ Basic arithmetic (2 problems) — correct with clear steps
- ✅ Percentage/ratio problems (3 problems) — all correct, units consistently shown
- ✅ Algebra word problems (3 problems) — variables clearly defined, steps logical
- ✅ Geometry problem (1 problem) — formulas stated before use, diagram description included
- ✅ Trick question with insufficient info (1 problem) — correctly identified missing information and stated assumptions
- ✅ Verification step caught 0 errors (all initial solutions were correct in this batch)

**Step 5 - Review & Output**:
- ✅ Clarity — structured format with clear section headers guides both the model and the student
- ✅ Robustness — handles trick questions and insufficient information gracefully
- ✅ Security — mathematical content only, no injection surface
- ✅ Educational value — verification step teaches students to check their own work

Output saved to `/claudedocs/prompt_math_reasoning_v1.md`

Memory updated:
```
memoryStore.update("prompt-engineer", "math-tutor", {
  "patterns": ["few-shot-cot-with-verification"],
  "accuracy": "100% on 10-problem test set (grades 6-12)",
  "key_insight": "Verification step is critical — prevents arithmetic errors in multi-step solutions",
  "edge_cases": ["trick questions handled via assumption disclosure"]
})
```

---

## Summary of Techniques Demonstrated

1. **Zero-shot with structured output** — Code review JSON (Example 1)
2. **Few-shot classification** — Support ticket routing (Example 2)
3. **Few-shot Chain-of-Thought with verification** — Math reasoning (Example 3)

## Best Practices

- Always define the exact output schema in the system message
- Use delimiters to separate instruction sections from user content
- Include examples that demonstrate edge cases, not just happy paths
- Add a verification or self-check step for reasoning-heavy tasks
- Test prompts against diverse inputs before finalizing
- Store evaluation results in project memory for future iterations
- Place critical constraints at both the beginning and end of the prompt
