# image-gen Memory

Project-specific memory for AI image generation, including brand guidelines, generation history, and effective prompt patterns.

## Purpose

This memory helps the `skill:image-gen` remember:
- Project brand colors, fonts, and visual style guidelines
- Previous image generations — what worked and what required refinement
- Prompt templates and techniques that produce high-quality results
- Common pitfalls to avoid for each project's image type
- Multi-turn editing patterns that resolved specific issues

## Memory Files Per Project

Each project gets its own directory: `{project-name}/`

### `brand_guidelines.md`

**Purpose**: Brand-consistent image generation across all requests for a project.

**Should contain**:
- **Brand colors**: Primary, secondary, accent — with hex codes
- **Typography preferences**: Font families, weights, and style descriptors for text overlays
- **Visual style**: Photorealistic vs. flat illustration vs. 3D render, mood, atmosphere
- **Logo usage rules**: Placement zones, exclusion areas, minimum sizes
- **Do's and don'ts**: Approved vs. prohibited visual elements
- **Reference images**: Descriptions of existing brand imagery for style matching

**When to update**:
- First generation: Create with all known brand details from the user
- Brand refresh: Update colors, fonts, or style when the project rebrands
- Stakeholder feedback: Record approved/rejected visual directions

---

### `generation_history.md`

**Purpose**: Track all image generations for the project to avoid repeating mistakes and build on successes.

**Should contain**:
- **Date and image type**: When and what was generated
- **Prompt summary**: Condensed version of the prompt used
- **Dimensions and format**: Output specifications
- **Outcome**: Success on first attempt, or number of refinement turns needed
- **Issues encountered**: Text legibility problems, color mismatches, composition issues
- **Resolution**: How issues were fixed (specific multi-turn prompts that worked)

**Example entry**:
```markdown
## 2025-07-15 — Hero Banner

- **Type**: Hero banner, 1920×1080
- **Prompt**: Dark gradient background, geometric teal accents, headline "Automate Your Workflow"
- **Turns**: 1 (success on first attempt)
- **Notes**: Specifying exact hex codes in prompt produced accurate color reproduction
```

**When to update**: After every generation, append a new entry.

---

### `prompt_patterns.md`

**Purpose**: Catalog of proven prompt techniques and templates that produce high-quality images.

**Should contain**:
- **Effective patterns**: Prompt structures that consistently produce good results
- **Anti-patterns**: Prompt approaches that produce poor results — with explanations
- **Image type templates**: Reusable prompt skeletons for hero banners, service cards, infographics, etc.
- **Text legibility techniques**: Proven methods for getting readable text in generated images
- **Style consistency directives**: Shared prefixes that maintain visual consistency across image sets
- **Multi-turn refinement phrases**: Specific follow-up prompts that reliably fix common issues

**Example patterns**:
```markdown
## Effective: Shared Style Directive for Image Sets

Prepend this block to every prompt in a set for consistent output:
"Flat vector illustration style, [W]x[H] pixels. Clean white background. 
Primary color [hex] for main shapes. Accent color [hex] for highlights. 
Minimalist, geometric. No gradients, no shadows."

## Effective: Text Legibility in Infographics

Always include: "All text must be large enough to read clearly at 50% zoom. 
Minimum text size equivalent to 24pt for body text, 48pt for titles. 
Add subtle white rounded-rectangle backgrounds behind text areas."

## Anti-pattern: Vague Style Descriptions

❌ "Make it look nice and modern"
✅ "Clean sans-serif typography, flat illustration style, pastel color palette 
   (#E8F6F3, #85C1E9, #F9E79F), generous whitespace, centered composition"
```

**When to update**: After each generation — save techniques that worked, flag those that didn't.

---

## Why This Skill Needs Memory

### Brand Consistency Across Sessions

**Without memory**: Each generation starts from scratch. The user must re-specify brand colors, fonts, and style every time, risking inconsistency.

**With memory**: Brand guidelines are loaded automatically. Every image matches the project's visual identity without repetitive input.

### Prompt Pattern Learning

**Without memory**: Effective prompt techniques are lost between sessions. The same text legibility issues recur on every infographic.

**With memory**: Proven prompt patterns are reused. Known anti-patterns are avoided. Generation quality improves over time.

### Generation History

**Without memory**: No record of what was generated, what failed, or how issues were resolved.

**With memory**: Previous generations inform future ones. If a hero banner required 3 turns to fix text, the next banner prompt pre-applies those fixes.

### Multi-Image Consistency

**Without memory**: Generating a new service card months later produces a style mismatch with the original set.

**With memory**: The shared style directive from the original set is preserved and reapplied, ensuring visual cohesion.

---

## Memory Growth Pattern

### First Generation (New Project)

1. User provides brand colors, style preferences, and image requirements
2. Generate the image following the full workflow
3. Create all three memory files:
   - `brand_guidelines.md` — from user-provided brand details
   - `generation_history.md` — first entry with prompt, outcome, and notes
   - `prompt_patterns.md` — any effective techniques discovered during generation

### Subsequent Generations

1. Load all memory files before crafting the prompt
2. Apply brand guidelines automatically — only ask the user for new or changed requirements
3. Reuse effective prompt patterns from `prompt_patterns.md`
4. Check `generation_history.md` for similar past requests to inform the prompt
5. After generation, update all three files with new learnings

### Ongoing Refinement

- `brand_guidelines.md` stabilizes after 2–3 generations (updated only on rebrands)
- `generation_history.md` grows with each generation (append-only log)
- `prompt_patterns.md` evolves as new image types are attempted and techniques are refined

---

## Related Documentation

- **Skill Documentation**: `../../skills/image-gen/SKILL.md` for the full generation workflow
- **Skill Examples**: `../../skills/image-gen/examples.md` for practical scenarios
- **Main Memory Index**: `../index.md` for memory system overview
- **Memory Lifecycle**: `../lifecycle.md` for freshness, pruning, and archival rules
- **Memory Quality**: `../quality_guidance.md` for validation standards
