# Lab 3: Background Jobs with Sidekiq

## Overview

Build a system for processing background jobs using Sidekiq and Redis. Learn to handle asynchronous tasks, job scheduling, and error handling.

## Learning Objectives

- Create Sidekiq workers
- Schedule background jobs
- Handle job failures and retries
- Use Sidekiq Web UI
- Test background jobs

## Prerequisites

- Ruby 3.2+
- Docker and Docker Compose
- Completed Tutorial 9 (Essential Gems - Sidekiq section)

## Lab Setup

```bash
cd labs/development/lab03_sidekiq_jobs
docker-compose up -d
docker-compose exec app bundle install
```

Access Sidekiq Web UI at: http://localhost:3000/sidekiq

## Exercises

### Exercise 1: Email Worker

Create a worker to send emails asynchronously:
- Welcome emails for new users
- Password reset emails
- Weekly digest emails

### Exercise 2: Report Generator

Create a worker for heavy computations:
- Generate PDF reports
- Export data to CSV
- Process large datasets

### Exercise 3: Scheduled Jobs

Implement recurring tasks:
- Daily cleanup of old records
- Hourly data synchronization
- Weekly summary reports

### Exercise 4: Error Handling

Implement robust error handling:
- Retry logic with exponential backoff
- Dead letter queue
- Error notifications
- Job monitoring

## Project Structure

```
lab03_sidekiq_jobs/
├── app/workers/
│   ├── email_worker.rb
│   ├── report_generator_worker.rb
│   └── cleanup_worker.rb
├── config/
│   └── sidekiq.yml
├── spec/workers/
└── docker-compose.yml (includes Redis)
```

## Success Criteria

- [ ] Workers process jobs correctly
- [ ] Proper error handling and retries
- [ ] Scheduled jobs run on time
- [ ] All worker tests pass
- [ ] Monitoring via Sidekiq Web UI

## Resources

- Tutorial 9: Essential Gems (Sidekiq)
- [Sidekiq Documentation](https://github.com/mperham/sidekiq)
- [Sidekiq Best Practices](https://github.com/mperham/sidekiq/wiki/Best-Practices)
