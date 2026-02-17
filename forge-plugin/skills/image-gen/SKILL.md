---
name: image-gen
description: "Generate website images with Gemini 3 Native Image Generation. Covers hero banners, service cards, infographics with legible text, team photos, and multi-turn editing. Prevents common errors including illegible text, aspect ratio distortion, brand inconsistency, and low-resolution output."
version: "1.0.0"
context:
  primary_domain: engineering
  always_load_files: []
  detection_required: false
  file_budget: 4
memory:
  scopes:
    - type: "skill-specific"
      files: [brand_guidelines.md, generation_history.md, prompt_patterns.md]
    - type: "shared-project"
      usage: "reference"
tags: [image-generation, gemini, google-genai, hero-banner, infographic, ai-images, web-design]
---

# skill:image-gen — Generate Website Images with Gemini 3

## Version: 1.0.0

## Purpose

Generate production-ready website images using Gemini 3 Native Image Generation. This skill handles the full lifecycle from requirement analysis through prompt crafting, generation, multi-turn refinement, and output validation. Use it when a project needs hero banners, service cards, infographics with legible text, team photos, or any other web imagery produced by Gemini's image generation API.

## File Structure

```
skills/image-gen/
├── SKILL.md (this file)
└── examples.md
```

## Interface References

- **Context**: Loaded via [ContextProvider Interface](../../interfaces/context_provider.md)
- **Memory**: Accessed via [MemoryStore Interface](../../interfaces/memory_store.md)
- **Shared Patterns**: [Shared Loading Patterns](../../interfaces/shared_loading_patterns.md)
- **Schemas**: Validated against [context_metadata.schema.json](../../interfaces/schemas/context_metadata.schema.json) and [memory_entry.schema.json](../../interfaces/schemas/memory_entry.schema.json)

---

## Common Errors to Prevent

> **These 5 errors occur frequently with AI image generation. The workflow below is designed to catch and prevent each one.**

### 1. Illegible Text in Images

Text overlays rendered by the model can appear blurry, misspelled, or stylistically inconsistent. Always specify exact text content, font style (e.g., sans-serif, bold), and placement in the prompt. Validate output at 100% zoom before delivery.

### 2. Aspect Ratio Distortion

Requesting dimensions without explicit aspect ratio guidance causes stretched or cropped compositions. Always declare both pixel dimensions and aspect ratio (e.g., "1920×1080, 16:9 landscape") in the prompt.

### 3. Brand Inconsistency

Generated images that ignore project brand colors, typography, or visual style look out of place on the website. Always load `brand_guidelines.md` from memory and include hex codes, font names, and style descriptors in the prompt.

### 4. Low-Resolution Output

Delivering images below the required resolution for retina or high-DPI displays. Always specify minimum dimensions (e.g., 2× for retina) and verify the output resolution matches the request.

### 5. Inconsistent Style Across a Set

When generating multiple images (e.g., a set of service cards), each image can drift in style, lighting, or color temperature. Include a shared style directive in every prompt and use multi-turn editing to harmonize the set.

---

## MANDATORY WORKFLOW (MUST FOLLOW EXACTLY)

> **IMPORTANT**: Execute ALL steps in order. Do not skip any step.

### ⚠️ STEP 1: Initial Analysis (REQUIRED)

**YOU MUST:**
1. Determine the **image type**:
   - Hero banner / landing page header
   - Service card / feature illustration
   - Infographic with data and text
   - Team photo / people illustration
   - Background texture / pattern
   - Custom illustration
2. Gather **dimensions and format**:
   - Pixel width × height (e.g., 1920×1080)
   - Aspect ratio (e.g., 16:9, 1:1, 4:3)
   - Output format (PNG, JPEG, WebP)
   - Retina/HiDPI requirements (1×, 2×)
3. Identify **style requirements**:
   - Photorealistic, flat illustration, 3D render, watercolor, etc.
   - Mood and atmosphere (professional, playful, dark, vibrant)
   - Color palette (brand colors, specific hex codes)
4. Capture **text overlay requirements**:
   - Exact text content (headline, subheadline, CTA)
   - Font style preference (sans-serif, serif, bold, light)
   - Placement (centered, left-aligned, overlaid on background)
5. Note **brand constraints**:
   - Logo placement or exclusion zones
   - Mandatory brand colors
   - Visual style guidelines from the project

**DO NOT PROCEED WITHOUT A CLEAR IMAGE SPECIFICATION**

### ⚠️ STEP 2: Load Memory (REQUIRED)

> Follow [Standard Memory Loading](../../interfaces/shared_loading_patterns.md#pattern-1-standard-memory-loading) with `skill="image-gen"` and `domain="engineering"`.

**YOU MUST:**
1. Use `memoryStore.getSkillMemory("image-gen", "{project-name}")` to load:
   - **`brand_guidelines.md`**: Brand colors, fonts, visual style, logo usage rules
   - **`generation_history.md`**: Previous generation results, what worked, what failed
   - **`prompt_patterns.md`**: Prompt templates and techniques that produced good results
2. Use `memoryStore.getByProject("{project-name}")` for cross-skill brand insights
3. If no memory exists, note that it will be created after generation

**DO NOT PROCEED WITHOUT CHECKING MEMORY**

### ⚠️ STEP 3: Load Context (REQUIRED)

> Follow [Standard Context Loading](../../interfaces/shared_loading_patterns.md#pattern-2-standard-context-loading) for the `engineering` domain. Stay within the file budget declared in frontmatter.

**YOU MUST:**
1. Load relevant context for image generation best practices
2. Check for project-level design system documentation
3. Review any existing brand assets or style guides in the repository

### ⚠️ STEP 4: Craft Image Prompt (REQUIRED)

**YOU MUST:**
1. Build a detailed, structured prompt for Gemini 3 that includes:
   - **Subject**: What the image depicts (scene, objects, people, abstract shapes)
   - **Composition**: Layout, focal point, rule of thirds, negative space
   - **Style**: Artistic style, rendering technique, visual treatment
   - **Text overlays**: Exact text content with font style and placement instructions
   - **Dimensions**: Explicit width × height and aspect ratio
   - **Mood/Atmosphere**: Lighting, color temperature, emotional tone
   - **Brand elements**: Specific hex colors, brand-consistent visual language
2. Apply learned prompt patterns from `prompt_patterns.md` if available
3. For text-heavy images (infographics, banners with headlines):
   - Spell out text content exactly — do not abbreviate or paraphrase
   - Specify font weight and size relationship (e.g., "large bold headline, smaller regular subheading")
   - Request high contrast between text and background
4. For image sets (service cards, feature illustrations):
   - Define a shared style directive to apply to every image in the set
   - Specify consistent lighting, perspective, and color palette

**DO NOT PROCEED WITH A VAGUE OR INCOMPLETE PROMPT**

### ⚠️ STEP 5: Generate Image (REQUIRED)

**YOU MUST:**
1. Call the Gemini 3 image generation API with the crafted prompt
2. Use the appropriate model configuration:
   - Model: `gemini-2.0-flash-preview-image-generation` (or current Gemini 3 image model)
   - Set `responseModalities: ["TEXT", "IMAGE"]`
3. Handle the response:
   - Extract base64-encoded image data from inline data parts
   - Save the image to the project's assets directory or `/claudedocs/`
4. For **multi-turn editing** (refinement):
   - Maintain conversation history with the model
   - Send follow-up prompts referencing the previous image: "Make the headline text larger and bolder", "Change the background color to #1a1a2e"
   - Each refinement turn preserves the base image while applying the requested changes
5. If generation fails or produces poor results:
   - Revise the prompt with more specific instructions
   - Try alternative style descriptions
   - Adjust dimensions or simplify composition

### ⚠️ STEP 6: Validate Output (REQUIRED)

**YOU MUST:**
1. **Check dimensions**: Verify the output matches requested width × height
2. **Assess text legibility**: If the image contains text overlays:
   - Confirm text is spelled correctly
   - Verify text is readable at intended display size
   - Check contrast ratio between text and background
3. **Verify brand consistency**:
   - Compare dominant colors against brand palette
   - Confirm visual style matches project design language
4. **Inspect for artifacts**: Check for distortions, unnatural elements, or visual glitches
5. If validation fails on any criterion:
   - Return to Step 5 with a corrective prompt (multi-turn editing)
   - Document the issue and fix in generation history

**DO NOT DELIVER AN IMAGE THAT FAILS VALIDATION**

### ⚠️ STEP 7: Generate Output (REQUIRED)

- Save the final image to the project's assets directory (e.g., `public/images/`, `src/assets/`)
- Save generation metadata to `/claudedocs/image-gen_{project}_{YYYY-MM-DD}.md` including:
  - Final prompt used
  - Dimensions and format
  - Number of generation/refinement turns
  - Validation results
- Follow naming conventions in `../OUTPUT_CONVENTIONS.md`

### ⚠️ STEP 8: Update Memory (REQUIRED)

> Follow [Standard Memory Update](../../interfaces/shared_loading_patterns.md#pattern-3-standard-memory-update) for `skill="image-gen"`.

**YOU MUST** use `memoryStore.update(layer="skill-specific", skill="image-gen", project="{project-name}", ...)` to store:

1. **`brand_guidelines.md`**: Update with any newly discovered brand colors, fonts, or style preferences
2. **`generation_history.md`**: Append entry with date, prompt summary, dimensions, outcome (success/refinement needed), and lessons learned
3. **`prompt_patterns.md`**: Save effective prompt templates and techniques; note any patterns that produced poor results to avoid in the future

Timestamps and staleness tracking are handled automatically by MemoryStore. See [MemoryStore Interface](../../interfaces/memory_store.md).

---

## Compliance Checklist

Before completing ANY image generation task, verify:

- [ ] Step 1: Image type, dimensions, style, text, and brand requirements captured
- [ ] Step 2: Memory loaded via `memoryStore.getSkillMemory("image-gen", "{project}")`
- [ ] Step 3: Context loaded within file budget
- [ ] Step 4: Detailed prompt crafted with subject, composition, style, text, dimensions, mood, and brand elements
- [ ] Step 5: Image generated via Gemini 3 API; multi-turn editing applied if needed
- [ ] Step 6: Output validated for dimensions, text legibility, brand consistency, and artifacts
- [ ] Step 7: Output saved with standard naming convention and metadata documented
- [ ] Step 8: Memory updated with brand guidelines, generation history, and prompt patterns

**FAILURE TO COMPLETE ALL STEPS INVALIDATES THE GENERATION**

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-07-15 | Initial release — Gemini 3 image generation with 8-step workflow, 5 error prevention rules, multi-turn editing support |
