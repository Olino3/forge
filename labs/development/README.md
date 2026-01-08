# Ruby Development Labs

Hands-on laboratories for practicing professional Ruby development skills. Each lab is a complete mini-application with its own Docker environment, allowing you to practice the concepts covered in the tutorials in isolation.

## Overview

These labs provide practical, project-based learning experiences. Each lab:
- Is a complete, runnable Ruby/Rails application
- Has its own Docker container setup for isolation
- Includes comprehensive exercises and challenges
- Maps to specific tutorials
- Follows real-world Ruby project structures

## Prerequisites

- Docker and Docker Compose installed
- Completed corresponding tutorials
- Basic command line knowledge
- Git for version control (optional)

## Lab List

### Lab 1: RSpec Testing - Mini Blog Application
**Tutorial References:** Tutorials 1, 3
**Duration:** 3-4 hours
**Topics:** RSpec, TDD, FactoryBot, test organization

Build a blog application using Test-Driven Development with RSpec. Practice writing model tests, controller tests, and feature tests while following the Red-Green-Refactor cycle.

**Key Skills:**
- Writing RSpec tests
- Using FactoryBot for test data
- Testing models, controllers, and features
- TDD workflow

```bash
cd lab01_rspec_blog
docker-compose up -d
docker-compose exec app rspec
```

### Lab 2: Minitest - Task Manager Application
**Tutorial Reference:** Tutorial 2
**Duration:** 2-3 hours
**Topics:** Minitest, assertions, integration tests

Build a task management system using Minitest. Compare approaches with RSpec and understand when to choose each framework.

**Key Skills:**
- Minitest assertions
- Testing with plain Ruby syntax
- Integration tests
- Comparing testing frameworks

```bash
cd lab02_minitest_tasks
docker-compose up -d
docker-compose exec app rails test
```

### Lab 3: Background Jobs with Sidekiq
**Tutorial Reference:** Tutorial 9
**Duration:** 3-4 hours
**Topics:** Sidekiq, Redis, asynchronous processing, job scheduling

Implement a background job processing system for handling emails, reports, and scheduled tasks.

**Key Skills:**
- Creating Sidekiq workers
- Job scheduling and retries
- Error handling
- Monitoring with Sidekiq Web UI

```bash
cd lab03_sidekiq_jobs
docker-compose up -d
# Access Sidekiq UI at http://localhost:3000/sidekiq
```

### Lab 4: Service Objects Refactoring
**Tutorial Reference:** Tutorial 7
**Duration:** 2-3 hours
**Topics:** Service Objects, SOLID principles, refactoring

Refactor a messy Rails application by extracting business logic into Service Objects.

**Key Skills:**
- Identifying fat controllers/models
- Creating Service Objects
- Single Responsibility Principle
- Testing service objects

```bash
cd lab04_service_objects
docker-compose up -d
```

### Lab 5: Code Quality and Linting
**Tutorial References:** Tutorials 5, 6
**Duration:** 2 hours
**Topics:** RuboCop, StandardRB, code quality, CI/CD

Set up and configure code quality tools, fix violations, and integrate into CI pipeline.

**Key Skills:**
- Configuring RuboCop
- Using StandardRB
- Auto-fixing violations
- CI/CD integration

```bash
cd lab05_code_quality
docker-compose exec app rubocop
docker-compose exec app rubocop -a  # Auto-fix
```

### Lab 6: Security Best Practices
**Tutorial Reference:** Tutorial 12
**Duration:** 3-4 hours
**Topics:** Secrets management, security vulnerabilities, authentication

Identify and fix common security vulnerabilities in a Rails application.

**Key Skills:**
- Secrets management with ENV variables
- Preventing SQL injection
- XSS prevention
- CSRF protection
- Secure authentication

```bash
cd lab06_security
docker-compose up -d
docker-compose exec app bundle exec brakeman
```

## Getting Started

### 1. Choose a Lab

Start with Lab 1 (RSpec Testing) if you're new, or jump to any lab based on your learning goals.

### 2. Navigate to Lab Directory

```bash
cd labs/development/lab0X_name
```

### 3. Start the Environment

```bash
docker-compose up -d
```

This starts all necessary services (database, Redis, web server, etc.) in isolated containers.

### 4. Set Up the Application

```bash
# Install dependencies
docker-compose exec app bundle install

# Create database
docker-compose exec app rails db:create db:migrate

# Run seeds (if available)
docker-compose exec app rails db:seed
```

### 5. Run Tests

```bash
# RSpec labs
docker-compose exec app rspec

# Minitest labs
docker-compose exec app rails test

# Specific file
docker-compose exec app rspec spec/models/user_spec.rb
```

### 6. Access the Application

Most labs run on http://localhost:3000

Some labs include web UIs:
- Sidekiq: http://localhost:3000/sidekiq

### 7. Make Changes

Edit files locally. Changes are synced to the container via volume mounts.

### 8. Clean Up

```bash
docker-compose down
docker-compose down -v  # Also remove volumes
```

## Lab Structure

Each lab follows this structure:

```
labXX_name/
├── README.md              # Lab instructions and exercises
├── Dockerfile             # Container definition
├── docker-compose.yml     # Multi-container setup
├── Gemfile                # Ruby dependencies
├── app/                   # Application code
│   ├── models/
│   ├── controllers/
│   └── workers/ (if applicable)
├── spec/ or test/         # Test files
├── config/                # Configuration
└── .env.example           # Example environment variables
```

## Tips for Success

### 1. Read the README First
Each lab's README contains:
- Learning objectives
- Prerequisites
- Exercise instructions
- Success criteria
- Resources

### 2. Follow TDD
For testing labs, write tests FIRST, then implement features.

### 3. Use Docker Logs
Debug issues with:
```bash
docker-compose logs app
docker-compose logs db
```

### 4. Enter the Container
For interactive debugging:
```bash
docker-compose exec app bash
docker-compose exec app rails console
```

### 5. Check Your Work
Each lab has success criteria. Verify you've met them before moving on.

### 6. Clean Up Between Labs
Stop containers when switching labs:
```bash
docker-compose down
```

### 7. Experiment!
These labs are sandboxed. Break things, experiment, and learn.

## Common Commands

### Docker Commands
```bash
docker-compose up -d              # Start services
docker-compose down               # Stop services
docker-compose ps                 # List running services
docker-compose logs -f app        # Follow app logs
docker-compose exec app bash      # Enter container shell
docker-compose restart app        # Restart a service
docker-compose down -v            # Remove everything including volumes
```

### Rails Commands (inside container)
```bash
docker-compose exec app rails console
docker-compose exec app rails db:migrate
docker-compose exec app rails routes
docker-compose exec app rails generate model User
```

### Testing Commands
```bash
docker-compose exec app rspec
docker-compose exec app rspec --format documentation
docker-compose exec app rspec spec/models
docker-compose exec app rails test
docker-compose exec app rubocop
```

## Troubleshooting

### Port Already in Use
If port 3000 is busy, edit docker-compose.yml:
```yaml
ports:
  - "3001:3000"  # Use port 3001 instead
```

### Database Connection Issues
```bash
docker-compose down
docker-compose up -d db
# Wait 10 seconds
docker-compose up -d app
```

### Dependency Issues
```bash
docker-compose down
docker-compose build --no-cache
docker-compose up -d
docker-compose exec app bundle install
```

### Clean Slate
```bash
docker-compose down -v
docker-compose up -d
docker-compose exec app rails db:create db:migrate
```

## Learning Path

**Beginner Path:**
1. Lab 1: RSpec Testing
2. Lab 2: Minitest
3. Lab 5: Code Quality

**Intermediate Path:**
1. Lab 3: Background Jobs
2. Lab 4: Service Objects
3. Lab 6: Security

**Advanced Path:**
Complete all labs, then try combining concepts:
- Add background jobs to Lab 1
- Add security features to Lab 3
- Refactor Lab 2 with Service Objects

## Additional Resources

### Tutorials
All labs reference specific tutorials in `/ruby/tutorials/development/`. Review these first for context.

### Documentation
- [Ruby Docs](https://ruby-doc.org/)
- [Rails Guides](https://guides.rubyonrails.org/)
- [RSpec](https://rspec.info/)
- [Sidekiq](https://github.com/mperham/sidekiq)

### Community
- [Ruby Reddit](https://www.reddit.com/r/ruby/)
- [Rails Discord](https://discord.gg/d8N68BCw)
- [Stack Overflow](https://stackoverflow.com/questions/tagged/ruby)

## Contributing

Found an issue or have improvements?
1. Open an issue
2. Submit a pull request
3. Share feedback

## License

These labs are part of the Forge project. See main repository LICENSE.

## Next Steps

After completing these labs:
1. Build your own Ruby/Rails projects
2. Contribute to open source Ruby projects
3. Explore advanced topics (metaprogramming, performance optimization)
4. Join the Ruby community

**Happy Coding! 🚀**
