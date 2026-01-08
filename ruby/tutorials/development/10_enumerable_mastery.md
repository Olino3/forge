# Tutorial 10: Enumerable Mastery and Ruby-Specific Algorithms

## Overview

Professional Rubyists rarely use `for` loops. Ruby's Enumerable module provides powerful, expressive methods that make code more readable and functional. This tutorial covers mastery of `#map`, `#reduce`, `#select`, `#reject`, and more, plus Ruby-specific algorithm patterns.

## Python Comparison

Ruby's Enumerable is similar to Python's list comprehensions and functional tools, but more integrated:

**Python:**
```python
# List comprehension
numbers = [1, 2, 3, 4, 5]
doubled = [x * 2 for x in numbers]
evens = [x for x in numbers if x % 2 == 0]

# Functional tools
from functools import reduce
total = reduce(lambda acc, x: acc + x, numbers)

# Generator expressions
squares = (x**2 for x in numbers)
```

**Ruby:**
```ruby
# Enumerable methods
numbers = [1, 2, 3, 4, 5]
doubled = numbers.map { |x| x * 2 }
evens = numbers.select { |x| x.even? }

# Reduce
total = numbers.reduce(0) { |acc, x| acc + x }
# Or even simpler:
total = numbers.sum

# Lazy evaluation (like generators)
squares = numbers.lazy.map { |x| x**2 }
```

Ruby's Enumerable is more consistent and readable!

## Core Enumerable Methods

### #each - Basic Iteration

```ruby
# Don't return anything, just iterate
[1, 2, 3].each do |num|
  puts num
end

# One-liner
[1, 2, 3].each { |num| puts num }
```

**Python comparison:**
```python
for num in [1, 2, 3]:
    print(num)
```

**When to use:** Side effects only (printing, writing to database), not transforming data.

### #map - Transform Each Element

```ruby
# Transform array
numbers = [1, 2, 3, 4, 5]
doubled = numbers.map { |n| n * 2 }
# => [2, 4, 6, 8, 10]

# With methods
names = ['alice', 'bob', 'charlie']
uppercased = names.map(&:upcase)
# => ['ALICE', 'BOB', 'CHARLIE']

# Hash transformation
users = User.all.map { |u| { id: u.id, name: u.name } }

# Alias: collect (same as map)
numbers.collect { |n| n * 2 }
```

**Python comparison:**
```python
doubled = [n * 2 for n in numbers]
# Or
doubled = list(map(lambda n: n * 2, numbers))

uppercased = [name.upper() for name in names]
```

**When to use:** Transforming every element, building new arrays.

### #select - Filter Elements (Keep Truthy)

```ruby
# Keep elements matching condition
numbers = [1, 2, 3, 4, 5, 6]
evens = numbers.select { |n| n.even? }
# => [2, 4, 6]

# With complex conditions
users = User.all.select { |u| u.active? && u.admin? }

# On hashes
hash = { a: 1, b: 2, c: 3 }
small = hash.select { |k, v| v < 3 }
# => { a: 1, b: 2 }

# Alias: find_all
numbers.find_all { |n| n.even? }
```

**Python comparison:**
```python
evens = [n for n in numbers if n % 2 == 0]
# Or
evens = list(filter(lambda n: n % 2 == 0, numbers))

users = [u for u in User.all() if u.active and u.is_admin]
```

**When to use:** Filtering, finding elements matching criteria.

### #reject - Filter Elements (Remove Truthy)

```ruby
# Remove elements matching condition
numbers = [1, 2, 3, 4, 5, 6]
odds = numbers.reject { |n| n.even? }
# => [1, 3, 5]

# Opposite of select
evens = numbers.reject { |n| n.odd? }
# => [2, 4, 6]

# Reject nil values
[1, nil, 2, nil, 3].reject(&:nil?)
# => [1, 2, 3]
# Or use compact:
[1, nil, 2, nil, 3].compact
# => [1, 2, 3]
```

**Python comparison:**
```python
odds = [n for n in numbers if not n % 2 == 0]

# Remove None
numbers = [1, None, 2, None, 3]
filtered = [n for n in numbers if n is not None]
```

**When to use:** Removing unwanted elements.

### #reduce - Accumulate Values

```ruby
# Sum
numbers = [1, 2, 3, 4, 5]
sum = numbers.reduce(0) { |acc, n| acc + n }
# => 15

# With symbol
sum = numbers.reduce(:+)
# => 15

# Even simpler for common operations
sum = numbers.sum
product = numbers.reduce(:*)

# Building hash
items = ['apple', 'banana', 'apple', 'cherry', 'banana']
counts = items.reduce(Hash.new(0)) do |hash, item|
  hash[item] += 1
  hash
end
# => {"apple"=>2, "banana"=>2, "cherry"=>1}

# Alias: inject
numbers.inject(0, :+)
```

**Python comparison:**
```python
from functools import reduce

sum = reduce(lambda acc, n: acc + n, numbers, 0)

# Or built-in
sum = sum(numbers)
product = reduce(lambda acc, n: acc * n, numbers, 1)
```

**When to use:** Aggregating, building complex data structures.

### #find - Get First Match

```ruby
# Find first matching element
numbers = [1, 2, 3, 4, 5]
first_even = numbers.find { |n| n.even? }
# => 2

# Returns nil if not found
first_large = numbers.find { |n| n > 10 }
# => nil

# With ActiveRecord
user = User.find { |u| u.email == 'alice@example.com' }

# Alias: detect
numbers.detect { |n| n.even? }
```

**Python comparison:**
```python
first_even = next((n for n in numbers if n % 2 == 0), None)

# Or
for n in numbers:
    if n % 2 == 0:
        first_even = n
        break
```

**When to use:** Finding first occurrence.

### #any? and #all? - Boolean Checks

```ruby
# Check if any element matches
numbers = [1, 2, 3, 4, 5]
has_even = numbers.any? { |n| n.even? }
# => true

# Check if all elements match
all_positive = numbers.all? { |n| n > 0 }
# => true

all_even = numbers.all?(&:even?)
# => false

# Without block (checks for truthy values)
[1, 2, nil].any?  # => true
[nil, false].any?  # => false
[1, 2, 3].all?    # => true
[1, nil, 3].all?  # => false
```

**Python comparison:**
```python
has_even = any(n % 2 == 0 for n in numbers)
all_positive = all(n > 0 for n in numbers)
```

**When to use:** Validation, boolean checks.

### #group_by - Partition by Criteria

```ruby
# Group by property
numbers = [1, 2, 3, 4, 5, 6]
by_parity = numbers.group_by { |n| n.even? ? 'even' : 'odd' }
# => {"odd"=>[1, 3, 5], "even"=>[2, 4, 6]}

# Group users by role
users = User.all.group_by(&:role)
# => {:admin=>[#<User id=1>, ...], :member=>[#<User id=2>, ...]}

# Group by date
orders = Order.all.group_by { |o| o.created_at.to_date }
```

**Python comparison:**
```python
from itertools import groupby

numbers = [1, 2, 3, 4, 5, 6]
by_parity = {}
for n in numbers:
    key = 'even' if n % 2 == 0 else 'odd'
    by_parity.setdefault(key, []).append(n)

# Or with groupby (requires sorting first)
```

**When to use:** Categorizing data, creating buckets.

### #partition - Split into Two Groups

```ruby
numbers = [1, 2, 3, 4, 5, 6]
evens, odds = numbers.partition(&:even?)
# evens => [2, 4, 6]
# odds  => [1, 3, 5]

# Active/inactive users
active, inactive = users.partition(&:active?)
```

**Python comparison:**
```python
evens = [n for n in numbers if n % 2 == 0]
odds = [n for n in numbers if n % 2 != 0]
```

**When to use:** Binary splits.

## Advanced Enumerable Patterns

### #each_with_index - Iteration with Index

```ruby
names = ['Alice', 'Bob', 'Charlie']
names.each_with_index do |name, index|
  puts "#{index + 1}. #{name}"
end
# 1. Alice
# 2. Bob
# 3. Charlie
```

**Python comparison:**
```python
for index, name in enumerate(names):
    print(f"{index + 1}. {name}")
```

### #each_with_object - Build Object While Iterating

```ruby
# Build hash
numbers = [1, 2, 3, 4, 5]
result = numbers.each_with_object({}) do |num, hash|
  hash[num] = num ** 2
end
# => {1=>1, 2=>4, 3=>9, 4=>16, 5=>25}

# Cleaner than reduce for building objects
# Compare to reduce version:
result = numbers.reduce({}) do |hash, num|
  hash[num] = num ** 2
  hash  # Must return hash!
end
```

**When to use:** Building hashes or arrays, clearer than reduce.

### #zip - Combine Arrays

```ruby
names = ['Alice', 'Bob', 'Charlie']
ages = [25, 30, 35]

pairs = names.zip(ages)
# => [["Alice", 25], ["Bob", 30], ["Charlie", 35]]

# Convert to hash
hash = names.zip(ages).to_h
# => {"Alice"=>25, "Bob"=>30, "Charlie"=>35}

# Multiple arrays
scores = [85, 90, 95]
combined = names.zip(ages, scores)
# => [["Alice", 25, 85], ["Bob", 30, 90], ["Charlie", 35, 95]]
```

**Python comparison:**
```python
pairs = list(zip(names, ages))
hash_map = dict(zip(names, ages))
```

### #flat_map - Map and Flatten

```ruby
# Map then flatten in one step
users = [
  { name: 'Alice', hobbies: ['reading', 'coding'] },
  { name: 'Bob', hobbies: ['gaming', 'music'] }
]

all_hobbies = users.flat_map { |u| u[:hobbies] }
# => ['reading', 'coding', 'gaming', 'music']

# vs map + flatten:
all_hobbies = users.map { |u| u[:hobbies] }.flatten
# Same result, but flat_map is more efficient
```

**Python comparison:**
```python
# List comprehension with nested loop
all_hobbies = [hobby for user in users for hobby in user['hobbies']]

# Or
from itertools import chain
all_hobbies = list(chain.from_iterable(u['hobbies'] for u in users))
```

### #take and #drop

```ruby
numbers = [1, 2, 3, 4, 5, 6]

numbers.take(3)
# => [1, 2, 3]

numbers.drop(3)
# => [4, 5, 6]

# With condition
numbers.take_while { |n| n < 4 }
# => [1, 2, 3]

numbers.drop_while { |n| n < 4 }
# => [4, 5, 6]
```

**Python comparison:**
```python
numbers[:3]  # take
numbers[3:]  # drop

from itertools import takewhile, dropwhile
list(takewhile(lambda n: n < 4, numbers))
```

## Lazy Evaluation (Ruby's Generators)

```ruby
# Process infinite sequences efficiently
(1..Float::INFINITY).lazy
  .select { |n| n.even? }
  .take(5)
  .force
# => [2, 4, 6, 8, 10]

# Without lazy, would never complete!

# File processing
File.foreach('huge_file.txt').lazy
  .select { |line| line.include?('ERROR') }
  .first(10)

# Chain operations efficiently
(1..1_000_000).lazy
  .map { |n| n * 2 }
  .select { |n| n > 100 }
  .first(10)
# Only processes enough to get 10 results
```

**Python comparison:**
```python
# Generator expressions
evens = (n for n in range(1, float('inf')) if n % 2 == 0)
first_five = list(islice(evens, 5))

# Or
from itertools import count, islice
evens = (n for n in count(1) if n % 2 == 0)
first_five = list(islice(evens, 5))
```

## Ruby-Specific Algorithm Patterns

### Memoization with ||=

```ruby
class Fibonacci
  def initialize
    @memo = {}
  end

  def calculate(n)
    @memo[n] ||= if n <= 1
      n
    else
      calculate(n - 1) + calculate(n - 2)
    end
  end
end

# Or instance variable memoization
class User
  def full_name
    @full_name ||= "#{first_name} #{last_name}"
  end

  def posts_count
    @posts_count ||= posts.count
  end
end
```

**Python comparison:**
```python
from functools import lru_cache

@lru_cache(maxsize=None)
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

# Or manual
class User:
    @property
    def full_name(self):
        if not hasattr(self, '_full_name'):
            self._full_name = f"{self.first_name} {self.last_name}"
        return self._full_name
```

### Safe Navigation (&.)

```ruby
# Safe navigation operator (Ruby 2.3+)
user&.profile&.avatar_url

# vs nil checking
user && user.profile && user.profile.avatar_url

# With try (Rails)
user.try(:profile).try(:avatar_url)
```

**Python comparison:**
```python
# Optional chaining (Python 3.10+ with walrus)
if (profile := user.profile) and (avatar := profile.avatar):
    url = avatar.url

# Or
url = getattr(getattr(user, 'profile', None), 'avatar_url', None)
```

### Hashes vs Arrays - Performance

```ruby
# Array - O(n) lookup
users = [user1, user2, user3]
users.find { |u| u.id == 123 }  # Linear search

# Hash - O(1) lookup
users_by_id = { 1 => user1, 2 => user2, 3 => user3 }
users_by_id[123]  # Constant time

# Index by for quick lookup
users = User.all
users_by_id = users.index_by(&:id)
users_by_id[123]  # Fast!
```

**Python comparison:**
```python
# List - O(n)
users = [user1, user2, user3]
next((u for u in users if u.id == 123), None)

# Dict - O(1)
users_by_id = {u.id: u for u in users}
users_by_id.get(123)
```

### Sorting

```ruby
# Simple sort
[3, 1, 4, 1, 5].sort
# => [1, 1, 3, 4, 5]

# Custom comparison
users.sort_by(&:created_at)
users.sort_by { |u| -u.age }  # Descending

# Multiple criteria
users.sort_by { |u| [u.role, u.name] }

# Reverse
users.sort_by(&:age).reverse

# Ruby's .sort uses Quicksort in MRI
```

**Python comparison:**
```python
sorted([3, 1, 4, 1, 5])

users.sort(key=lambda u: u.created_at)
users.sort(key=lambda u: -u.age)

# Multiple criteria
users.sort(key=lambda u: (u.role, u.name))
```

## Exercises

1. **Refactor Loops**: Take code with `for` loops and refactor using Enumerable methods.

2. **Data Transformation**: Given an array of users, create a hash mapping emails to user objects.

3. **Lazy Evaluation**: Process a large file using lazy enumeration to find first 100 matching lines.

4. **Memoization**: Implement a memoized factorial function using `||=`.

5. **Compare Performance**: Benchmark Array#find vs Hash lookup for 10,000 items.

## Summary

Mastering Enumerable is essential for writing idiomatic Ruby. Professional Rubyists chain methods fluently, avoid explicit loops, and use lazy evaluation for performance. These patterns make code more readable and maintainable.

**Key Takeaways:**
- Prefer Enumerable methods over `for` loops
- `map`, `select`, `reject`, `reduce` are your core tools
- Use `lazy` for infinite sequences or large datasets
- Memoize expensive calculations with `||=`
- Choose Hash over Array for O(1) lookups

**Next Tutorial:** SOLID Principles in Ruby - learn to write maintainable, flexible object-oriented code.
