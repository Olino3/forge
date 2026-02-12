# Rails Skill Examples

This file provides sample usage scenarios for the `rails` skill.

---

## Example 1: Service Object Refactor

### Scenario
A Rails app has bloated controllers that need service extraction.

### User Prompt
"Refactor our checkout flow into service objects."

### Skill Execution
- **Step 1**: Confirm Rails 7, payment stack, and controller scope.
- **Step 2**: Load memory for `storefront` conventions.
- **Step 3**: Load engineering and security context.
- **Step 4**: Inspect controllers and models.
- **Step 5**: Recommend service object structure.
- **Step 6**: Output to `/claudedocs/rails_storefront_2026-02-12.md`.

### Generated Output
```markdown
# Rails Guidance - storefront

## Service Object Plan
- Create `Checkout::CreateOrder`
- Move payment logic into `Checkout::ChargePayment`
- Keep controllers thin with `render` only
```

---

## Example 2: N+1 Query Elimination

### Scenario
The dashboard loads slowly due to N+1 queries.

### User Prompt
"Optimize our dashboard queries and caching."

### Skill Execution
- **Step 1**: Confirm affected models and scope.
- **Step 2**: Load memory for performance notes.
- **Step 3**: Load engineering context.
- **Step 4**: Inspect ActiveRecord queries.
- **Step 5**: Recommend eager loading and caching.
- **Step 6**: Output to `/claudedocs/rails_dashboard_2026-02-12.md`.

### Generated Output
```markdown
# Rails Guidance - dashboard

## Query Fixes
- Add `includes(:account, :owner)` for dashboard queries
- Remove per-row count queries with `counter_cache`

## Caching
- Cache dashboard widgets for 2 minutes
- Invalidate on account updates
```

---

## Example 3: Background Job Strategy

### Scenario
Sending receipts should move to Sidekiq.

### User Prompt
"Move receipt emails to background jobs with retries."

### Skill Execution
- **Step 1**: Confirm ActiveJob adapter and email stack.
- **Step 2**: Load memory for job queue notes.
- **Step 3**: Load engineering context.
- **Step 4**: Review current mailer usage.
- **Step 5**: Recommend Sidekiq job and retry strategy.
- **Step 6**: Output to `/claudedocs/rails_jobs_2026-02-12.md`.

### Generated Output
```markdown
# Rails Guidance - jobs

## Job Setup
- Use `ReceiptMailerJob` with `queue_as :mailers`
- Add retry with exponential backoff (5 attempts)

## Monitoring
- Enable Sidekiq web UI behind admin auth
```
