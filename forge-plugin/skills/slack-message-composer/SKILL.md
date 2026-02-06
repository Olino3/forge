---
name: slack-message-composer
description: Shapes team communications for Slack — announcements, updates, requests, thread replies, incident notifications, and cross-team coordination. Analyzes channel context, calibrates tone and urgency, structures messages for maximum clarity in fast-moving channels, and produces polished Slack messages that cut through the noise. Like Iris streaking across the sky to deliver divine proclamations, this skill ensures every message lands with precision, purpose, and the right weight for its audience.
---

# Slack Message Composer

## ⚠️ MANDATORY COMPLIANCE ⚠️

**CRITICAL**: The 4-step workflow outlined in this document MUST be followed in exact order for EVERY Slack message composition. Skipping steps or deviating from the procedure will result in messages that miss their audience, clutter channels, or fail to drive action. This is non-negotiable.

## File Structure

- **SKILL.md** (this file): Main instructions and MANDATORY workflow
- **examples.md**: Usage scenarios with different message types and generated Slack messages
- **../../memory/skills/slack-message-composer/**: Project-specific memory storage
  - `{project-name}/`: Per-project channel conventions and communication patterns
- **templates/**:
  - `slack_template.md`: Standard Slack message output format template

## Focus Areas

Slack message composition evaluates 7 critical dimensions:

1. **Channel Awareness**: Identify the target channel's purpose, audience size, norms, and posting conventions — #incidents demands different framing than #random
2. **Message Formatting**: Leverage Slack's native formatting — bold, code blocks, bullet points, blockquotes, dividers — to maximize scannability in a fast-scrolling feed
3. **Audience Targeting**: Determine who needs to see this message, who needs to act on it, and whether @here, @channel, or specific @mentions are warranted
4. **Urgency Calibration**: Match the signal strength to the situation — routine updates should not trigger the same response as production incidents
5. **Threading Strategy**: Decide whether the message belongs in a thread or the main channel, and structure thread-friendly content that doesn't fragment context
6. **Emoji & Reaction Guidance**: Use emoji strategically for visual scanning (🚨 for incidents, ✅ for completions, 📣 for announcements) without descending into noise
7. **Brevity & Clarity**: Respect readers' attention — lead with the headline, support with context, close with action; every word must earn its place

**Note**: The skill composes Slack message content for the user to review and post. It does not send messages itself unless explicitly integrated with the Slack API.

---

## MANDATORY WORKFLOW (MUST FOLLOW EXACTLY)

### ⚠️ STEP 1: Understand Intent (REQUIRED)

**YOU MUST:**
1. Determine the **purpose** of the message: announcement, status update, request for help, incident notification, celebration, question, or thread reply
2. Identify the **target channel**: what channel or DM this message will be posted in, and what that channel's conventions are
3. Identify the **audience**: who will read this — the whole engineering org, a specific team, leadership, on-call engineers, or a cross-functional group
4. Assess the **urgency level**: is this a 🚨 production incident, a ⏰ time-sensitive request, a 📋 routine update, or a 🎉 celebratory FYI
5. Ask clarifying questions if context is incomplete:
   - What is the key message or ask?
   - Who specifically needs to take action?
   - Is this a new thread or a reply to an existing conversation?
   - Should this trigger notifications (@here, @channel)?

**DO NOT PROCEED WITHOUT UNDERSTANDING PURPOSE, CHANNEL, AND AUDIENCE**

### ⚠️ STEP 2: Structure Message (REQUIRED)

**YOU MUST:**
1. **Choose the message format** based on type:
   - **Announcement**: Emoji header + bold headline + context + action items + relevant links
   - **Incident Notification**: Severity emoji + status + impact + who's investigating + thread for updates
   - **Status Update**: Progress indicator + summary + blockers + next steps
   - **Request for Help**: Clear ask + context + urgency + who can help + deadline
   - **Thread Reply**: Reference parent context + concise response + next action
   - **Celebration/Recognition**: Emoji + who + what they did + why it matters
2. **Determine notification strategy**:
   - `@here` — Only when the message requires immediate attention from active channel members
   - `@channel` — Only for critical announcements or incidents affecting the entire channel
   - `@specific-person` — When a specific individual must act
   - No mention — For informational posts that don't require immediate response
3. **Plan message sections**: headline, context, details, action items, links/references
4. **Identify supporting elements**: links, screenshots, code snippets, or related threads to reference

**DO NOT PROCEED WITHOUT A CLEAR MESSAGE STRUCTURE**

### ⚠️ STEP 3: Compose Message (REQUIRED)

**YOU MUST:**
1. **Write the headline/opening line**:
   - Lead with a relevant emoji to enable visual scanning
   - Bold the key information: `*Deployment complete*`, `*Incident resolved*`
   - State the purpose in the first line — readers decide to keep reading or scroll past based on this
2. **Write the body**:
   - Use Slack markdown formatting (see Slack Formatting Reference below)
   - Keep paragraphs to 2-3 lines maximum — walls of text get skipped
   - Use bullet points or numbered lists for multiple items
   - Use `>` blockquotes for context from other sources
   - Use `` `code blocks` `` for technical details, commands, or error messages
   - Use `---` dividers sparingly to separate logical sections
3. **Write action items** (if applicable):
   - Tag specific owners with @mentions
   - Use checkbox emoji (☐) or numbered steps for trackable actions
   - Include deadlines in bold
4. **Add threading guidance**:
   - If the message will generate discussion, add "🧵 Thread for discussion" or "Updates in thread ↓"
   - If replying to a thread, reference the parent message context briefly
5. **Close appropriately**:
   - For requests: restate the ask and deadline
   - For announcements: point to where to find more info
   - For incidents: state next update time

**DO NOT WRITE WALLS OF UNFORMATTED TEXT**

### ⚠️ STEP 4: Review & Optimize (REQUIRED)

**YOU MUST validate the message against these criteria:**
1. **Length check**:
   - [ ] Message is concise — can be read in under 30 seconds
   - [ ] No unnecessary preamble or filler words
   - [ ] Details that support but aren't essential are threaded, not in the main message
2. **Formatting check**:
   - [ ] Bold text highlights key information
   - [ ] Lists are used for multiple items (not comma-separated run-on sentences)
   - [ ] Code blocks wrap technical content
   - [ ] Emoji usage is purposeful, not decorative noise
3. **Clarity check**:
   - [ ] The purpose is obvious from the first line
   - [ ] Action items are explicit — who does what by when
   - [ ] No jargon without context for cross-team audiences
   - [ ] No ambiguous references ("the thing we discussed")
4. **Actionability check**:
   - [ ] Recipients know if they need to act or just be aware
   - [ ] @mentions are used correctly and only when necessary
   - [ ] Response expectations are clear (reply in thread, react with ✅, etc.)
5. **Present the final message** to the user for review
6. **Offer alternatives**: Provide 1-2 alternative phrasings for the opening line or key sections

**DO NOT SKIP VALIDATION**

**OPTIONAL: Update Project Memory**

If project-specific channel conventions or communication patterns are discovered during the process, store insights in `../../memory/skills/slack-message-composer/{project-name}/`:
- Channel naming conventions and purposes
- Preferred message formats and emoji usage
- Common @mention groups and distribution patterns
- Recurring message types and templates

---

## Compliance Checklist

Before completing ANY Slack message composition, verify:
- [ ] Step 1: Intent understood — purpose, channel, audience, and urgency established
- [ ] Step 2: Message structured — format chosen, notification strategy determined, sections planned
- [ ] Step 3: Message composed — headline, body, action items, and threading guidance written with Slack formatting
- [ ] Step 4: Message reviewed — length, formatting, clarity, and actionability validated

**FAILURE TO COMPLETE ALL STEPS INVALIDATES THE MESSAGE**

---

## Special Case Handling

### Incident Communications

When composing messages for production incidents or outages:
1. Lead with severity and status — `🔴 SEV-1` or `🟡 SEV-3` immediately signals priority
2. State impact in user-facing terms — "customers cannot log in" not "auth service returning 500s"
3. Identify who is investigating and where coordination is happening
4. Commit to a next-update time — "Next update in 30 minutes or when status changes"
5. Keep the main channel message brief; use a thread for technical details and timeline
6. Post resolution and follow-up links when the incident closes

### Cross-Team Announcements

When composing messages that span multiple teams or channels:
1. Tailor the message framing for each audience — engineering cares about technical impact, product cares about user impact
2. Link to a single source of truth rather than duplicating details across channels
3. Clearly state what each team needs to do (or that no action is needed)
4. Use `@here` judiciously — not every cross-team post warrants a notification
5. Include a point of contact for questions

### Sensitive Topics

When composing messages about sensitive matters (reorgs, personnel changes, security vulnerabilities):
1. Use DMs or private channels — never post sensitive information in public channels
2. Keep language factual and neutral — avoid speculation or editorializing
3. Coordinate timing with leadership or HR before posting
4. Avoid @channel or @here for sensitive announcements in large channels
5. Direct follow-up questions to appropriate channels or individuals

---

## Slack Formatting Reference

| Format | Syntax | Example |
|--------|--------|---------|
| **Bold** | `*text*` | *important update* |
| _Italic_ | `_text_` | _additional context_ |
| ~~Strikethrough~~ | `~text~` | ~old approach~ |
| `Inline code` | `` `text` `` | `git pull origin main` |
| Code block | ```` ```text``` ```` | Multi-line code or logs |
| Blockquote | `> text` | > quoted context |
| Ordered list | `1. item` | 1. First step |
| Bulleted list | `• item` or `- item` | • Action item |
| Link | `<url\|display text>` | <https://wiki.internal\|Wiki Link> |
| User mention | `@username` | @oncall-engineer |
| Channel mention | `#channel-name` | #incidents |
| `@here` | `@here` | Notifies active members |
| `@channel` | `@channel` | Notifies all members |
| Emoji | `:emoji_name:` | :rocket: :white_check_mark: |
| Divider | `---` | Horizontal rule |

---

## Further Reading

Refer to official documentation and resources:
- **Slack Formatting**:
  - Slack Message Formatting Guide: https://api.slack.com/reference/surfaces/formatting
  - Block Kit Builder: https://app.slack.com/block-kit-builder
- **Communication Best Practices**:
  - Slack Etiquette Guide: https://slack.com/blog/collaboration/etiquette-tips-in-slack
  - Incident Communication: https://sre.google/sre-book/effective-troubleshooting/
- **Team Communication**:
  - GitLab Handbook on Communication: https://about.gitlab.com/handbook/communication/
  - Async Communication Best Practices: https://nohq.co/guides/async-communication/

---

## Version History

- v1.0.0 (2025-01-XX): Initial release
  - Mandatory 4-step workflow for Slack message composition
  - Channel awareness and audience targeting
  - Support for announcements, incidents, updates, requests, celebrations, and thread replies
  - Project memory integration for channel convention persistence
  - Template-based output formatting
  - Slack-native formatting reference
