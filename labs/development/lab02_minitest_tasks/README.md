# Lab 2: Minitest - Task Manager Application

## Overview

Build a task manager application using Minitest, Ruby's built-in testing framework. Compare testing approaches between Minitest and RSpec.

## Learning Objectives

- Write tests with Minitest
- Understand Minitest assertions
- Compare Minitest vs RSpec workflows
- Use fixtures and factories
- Test validations and associations

## Prerequisites

- Ruby 3.2+
- Docker and Docker Compose
- Completed Tutorial 2 (Testing with Minitest)

## Lab Setup

```bash
cd labs/development/lab02_minitest_tasks
docker-compose up -d
docker-compose exec app bundle install
docker-compose exec app rails db:create db:migrate
docker-compose exec app rails test
```

## Exercises

### Exercise 1: Task Model Tests

Requirements:
- Title (required, minimum 5 characters)
- Description (optional)
- Status (pending, in_progress, completed)
- Due date validation
- belongs_to :user

### Exercise 2: User Model Tests

Requirements:
- Email validation
- has_many :tasks
- Methods: `overdue_tasks`, `completed_tasks_count`

### Exercise 3: Controller Tests

Test TasksController:
- index, show, create, update, destroy
- Proper authorization
- Error handling

### Exercise 4: Integration Tests

Test complete workflows:
- Creating and completing tasks
- Filtering tasks by status
- Marking tasks as overdue

## Success Criteria

- [ ] All Minitest tests pass
- [ ] Proper use of assertions
- [ ] Tests cover edge cases
- [ ] Compare with RSpec patterns

## Resources

- Tutorial 2: Testing with Minitest
- [Minitest Documentation](https://github.com/seattlerb/minitest)
