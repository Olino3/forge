# Image Generation Examples

Practical scenarios demonstrating the `skill:image-gen` workflow with Gemini 3 Native Image Generation.

---

## Example 1: Hero Banner for a SaaS Landing Page

### Scenario

A SaaS startup needs a hero banner for their landing page. The banner must include a headline text overlay, use brand colors, and convey a professional yet modern atmosphere.

### User Prompt

> "Generate a hero banner for our SaaS landing page. Dimensions: 1920×1080. Headline: 'Automate Your Workflow'. Brand colors: #6C5CE7 (primary purple), #00CEC9 (accent teal), #FFFFFF (white text). Style: modern, clean, tech-forward. Dark gradient background."

### Skill Execution

#### Step 1: Initial Analysis

- **Image type**: Hero banner / landing page header
- **Dimensions**: 1920×1080 (16:9 landscape)
- **Style**: Modern, clean, tech-forward with dark gradient background
- **Text overlay**: "Automate Your Workflow" — large, bold, sans-serif, white, centered
- **Brand colors**: Primary #6C5CE7, accent #00CEC9, text #FFFFFF
- **Retina**: 2× recommended (3840×2160 generation, downscale for 1×)

#### Step 2: Load Memory

```
memoryStore.getSkillMemory("image-gen", "workflow-saas")
→ No existing memory found (first generation for this project)
```

#### Step 3: Load Context

Loaded engineering context for web image best practices. No existing brand assets in repository.

#### Step 4: Craft Image Prompt

```
A professional hero banner for a SaaS website, 1920x1080 pixels, 16:9 landscape aspect ratio.

Dark gradient background transitioning from deep navy (#1a1a2e) on the left to dark purple (#6C5CE7) on the right.

Abstract geometric shapes and flowing lines in teal (#00CEC9) with subtle glow effects, suggesting automation and workflow connections. Nodes connected by smooth curved lines, representing a digital workflow.

Centered headline text reading exactly "Automate Your Workflow" in large bold white (#FFFFFF) sans-serif font. The text must be crisp, legible, and prominently placed with generous padding. Below the headline, smaller text area left empty for a subheading to be added later.

Clean negative space around the text. No cluttered elements. Modern, professional, tech-forward atmosphere. Subtle particle effects in the background for depth.
```

#### Step 5: Generate Image

- Called Gemini 3 API with `gemini-2.0-flash-preview-image-generation`
- Response returned base64 PNG data
- Saved to `public/images/hero-banner.png`

#### Step 6: Validate Output

- ✅ Dimensions: 1920×1080 confirmed
- ✅ Text: "Automate Your Workflow" is legible, correctly spelled, high contrast
- ✅ Brand colors: Purple gradient and teal accents match brand palette
- ✅ No artifacts or distortions detected

#### Step 7: Generate Output

- Image saved to `public/images/hero-banner.png`
- Metadata saved to `/claudedocs/image-gen_workflow-saas_2025-07-15.md`

#### Step 8: Update Memory

Created initial memory files:
- `brand_guidelines.md`: Documented #6C5CE7, #00CEC9, #FFFFFF palette and dark gradient style
- `generation_history.md`: Logged first successful generation with prompt and outcome
- `prompt_patterns.md`: Saved the dark gradient + geometric shapes pattern as effective for tech SaaS

---

## Example 2: Service Cards with Consistent Style

### Scenario

A consulting website needs four service card illustrations with a unified visual style. Each card represents a different service but must look cohesive when displayed side by side.

### User Prompt

> "Create 4 service card images for our consulting website. Services: Strategy, Technology, Operations, People. Each should be 600×400 square-ish, flat illustration style, white background, using our brand blue #2D3436 and orange #E17055. Consistent style across all four."

### Skill Execution

#### Step 1: Initial Analysis

- **Image type**: Service card illustrations (set of 4)
- **Dimensions**: 600×400 each (3:2 landscape)
- **Style**: Flat illustration, white background, minimal, professional
- **Text overlay**: None (service names handled in HTML)
- **Brand colors**: Dark #2D3436, accent orange #E17055
- **Consistency requirement**: Shared style directive across all 4 images

#### Step 2: Load Memory

```
memoryStore.getSkillMemory("image-gen", "apex-consulting")
→ brand_guidelines.md found: #2D3436 primary, #E17055 accent, flat illustration preference
→ prompt_patterns.md found: "flat vector, white background, centered icon" pattern rated effective
```

#### Step 3: Load Context

Loaded engineering context. Existing site uses flat design language confirmed in brand memory.

#### Step 4: Craft Image Prompts

**Shared style directive** (prepended to each prompt):
```
Flat vector illustration style, 600x400 pixels, 3:2 landscape. Clean white (#FFFFFF) background. 
Primary color dark charcoal (#2D3436) for main shapes. Accent color warm orange (#E17055) for 
highlights and focal elements. Minimalist, geometric, professional. Consistent line weight and 
shape language. No gradients, no shadows, no 3D effects. Centered composition.
```

**Card 1 — Strategy**:
```
[Shared style directive]
A chess piece (knight) composed of simple geometric shapes, with an upward arrow integrated into the design. The knight is in dark charcoal (#2D3436) with the arrow tip highlighted in orange (#E17055). Represents strategic thinking and forward planning.
```

**Card 2 — Technology**:
```
[Shared style directive]
A circuit board pattern forming the shape of a lightbulb. Clean geometric lines in dark charcoal (#2D3436) with connection nodes highlighted in orange (#E17055). Represents innovation through technology.
```

**Card 3 — Operations**:
```
[Shared style directive]
Three interlocking gears of different sizes, arranged in a triangular composition. Gears in dark charcoal (#2D3436) with the central gear's teeth highlighted in orange (#E17055). Represents operational efficiency and process optimization.
```

**Card 4 — People**:
```
[Shared style directive]
Three simplified human figures standing together, with a speech bubble connecting them. Figures in dark charcoal (#2D3436) with the speech bubble and connection lines in orange (#E17055). Represents collaboration and human capital.
```

#### Step 5: Generate Images

- Generated all 4 images sequentially using Gemini 3 API
- Each used the same shared style directive for consistency
- Saved to `public/images/services/`

#### Step 6: Validate Output

- ✅ Dimensions: All 4 images are 600×400
- ✅ Style consistency: Flat illustration, matching line weights, same color palette across set
- ✅ Brand colors: #2D3436 and #E17055 used consistently
- ⚠️ Card 3 (Operations): Center gear slightly off-center → used multi-turn edit: "Shift the central gear 20px to the right to center it in the composition"
- ✅ After refinement: All 4 cards pass validation

#### Step 7: Generate Output

- Images saved to `public/images/services/strategy.png`, `technology.png`, `operations.png`, `people.png`
- Metadata saved to `/claudedocs/image-gen_apex-consulting_2025-07-15.md`

#### Step 8: Update Memory

- `generation_history.md`: Logged 4-card generation with shared style directive approach
- `prompt_patterns.md`: Confirmed "shared style directive" pattern is effective for multi-image consistency; saved the directive template for reuse

---

## Example 3: Multi-Turn Editing — Infographic Refinement

### Scenario

A marketing team needs an infographic showing "5 Steps to Digital Transformation." The initial generation has legibility issues with the text, and the brand colors need adjustment after stakeholder feedback.

### User Prompt

> "Create an infographic titled '5 Steps to Digital Transformation'. Steps: 1. Assess, 2. Plan, 3. Build, 4. Deploy, 5. Optimize. Portrait format 1080×1920. Brand colors: #0984E3 blue, #00B894 green, #DFE6E9 light gray background. Each step should have an icon and description text."

### Skill Execution

#### Step 1: Initial Analysis

- **Image type**: Infographic with structured data and text
- **Dimensions**: 1080×1920 (9:16 portrait)
- **Style**: Clean infographic, numbered steps, icons per step
- **Text overlay**: Title + 5 step labels + descriptions — text-heavy, legibility is critical
- **Brand colors**: Blue #0984E3, green #00B894, background #DFE6E9

#### Step 2: Load Memory

```
memoryStore.getSkillMemory("image-gen", "digitech-corp")
→ prompt_patterns.md: "For text-heavy infographics, specify font size hierarchy and 
   high-contrast text backgrounds. Gemini tends to make text too small on first attempt."
```

#### Step 3: Load Context

Loaded engineering context. Prior memory warns about text sizing issues on infographics.

#### Step 4: Craft Image Prompt (Turn 1)

```
A vertical infographic, 1080x1920 pixels, 9:16 portrait orientation.

Light gray (#DFE6E9) background.

Title at the top: "5 Steps to Digital Transformation" in large bold sans-serif font, 
dark charcoal text (#2D3436), centered.

Five vertically stacked sections, each containing:
- A step number in a blue (#0984E3) circle
- A simple flat icon next to the number
- The step name in bold medium sans-serif: "Assess", "Plan", "Build", "Deploy", "Optimize"
- A one-line description in regular smaller sans-serif below each step name

Step icons:
1. Assess — magnifying glass icon
2. Plan — clipboard with checkmarks
3. Build — wrench and gear
4. Deploy — rocket launching
5. Optimize — upward trending graph

Connected by a vertical dotted line in green (#00B894) running between the step circles.

All text must be large enough to read clearly at 50% zoom. High contrast between text and 
background. Minimum text size equivalent to 24pt for step names, 18pt for descriptions, 
48pt for the title.
```

#### Step 5: Generate Image (Turn 1)

- Called Gemini 3 API — initial image generated
- Saved to `public/images/infographic-v1.png`

#### Step 6: Validate Output (Turn 1)

- ✅ Dimensions: 1080×1920 confirmed
- ✅ Layout: 5 steps vertically stacked with connecting line
- ⚠️ **Text legibility issue**: Step descriptions are too small and slightly blurry at intended display size
- ⚠️ **Spelling**: Step 4 description has a truncated word
- ✅ Brand colors: Blue and green match, background correct

**Validation failed** — returning to Step 5 for multi-turn refinement.

#### Step 5: Generate Image (Turn 2 — Fix Text)

Multi-turn prompt sent to the same conversation:

```
The step description text is too small and blurry. Please make the following changes:
1. Increase the description text size by 50% — it should be clearly readable
2. Fix the description for Step 4 (Deploy) to read: "Launch your solution with confidence and zero downtime"
3. Add a subtle white rounded-rectangle background behind each step's text area to improve contrast
4. Keep everything else exactly the same
```

- Refined image generated in the same conversation thread
- Saved to `public/images/infographic-v2.png`

#### Step 6: Validate Output (Turn 2)

- ✅ Dimensions: 1080×1920 confirmed
- ✅ Text legibility: All text now clearly readable at 50% zoom
- ✅ Spelling: Step 4 description corrected
- ✅ White text backgrounds improve contrast
- ✅ Brand colors maintained

**Stakeholder feedback received**: "Can we change the blue to our updated brand blue #0652DD?"

#### Step 5: Generate Image (Turn 3 — Brand Color Update)

Multi-turn prompt:

```
Great improvement. One final change: replace all instances of the current blue (#0984E3) 
with our updated brand blue (#0652DD). This includes the step number circles and any 
blue accents. Keep the green (#00B894) and all other elements unchanged.
```

- Final image generated
- Saved to `public/images/infographic-final.png`

#### Step 6: Validate Output (Turn 3)

- ✅ Dimensions: 1080×1920 confirmed
- ✅ Text legibility: All text clear and correctly spelled
- ✅ Brand colors: Updated blue #0652DD applied, green #00B894 preserved
- ✅ No artifacts or distortions
- ✅ All 5 steps present with correct icons and descriptions

**Validation passed after 3 generation turns.**

#### Step 7: Generate Output

- Final image saved to `public/images/digital-transformation-infographic.png`
- Previous versions cleaned up (v1, v2 removed)
- Metadata saved to `/claudedocs/image-gen_digitech-corp_2025-07-15.md`:
  - 3 generation turns documented
  - Text legibility fix noted
  - Brand color update logged
  - Final prompt preserved for future infographic generation

#### Step 8: Update Memory

- `brand_guidelines.md`: Updated brand blue from #0984E3 to #0652DD
- `generation_history.md`: Logged 3-turn generation with progressive refinement
- `prompt_patterns.md`: Added lessons learned:
  - "For infographics, always specify minimum text size equivalents (e.g., 24pt, 48pt)"
  - "Add white rounded-rectangle backgrounds behind text areas for contrast"
  - "Text-heavy images typically require 2–3 refinement turns"
