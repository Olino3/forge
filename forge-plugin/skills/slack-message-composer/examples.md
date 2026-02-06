# Slack Message Composer Examples

This file contains example scenarios demonstrating how to use the slack-message-composer skill to craft effective Slack messages for various communication needs.

---

## Example 1: Deployment Announcement to #engineering

### Scenario
Backend team lead needs to announce a successful production deployment of a new API versioning system to the engineering channel.

### User Prompt
```
Announce in #engineering that we just deployed API versioning (v2 routing layer) to production. All v1 endpoints are still active, no breaking changes. The migration guide is at https://wiki.internal/api-v2-migration. Teams should start planning their migration — soft deadline is end of Q2.
```

### Skill Execution

**Step 1 - Understand Intent**:
- **Purpose**: Announcement — inform engineering of a production deployment and upcoming migration
- **Channel**: #engineering — broad technical audience, expects formatted updates
- **Audience**: All engineers — varying familiarity with the API layer, need actionable next steps
- **Urgency**: 📋 Routine — no immediate action required, soft deadline is months away

**Step 2 - Structure Message**:
- Format: Announcement — emoji header + bold headline + what shipped + impact + action + link
- Notification strategy: No @here or @channel — informational, not time-sensitive
- Key elements: What deployed, backward compatibility assurance, migration guide link, timeline

**Step 3 - Compose Message**:

**Step 4 - Review**:
- ✅ Concise — readable in 15 seconds
- ✅ Bold headline makes purpose immediately clear
- ✅ Backward compatibility emphasized to prevent alarm
- ✅ Clear action with soft deadline
- ✅ Link to migration guide for self-service

### Generated Slack Message

```
🚀 *API Versioning (v2) is now live in production*

The new v2 routing layer has been deployed. Here's what you need to know:

• *No breaking changes* — all v1 endpoints remain active and fully supported
• v2 introduces versioned routing, improved error responses, and rate limit headers
• v1 will continue to function during the migration period

*What to do:*
1. Review the migration guide: https://wiki.internal/api-v2-migration
2. Start planning your team's migration to v2 endpoints
3. Soft deadline: *end of Q2*

Questions? Drop them in 🧵 below or reach out in #api-platform.
```

---

## Example 2: Bug Report in #incidents Channel

### Scenario
On-call engineer needs to post an incident notification after discovering that the payment processing service is returning intermittent 502 errors affecting ~5% of checkout transactions.

### User Prompt
```
Post an incident in #incidents. Payment processing is returning intermittent 502s — about 5% of checkout transactions are failing. Started around 14:30 UTC. I'm investigating and think it's related to the Redis cache cluster. No customer-facing error page yet, they just see a retry prompt.
```

### Skill Execution

**Step 1 - Understand Intent**:
- **Purpose**: Incident notification — alert teams to an active production issue
- **Channel**: #incidents — high-signal channel, expects structured incident posts
- **Audience**: Engineering, SRE, on-call, and engineering leadership — need impact and status
- **Urgency**: 🚨 High — active production issue affecting customers

**Step 2 - Structure Message**:
- Format: Incident — severity + status + impact + who's investigating + next update time
- Notification strategy: `@here` — active incident requiring awareness from online engineers
- Key elements: Severity, impact quantification, start time, investigation lead, suspected cause

**Step 3 - Compose Message**:

**Step 4 - Review**:
- ✅ Severity and status immediately visible
- ✅ Impact quantified in user-facing terms
- ✅ Investigation ownership clear
- ✅ Next update time committed
- ✅ Thread guidance for coordination

### Generated Slack Message

```
🟠 *SEV-2 — Payment Processing Intermittent Failures*

*Status:* Investigating
*Started:* 14:30 UTC
*Impact:* ~5% of checkout transactions returning 502 errors. Customers see a retry prompt — no error page displayed.

*Investigating:* @on-call-engineer
*Suspected cause:* Redis cache cluster connectivity issues

*Customer impact:* Affected users can retry and most succeed on second attempt. No data loss observed.

Next update in *30 minutes* or when status changes.
🧵 Technical details and coordination in thread ↓
```

---

## Example 3: Sprint Standup Update

### Scenario
Developer needs to post their daily standup update in the team's #team-atlas-standup channel.

### User Prompt
```
Post my standup. Yesterday I finished the database index optimization for the search service — query latency dropped from 800ms to 120ms. Today I'm picking up the caching layer for user profiles (ATLAS-342). Blocked on the Redis cluster upgrade — need DevOps to finish that before I can test.
```

### Skill Execution

**Step 1 - Understand Intent**:
- **Purpose**: Status update — daily standup async post
- **Channel**: #team-atlas-standup — small team channel, expects consistent standup format
- **Audience**: Team Atlas members and their engineering manager — technical, want quick status
- **Urgency**: 📋 Routine — standard daily update

**Step 2 - Structure Message**:
- Format: Standup — yesterday/today/blockers structure with concise bullet points
- Notification strategy: No mentions — standup updates are read asynchronously
- Key elements: Completed work with impact, today's plan with ticket ref, blocker with dependency

**Step 3 - Compose Message**:

**Step 4 - Review**:
- ✅ Standard standup format — easy to scan
- ✅ Yesterday includes measurable impact
- ✅ Today references ticket number
- ✅ Blocker identifies specific dependency and team
- ✅ Concise — under 10 seconds to read

### Generated Slack Message

```
🔄 *Standup — [Date]*

*Yesterday:*
• ✅ Completed database index optimization for search service
  → Query latency: *800ms → 120ms* (85% reduction)

*Today:*
• 🔨 Starting user profile caching layer (`ATLAS-342`)

*Blockers:*
• 🚫 Redis cluster upgrade (DevOps) — need this completed before I can test the caching implementation. @devops-team any ETA?
```

---

## Example 4: RFC/Proposal Announcement

### Scenario
Senior engineer wants to announce a new RFC for migrating from monolith to microservices architecture and solicit feedback from the engineering organization.

### User Prompt
```
Announce my RFC for the monolith-to-microservices migration in #engineering-rfcs. The RFC proposes a strangler fig pattern over 6 months, starting with the auth and notification services. I want feedback by end of next week. The doc is at https://docs.internal/rfc-2025-007.
```

### Skill Execution

**Step 1 - Understand Intent**:
- **Purpose**: Announcement — solicit feedback on a technical proposal
- **Channel**: #engineering-rfcs — dedicated RFC channel, expects structured proposal announcements
- **Audience**: Engineering organization — architects, team leads, and interested ICs
- **Urgency**: ⏰ Time-sensitive — feedback window closes end of next week

**Step 2 - Structure Message**:
- Format: RFC Announcement — title + summary + scope + feedback ask + deadline + link
- Notification strategy: `@here` — RFCs in the dedicated channel warrant attention from active members
- Key elements: RFC number, approach summary, scope, feedback deadline, document link

**Step 3 - Compose Message**:

**Step 4 - Review**:
- ✅ RFC number and title prominent
- ✅ Approach summarized without requiring doc read
- ✅ Scope clearly bounded to first two services
- ✅ Feedback deadline bolded
- ✅ Multiple feedback channels offered

### Generated Slack Message

```
📣 *RFC-2025-007: Monolith to Microservices Migration*

@here — New RFC open for review and feedback.

*Proposal:* Adopt the strangler fig pattern to incrementally extract services from the monolith over a *6-month* timeline.

*Initial scope:*
• Phase 1: Auth service extraction (months 1-2)
• Phase 2: Notification service extraction (months 3-4)
• Phase 3: Evaluate and plan next candidates (months 5-6)

*Key decisions seeking input:*
1. Service boundary definitions for auth and notifications
2. Inter-service communication pattern (sync REST vs. async events)
3. Data migration strategy and dual-write period

📄 *Full RFC:* https://docs.internal/rfc-2025-007

:speech_balloon: *Feedback deadline: Friday, [Date]*
Please comment directly in the doc or drop thoughts in 🧵 below.

cc: @backend-team @platform-team @architecture-guild
```

---

## Example 5: Team Celebration / Recognition Message

### Scenario
Engineering manager wants to recognize a team member who went above and beyond during a critical production incident, resolving it in record time and writing a thorough post-mortem.

### User Prompt
```
Give a shoutout in #engineering to Priya Sharma. She was on-call last weekend when the database failover incident hit. She identified the root cause in 12 minutes, restored service in under 30 minutes, and wrote the most thorough post-mortem we've had. The post-mortem is already driving two infrastructure improvements.
```

### Skill Execution

**Step 1 - Understand Intent**:
- **Purpose**: Celebration/recognition — publicly acknowledge outstanding work
- **Channel**: #engineering — broad engineering audience, appropriate for recognition
- **Audience**: Entire engineering org — will see the recognition and learn what excellence looks like
- **Urgency**: 📋 Routine — celebratory, not time-sensitive

**Step 2 - Structure Message**:
- Format: Recognition — emoji + who + what they did + specific impact + appreciation
- Notification strategy: No @here or @channel — celebratory posts don't need notifications
- Key elements: Name, specific actions, measurable impact, downstream value

**Step 3 - Compose Message**:

**Step 4 - Review**:
- ✅ Name and accomplishment prominent
- ✅ Specific metrics cited (12 min, 30 min) — not vague praise
- ✅ Downstream impact highlighted (infrastructure improvements)
- ✅ Warm but professional tone
- ✅ Invites community reaction

### Generated Slack Message

```
🌟 *Shoutout to @priya.sharma!*

Priya was on-call last weekend when a database failover incident hit production. Here's how she handled it:

• 🔍 Identified the root cause in *12 minutes*
• 🔧 Restored full service in *under 30 minutes*
• 📝 Wrote one of the most thorough post-mortems our team has seen

The best part? Her post-mortem is already driving *two infrastructure improvements* that will make our systems more resilient for everyone.

This is what on-call excellence looks like — fast response, calm execution, and turning incidents into lasting improvements. Thank you, Priya! :tada:
```

---

## Example 6: Cross-Team Request for Help

### Scenario
Frontend team lead needs to request help from the platform team to diagnose a CORS issue that is blocking the release of a new feature, with a deadline of end of day tomorrow.

### User Prompt
```
Post in #platform-support asking for help with a CORS issue. Our new dashboard feature is blocked because API responses from the reporting service are missing CORS headers in staging. We've verified our request headers are correct and this works in local dev. Need someone from platform to look at the API gateway config. We need this resolved by end of day tomorrow because the feature is scheduled for Thursday release.
```

### Skill Execution

**Step 1 - Understand Intent**:
- **Purpose**: Request for help — need technical assistance from another team
- **Channel**: #platform-support — support channel for platform team, expects structured requests
- **Audience**: Platform team engineers — highly technical, need enough detail to diagnose
- **Urgency**: ⏰ Time-sensitive — blocking a Thursday release, need resolution by tomorrow EOD

**Step 2 - Structure Message**:
- Format: Request — clear ask + context + what's been tried + urgency + deadline
- Notification strategy: `@here` — time-sensitive request in the team's support channel
- Key elements: What's broken, what's been tried, where to look, deadline, release context

**Step 3 - Compose Message**:

**Step 4 - Review**:
- ✅ Clear ask in the first line
- ✅ Technical details sufficient for diagnosis
- ✅ What's been tried prevents redundant suggestions
- ✅ Deadline and business context provided
- ✅ Offers to collaborate — not just throwing a problem over the wall

### Generated Slack Message

```
👋 @here *Need help: CORS headers missing on reporting service (staging)*

Our new dashboard feature is *blocked* by a CORS issue in staging, and we need platform team assistance.

*The problem:*
API responses from the reporting service in staging are missing CORS headers (`Access-Control-Allow-Origin`). Requests from the dashboard frontend are being rejected by the browser.

*What we've verified:*
• ✅ Request headers are correctly configured on the frontend
• ✅ Works in local development (direct service-to-service)
• ❌ Fails in staging — headers absent in API gateway responses

*Suspected cause:*
API gateway CORS configuration may not be applied to the reporting service routes in staging.

*Timeline:*
• 🗓 Feature is scheduled for *Thursday release*
• ⏰ Need resolution by *tomorrow EOD* to complete integration testing

Happy to pair on this or hop on a call — reach out to me or drop a note in 🧵.
Thanks! :pray:
```

---

## Summary of Message Types

1. **Deployment Announcement** (🚀) — Inform teams of production changes with impact and action items
2. **Incident Notification** (🟠/🔴) — Structured incident posts with severity, status, impact, and next update
3. **Standup Update** (🔄) — Consistent yesterday/today/blockers format for async standups
4. **RFC Announcement** (📣) — Solicit feedback on proposals with scope, deadline, and discussion channels
5. **Recognition/Celebration** (🌟) — Specific, measurable praise that highlights impact
6. **Cross-Team Request** (👋) — Clear asks with context, attempted solutions, and timeline

## Best Practices

- Lead with the headline — readers decide in the first line whether to read on or scroll past
- Use emoji as visual anchors, not decoration — 🚨 for incidents, ✅ for completions, 📣 for announcements
- Bold the key information — dates, deadlines, status, and decisions should jump off the screen
- Use bullet points for multiple items — never write a paragraph when a list will do
- Keep main channel messages concise — push details, discussion, and updates into threads
- Only use @here and @channel when action or awareness is genuinely needed — notification fatigue is real
- Include a clear call to action — tell readers exactly what you need them to do (or that nothing is needed)
- Reference tickets, docs, and links — let people self-serve for details instead of packing everything into the message
- Match the channel's conventions — an incident post in #incidents follows a different format than a shoutout in #engineering
- When in doubt, shorter is better — you can always add context in a thread
