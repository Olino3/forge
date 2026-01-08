# Tutorial 5: Code Quality with RuboCop - Automated Linting and Formatting

## Overview

Ruby is a flexible language, which means it's easy to write "messy" code. RuboCop is the most important tool for maintaining code quality in Ruby projects. It's a linter and formatter that automatically checks your code against the Ruby Style Guide and can even auto-correct common mistakes. Think of it as your automated code reviewer that enforces consistency across your team.

## Python Comparison

**Python's flake8/pylint vs Ruby's RuboCop:**

**Python (flake8):**
```python
# .flake8
[flake8]
max-line-length = 88
ignore = E203, W503

# Run
$ flake8 myfile.py
myfile.py:10:1: E302 expected 2 blank lines, found 1
myfile.py:15:80: E501 line too long (85 > 79 characters)
```

**Ruby (RuboCop):**
```ruby
# .rubocop.yml
Layout/LineLength:
  Max: 120

# Run
$ rubocop myfile.rb
Inspecting 1 file
C

Offenses:

myfile.rb:10:1: C: Layout/EmptyLines: Extra blank line detected.
myfile.rb:15:80: C: Layout/LineLength: Line is too long. [125/120]

1 file inspected, 2 offenses detected, 2 offenses auto-correctable
```

Key difference: **RuboCop can auto-fix most issues!** Python's Black provides auto-formatting, but RuboCop combines linting AND formatting in one tool.

## Installation

```ruby
# Gemfile
group :development, :test do
  gem 'rubocop', require: false
  gem 'rubocop-performance', require: false  # Performance cops
  gem 'rubocop-rails', require: false        # Rails-specific cops
  gem 'rubocop-rspec', require: false        # RSpec-specific cops
end
```

```bash
bundle install

# Generate default config
rubocop --init
```

This creates `.rubocop.yml` in your project root.

**Python comparison:**
```bash
pip install flake8 black isort
```

RuboCop is all-in-one; Python needs multiple tools.

## Basic Usage

```bash
# Check all Ruby files
rubocop

# Check specific files
rubocop app/models/user.rb spec/

# Auto-correct safe violations
rubocop -a

# Auto-correct ALL violations (including unsafe)
rubocop -A

# Show only offenses from specific cop
rubocop --only Style/StringLiterals

# Disable specific cop
rubocop --except Style/Documentation

# Generate TODO file for existing offenses
rubocop --auto-gen-config
```

**Python comparison:**
```bash
flake8 myfile.py
black myfile.py  # Auto-format
isort myfile.py  # Sort imports
```

## Configuration

### .rubocop.yml Structure

```yaml
# .rubocop.yml
require:
  - rubocop-performance
  - rubocop-rails
  - rubocop-rspec

AllCops:
  TargetRubyVersion: 3.2
  NewCops: enable
  Exclude:
    - 'db/schema.rb'
    - 'db/migrate/*.rb'
    - 'vendor/**/*'
    - 'node_modules/**/*'
    - 'bin/*'

# Configure specific cops
Layout/LineLength:
  Max: 120
  Exclude:
    - 'config/**/*'

Style/Documentation:
  Enabled: false  # Don't require class documentation

Style/FrozenStringLiteralComment:
  Enabled: false  # Don't require frozen_string_literal comment

Metrics/BlockLength:
  Exclude:
    - 'spec/**/*'  # Allow long blocks in tests
    - 'config/routes.rb'

Metrics/MethodLength:
  Max: 15
  Exclude:
    - 'db/migrate/*.rb'

# Use single quotes by default
Style/StringLiterals:
  EnforcedStyle: single_quotes
```

**Python comparison:**
```ini
# setup.cfg
[flake8]
max-line-length = 88
exclude = .git,__pycache__,migrations
ignore = E203,W503

# pyproject.toml
[tool.black]
line-length = 88
exclude = '''
/(
    \.git
  | migrations
)/
'''
```

## Common Cops and What They Check

### Layout Cops (Formatting)

```ruby
# Layout/EmptyLines
# BAD
class User

  def initialize

  end
end

# GOOD
class User
  def initialize
  end
end

# Layout/SpaceAroundOperators
# BAD
x=1+2
result = 5*3

# GOOD
x = 1 + 2
result = 5 * 3

# Layout/IndentationWidth
# BAD
class User
    def name  # 4 spaces
      "Alice"
    end
end

# GOOD (2 spaces)
class User
  def name
    "Alice"
  end
end

# Layout/TrailingWhitespace
# BAD
def greet  # Trailing spaces here    
  "Hello"
end

# GOOD
def greet
  "Hello"
end
```

### Style Cops (Code Style)

```ruby
# Style/StringLiterals
# Single quotes preferred (unless interpolation needed)
# BAD
name = "Alice"

# GOOD
name = 'Alice'
message = "Hello, #{name}"  # OK - needs interpolation

# Style/SymbolArray / Style/WordArray
# BAD
colors = ["red", "blue", "green"]
statuses = [:pending, :approved, :rejected]

# GOOD
colors = %w[red blue green]
statuses = %i[pending approved rejected]

# Style/HashSyntax
# BAD (old syntax)
user = { :name => "Alice", :age => 30 }

# GOOD (new syntax)
user = { name: "Alice", age: 30 }

# Style/IfUnlessModifier
# BAD
if user.admin?
  grant_access
end

# GOOD (for simple conditions)
grant_access if user.admin?

# Style/GuardClause
# BAD
def process(user)
  if user.present?
    if user.active?
      send_email(user)
    end
  end
end

# GOOD
def process(user)
  return unless user.present?
  return unless user.active?
  
  send_email(user)
end
```

**Python comparison:**
```python
# Python (Black enforces formatting)
# Double quotes standard
name = "Alice"

# List literals (no special syntax)
colors = ["red", "blue", "green"]

# Dict syntax
user = {"name": "Alice", "age": 30}

# Guard clauses less common in Python
def process(user):
    if not user:
        return
    if not user.active:
        return
    send_email(user)
```

### Lint Cops (Bug Detection)

```ruby
# Lint/UnusedBlockArgument
# BAD
users.each do |user|
  puts "Processing..."  # 'user' not used
end

# GOOD
users.each do |_user|  # Prefix with underscore
  puts "Processing..."
end

# Or
users.each do
  puts "Processing..."  # No argument
end

# Lint/DuplicateMethods
# BAD
class User
  def name
    "Alice"
  end

  def name  # Duplicate!
    "Bob"
  end
end

# Lint/ShadowingOuterLocalVariable
# BAD
user = "Alice"
users.each do |user|  # Shadows outer 'user'
  puts user
end

# GOOD
user = "Alice"
users.each do |u|
  puts u
end

# Lint/UnreachableCode
# BAD
def greet
  return "Hello"
  puts "This never executes"  # Unreachable
end

# Lint/UselessAssignment
# BAD
def calculate
  result = 5 + 3  # Never used
  42
end

# GOOD
def calculate
  result = 5 + 3
  result * 2
end
```

**Python comparison:**
```python
# pylint detects similar issues
# W0612: Unused variable
# W0621: Redefining from outer scope
# W0101: Unreachable code
```

### Metrics Cops (Complexity)

```ruby
# Metrics/MethodLength
# Warns if methods are too long (default: 10 lines)

# Metrics/CyclomaticComplexity
# Warns if too many conditional branches

# Metrics/AbcSize
# Measures assignment, branches, conditions

# Metrics/ClassLength
# Warns if classes are too long

# Metrics/BlockNesting
# Warns about deeply nested blocks
# BAD
if condition1
  if condition2
    if condition3
      if condition4  # Too deep!
        do_something
      end
    end
  end
end
```

### Naming Cops

```ruby
# Naming/MethodName
# BAD
def GetUser
  # ...
end

# GOOD
def get_user
  # ...
end

# Naming/VariableName
# BAD
UserName = "Alice"  # Constants should be SCREAMING_SNAKE_CASE
firstName = "Alice"  # Use snake_case

# GOOD
USER_NAME = "Alice"
first_name = "Alice"

# Naming/PredicateName
# BAD
def is_admin?
  role == :admin
end

# GOOD
def admin?
  role == :admin
end
```

**Python comparison:**
```python
# PEP 8 naming conventions
# Functions: lowercase_with_underscores
# Constants: UPPERCASE_WITH_UNDERSCORES
# Classes: CapitalizedWords

# Python predicates often use 'is_' prefix
def is_admin(user):
    return user.role == "admin"
```

## Auto-Correction

RuboCop can fix most style violations automatically:

```bash
# Safe auto-corrections only
rubocop -a

# All auto-corrections (including potentially unsafe ones)
rubocop -A
```

Example of what gets auto-corrected:

```ruby
# Before
def greet(name)
  message = "Hello, "+name
  if message.length>20
    puts message
  end
end

# After: rubocop -a
def greet(name)
  message = "Hello, " + name
  puts message if message.length > 20
end
```

**Python comparison:**
```bash
black myfile.py  # Auto-formats entire file
autopep8 --in-place myfile.py  # Fix PEP 8 violations
```

## Disabling Cops

### Inline Disabling

```ruby
# Disable for one line
user = User.find(params[:id]) # rubocop:disable Rails/DynamicFindBy

# Disable for block
# rubocop:disable Metrics/MethodLength
def complex_method
  # ... many lines ...
end
# rubocop:enable Metrics/MethodLength

# Disable multiple cops
# rubocop:disable Metrics/AbcSize, Metrics/MethodLength
def another_complex_method
  # ...
end
# rubocop:enable Metrics/AbcSize, Metrics/MethodLength
```

**Python comparison:**
```python
# noqa: disable specific error
x = some_long_line_that_goes_over_limit  # noqa: E501

# flake8: noqa - disable all checks for line
complicated_line()  # flake8: noqa
```

### File-Level Disabling

```ruby
# At top of file
# rubocop:disable Style/Documentation
class MyClass
  # ...
end
# rubocop:enable Style/Documentation
```

### Config-Level Disabling

```yaml
# .rubocop.yml
Style/Documentation:
  Enabled: false

# Or exclude specific files
Metrics/BlockLength:
  Exclude:
    - 'spec/**/*'
```

## Gradual Adoption with TODO

For existing projects with many violations:

```bash
# Generate TODO file
rubocop --auto-gen-config
```

This creates `.rubocop_todo.yml`:
```yaml
# .rubocop_todo.yml
# This file was auto-generated

Style/StringLiterals:
  Exclude:
    - 'app/models/user.rb'
    - 'app/controllers/users_controller.rb'

Metrics/MethodLength:
  Max: 25  # Temporarily allow longer methods
```

Include in main config:
```yaml
# .rubocop.yml
inherit_from: .rubocop_todo.yml
```

Then gradually fix violations and remove from TODO.

**Python comparison:**
```bash
# Similar approach with flake8
flake8 . > violations.txt
# Then fix gradually
```

## CI/CD Integration

### GitHub Actions

```yaml
# .github/workflows/rubocop.yml
name: RuboCop

on: [push, pull_request]

jobs:
  rubocop:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: ruby/setup-ruby@v1
        with:
          ruby-version: 3.2
      - run: bundle install
      - run: bundle exec rubocop
```

### Fail on Violations

```bash
# Exit with error code if violations found
rubocop --fail-level warning

# Or in Rake task
task :rubocop do
  require 'rubocop/rake_task'
  RuboCop::RakeTask.new(:rubocop) do |task|
    task.fail_on_error = true
  end
end
```

**Python comparison:**
```yaml
# GitHub Actions for flake8
- run: pip install flake8
- run: flake8 . --exit-zero  # Don't fail
# or
- run: flake8 .  # Fail on violations
```

## Pre-commit Hooks

Automatically run RuboCop before commits:

```bash
# Install overcommit gem
gem install overcommit

# In project
overcommit --install

# .overcommit.yml
PreCommit:
  RuboCop:
    enabled: true
    command: ['bundle', 'exec', 'rubocop']
    on_warn: fail
```

**Python comparison:**
```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.1.0
    hooks:
      - id: black
  - repo: https://github.com/pycqa/flake8
    rev: 6.0.0
    hooks:
      - id: flake8
```

## Editor Integration

### VS Code

Install "Ruby" extension, then:
```json
// settings.json
{
  "ruby.lint": {
    "rubocop": {
      "enabled": true,
      "auto": true
    }
  },
  "ruby.format": "rubocop"
}
```

### RubyMine

RuboCop is built-in:
- Settings → Editor → Inspections → Ruby → Gems and gems → RuboCop
- Enable "RuboCop inspection"

### Vim

```vim
" .vimrc
Plug 'ngmy/vim-rubocop'

" Auto-run on save
let g:vimrubocop_keymap = 0
nmap <Leader>r :RuboCop<CR>
```

## Performance Tips

```bash
# Use cache for faster runs
rubocop --cache true

# Parallel execution
rubocop --parallel

# Check only changed files (with git)
git diff --name-only master | grep '\.rb$' | xargs rubocop

# Format for machine parsing
rubocop --format json > rubocop-results.json
```

## Best Practices

1. **Enable NewCops**: Stay current with new checks
   ```yaml
   AllCops:
     NewCops: enable
   ```

2. **Team Configuration**: Commit `.rubocop.yml` to repo
   
3. **Gradual Adoption**: Use `--auto-gen-config` for legacy projects

4. **Auto-correct Regularly**: Run `rubocop -a` frequently

5. **Don't Disable Without Reason**: Document why cops are disabled
   ```yaml
   Style/Documentation:
     Enabled: false  # Team decision: docs in README
   ```

6. **Review Auto-corrections**: Always review what `-A` changes

## Custom Cops

Create project-specific rules:

```ruby
# lib/custom_cops/no_binding_pry.rb
module CustomCops
  class NoBindingPry < RuboCop::Cop::Base
    MSG = 'Remove `binding.pry` before committing'

    def on_send(node)
      return unless node.method_name == :pry
      return unless node.receiver&.const_name == :binding

      add_offense(node)
    end
  end
end
```

## Exercises

1. **Configure RuboCop**: Set up `.rubocop.yml` for a new project with:
   - Line length: 120
   - String literals: single quotes
   - Exclude: db/schema.rb, vendor/

2. **Fix Violations**: Take a messy Ruby file and:
   - Run `rubocop`
   - Auto-fix with `rubocop -a`
   - Manually fix remaining issues
   - Document any disabled cops

3. **CI Integration**: Add RuboCop to GitHub Actions, make it fail on violations

4. **Compare with Python**: Run both RuboCop on a Ruby file and flake8 on equivalent Python code. Compare:
   - Number of violations detected
   - Types of issues found
   - Auto-correction capabilities

## Summary

RuboCop is essential for professional Ruby development. It enforces consistent style, catches common bugs, and can auto-fix most issues. The combination of linting and formatting in one tool makes it more powerful than Python's split approach (flake8 + black + isort).

**Key Takeaways:**
- RuboCop = linter + formatter in one tool
- Auto-correction with `-a` (safe) and `-A` (all)
- Highly configurable via `.rubocop.yml`
- Many plugins: rubocop-rails, rubocop-rspec, rubocop-performance
- Gradual adoption via `--auto-gen-config`
- Essential for team consistency

**Next Tutorial:** StandardRB and Style Guides - exploring the "no-config" alternative to RuboCop and understanding the Ruby Style Guide.
