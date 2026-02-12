# /brainstorm Examples

## Example 1: New Feature Exploration

```
/brainstorm "user notification system" --depth normal
```

**What happens**:
1. Begins Socratic dialogue:
   - "What types of notifications (email, push, in-app)?"
   - "Who receives notifications and when?"
   - "What's the priority for real-time vs batched?"
2. Gathers 5-10 responses through progressive questioning
3. Generates requirements document with user stories
4. Identifies scope: Medium (M) - multiple components needed
5. Saves to `/claudedocs/requirements_notifications_20260209.md`

## Example 2: Deep Feature Exploration

```
/brainstorm "payment processing integration" --depth deep
```

**What happens**:
1. Phase 1 - Clarifying:
   - "Which payment providers (Stripe, PayPal, Square)?"
   - "What payment methods (credit card, ACH, crypto)?"
2. Phase 2 - Probing:
   - "What compliance requirements (PCI DSS, SOC 2)?"
   - "What's the expected transaction volume?"
3. Phase 3 - Exploring:
   - "What's the MVP: single provider + credit card?"
   - "What happens on payment failure? Retry logic?"
4. Generates comprehensive requirements with risk assessment
5. Identifies: High risk, Large (L) scope, PCI compliance needed

## Example 3: Quick Exploration

```
/brainstorm "add export to CSV feature" --depth shallow
```

**What happens**:
1. Quick 3-5 questions:
   - "Which data should be exportable?"
   - "Any size limits or pagination for large exports?"
   - "Should it be synchronous or background job?"
2. Generates concise requirements: 2-3 user stories
3. Scope: Small (S), Low risk
4. Recommends proceeding to `/implement`

## Example 4: Data-Driven Feature

```
/brainstorm "analytics dashboard" --depth deep
```

**What happens**:
1. Identifies data modeling is central
2. Delegates to `skill:database-schema-analysis` to understand existing data
3. Explores through dialogue:
   - "Which metrics are most important?"
   - "What time ranges (daily, weekly, monthly)?"
   - "Real-time updates or periodic refresh?"
4. Generates requirements with data model considerations
5. Lists integration points with existing schema

## Example 5: API Feature

```
/brainstorm "REST API for partner integrations" --depth normal --output stories
```

**What happens**:
1. Explores partner integration requirements:
   - "Which partners and what data do they need?"
   - "Authentication: API keys, OAuth, or both?"
   - "Rate limiting requirements?"
2. Generates user stories in Given/When/Then format
3. Identifies non-functional requirements (rate limits, SLAs)
4. Output focused on user stories per `--output stories`

## Example 6: Building on Previous Brainstorm

```
/brainstorm "extend notification system with scheduling" --depth normal
```

**What happens** (with existing memory):
1. Loads previous brainstorm notes for notification system
2. References existing requirements as starting point
3. Focuses questions on scheduling-specific needs:
   - "Schedule by time zone or UTC?"
   - "Recurring schedules or one-time only?"
4. Generates addendum to existing requirements
5. Updates brainstorm memory with new decisions
