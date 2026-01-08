# Tutorial 2: Testing with Minitest - Ruby's Built-in Testing Framework

## Overview

While RSpec is the industry standard, Minitest is Ruby's built-in testing framework. It's faster, uses plain Ruby syntax instead of a DSL, and comes with Ruby's standard library. Many developers prefer Minitest for its simplicity and performance, especially for smaller projects or when DSL syntax feels like overkill.

## Python Comparison

**Minitest is very similar to Python's unittest:**

**Python (unittest):**
```python
import unittest

class TestCalculator(unittest.TestCase):
    def setUp(self):
        self.calc = Calculator()
    
    def test_add(self):
        self.assertEqual(self.calc.add(2, 3), 5)
    
    def test_subtract(self):
        self.assertEqual(self.calc.subtract(5, 3), 2)
```

**Ruby (Minitest):**
```ruby
require 'minitest/autorun'

class TestCalculator < Minitest::Test
  def setup
    @calc = Calculator.new
  end

  def test_add
    assert_equal 5, @calc.add(2, 3)
  end

  def test_subtract
    assert_equal 2, @calc.subtract(5, 3)
  end
end
```

The similarity is striking! Both use class-based tests, setup/teardown methods, and assertion methods. If you're comfortable with Python's unittest, Minitest will feel very familiar.

## Installation and Setup

Minitest comes with Ruby (no installation needed!), but you can add it to your Gemfile for version control:

```ruby
# Gemfile
group :development, :test do
  gem 'minitest'
end
```

Create a test file:
```bash
mkdir test
touch test/test_helper.rb
```

```ruby
# test/test_helper.rb
require 'minitest/autorun'
require 'minitest/pride'  # Colorful output (optional but fun!)

# Load your application code
$LOAD_PATH.unshift File.expand_path('../lib', __dir__)
```

**Python comparison:** Similar to creating a `tests/` directory with `__init__.py`

## Core Testing Styles

Minitest supports two styles: **Unit style** (traditional) and **Spec style** (RSpec-like).

### Unit Style (Traditional)

```ruby
# test/user_test.rb
require 'test_helper'
require 'user'

class UserTest < Minitest::Test
  def setup
    @user = User.new("Alice", 30)
  end

  def teardown
    @user = nil
  end

  def test_has_name
    assert_equal "Alice", @user.name
  end

  def test_has_age
    assert_equal 30, @user.age
  end

  def test_is_adult
    assert @user.adult?
  end

  def test_rejects_invalid_age
    assert_raises(ArgumentError) do
      User.new("Bob", -5)
    end
  end
end
```

### Spec Style (DSL)

Minitest also supports an RSpec-like DSL:

```ruby
# test/user_spec.rb
require 'test_helper'
require 'minitest/spec'

describe User do
  before do
    @user = User.new("Alice", 30)
  end

  it "has a name" do
    expect(@user.name).must_equal "Alice"
  end

  it "has an age" do
    expect(@user.age).must_equal 30
  end

  it "is an adult" do
    expect(@user.adult?).must_equal true
  end
end
```

**Python comparison:** unittest doesn't have a spec-style variant. pytest provides similar DSL-free testing but with plain functions, not classes.

## Assertions Reference

Minitest provides a comprehensive set of assertions:

### Basic Assertions

```ruby
# Equality
assert_equal expected, actual
refute_equal expected, actual

# Identity (same object)
assert_same expected, actual
refute_same expected, actual

# Nil
assert_nil actual
refute_nil actual

# Boolean
assert actual           # Truthy
refute actual           # Falsy

# Inclusion
assert_includes collection, item
refute_includes collection, item

# Instance type
assert_instance_of Class, object
refute_instance_of Class, object

# Kind of (inheritance aware)
assert_kind_of Class, object
refute_kind_of Class, object

# Pattern matching
assert_match /pattern/, string
refute_match /pattern/, string

# Empty
assert_empty collection
refute_empty collection

# Exceptions
assert_raises(ExceptionClass) { risky_code }
assert_raises(ExceptionClass, "message") { risky_code }

# Silent (no output)
assert_silent { code_that_shouldnt_print }
assert_output("expected output") { puts "expected output" }
```

**Python unittest comparison:**
```python
self.assertEqual(expected, actual)
self.assertNotEqual(expected, actual)
self.assertIs(expected, actual)
self.assertIsNone(actual)
self.assertTrue(actual)
self.assertIn(item, collection)
self.assertIsInstance(object, Class)
self.assertRegex(string, pattern)
self.assertRaises(Exception)
```

Very similar! The main difference is syntax (method style vs assertion functions).

## Spec-style Expectations

When using Minitest's spec style:

```ruby
describe User do
  let(:user) { User.new("Alice") }

  it "validates presence" do
    expect(user.name).must_equal "Alice"
    expect(user.name).wont_be_nil
    expect(user).must_be_kind_of User
    expect(user.errors).must_be_empty
  end
end
```

Spec-style expectations mirror assertions:
- `must_equal` → `assert_equal`
- `wont_equal` → `refute_equal`
- `must_be_nil` → `assert_nil`
- `must_include` → `assert_includes`

## Setup and Teardown

```ruby
class UserTest < Minitest::Test
  def setup
    # Runs before each test
    @user = User.new("Alice")
    @db = Database.connect
  end

  def teardown
    # Runs after each test
    @db.disconnect
  end

  def test_something
    # Use @user and @db here
  end
end
```

For setup/teardown that runs once for all tests:

```ruby
class UserTest < Minitest::Test
  def self.setup_class
    @@db = Database.connect
  end

  def self.teardown_class
    @@db.disconnect
  end
end
```

**Python comparison:**
```python
class TestUser(unittest.TestCase):
    def setUp(self):
        self.user = User("Alice")
    
    def tearDown(self):
        self.user = None
    
    @classmethod
    def setUpClass(cls):
        cls.db = Database.connect()
    
    @classmethod
    def tearDownClass(cls):
        cls.db.disconnect()
```

Nearly identical!

## Running Tests

```bash
# Run all tests
ruby test/user_test.rb

# Or use rake
rake test

# Run specific test method
ruby test/user_test.rb --name test_has_name

# Run tests matching pattern
ruby test/user_test.rb --name /adult/

# Verbose output
ruby test/user_test.rb --verbose

# Run all tests in directory
ruby -Ilib:test test/**/*_test.rb
```

**Python comparison:**
```bash
python -m unittest test_user.py
python -m unittest test_user.TestUser.test_has_name
python -m unittest discover
```

## Minitest vs RSpec: When to Use Each

### Use Minitest when:
- ✅ You prefer plain Ruby over DSL
- ✅ You want faster test execution
- ✅ You're building a gem/library (no dependencies)
- ✅ Your team values simplicity
- ✅ You're coming from Python's unittest background

### Use RSpec when:
- ✅ You want expressive, readable test descriptions
- ✅ Your team prefers behavior-driven development
- ✅ You need advanced features (shared examples, complex matchers)
- ✅ You're working on a large Rails application
- ✅ The job market in your area expects RSpec

## Advanced Minitest Features

### Parallel Test Execution

```ruby
class UserTest < Minitest::Test
  parallelize_me!  # Run tests in parallel

  def test_something
    # Tests will run in separate threads
  end
end
```

**Python comparison:** pytest-xdist provides similar functionality with `-n` flag.

### Custom Assertions

Create your own assertions:

```ruby
module CustomAssertions
  def assert_valid(object)
    assert object.valid?, "Expected #{object.inspect} to be valid"
  end
end

class UserTest < Minitest::Test
  include CustomAssertions

  def test_user_validity
    user = User.new("Alice")
    assert_valid user
  end
end
```

### Benchmarking

Minitest includes benchmarking capabilities:

```ruby
require 'minitest/benchmark'

class TestFibonacci < Minitest::Benchmark
  def bench_linear_fibonacci
    assert_performance_linear 0.99 do |n|
      fibonacci(n)
    end
  end

  def bench_exponential_fibonacci
    assert_performance_exponential 0.99 do |n|
      fibonacci_slow(n)
    end
  end
end
```

**Python comparison:** Use `pytest-benchmark` or `timeit` module.

### Mock and Stub

Minitest includes simple mocking:

```ruby
require 'minitest/mock'

def test_with_mock
  mock = Minitest::Mock.new
  mock.expect :call, "mocked result", ["arg1"]
  
  result = mock.call("arg1")
  assert_equal "mocked result", result
  mock.verify  # Ensures expectations were met
end

def test_with_stub
  user = User.new("Alice")
  user.stub :admin?, true do
    assert user.admin?
  end
  # After block, original method restored
end
```

**Python comparison:**
```python
from unittest.mock import Mock, patch

mock = Mock()
mock.return_value = "mocked result"

with patch.object(user, 'is_admin', return_value=True):
    assert user.is_admin()
```

## Best Practices

1. **Name tests clearly**: Use `test_` prefix and descriptive names
   ```ruby
   def test_user_cannot_withdraw_more_than_balance
   ```

2. **One assertion concept per test**: Test one behavior per method
   
3. **Use setup wisely**: Don't make tests dependent on complex setup
   
4. **Test public interfaces**: Avoid testing private methods directly

5. **Keep tests fast**: Use in-memory databases, avoid network calls

6. **Use meaningful assertion messages**:
   ```ruby
   assert user.valid?, "User should be valid with all required fields: #{user.errors.full_messages}"
   ```

## Common Patterns

### Testing Exceptions with Messages

```ruby
def test_invalid_age_raises_error
  error = assert_raises(ArgumentError) do
    User.new("Bob", -5)
  end
  assert_match /must be positive/, error.message
end
```

### Testing Output

```ruby
def test_greeting_output
  assert_output("Hello, Alice!\n") do
    greet("Alice")
  end
end
```

### Testing File Operations

```ruby
def test_saves_to_file
  file = Tempfile.new('test')
  user = User.new("Alice")
  user.save_to_file(file.path)
  
  content = File.read(file.path)
  assert_includes content, "Alice"
ensure
  file.close
  file.unlink
end
```

## Minitest Reporters

Enhance output with minitest-reporters:

```ruby
# Gemfile
gem 'minitest-reporters'

# test/test_helper.rb
require 'minitest/reporters'
Minitest::Reporters.use! [
  Minitest::Reporters::SpecReporter.new,  # RSpec-like output
  Minitest::Reporters::HtmlReporter.new   # HTML report
]
```

## Performance Comparison

```ruby
# Benchmark: 10,000 tests
# Minitest: ~15 seconds
# RSpec:    ~45 seconds
```

Minitest is typically 2-3x faster than RSpec due to:
- Less DSL overhead
- Simpler matcher system
- Less metaprogramming

## Exercises

1. **Convert RSpec to Minitest**: Take the BankAccount tests from Tutorial 1 and rewrite them in Minitest unit style.

2. **Custom Assertion**: Create an `assert_json_valid` assertion that checks if a string is valid JSON.

3. **Mock External API**: Write a test using Minitest::Mock to test a service that calls an external API without actually making the network call.

4. **Benchmark Comparison**: Create two implementations of a sorting algorithm and use Minitest::Benchmark to compare their performance.

## Summary

Minitest is Ruby's answer to Python's unittest - a simple, fast, no-frills testing framework. While RSpec provides more expressive syntax, Minitest offers:
- **Zero dependencies** (built into Ruby)
- **Faster execution** (2-3x faster than RSpec)
- **Familiar syntax** (especially for Python developers)
- **Less magic** (plain Ruby, no DSL to learn)

For Python developers transitioning to Ruby, Minitest provides a comfortable stepping stone with familiar concepts and patterns.

**Key Takeaways:**
- Minitest is built into Ruby (no installation required)
- Supports both unit style and spec style
- Very similar to Python's unittest
- Faster than RSpec, simpler syntax
- Great for gems, libraries, and simpler projects

**Next Tutorial:** Test Data with FactoryBot - learn to generate dynamic test data instead of using static fixtures.
