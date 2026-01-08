# Tutorial 1: Testing with RSpec - The Ruby Heartbeat

## Overview

Ruby culture is deeply rooted in Test-Driven Development (TDD). In the Ruby community, you aren't considered "done" with a feature until it has a passing test suite. RSpec is the industry standard testing framework that uses a Domain Specific Language (DSL) to describe behavior in a readable, expressive way.

## Python Comparison

**Python's pytest vs Ruby's RSpec:**
- **Python (pytest)**: Uses plain functions with assert statements
  ```python
  def test_user_name():
      user = User("Alice")
      assert user.name == "Alice"
  ```
- **Ruby (RSpec)**: Uses a behavior-driven DSL with expect syntax
  ```ruby
  describe User do
    it "has a name" do
      user = User.new("Alice")
      expect(user.name).to eq("Alice")
    end
  end
  ```

The RSpec DSL reads more like natural language, making tests self-documenting. While Python emphasizes simplicity, Ruby emphasizes expressiveness.

## Core Concepts

### 1. Installation

Add RSpec to your Gemfile:
```ruby
# Gemfile
group :development, :test do
  gem 'rspec'
end
```

Install and initialize:
```bash
bundle install
rspec --init
```

This creates:
- `.rspec` - Configuration file
- `spec/spec_helper.rb` - Test setup and configuration

**Python equivalent:** `pip install pytest` and optionally create `pytest.ini`

### 2. Basic Structure

RSpec organizes tests using `describe` and `context` blocks:

```ruby
# spec/calculator_spec.rb
require 'spec_helper'
require_relative '../lib/calculator'

describe Calculator do
  describe '#add' do
    context 'with positive numbers' do
      it 'returns the sum' do
        calculator = Calculator.new
        result = calculator.add(2, 3)
        expect(result).to eq(5)
      end
    end

    context 'with negative numbers' do
      it 'handles negative values correctly' do
        calculator = Calculator.new
        result = calculator.add(-2, -3)
        expect(result).to eq(-5)
      end
    end
  end
end
```

**Python comparison:**
```python
# test_calculator.py
class TestCalculator:
    def test_add_positive_numbers(self):
        calc = Calculator()
        assert calc.add(2, 3) == 5
    
    def test_add_negative_numbers(self):
        calc = Calculator()
        assert calc.add(-2, -3) == -5
```

Ruby's nested blocks provide better organization for complex test suites.

### 3. RSpec Expectations

RSpec uses a rich expectation syntax:

```ruby
# Equality
expect(actual).to eq(expected)           # ==
expect(actual).to be(expected)           # equal? (same object)
expect(actual).not_to eq(expected)

# Comparison
expect(actual).to be > 3
expect(actual).to be_between(1, 10).inclusive

# Type checking
expect(actual).to be_a(String)
expect(actual).to be_an_instance_of(User)

# Truthiness
expect(actual).to be_truthy
expect(actual).to be_falsey
expect(actual).to be_nil

# Collections
expect(array).to include(item)
expect(hash).to have_key(:name)
expect(collection).to be_empty
expect(array).to match_array([1, 2, 3])  # Order independent

# Regex
expect(string).to match(/pattern/)

# Exceptions
expect { risky_method }.to raise_error(ArgumentError)
expect { risky_method }.to raise_error(ArgumentError, "invalid input")
```

**Python comparison:**
```python
# pytest uses simple assertions
assert actual == expected
assert actual > 3
assert isinstance(actual, str)
assert actual is None
assert item in array
assert 'name' in dictionary

# For exceptions
with pytest.raises(ValueError):
    risky_function()
```

RSpec's matchers are more expressive and provide better error messages.

### 4. Setup and Teardown (Hooks)

RSpec provides several hooks for test setup:

```ruby
describe User do
  before(:each) do
    # Runs before each test
    @user = User.new("Alice")
  end

  after(:each) do
    # Runs after each test (cleanup)
    @user = nil
  end

  before(:all) do
    # Runs once before all tests in this describe block
    @database = Database.connect
  end

  after(:all) do
    # Runs once after all tests
    @database.disconnect
  end

  it "has a name" do
    expect(@user.name).to eq("Alice")
  end
end
```

**Python comparison:**
```python
class TestUser:
    def setup_method(self):
        """Runs before each test"""
        self.user = User("Alice")
    
    def teardown_method(self):
        """Runs after each test"""
        self.user = None
    
    @classmethod
    def setup_class(cls):
        """Runs once before all tests"""
        cls.database = Database.connect()
    
    @classmethod
    def teardown_class(cls):
        """Runs once after all tests"""
        cls.database.disconnect()
```

### 5. let and subject

RSpec provides `let` for lazy-loaded test data (memoization):

```ruby
describe User do
  let(:user) { User.new("Alice", 30) }
  let(:admin) { User.new("Bob", 40, role: :admin) }

  it "has a name" do
    expect(user.name).to eq("Alice")
  end

  it "has an age" do
    expect(user.age).to eq(30)
  end
end
```

`let` is lazy - it only creates the object when first accessed, and then memoizes it for the duration of the test.

Use `let!` for eager evaluation:
```ruby
let!(:user) { User.create(name: "Alice") }  # Created immediately
```

`subject` defines the main object under test:
```ruby
describe User do
  subject { User.new("Alice") }

  it { is_expected.to be_valid }
  it { is_expected.not_to be_admin }
end
```

**Python comparison:**
```python
# pytest fixtures
@pytest.fixture
def user():
    return User("Alice", 30)

@pytest.fixture
def admin():
    return User("Bob", 40, role="admin")

def test_has_name(user):
    assert user.name == "Alice"
```

Both provide similar functionality, but RSpec's `let` syntax is more concise.

### 6. Shared Examples

DRY up tests with shared examples:

```ruby
shared_examples 'a timestamped model' do
  it 'has created_at timestamp' do
    expect(subject.created_at).to be_a(Time)
  end

  it 'has updated_at timestamp' do
    expect(subject.updated_at).to be_a(Time)
  end
end

describe User do
  subject { User.create(name: "Alice") }
  it_behaves_like 'a timestamped model'
end

describe Post do
  subject { Post.create(title: "Hello") }
  it_behaves_like 'a timestamped model'
end
```

**Python comparison:**
```python
# pytest doesn't have built-in shared examples
# You'd typically use inheritance or parametrize
def timestamp_tests(model):
    assert isinstance(model.created_at, datetime)
    assert isinstance(model.updated_at, datetime)
```

## Test-Driven Development Workflow

The TDD cycle in Ruby (Red-Green-Refactor):

1. **Red**: Write a failing test
```ruby
describe Calculator do
  it 'multiplies two numbers' do
    calc = Calculator.new
    expect(calc.multiply(2, 3)).to eq(6)
  end
end
```

2. **Green**: Write minimal code to make it pass
```ruby
class Calculator
  def multiply(a, b)
    a * b
  end
end
```

3. **Refactor**: Improve the code while keeping tests green

This is identical to Python's TDD workflow, but Ruby culture enforces it more strictly.

## Running Tests

```bash
# Run all tests
rspec

# Run specific file
rspec spec/user_spec.rb

# Run specific test by line number
rspec spec/user_spec.rb:23

# Run tests matching a pattern
rspec --pattern "spec/**/*_spec.rb"

# Run with documentation format
rspec --format documentation

# Run failed tests only
rspec --only-failures
```

**Python comparison:**
```bash
# pytest
pytest                          # All tests
pytest test_user.py            # Specific file
pytest -k "test_name"          # Pattern matching
pytest -v                      # Verbose
pytest --lf                    # Last failed
```

## Best Practices

1. **One assertion per test**: Each `it` block should test one thing
2. **Descriptive test names**: Use strings that describe behavior
3. **Arrange-Act-Assert**: Structure tests clearly
4. **Avoid logic in tests**: Tests should be simple and obvious
5. **Use let for setup**: Lazy-load test data
6. **Test behavior, not implementation**: Focus on outcomes, not internals

## Common Patterns

### Testing instance methods
```ruby
describe User do
  let(:user) { User.new("Alice") }

  describe '#full_name' do
    it 'combines first and last name' do
      user.last_name = "Smith"
      expect(user.full_name).to eq("Alice Smith")
    end
  end
end
```

### Testing class methods
```ruby
describe User do
  describe '.find_by_email' do
    it 'returns the user with matching email' do
      user = User.create(email: "alice@example.com")
      found = User.find_by_email("alice@example.com")
      expect(found).to eq(user)
    end
  end
end
```

### Testing private methods (generally discouraged)
```ruby
describe User do
  it 'normalizes email addresses' do
    user = User.new(email: "ALICE@EXAMPLE.COM")
    # Test through public interface
    expect(user.email).to eq("alice@example.com")
  end
end
```

## Exercises

1. Create a `String` class extension that adds a `palindrome?` method. Write RSpec tests first using TDD.

2. Create a `BankAccount` class with deposit, withdraw, and balance methods. Write comprehensive RSpec tests covering:
   - Happy paths
   - Edge cases (zero amounts, negative amounts)
   - Overdraft scenarios

3. Refactor one of your Python test suites to RSpec. Note the differences in:
   - Test organization (describe/context blocks)
   - Assertion syntax (expect vs assert)
   - Setup/teardown (before/after vs fixtures)

## Summary

RSpec is the heartbeat of Ruby development. Its expressive DSL makes tests readable and maintainable. While Python's pytest emphasizes simplicity with plain assertions, RSpec emphasizes clarity through natural language. The Ruby community's commitment to TDD means mastering RSpec is essential for professional Ruby development.

**Key Takeaways:**
- RSpec uses `describe`/`context`/`it` for test organization
- `expect().to` syntax for expressive assertions
- `let` for lazy-loaded test data
- Hooks (`before`/`after`) for setup and teardown
- TDD is not optional in Ruby culture

**Next Tutorial:** Testing with Minitest - exploring Ruby's built-in testing framework as a lighter alternative to RSpec.
