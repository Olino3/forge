# Lab 1: RSpec Testing - Mini Blog Application

## Overview

Build a mini blog application using Test-Driven Development (TDD) with RSpec. This lab gives you hands-on experience with RSpec testing patterns, FactoryBot, and Rails testing best practices.

## Learning Objectives

- Write tests before implementation (TDD)
- Use RSpec for model, controller, and feature tests
- Create test data with FactoryBot
- Understand test organization and best practices
- Practice Red-Green-Refactor cycle

## Prerequisites

- Ruby 3.2+
- Docker and Docker Compose (for containerized environment)
- Basic Rails knowledge
- Completed Tutorial 1 (Testing with RSpec)

## Lab Setup

### Using Docker (Recommended)

```bash
cd labs/development/lab01_rspec_blog
docker-compose up -d
docker-compose exec app bundle install
docker-compose exec app rails db:create db:migrate
docker-compose exec app rspec
```

## Project Structure

This lab provides a skeleton Rails app. You'll write tests and implement features using TDD.

```
lab01_rspec_blog/
├── app/models/         # Implement models here
├── spec/
│   ├── models/         # Write model tests
│   ├── controllers/    # Write controller tests
│   ├── features/       # Write feature tests
│   └── factories/      # Define FactoryBot factories
├── Dockerfile
├── docker-compose.yml
└── README.md
```

## Exercises

### Exercise 1: User Model (TDD)

Write RSpec tests for a User model with these requirements:
- Email (required, valid format, unique)
- Name (required)
- has_many :posts

### Exercise 2: Post Model (TDD)

Test a Post model:
- belongs_to :user
- Title and body (both required)
- has_many :comments
- `excerpt` method (first 100 chars)

### Exercise 3: Controller Tests

Test PostsController CRUD actions with authentication.

### Exercise 4: Feature Tests

Test complete workflows:
- Creating a post
- Commenting on a post
- Editing/deleting own posts

## Success Criteria

- [ ] All tests pass
- [ ] 90%+ test coverage
- [ ] Following TDD (tests first)
- [ ] Clean, readable test code

## Resources

- Tutorial 1: Testing with RSpec
- Tutorial 3: Test Data with FactoryBot
- [RSpec Documentation](https://rspec.info/)
