# Tutorial 9: Essential Gems - Bundler, Pry, Sidekiq, and Bullet

## Overview

A Ruby developer is only as good as their ability to leverage the community's existing work. This tutorial covers four essential tools that every professional Rubyist must master: Bundler (dependency management), Pry (debugging), Sidekiq (background jobs), and Bullet (performance monitoring).

## Python Comparison

All these tools have Python equivalents:

| Ruby | Python | Purpose |
|------|--------|---------|
| Bundler | pip + virtualenv/poetry | Dependency management |
| Pry | ipdb/pdb++ | Interactive debugger |
| Sidekiq | Celery/RQ | Background job processing |
| Bullet | django-silk/py-spy | Performance monitoring |

## 1. Bundler: Dependency Management

Bundler ensures every developer on your project uses the exact same versions of libraries (gems).

### Installation

Bundler comes with Ruby 2.6+, but you can install/update it:

```bash
gem install bundler
```

**Python comparison:**
```bash
pip install virtualenv
# or
pip install poetry
```

### The Gemfile

The `Gemfile` defines your project's dependencies:

```ruby
# Gemfile
source 'https://rubygems.org'

ruby '3.2.0'  # Specify Ruby version

# Core gems
gem 'rails', '~> 7.0'
gem 'pg', '~> 1.5'  # PostgreSQL
gem 'puma', '~> 6.0'  # Web server

# Development/Test only
group :development, :test do
  gem 'rspec-rails'
  gem 'factory_bot_rails'
  gem 'pry-byebug'
end

group :development do
  gem 'rubocop', require: false
  gem 'bullet'
end

group :test do
  gem 'capybara'
  gem 'selenium-webdriver'
end

# Production only
group :production do
  gem 'rack-timeout'
end
```

**Python comparison (requirements.txt):**
```
# requirements.txt
Django==4.2.0
psycopg2==2.9.6
gunicorn==20.1.0

# or pyproject.toml (Poetry)
[tool.poetry.dependencies]
python = "^3.11"
django = "^4.2"
```

### Version Constraints

```ruby
# Exact version
gem 'rails', '7.0.4'

# Pessimistic operator (~>)
gem 'rails', '~> 7.0'     # >= 7.0.0, < 8.0.0
gem 'rails', '~> 7.0.4'   # >= 7.0.4, < 7.1.0

# Greater than
gem 'rails', '>= 7.0'

# Range
gem 'rails', '>= 7.0', '< 8.0'
```

**Python comparison:**
```
Django>=4.2,<5.0
Django~=4.2.0  # Compatible release
```

### Basic Commands

```bash
# Install all gems
bundle install

# Update all gems
bundle update

# Update specific gem
bundle update rails

# Show outdated gems
bundle outdated

# Check for vulnerabilities
bundle audit

# Execute command with bundled gems
bundle exec rspec

# Create new Gemfile
bundle init
```

**Python comparison:**
```bash
pip install -r requirements.txt
pip list --outdated
pip-audit  # Security check
```

### Gemfile.lock

After `bundle install`, Bundler creates `Gemfile.lock`:

```ruby
# Gemfile.lock
GEM
  remote: https://rubygems.org/
  specs:
    rails (7.0.4)
      actioncable (= 7.0.4)
      actionmailbox (= 7.0.4)
      # ... exact versions
```

**Always commit Gemfile.lock!** It ensures deterministic builds.

**Python comparison:** `requirements.lock` or `poetry.lock`

### Why bundle exec?

```bash
# WITHOUT bundle exec - uses system gem
rspec

# WITH bundle exec - uses gem from Gemfile
bundle exec rspec
```

Alternative: Use `binstubs`:
```bash
bundle binstubs rspec-core
bin/rspec  # Uses bundled version
```

## 2. Pry: Powerful Alternative to IRB

Pry is a runtime developer console and REPL with syntax highlighting, debugging capabilities, and introspection tools.

### Installation

```ruby
# Gemfile
group :development, :test do
  gem 'pry'
  gem 'pry-byebug'  # Adds debugging commands
end
```

**Python comparison:**
```bash
pip install ipython ipdb
```

### Basic Usage

```ruby
# Drop into Pry console anywhere in code
require 'pry'

def complex_method
  x = 10
  y = 20
  binding.pry  # Execution stops here!
  x + y
end

complex_method
```

When execution hits `binding.pry`, you get an interactive console:

```ruby
From: app/models/user.rb @ line 15:

    13: def complex_method
    14:   x = 10
 => 15:   binding.pry
    16:   x + y
    17: end

[1] pry(main)> x
=> 10
[2] pry(main)> y
=> 20
[3] pry(main)> x + y
=> 30
```

**Python comparison:**
```python
import ipdb

def complex_method():
    x = 10
    y = 20
    ipdb.set_trace()  # Breakpoint
    return x + y
```

### Pry Commands

```ruby
# Navigation
ls              # List available methods and variables
cd User         # Change context to User class
cd ..           # Go back

# Source code
show-source User#initialize
show-doc Array#each

# History
hist            # Show command history
hist --grep def # Search history

# Shell
.ls             # Run shell command
.pwd

# Exit
exit            # Exit Pry
!!!             # Exit immediately (bang-bang-bang)
```

### Debugging with pry-byebug

```ruby
require 'pry-byebug'

def calculate_total(items)
  total = 0
  
  items.each do |item|
    binding.pry  # Breakpoint
    total += item.price
  end
  
  total
end
```

Debugging commands:
```ruby
step      # Step into method
next      # Next line
continue  # Continue execution
finish    # Finish current frame
break     # Set breakpoint
```

**Python comparison (ipdb):**
```python
s  # step
n  # next
c  # continue
l  # list
```

### Advanced Pry Features

```ruby
# Edit code directly
edit User  # Opens User class in $EDITOR

# Show method source
$ User.first.name
=> "Alice"

$ show-source User#name
def name
  "#{first_name} #{last_name}"
end

# Introspection
ls -m User              # Methods only
ls -i User              # Instance variables
whereami                # Show context
wtf?                    # Show last exception

# State manipulation
play -l 10              # Replay last 10 commands
reload!                 # Reload code (in Rails console)
```

### Pry as Rails Console

```bash
# Add to Gemfile
gem 'pry-rails'

# Now `rails console` uses Pry instead of IRB
rails console

# Interactive database queries
User.first
User.where(active: true).count
```

**Python comparison:**
```bash
# Django shell with IPython
python manage.py shell
# Or
python manage.py shell_plus  # django-extensions
```

## 3. Sidekiq: Background Job Processing

Sidekiq processes background jobs using Redis, making your app faster and more responsive.

### Installation

```ruby
# Gemfile
gem 'sidekiq'
gem 'redis'
```

```bash
bundle install

# Install Redis
# Mac: brew install redis
# Ubuntu: sudo apt-get install redis-server
```

**Python comparison:**
```bash
pip install celery redis
```

### Creating Workers

```ruby
# app/workers/send_email_worker.rb
class SendEmailWorker
  include Sidekiq::Worker
  
  sidekiq_options queue: :mailers, retry: 5

  def perform(user_id, email_type)
    user = User.find(user_id)
    
    case email_type
    when 'welcome'
      UserMailer.welcome(user).deliver_now
    when 'reminder'
      UserMailer.reminder(user).deliver_now
    end
  end
end

# Usage
SendEmailWorker.perform_async(user.id, 'welcome')
```

**Python comparison (Celery):**
```python
from celery import shared_task

@shared_task
def send_email(user_id, email_type):
    user = User.objects.get(id=user_id)
    if email_type == 'welcome':
        send_welcome_email(user)
```

### Worker Options

```ruby
class ImportWorker
  include Sidekiq::Worker
  
  sidekiq_options queue: :critical,
                  retry: 10,
                  backtrace: true,
                  dead: false

  def perform(file_path)
    # Long-running import
  end
end
```

Options:
- `queue`: Which queue to use
- `retry`: Number of retries on failure
- `backtrace`: Include full backtrace on error
- `dead`: Send to dead queue if all retries fail

### Scheduling Jobs

```ruby
# Immediate (async)
MyWorker.perform_async(args)

# Delayed (in X seconds)
MyWorker.perform_in(5.minutes, args)
MyWorker.perform_in(1.hour, args)

# At specific time
MyWorker.perform_at(2.hours.from_now, args)

# Bulk enqueue
Sidekiq::Client.push_bulk(
  'class' => MyWorker,
  'args' => [[1], [2], [3]]  # Enqueue 3 jobs
)
```

**Python comparison:**
```python
# Celery
send_email.delay(user_id)  # Async
send_email.apply_async(args=[user_id], countdown=300)  # Delayed
```

### Running Sidekiq

```bash
# Start Sidekiq
bundle exec sidekiq

# Specific queue
bundle exec sidekiq -q critical,5 -q default,3 -q low,1

# Configuration file
bundle exec sidekiq -C config/sidekiq.yml
```

Config file:
```yaml
# config/sidekiq.yml
:concurrency: 5
:queues:
  - [critical, 5]
  - [default, 3]
  - [low, 1]
```

### Web Dashboard

```ruby
# config/routes.rb
require 'sidekiq/web'

Rails.application.routes.draw do
  mount Sidekiq::Web => '/sidekiq'
end
```

Access at `http://localhost:3000/sidekiq`

### Best Practices

```ruby
# GOOD - Pass IDs, not objects
SendEmailWorker.perform_async(user.id)

# BAD - Don't serialize objects
SendEmailWorker.perform_async(user)  # Will fail!

# GOOD - Small, focused workers
class ProcessPaymentWorker
  def perform(order_id)
    ProcessPayment.call(order_id)
  end
end

# GOOD - Idempotent workers (safe to retry)
def perform(user_id)
  user = User.find(user_id)
  user.update(processed: true) unless user.processed?
end
```

**Python comparison:** Same principles apply to Celery!

## 4. Bullet: N+1 Query Detector

Bullet monitors your app for N+1 queries and suggests eager loading.

### Installation

```ruby
# Gemfile
group :development do
  gem 'bullet'
end
```

```ruby
# config/environments/development.rb
Rails.application.configure do
  config.after_initialize do
    Bullet.enable = true
    Bullet.alert = true
    Bullet.bullet_logger = true
    Bullet.console = true
    Bullet.rails_logger = true
    Bullet.add_footer = true  # Shows alert in browser
  end
end
```

**Python comparison:**
```bash
pip install django-silk  # Django
pip install nplusone     # Flask/SQLAlchemy
```

### What Bullet Detects

#### N+1 Query Problem

```ruby
# BAD - N+1 queries
users = User.all
users.each do |user|
  puts user.posts.count  # Separate query for each user!
end
# Generates: 1 query for users + N queries for posts

# Bullet alerts:
# user: app/controllers/users_controller.rb:10
# USE eager loading detected
#   User => [:posts]
#   Add to query: .includes(:posts)
```

**Python (Django) comparison:**
```python
# Bad - N+1
users = User.objects.all()
for user in users:
    print(user.posts.count())  # N+1!

# Good
users = User.objects.prefetch_related('posts')
```

#### Solution: Eager Loading

```ruby
# GOOD - Single query with JOIN
users = User.includes(:posts).all
users.each do |user|
  puts user.posts.count  # No extra queries!
end
# Generates: 1 query with JOIN
```

### Bullet Notifications

Bullet can notify via:
- Browser alert
- Console output
- Rails logger
- Slack/Email (with custom config)
- Exception (fail tests)

For tests:
```ruby
# spec/spec_helper.rb
RSpec.configure do |config|
  config.before(:each) do
    Bullet.start_request
  end

  config.after(:each) do
    Bullet.perform_out_of_channel_notifications if Bullet.notification?
    Bullet.end_request
  end
end

# Fail on N+1 in tests
Bullet.raise = true
```

### Common Bullet Warnings

```ruby
# Unused eager loading
users = User.includes(:posts).all
users.each { |u| puts u.name }  # Never use posts!
# Bullet: Remove .includes(:posts)

# Counter cache
posts = Post.includes(:comments).all
posts.each { |p| puts p.comments.count }
# Bullet: Use counter_cache instead

# Deep associations
users = User.includes(:posts).all
users.each do |user|
  user.posts.each do |post|
    puts post.comments.count  # N+1 on comments!
  end
end
# Need: User.includes(posts: :comments)
```

## Combining These Tools

### Gemfile for Professional Project

```ruby
source 'https://rubygems.org'

gem 'rails', '~> 7.0'
gem 'pg'
gem 'puma'
gem 'sidekiq'
gem 'redis'

group :development, :test do
  gem 'pry-byebug'
  gem 'rspec-rails'
  gem 'factory_bot_rails'
end

group :development do
  gem 'bullet'
  gem 'rubocop', require: false
  gem 'rubocop-rails', require: false
  gem 'rubocop-rspec', require: false
end

group :test do
  gem 'capybara'
  gem 'shoulda-matchers'
end
```

### Workflow

```bash
# 1. Install dependencies
bundle install

# 2. Debug with Pry
binding.pry in code
bundle exec rspec

# 3. Run background jobs
bundle exec sidekiq

# 4. Check for N+1 queries (Bullet watches automatically in dev)

# 5. Lint code
bundle exec rubocop
```

## Exercises

1. **Gemfile Setup**: Create a complete Gemfile for a Rails project with appropriate groups and version constraints.

2. **Pry Debugging**: Add `binding.pry` to a complex method and practice using step, next, and continue.

3. **Sidekiq Worker**: Create a worker that:
   - Processes uploaded CSV files
   - Sends completion email
   - Has retry logic

4. **N+1 Detective**: Find and fix N+1 queries in a sample app using Bullet.

5. **Compare to Python**: Set up equivalent tools in a Python project (pip, ipdb, Celery, django-silk) and compare workflows.

## Summary

These four tools are essential for professional Ruby development. Bundler manages dependencies reliably, Pry provides powerful debugging, Sidekiq handles background processing, and Bullet prevents performance issues. Master them all!

**Key Takeaways:**
- **Bundler**: Lock dependencies, use `bundle exec`
- **Pry**: Interactive debugging, better than IRB
- **Sidekiq**: Fast background jobs with Redis
- **Bullet**: Detect N+1 queries automatically

**Next Tutorial:** Enumerable Mastery and Ruby-specific Algorithms - learn to write idiomatic, performant Ruby code.
