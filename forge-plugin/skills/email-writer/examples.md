# Email Writer Examples

This file contains example scenarios demonstrating how to use the email-writer skill to compose professional correspondence for various communication needs.

---

## Example 1: Project Status Update to Stakeholders

### Scenario
Engineering lead needs to send a weekly status update to stakeholders about an API migration project.

### User Prompt
```
Write a status update email to stakeholders about our API v2 migration. We're 70% complete, on track for the March deadline, but we hit a snag with the auth service that cost us 3 days. The team resolved it by implementing a token bridge.
```

### Skill Execution

**Step 1 - Gather Context**:
- **Purpose**: Status update — inform stakeholders of progress, blockers, and timeline
- **Audience**: Stakeholders (product managers, engineering directors) — semi-technical, care about timelines and risks
- **Urgency**: Routine weekly update
- **Tone**: Professional, confident, transparent about the blocker

**Step 2 - Structure Content**:
- Format: Status Update — progress summary, blocker/resolution, timeline, next steps
- Key points: 70% complete, on track, auth blocker resolved, no timeline impact
- Action items: None — FYI only

**Step 3 - Compose Email**:

**Step 4 - Review**:
- ✅ Purpose stated in opening sentence
- ✅ Blocker presented with resolution — shows transparency and competence
- ✅ Timeline confidence reinforced
- ✅ No action required — clearly marked as FYI

### Generated Email

**To**: api-migration-stakeholders@company.com
**CC**: engineering-leads@company.com
**Subject**: [Update] API v2 Migration — 70% Complete, On Track for March

---

Hi team,

Here's the weekly update on the API v2 migration. **We are 70% complete and remain on track for the March deadline.**

**Progress This Week:**
- Completed migration of 8 remaining endpoints to v2 schema
- Integration tests passing for all migrated services
- Client SDK updates drafted and under review

**Blocker Resolved:**
We encountered an authentication compatibility issue when migrating the auth service to the new token format. This cost approximately 3 days of investigation. The team resolved it by implementing a token bridge that translates v1 tokens during the transition period, allowing both versions to coexist without disruption. The 3-day delay has been absorbed by our buffer — no impact to the March timeline.

**Next Week:**
- Begin migration of payment processing endpoints
- Start canary deployment of migrated services to staging
- Finalize client SDK documentation

No action is required from this group. I'll flag any timeline risks immediately if they arise.

Best regards,
[Your Name]

---

## Example 2: Technical Incident Post-Mortem Notification

### Scenario
SRE team lead needs to notify engineering and product teams about a completed post-mortem for a production outage.

### User Prompt
```
Write an email sharing the post-mortem for last Tuesday's 45-minute production outage. Root cause was a misconfigured database connection pool that exhausted under load. We've implemented connection pool monitoring and auto-scaling as remediation. Link to full post-mortem doc: https://wiki.internal/postmortem-2025-01-14
```

### Skill Execution

**Step 1 - Gather Context**:
- **Purpose**: Announcement — share post-mortem findings and remediation
- **Audience**: Engineering and product teams — technical, need to understand impact and prevention
- **Urgency**: Timely follow-up, not urgent
- **Tone**: Transparent, blameless, action-oriented

**Step 2 - Structure Content**:
- Format: Incident Follow-up — summary, root cause, impact, remediation, link to full document
- Key points: 45-min outage, root cause identified, remediation implemented
- Action items: Review post-mortem document, share feedback

**Step 3 - Compose Email**:

**Step 4 - Review**:
- ✅ Blameless language throughout
- ✅ Impact clearly quantified
- ✅ Remediation actions are concrete and already implemented
- ✅ Link to full document for those who want details

### Generated Email

**To**: engineering-all@company.com
**CC**: product-team@company.com
**Subject**: [Post-Mortem] Jan 14 Production Outage — Root Cause & Remediation

---

Hi everyone,

The post-mortem for last Tuesday's production outage is now complete. I'm sharing the summary below with a link to the full document for your review.

**Incident Summary:**
- **Duration**: 45 minutes (14:23–15:08 UTC, January 14, 2025)
- **Impact**: API error rate spiked to 34%; approximately 2,100 requests failed
- **Detection**: Automated alerting triggered at 14:25 UTC; on-call responded within 2 minutes

**Root Cause:**
The database connection pool was configured with a static maximum of 20 connections. During a traffic surge, all connections were exhausted, causing cascading request failures. The configuration had not been updated since the service was originally provisioned at lower traffic levels.

**Remediation (Implemented):**
1. Connection pool maximum increased to 100 with dynamic scaling based on load
2. Added connection pool utilization monitoring with alerts at 70% and 90% thresholds
3. Runbook updated with connection pool troubleshooting procedures
4. Automated load testing added to deployment pipeline to catch pool exhaustion under simulated traffic

**Full Post-Mortem**: https://wiki.internal/postmortem-2025-01-14

**Action Requested**: Please review the post-mortem document and share any feedback or questions in the #incident-review channel by end of week. If your team manages services with similar connection pool configurations, we recommend auditing your settings using the checklist in Section 4 of the document.

Thank you to everyone who helped during the incident and the review process.

Best regards,
[Your Name]

---

## Example 3: Feature Release Announcement

### Scenario
Product manager needs to announce a new feature release to internal teams and prepare them for customer-facing communication.

### User Prompt
```
Announce the launch of our new real-time collaboration feature to internal teams. It goes live next Monday. Sales and support need to know how to talk about it. There's a demo video and FAQ doc ready.
```

### Skill Execution

**Step 1 - Gather Context**:
- **Purpose**: Announcement — inform teams of upcoming feature launch, enable customer-facing readiness
- **Audience**: Sales, support, engineering, product — mixed technical levels, need talking points
- **Urgency**: Time-sensitive — launch is next Monday
- **Tone**: Enthusiastic but professional, enabling and informative

**Step 2 - Structure Content**:
- Format: Announcement — what's launching, when, why it matters, resources, action items by team
- Key points: Real-time collaboration, Monday launch, demo and FAQ available
- Action items: Sales and support to review materials; engineering to monitor

**Step 3 - Compose Email**:

**Step 4 - Review**:
- ✅ Launch date prominent and bolded
- ✅ Resources linked for self-service enablement
- ✅ Action items segmented by team role
- ✅ Enthusiasm appropriate without overpromising

### Generated Email

**To**: all-hands@company.com
**Subject**: [Launch] Real-Time Collaboration Goes Live Monday, Jan 20 🚀

---

Hi everyone,

I'm excited to announce that **Real-Time Collaboration** will go live for all customers on **Monday, January 20**. This is one of our most requested features, and it's ready for launch.

**What's Launching:**
Real-time collaboration allows multiple users to edit documents, dashboards, and configurations simultaneously with live cursor tracking, instant sync, and conflict resolution. Think Google Docs-style editing, built natively into our platform.

**Why It Matters:**
- Addresses the #1 feature request from enterprise customers in Q3/Q4 surveys
- Eliminates the "save conflict" pain point that generates ~200 support tickets/month
- Differentiates us from competitors who only offer lock-based editing

**Resources:**
- 📹 **Demo Video**: https://wiki.internal/realtime-collab-demo
- 📄 **FAQ Document**: https://wiki.internal/realtime-collab-faq
- 📊 **Feature Spec**: https://wiki.internal/realtime-collab-spec

**Action Items by Team:**

| Team | Action | Deadline |
|------|--------|----------|
| **Sales** | Review demo video and FAQ; update pitch decks | Friday, Jan 17 |
| **Support** | Review FAQ and known limitations; update runbooks | Friday, Jan 17 |
| **Engineering** | Monitor performance dashboards post-launch | Monday, Jan 20 |
| **Marketing** | Blog post and social media scheduled | Monday, Jan 20 |

If you have questions before launch, drop them in the #realtime-collab channel and we'll address them promptly.

Let's make this a great launch! 🎉

Best regards,
[Your Name]

---

## Example 4: Request for Code Review / Collaboration

### Scenario
Developer needs to request a thorough code review from a senior engineer for a complex PR that touches authentication logic.

### User Prompt
```
Ask Sarah Chen to review my PR #472 which refactors the OAuth2 flow. It's 800 lines across 12 files, touches the token refresh logic, and I'd appreciate her security expertise. I need the review by Thursday because we're deploying Friday.
```

### Skill Execution

**Step 1 - Gather Context**:
- **Purpose**: Request — ask for code review with specific expertise and deadline
- **Audience**: Senior engineer (Sarah Chen) — highly technical, security expertise
- **Urgency**: Time-sensitive — review needed by Thursday for Friday deploy
- **Tone**: Respectful, specific, appreciative of expertise

**Step 2 - Structure Content**:
- Format: Request — what's needed, why this reviewer, key areas to focus on, deadline
- Key points: PR #472, OAuth2 refactor, 800 lines/12 files, security focus, Thursday deadline
- Action items: Review PR by Thursday

**Step 3 - Compose Email**:

**Step 4 - Review**:
- ✅ Specific about what's needed and why
- ✅ Highlights areas requiring security expertise
- ✅ Provides context to make the review efficient
- ✅ Deadline is clear with reasoning

### Generated Email

**To**: sarah.chen@company.com
**Subject**: [Review Request] PR #472 — OAuth2 Flow Refactor (by Thursday)

---

Hi Sarah,

I'd appreciate your review on **PR #472**, which refactors our OAuth2 authentication flow. Given your security expertise, you're the ideal reviewer for this change.

**PR Overview:**
- **Scope**: 800 lines across 12 files
- **Link**: https://github.com/org/repo/pull/472
- **Branch**: `refactor/oauth2-flow`

**What Changed:**
- Restructured the token refresh logic to handle concurrent refresh requests without race conditions
- Migrated from implicit grant to authorization code flow with PKCE
- Added token rotation on refresh to limit exposure window
- Updated error handling for expired and revoked tokens

**Areas Where I'd Value Your Input:**
1. **Token refresh concurrency** — I used a mutex-based approach; curious if you see edge cases
2. **PKCE implementation** — First time implementing this; want to ensure it follows RFC 7636 correctly
3. **Token rotation security** — Does the rotation strategy adequately limit blast radius?

**Timeline**: I'm targeting a **Friday deployment**, so I'd need your review by **end of day Thursday**. If that's too tight, please let me know and I can adjust the deploy schedule.

Happy to walk you through the changes in person or on a call if that would be more efficient. Thanks for your time!

Best regards,
[Your Name]

---

## Example 5: Meeting Follow-Up with Action Items

### Scenario
Project manager needs to send a follow-up email after a sprint planning meeting with clear decisions and action items.

### User Prompt
```
Write a follow-up email for today's sprint planning meeting. Attendees: dev team, QA lead, product owner. Key decisions: we're deprioritizing the dashboard redesign to focus on the payment integration. Action items: Alex builds the payment API client by Wednesday, Jamie writes integration tests by Friday, Maria updates the sprint board today.
```

### Skill Execution

**Step 1 - Gather Context**:
- **Purpose**: Follow-up — document decisions and action items from meeting
- **Audience**: Meeting attendees (dev team, QA lead, product owner) — technical, need clarity on commitments
- **Urgency**: Same-day follow-up to establish accountability
- **Tone**: Clear, direct, collaborative

**Step 2 - Structure Content**:
- Format: Follow-up — reference meeting, decisions, action items with owners and deadlines
- Key points: Dashboard deprioritized, payment integration prioritized, three action items
- Action items: Three with specific owners and deadlines

**Step 3 - Compose Email**:

**Step 4 - Review**:
- ✅ Decisions documented clearly
- ✅ Action items have owners and deadlines
- ✅ Rationale for deprioritization included
- ✅ Opens door for corrections if anyone remembers differently

### Generated Email

**To**: dev-team@company.com, jamie.qalead@company.com, maria.product@company.com
**Subject**: [Follow-Up] Sprint Planning — Payment Integration Priority & Action Items

---

Hi team,

Thanks for a productive sprint planning session today. Below is a summary of the key decisions and action items for the record.

**Key Decisions:**

1. **Dashboard redesign deprioritized** — We're moving the dashboard redesign to the next sprint to focus engineering capacity on the payment integration, which is blocking the enterprise launch timeline.

2. **Payment integration is the sprint priority** — All available dev resources will focus on the Stripe payment integration this sprint. Target: feature-complete by end of sprint (Friday, Jan 24).

**Action Items:**

| Owner | Task | Deadline |
|-------|------|----------|
| **Alex** | Build the payment API client and webhook handlers | Wednesday, Jan 22 |
| **Jamie** | Write integration tests for payment flow (happy path + error cases) | Friday, Jan 24 |
| **Maria** | Update sprint board to reflect reprioritization | Today, Jan 17 |

**Parking Lot:**
- Dashboard redesign will be re-evaluated in next sprint planning
- Alex to flag any Stripe API limitations by end of day Monday

If I've missed anything or misrepresented a decision, please reply to this thread so we can correct the record.

Thanks,
[Your Name]

---

## Example 6: Escalation Email to Management

### Scenario
Tech lead needs to escalate a critical dependency risk to engineering management that threatens a product launch deadline.

### User Prompt
```
Escalate to my VP of Engineering that our launch is at risk because the third-party payment provider (StripeConnect) hasn't delivered their sandbox API credentials despite 3 weeks of follow-up. We've contacted their support twice and our account manager once. If we don't get credentials by Friday, we'll miss the Feb 1 launch window and the next available window is March 1.
```

### Skill Execution

**Step 1 - Gather Context**:
- **Purpose**: Escalation — raise a blocking risk to leadership for intervention
- **Audience**: VP of Engineering — executive, needs impact and options, not technical details
- **Urgency**: High — Friday deadline before launch impact
- **Tone**: Professional, urgent without panic, solution-oriented

**Step 2 - Structure Content**:
- Format: Escalation — issue summary, business impact, actions taken, help needed, deadline
- Key points: Credentials blocked 3 weeks, Feb 1 launch at risk, next window March 1
- Action items: VP to escalate with vendor executive contact

**Step 3 - Compose Email**:

**Step 4 - Review**:
- ✅ Impact leads — business consequence is immediately clear
- ✅ Actions already taken demonstrate due diligence
- ✅ Specific ask — not vague "help needed"
- ✅ Options provided with trade-offs
- ✅ Deadline is explicit

### Generated Email

**To**: vp.engineering@company.com
**CC**: director.engineering@company.com
**Subject**: [Escalation] Feb 1 Launch at Risk — StripeConnect Credentials Blocked

---

Hi [VP Name],

I'm escalating a blocking dependency risk that threatens our **February 1 product launch**. I need your help to resolve this by **Friday, January 24**.

**The Issue:**
Our third-party payment provider (StripeConnect) has not delivered the sandbox API credentials required to complete payment integration and testing. Without these credentials, we cannot validate the payment flow, which is a hard launch requirement.

**Business Impact:**
- If credentials are not received by **Friday, Jan 24**, we will miss the **Feb 1 launch window**
- The next available launch window is **March 1** — a 4-week delay
- Revenue impact: estimated $180K in delayed enterprise contracts awaiting this feature
- Three enterprise customers have launch-contingent contracts with Feb 15 activation dates

**Actions Already Taken:**
1. **Jan 3**: Initial credential request submitted through StripeConnect developer portal
2. **Jan 10**: Follow-up with StripeConnect technical support (ticket #SC-8842) — response: "being processed"
3. **Jan 17**: Second follow-up with support — no new information provided
4. **Jan 17**: Contacted our StripeConnect account manager (Dana Rivera) — awaiting response

**What I Need:**
Could you reach out to your executive contact at StripeConnect to expedite the credential provisioning? An executive-to-executive escalation may bypass the support queue that has been unresponsive for 3 weeks.

**Options If Credentials Are Delayed:**
| Option | Trade-off |
|--------|-----------|
| **A. Executive escalation** (recommended) | Fastest path to unblocking; no launch delay |
| **B. Delay launch to March 1** | 4-week delay; requires customer communication |
| **C. Launch without payment integration** | Reduced feature set; manual payment processing as stopgap |

I'm happy to provide any additional context or join a call with StripeConnect if helpful.

Regards,
[Your Name]

---

## Summary of Email Types

1. **Status Update** (`[Update]`) — Regular progress communication to stakeholders
2. **Post-Mortem Notification** (`[Post-Mortem]`) — Blameless incident follow-up with findings and remediation
3. **Feature Announcement** (`[Launch]`) — Internal enablement for upcoming releases
4. **Review Request** (`[Review Request]`) — Targeted request for expertise with clear scope and deadline
5. **Meeting Follow-Up** (`[Follow-Up]`) — Decisions and action items documented for accountability
6. **Escalation** (`[Escalation]`) — Risk elevation to leadership with impact, actions taken, and options

## Best Practices

- Always state the purpose in the first sentence — recipients should know why they're reading
- Lead with impact for executive audiences; lead with details for technical audiences
- Use subject line prefixes (`[Action Required]`, `[FYI]`, `[Urgent]`) to set expectations
- Keep emails scannable — use bullets, tables, and bold text for key information
- Every action item needs an owner and a deadline
- Be explicit about whether a response is expected and by when
- For sensitive topics, draft the email, step away, and review with fresh eyes before sending
- When in doubt, shorter is better — link to documents for details
- Always maintain a blameless, professional tone even in escalations and incident communications
- Proofread for tone — read the email as if you were the recipient
