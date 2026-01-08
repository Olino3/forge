# Tutorial 6: StandardRB and the Ruby Style Guide - Zero-Config Code Quality

## Overview

StandardRB is a "no-config" wrapper for RuboCop that enforces one single style, so teams don't waste time arguing over tabs vs. spaces, line length, or quote styles. It's inspired by JavaScript's StandardJS and embodies the philosophy: "Stop bikeshedding, start shipping."

## Python Comparison

**Python's Black vs Ruby's StandardRB:**

**Python (Black - "The Uncompromising Code Formatter"):**
```bash
pip install black
black myfile.py

# No configuration needed!
# Black makes all decisions for you
```

**Ruby (StandardRB):**
```bash
gem install standard
standardrb --fix

# Also no configuration needed!
# Standard makes all decisions for you
```

Both philosophies are identical: **opinionated, zero-config, auto-formatting**. If you like Black, you'll love StandardRB!

Key difference: Black ONLY formats. StandardRB formats AND lints (catches bugs).

## The Ruby Style Guide

Before diving into StandardRB, understand the community standard. The [Ruby Style Guide](https://rubystyle.guide/) is a community-driven document defining the "Ruby Way."

### Core Principles

#### 1. Two-Space Indentation

```ruby
# GOOD
class User
  def initialize(name)
    @name = name
  end
end

# BAD - 4 spaces
class User
    def initialize(name)
        @name = name
    end
end
```

**Python comparison:** Python uses 4 spaces (PEP 8). Ruby uses 2.

#### 2. Snake_case for Methods and Variables

```ruby
# GOOD
def calculate_total_price
  unit_price = 10
  total_items = 5
  unit_price * total_items
end

# BAD
def calculateTotalPrice  # camelCase
  unitPrice = 10
  TOTAL_ITEMS = 5
  unitPrice * TOTAL_ITEMS
end
```

**Python comparison:** Same! Python also uses snake_case for functions and variables.

#### 3. CamelCase for Classes

```ruby
# GOOD
class UserAccount
end

class HTTPClient
end

# BAD
class user_account  # snake_case
end

class Http_Client  # mixed
end
```

**Python comparison:** Same! Python uses PascalCase for classes.

#### 4. SCREAMING_SNAKE_CASE for Constants

```ruby
# GOOD
MAX_USERS = 100
API_ENDPOINT = 'https://api.example.com'
DEFAULT_TIMEOUT = 30

# BAD
maxUsers = 100
Api_Endpoint = 'https://api.example.com'
```

**Python comparison:** Same! Python uses UPPERCASE for constants.

#### 5. Use ? for Predicate Methods

```ruby
# GOOD
def admin?
  role == :admin
end

def empty?
  items.count.zero?
end

# BAD
def is_admin  # No '?'
  role == :admin
end

def check_empty  # Verbose
  items.count.zero?
end
```

**Python comparison:** Python typically uses `is_` prefix:
```python
def is_admin(user):
    return user.role == "admin"

def is_empty(collection):
    return len(collection) == 0
```

#### 6. Use ! for Dangerous Methods

Methods that modify the receiver or raise exceptions should end with `!`:

```ruby
# Modifying receiver
name.upcase!   # Modifies name in place
array.sort!    # Sorts array in place

# vs safe versions
name.upcase    # Returns new string
array.sort     # Returns new array

# Raising exceptions
user.save!     # Raises if validation fails
user.save      # Returns true/false
```

**Python comparison:** Python doesn't have this convention. List methods like `sort()` modify in place, `sorted()` returns new list, but no `!` marker.

#### 7. Single Quotes for Strings (Unless Interpolation Needed)

```ruby
# GOOD
name = 'Alice'
message = "Hello, #{name}!"  # Interpolation requires double quotes

# BAD
name = "Alice"  # Unnecessary double quotes
```

**Python comparison:** Python prefers double quotes (per Black), though both are valid.

#### 8. Use %w for Word Arrays

```ruby
# GOOD
fruits = %w[apple banana orange]
statuses = %i[pending approved rejected]

# BAD
fruits = ['apple', 'banana', 'orange']
statuses = [:pending, :approved, :rejected]
```

**Python comparison:** Python has no equivalent shorthand.

#### 9. Modern Hash Syntax

```ruby
# GOOD (Ruby 1.9+)
user = { name: 'Alice', age: 30 }

# BAD (old syntax, pre-1.9)
user = { :name => 'Alice', :age => 30 }
```

**Python comparison:** Python dicts use `{"name": "Alice"}`.

#### 10. Trailing Commas in Multi-line Collections

```ruby
# GOOD - Easier diffs
users = [
  'Alice',
  'Bob',
  'Charlie',  # Trailing comma
]

# OKAY but less preferred
users = [
  'Alice',
  'Bob',
  'Charlie'  # No trailing comma
]
```

**Python comparison:** Python also allows (and Black enforces) trailing commas.

## StandardRB: The Zero-Config Solution

### Installation

```ruby
# Gemfile
group :development, :test do
  gem 'standard'
end
```

```bash
bundle install

# Or globally
gem install standard
```

### Basic Usage

```bash
# Check files
standardrb

# Auto-fix
standardrb --fix

# Check specific files
standardrb app/models/user.rb

# Generate TODO for existing violations
standardrb --generate-todo
```

**Python comparison:**
```bash
black .
black --check .  # Check without fixing
```

### What StandardRB Enforces

StandardRB is RuboCop with a carefully chosen set of rules:

1. **2-space indentation**
2. **Single quotes** (unless interpolation)
3. **No trailing whitespace**
4. **120 character line length** (vs RuboCop default of 80)
5. **Modern hash syntax**
6. **%w for word arrays**
7. **Spaces around operators**
8. **Guard clauses** over nested conditions
9. **No semicolons** (except for multi-statement lines)
10. **Trailing commas** in multi-line literals

### Configuration (or Lack Thereof)

StandardRB's philosophy: **NO CONFIGURATION!**

```ruby
# .standard.yml - Only for ignoring files
ignore:
  - 'db/schema.rb'
  - 'vendor/**/*'
  - 'node_modules/**/*'
```

That's it! No style configuration allowed.

**Python comparison:**
```toml
# pyproject.toml for Black
[tool.black]
# Almost no config allowed!
# Just exclusions and line length
exclude = '''
/(
    \.git
  | vendor
)/
'''
```

## StandardRB vs RuboCop

### RuboCop Approach
```yaml
# .rubocop.yml - Endless configuration options!
Layout/LineLength:
  Max: 120

Style/StringLiterals:
  EnforcedStyle: single_quotes

Style/HashSyntax:
  EnforcedStyle: ruby19

# ... hundreds more possible options
```

### StandardRB Approach
```bash
# No config file needed!
standardrb --fix
```

### When to Use Each

**Use StandardRB when:**
- ✅ You want zero configuration
- ✅ You're starting a new project
- ✅ You want to stop style debates
- ✅ You value convention over customization
- ✅ You're a small team or solo developer

**Use RuboCop when:**
- ✅ You need custom rules
- ✅ Legacy codebase requires gradual adoption
- ✅ You have specific style requirements
- ✅ You need framework-specific cops (Rails, RSpec)
- ✅ You want fine-grained control

**Python comparison:** Similar to choosing Black (opinionated) vs autopep8 (configurable).

## Example Transformations

### Before Standard

```ruby
class User
    attr_accessor :name,:age

    def initialize(name,age)
      @name=name
      @age=age
    end

    def adult?()
      if @age >= 18
        return true
      else
        return false
      end
    end

    def display_info
      puts "Name: #{@name}, Age: #{@age}"
    end
end

user=User.new("Alice",30)
```

### After `standardrb --fix`

```ruby
class User
  attr_accessor :name, :age

  def initialize(name, age)
    @name = name
    @age = age
  end

  def adult?
    @age >= 18
  end

  def display_info
    puts "Name: #{@name}, Age: #{@age}"
  end
end

user = User.new('Alice', 30)
```

Changes made:
- ✅ Fixed indentation (2 spaces)
- ✅ Added space after commas
- ✅ Added spaces around `=`
- ✅ Removed redundant `return`
- ✅ Removed unnecessary `()` from method definition
- ✅ Simplified `if/else` to direct expression
- ✅ Changed double quotes to single quotes

## CI/CD Integration

### GitHub Actions

```yaml
# .github/workflows/standard.yml
name: StandardRB

on: [push, pull_request]

jobs:
  standard:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: ruby/setup-ruby@v1
        with:
          ruby-version: 3.2
          bundler-cache: true
      - run: bundle exec standardrb
```

**Python comparison:**
```yaml
# Black in GitHub Actions
- run: pip install black
- run: black --check .
```

### Rake Task

```ruby
# Rakefile
require 'standard/rake'

# Now you can run:
# rake standard          # Check
# rake standard:fix      # Auto-fix
```

## Editor Integration

### VS Code

```bash
# Install extension
code --install-extension testdouble.vscode-standard-ruby
```

```json
// settings.json
{
  "ruby.lint": {
    "standard": {
      "enabled": true
    }
  },
  "ruby.format": "standard",
  "[ruby]": {
    "editor.formatOnSave": true
  }
}
```

### RubyMine

Install "Standard Ruby" plugin from marketplace.

### Vim

```vim
" .vimrc
Plug 'testdouble/standard.vim'

" Format on save
autocmd bufwritepost *.rb silent !standardrb --fix %
```

## Gradual Adoption

For existing projects:

```bash
# Generate TODO file
standardrb --generate-todo

# Creates .standard_todo.yml with current violations
# Fix gradually and remove from todo
```

Example `.standard_todo.yml`:
```yaml
# This configuration was generated by `standard --generate-todo`

ignore:
  - 'app/models/user.rb':
    - Layout/LineLength
    - Style/StringLiterals
  - 'app/controllers/users_controller.rb':
    - Metrics/MethodLength
```

## Ignoring Code

```ruby
# Disable for one line
long_line = "some really long string that violates line length" # standard:disable Layout/LineLength

# Disable for block
# standard:disable all
def legacy_method
  # Old messy code
end
# standard:enable all
```

**Use sparingly!** The point of Standard is NOT to configure.

## StandardRB Rules Reference

StandardRB enables these RuboCop cops:

### Layout
- 2-space indentation
- Space after commas
- Space around operators
- No trailing whitespace
- 120 char line length
- Trailing commas in multi-line

### Style
- Single quotes (unless interpolation)
- Modern hash syntax (`:`)
- `%w` for word arrays
- `%i` for symbol arrays
- Guard clauses over nested ifs
- No redundant `return`
- Predicate methods end with `?`

### Lint
- No unused variables
- No shadowing variables
- No unreachable code
- No duplicate methods
- Proper rescue syntax

### Naming
- snake_case for methods/variables
- CamelCase for classes
- SCREAMING_SNAKE_CASE for constants

## Real-World Example

### Messy Code

```ruby
class OrderProcessor
  def process_order( order )
    if order.valid?
      if order.payment_received?
        if order.items.present?
          total = 0
          order.items.each do |item|
            total = total + item.price
          end
          order.update_attribute( :total, total )
          send_confirmation_email( order )
          return true
        else
          return false
        end
      else
        return false
      end
    else
      return false
    end
  end

  def send_confirmation_email( order )
    puts "Sending email to #{order.customer.email}"
  end
end
```

### After `standardrb --fix`

```ruby
class OrderProcessor
  def process_order(order)
    return false unless order.valid?
    return false unless order.payment_received?
    return false unless order.items.present?

    total = order.items.sum(&:price)
    order.update_attribute(:total, total)
    send_confirmation_email(order)
    true
  end

  def send_confirmation_email(order)
    puts "Sending email to #{order.customer.email}"
  end
end
```

Much cleaner!

## Best Practices

1. **Adopt from Day One**: Easier than retrofitting

2. **Run on Save**: Configure editor to format on save

3. **Pre-commit Hooks**: Prevent bad code from being committed
   ```bash
   # .git/hooks/pre-commit
   #!/bin/sh
   bundle exec standardrb
   ```

4. **CI Enforcement**: Fail builds on violations

5. **Team Buy-in**: Get everyone to agree on StandardRB upfront

6. **Don't Fight It**: If Standard says it's wrong, it's wrong. Accept it and move on.

## Alternatives to Standard

If you need configuration but want simplicity:

- **StandardRB**: Zero config
- **Relaxed.Ruby.Style**: More lenient than Standard
- **Custom RuboCop**: Full control

**Python comparison:**
- **Black**: Zero config (like Standard)
- **autopep8**: Configurable
- **YAPF**: Highly configurable

## Exercises

1. **Clean Up Messy Code**: Take a poorly formatted Ruby file and run `standardrb --fix`. Examine each change.

2. **Configure CI**: Add StandardRB to GitHub Actions for a project.

3. **Editor Setup**: Configure your editor to run StandardRB on save.

4. **Compare Approaches**: Take the same code and format with:
   - StandardRB
   - RuboCop (custom config)
   - No formatter
   
   Compare readability and consistency.

5. **Python Comparison**: Format a Python file with Black and a Ruby file with StandardRB. Note similarities in philosophy.

## Summary

StandardRB brings the "stop bikeshedding" philosophy of JavaScript's Standard and Python's Black to Ruby. It eliminates configuration, enforces consistency, and lets you focus on writing code instead of arguing about style.

**Key Takeaways:**
- StandardRB = Zero-config RuboCop
- Inspired by JavaScript's Standard and Python's Black
- Enforces Ruby Style Guide automatically
- No configuration allowed (by design)
- Perfect for new projects and small teams
- Use RuboCop for legacy code or custom needs

**Next Tutorial:** Service Objects Pattern - learn to organize complex business logic into dedicated, testable classes.
