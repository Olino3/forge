# Slack Message: [MESSAGE_HEADLINE]

**Generated**: [YYYY-MM-DD HH:MM:SS]
**Skill**: slack-message-composer v1.0.0

---

## Message Metadata

| Field | Value |
|-------|-------|
| **Channel** | [TARGET_CHANNEL] |
| **Thread** | [NEW_THREAD / REPLY_TO_THREAD — thread context if replying] |
| **Type** | [MESSAGE_TYPE — Announcement/Incident/Update/Request/Celebration/Thread Reply] |
| **Urgency** | [URGENCY — 🚨 Critical / ⏰ Time-sensitive / 📋 Routine / 🎉 Celebratory] |
| **Mentions** | [MENTION_STRATEGY — @here / @channel / @specific-users / None] |

---

## Context Analysis

- **Purpose**: [MESSAGE_PURPOSE — brief description of why this message is being sent]
- **Channel Context**: [CHANNEL_DESCRIPTION — channel purpose, audience size, posting norms]
- **Audience**: [AUDIENCE_DESCRIPTION — who will read this, their roles and what they care about]
- **Tone**: [TONE_SELECTION — urgent/professional/casual/celebratory/blameless]
- **Key Message**: [CORE_MESSAGE — the single most important takeaway for the reader]

---

## Generated Message

```
[EMOJI_HEADER] *[BOLD_HEADLINE]*

[MENTION_IF_NEEDED — @here / @channel / omit]

[OPENING_LINE — state purpose immediately, 1 sentence]

[BODY_SECTION_1 — primary content with Slack formatting]
• [BULLET_POINT_1]
• [BULLET_POINT_2]
• [BULLET_POINT_3]

[BODY_SECTION_2 — supporting details, if needed]

[ACTION_ITEMS_SECTION — if applicable]
*What to do:*
1. [ACTION_1 — @owner if specific] — by [DEADLINE_1]
2. [ACTION_2 — @owner if specific] — by [DEADLINE_2]

[CLOSING_LINE — next update time, where to ask questions, or thread guidance]
[THREAD_GUIDANCE — "🧵 Discussion in thread" or "Updates in thread ↓"]
```

---

## Threading Suggestions

| Thread Content | Purpose |
|----------------|---------|
| [THREAD_ITEM_1] | [WHY_THREADED_1 — e.g., "Technical details for interested engineers"] |
| [THREAD_ITEM_2] | [WHY_THREADED_2 — e.g., "Timeline and milestones for tracking"] |
| [THREAD_ITEM_3] | [WHY_THREADED_3 — e.g., "Discussion and Q&A"] |

---

## Alternative Phrasings

### Opening Line Alternatives
1. `[ALT_OPENING_1]`
2. `[ALT_OPENING_2]`

### Headline Alternatives
1. `[ALT_HEADLINE_1]`
2. `[ALT_HEADLINE_2]`

**Rationale**: [WHY_ALTERNATIVES_DIFFER — e.g., varying urgency, formality, or emphasis]

---

## Quality Checklist

- [ ] Purpose is clear from the first line
- [ ] Message is scannable in under 30 seconds
- [ ] Bold text highlights key information (dates, status, decisions)
- [ ] Emoji usage is purposeful (visual anchors, not decoration)
- [ ] Action items specify who, what, and when
- [ ] @mentions are used only when notification is warranted
- [ ] Technical details are in code blocks
- [ ] Threading guidance is provided for messages that will generate discussion
- [ ] Tone matches the channel and situation
- [ ] Message respects the channel's conventions

---

## Metadata

- **Composed by**: Claude Code slack-message-composer skill v1.0.0
- **Composition date**: [YYYY-MM-DD HH:MM:SS]
- **Repository**: [REPO_PATH]
- **Project**: [PROJECT_NAME]

---

<!--
Template Usage Instructions:

Replace all placeholders in [BRACKETS] with actual values:
- [MESSAGE_HEADLINE] - Concise headline for the Slack message
- [TARGET_CHANNEL] - Slack channel name (e.g., #engineering, #incidents)
- [NEW_THREAD / REPLY_TO_THREAD] - Whether this is a new message or thread reply
- [MESSAGE_TYPE] - Category: Announcement, Incident, Update, Request, Celebration, Thread Reply
- [URGENCY] - Priority with emoji: 🚨 Critical, ⏰ Time-sensitive, 📋 Routine, 🎉 Celebratory
- [MENTION_STRATEGY] - Notification approach: @here, @channel, @specific-users, or None
- [MESSAGE_PURPOSE] - Brief description of why the message is being sent
- [CHANNEL_DESCRIPTION] - Context about the target channel
- [AUDIENCE_DESCRIPTION] - Who will read this and what they care about
- [TONE_SELECTION] - Chosen tone: urgent, professional, casual, celebratory, blameless
- [CORE_MESSAGE] - The single most important takeaway
- [EMOJI_HEADER] - Leading emoji for visual scanning (🚀, 🚨, 📣, 🌟, etc.)
- [BOLD_HEADLINE] - Main headline wrapped in *bold* Slack syntax
- [MENTION_IF_NEEDED] - @here, @channel, or omit entirely
- [OPENING_LINE] - First sentence stating the purpose
- [BODY_SECTION_1/2] - Content sections with Slack markdown formatting
- [BULLET_POINT_1/2/3] - Key items as bullet points
- [ACTION_ITEMS_SECTION] - Action items with owners and deadlines
- [CLOSING_LINE] - Final line with next steps or guidance
- [THREAD_GUIDANCE] - Instructions for thread usage
- [THREAD_ITEM_1/2/3] - Suggested thread follow-ups
- [WHY_THREADED_1/2/3] - Rationale for threading each item
- [ALT_OPENING_1/2] - Alternative opening line options
- [ALT_HEADLINE_1/2] - Alternative headline options
- [WHY_ALTERNATIVES_DIFFER] - Explanation of how alternatives serve different needs
- [REPO_PATH] - Path to the repository
- [PROJECT_NAME] - Name of the project

Conditional Sections:
- Include "Action Items" only if the message requires action from readers
- Include "Threading Suggestions" only for messages likely to generate discussion
- Include "@here / @channel" mention only when urgency warrants notification
- Adjust "Alternative Phrasings" based on how many valid framings exist
- For incident messages, include severity level and next update time

Formatting:
- Use proper markdown syntax throughout
- Wrap the Slack message content in a code block for easy copying
- Use tables for structured metadata and analysis
- Use checkboxes for the quality checklist
- Bold key dates, names, and action items within the message body
- Use Slack-native markdown (not standard markdown) inside the message code block

Output Location:
- Save to: /claudedocs/slack_msg_{descriptor}.md
- Ensure /claudedocs directory exists
- Use a descriptive name based on message type and topic (e.g., slack_msg_deployment_api_v2.md)
-->
