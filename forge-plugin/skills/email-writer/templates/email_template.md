# Email: [SUBJECT_LINE]

**Generated**: [YYYY-MM-DD HH:MM:SS]
**Skill**: email-writer v1.0.0

---

## Email Metadata

| Field | Value |
|-------|-------|
| **To** | [RECIPIENTS] |
| **CC** | [CC_RECIPIENTS] |
| **BCC** | [BCC_RECIPIENTS] |
| **Subject** | [SUBJECT_LINE] |
| **Type** | [EMAIL_TYPE — Update/Request/Announcement/Escalation/Follow-up/Response] |
| **Urgency** | [URGENCY — Routine/Time-sensitive/Urgent] |

---

## Context Analysis

- **Purpose**: [EMAIL_PURPOSE — brief description of why this email is being sent]
- **Audience**: [AUDIENCE_DESCRIPTION — roles, technical level, decision-making authority]
- **Tone**: [TONE_SELECTION — formal/semi-formal/casual/urgent/celebratory]
- **Key Message**: [CORE_MESSAGE — the single most important takeaway for the reader]

---

## Generated Email

```
Subject: [SUBJECT_LINE]

[GREETING],

[OPENING_PARAGRAPH — state purpose immediately, 1-2 sentences]

[BODY_PARAGRAPH_1 — primary content, context, or update]

[BODY_PARAGRAPH_2 — supporting details, data, or background]

[ACTION_ITEMS_SECTION — if applicable]

Action Items:
- [OWNER_1]: [TASK_1] — by [DEADLINE_1]
- [OWNER_2]: [TASK_2] — by [DEADLINE_2]
- [OWNER_3]: [TASK_3] — by [DEADLINE_3]

[CLOSING_PARAGRAPH — summarize, restate key ask, or set expectations]

[SIGN_OFF],
[SIGNATURE_NAME]
[SIGNATURE_TITLE]
```

---

## Tone Analysis

| Dimension | Assessment |
|-----------|------------|
| **Formality** | [FORMALITY_LEVEL — Formal/Semi-formal/Casual] |
| **Directness** | [DIRECTNESS_LEVEL — Direct/Balanced/Diplomatic] |
| **Urgency** | [URGENCY_CONVEYED — High/Medium/Low/None] |
| **Empathy** | [EMPATHY_LEVEL — High/Moderate/Neutral] |
| **Actionability** | [ACTIONABILITY — Clear actions/FYI only/Discussion requested] |

---

## Alternative Subject Lines

1. `[ALT_SUBJECT_1]`
2. `[ALT_SUBJECT_2]`
3. `[ALT_SUBJECT_3]`

**Rationale**: [WHY_ALTERNATIVES_DIFFER — e.g., varying urgency, specificity, or audience focus]

---

## Quality Checklist

- [ ] Purpose stated in first two sentences
- [ ] Subject line is specific and under 60 characters
- [ ] Tone matches audience and situation
- [ ] Action items have owners and deadlines (if applicable)
- [ ] No jargon without explanation for non-technical recipients
- [ ] No passive-aggressive or ambiguous phrasing
- [ ] Closing sets clear expectations for next steps
- [ ] CC/BCC recipients are justified
- [ ] Email is scannable — uses bullets, bold, and short paragraphs

---

## Metadata

- **Composed by**: Claude Code email-writer skill v1.0.0
- **Composition date**: [YYYY-MM-DD HH:MM:SS]
- **Repository**: [REPO_PATH]
- **Project**: [PROJECT_NAME]

---

<!--
Template Usage Instructions:

Replace all placeholders in [BRACKETS] with actual values:
- [SUBJECT_LINE] - Concise, specific email subject (≤60 chars preferred)
- [RECIPIENTS] - Primary recipients (To field)
- [CC_RECIPIENTS] - Carbon copy recipients (CC field), or "—" if none
- [BCC_RECIPIENTS] - Blind carbon copy recipients (BCC field), or "—" if none
- [EMAIL_TYPE] - Category: Update, Request, Announcement, Escalation, Follow-up, Response
- [URGENCY] - Priority level: Routine, Time-sensitive, Urgent
- [EMAIL_PURPOSE] - Brief description of why the email is being sent
- [AUDIENCE_DESCRIPTION] - Who the recipients are, their roles and technical level
- [TONE_SELECTION] - Chosen tone: formal, semi-formal, casual, urgent, celebratory
- [CORE_MESSAGE] - The single most important point the reader should take away
- [GREETING] - Opening salutation matching tone (e.g., "Hi team", "Dear Dr. Smith")
- [OPENING_PARAGRAPH] - States purpose immediately in 1-2 sentences
- [BODY_PARAGRAPH_1] - Primary content section
- [BODY_PARAGRAPH_2] - Supporting details section
- [ACTION_ITEMS_SECTION] - Distinct section for action items with owners and deadlines
- [CLOSING_PARAGRAPH] - Summary, restatement of ask, or next-step expectations
- [SIGN_OFF] - Closing salutation matching tone (e.g., "Best regards", "Thanks", "Cheers")
- [SIGNATURE_NAME] - Sender's name
- [SIGNATURE_TITLE] - Sender's title/role
- [FORMALITY_LEVEL] - Formal, Semi-formal, or Casual
- [DIRECTNESS_LEVEL] - Direct, Balanced, or Diplomatic
- [URGENCY_CONVEYED] - High, Medium, Low, or None
- [EMPATHY_LEVEL] - High, Moderate, or Neutral
- [ACTIONABILITY] - Clear actions, FYI only, or Discussion requested
- [ALT_SUBJECT_1/2/3] - Alternative subject line options
- [WHY_ALTERNATIVES_DIFFER] - Explanation of how alternatives serve different needs
- [REPO_PATH] - Path to the repository
- [PROJECT_NAME] - Name of the project

Conditional Sections:
- Include "Action Items" section only if the email requires action from recipients
- Include "BCC" field only if BCC recipients are specified
- Include "Alternative Subject Lines" only when multiple valid framings exist
- Adjust "Tone Analysis" dimensions based on email type and context

Formatting:
- Use proper markdown syntax throughout
- Wrap the email content in a code block for easy copying
- Use tables for structured metadata and analysis
- Use checkboxes for the quality checklist
- Bold key dates, names, and action items within the email body

Output Location:
- Save to: /claudedocs/email_{descriptor}.md
- Ensure /claudedocs directory exists
- Use a descriptive name based on email type and topic (e.g., email_api_migration_update.md)
-->
