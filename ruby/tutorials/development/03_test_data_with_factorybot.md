# Tutorial 3: Test Data with FactoryBot - Dynamic Test Fixtures

## Overview

Hard-coded test data (fixtures) becomes a maintenance nightmare as applications grow. FactoryBot (formerly FactoryGirl) is the Ruby standard for generating dynamic test data. It allows you to define blueprints for your models and create test objects with sensible defaults, overriding only what's relevant for each test.

## Python Comparison

**Python's factory_boy vs Ruby's FactoryBot:**

Both libraries share the same philosophy and even similar APIs (FactoryBot inspired factory_boy!).

**Python (factory_boy):**
```python
import factory

class UserFactory(factory.Factory):
    class Meta:
        model = User
    
    name = "Alice"
    email = factory.Sequence(lambda n: f"user{n}@example.com")
    age = 30
    created_at = factory.LazyFunction(datetime.now)

# Usage
user = UserFactory.create()
admin = UserFactory.create(role="admin")
```

**Ruby (FactoryBot):**
```ruby
FactoryBot.define do
  factory :user do
    name { "Alice" }
    sequence(:email) { |n| "user#{n}@example.com" }
    age { 30 }
    created_at { Time.now }
  end
end

# Usage
user = create(:user)
admin = create(:user, role: :admin)
```

The concepts are nearly identical! If you know factory_boy, you already understand FactoryBot.

## Installation

```ruby
# Gemfile
group :development, :test do
  gem 'factory_bot'
  # Or for Rails:
  gem 'factory_bot_rails'
end
```

```bash
bundle install
```

Setup for RSpec:
```ruby
# spec/spec_helper.rb
require 'factory_bot'

RSpec.configure do |config|
  config.include FactoryBot::Syntax::Methods
end
```

Setup for Minitest:
```ruby
# test/test_helper.rb
require 'factory_bot'

class Minitest::Test
  include FactoryBot::Syntax::Methods
end
```

**Python comparison:**
```python
# conftest.py (pytest)
import factory_boy

# No special setup needed, just import and use
```

## Basic Factory Definitions

Create factories in `spec/factories/` (RSpec) or `test/factories/` (Minitest):

```ruby
# spec/factories/users.rb
FactoryBot.define do
  factory :user do
    name { "Alice Smith" }
    email { "alice@example.com" }
    age { 30 }
    active { true }
  end
end
```

### Why Use Blocks?

Notice the `{ }` blocks? This is crucial:

```ruby
# WRONG - Evaluated once at factory definition time
factory :user do
  created_at Time.now  # Same timestamp for all users!
end

# CORRECT - Evaluated each time factory is used
factory :user do
  created_at { Time.now }  # Different timestamp each time
end
```

**Python comparison:**
```python
# factory_boy uses lazy attributes similarly
created_at = factory.LazyFunction(datetime.now)
```

## Creating Test Objects

FactoryBot provides several creation strategies:

```ruby
# build: Creates object in memory (not saved to DB)
user = build(:user)
user.new_record?  # => true

# create: Creates and saves to database
user = create(:user)
user.persisted?  # => true

# build_stubbed: Creates fake object (faster, no DB)
user = build_stubbed(:user)
user.id  # => 1001 (fake ID)

# attributes_for: Returns hash of attributes
attrs = attributes_for(:user)
# => { name: "Alice Smith", email: "alice@example.com", ... }
```

**Python comparison:**
```python
user = UserFactory.build()        # Not saved
user = UserFactory.create()       # Saved to DB
attrs = UserFactory.build().__dict__  # Attributes
```

### When to Use Each Strategy

- **`build`**: Fast, use when you don't need database persistence
- **`create`**: When you need database features (queries, associations, validations)
- **`build_stubbed`**: Fastest, for pure unit tests
- **`attributes_for`**: For controller tests, form submissions

## Overriding Attributes

```ruby
# Use defaults
user = create(:user)
user.name  # => "Alice Smith"

# Override specific attributes
user = create(:user, name: "Bob Jones", age: 25)
user.name  # => "Bob Jones"
user.age   # => 25

# Build with overrides
user = build(:user, email: "custom@example.com")
```

**Python comparison:**
```python
user = UserFactory.create(name="Bob Jones", age=25)
```

Identical concept!

## Sequences - Unique Values

Sequences generate unique values to avoid uniqueness constraint violations:

```ruby
FactoryBot.define do
  factory :user do
    sequence(:email) { |n| "user#{n}@example.com" }
    sequence(:username) { |n| "user_#{n}" }
  end
end

# Usage
user1 = create(:user)  # email: user1@example.com
user2 = create(:user)  # email: user2@example.com
user3 = create(:user)  # email: user3@example.com
```

You can also use sequences with formatted strings:

```ruby
sequence(:email) { |n| "person_#{n}@example.com" }
sequence(:code, 1000) { |n| "CODE-#{n}" }  # Start at 1000
```

**Python comparison:**
```python
class UserFactory(factory.Factory):
    email = factory.Sequence(lambda n: f"user{n}@example.com")
    username = factory.Sequence(lambda n: f"user_{n}")
```

## Associations - Related Objects

FactoryBot handles associations elegantly:

```ruby
# Models
class User < ApplicationRecord
  has_many :posts
end

class Post < ApplicationRecord
  belongs_to :user
end

# Factories
FactoryBot.define do
  factory :user do
    name { "Alice" }
  end

  factory :post do
    title { "My Post" }
    content { "Post content" }
    user  # Automatically creates associated user
  end
end

# Usage
post = create(:post)
post.user.name  # => "Alice" (automatically created)

# Override association
user = create(:user, name: "Bob")
post = create(:post, user: user)
post.user.name  # => "Bob"
```

### Explicit Association Naming

```ruby
factory :post do
  title { "My Post" }
  association :author, factory: :user  # User factory, but called 'author'
end
```

**Python comparison:**
```python
class PostFactory(factory.Factory):
    class Meta:
        model = Post
    
    title = "My Post"
    user = factory.SubFactory(UserFactory)

# Or with different name
class PostFactory(factory.Factory):
    author = factory.SubFactory(UserFactory)
```

## Traits - Reusable Variations

Traits define preset variations of your factories:

```ruby
FactoryBot.define do
  factory :user do
    name { "Alice" }
    email { "alice@example.com" }
    role { :member }

    trait :admin do
      role { :admin }
    end

    trait :inactive do
      active { false }
    end

    trait :with_posts do
      after(:create) do |user|
        create_list(:post, 3, user: user)
      end
    end
  end
end

# Usage
admin = create(:user, :admin)
inactive_admin = create(:user, :admin, :inactive)
user_with_posts = create(:user, :with_posts)
```

Traits are composable - you can use multiple traits together!

**Python comparison:**
```python
class UserFactory(factory.Factory):
    class Meta:
        model = User
    
    name = "Alice"
    role = "member"
    
    class Params:
        admin = factory.Trait(
            role="admin"
        )
        inactive = factory.Trait(
            active=False
        )

# Usage
admin = UserFactory(admin=True)
```

## Factory Inheritance

Create specialized factories through inheritance:

```ruby
FactoryBot.define do
  factory :user do
    name { "User" }
    role { :member }
  end

  factory :admin, parent: :user do
    role { :admin }
  end

  factory :moderator, parent: :user do
    role { :moderator }
    verified { true }
  end
end

# Usage
user = create(:user)       # role: :member
admin = create(:admin)     # role: :admin
mod = create(:moderator)   # role: :moderator, verified: true
```

**Python comparison:**
```python
class UserFactory(factory.Factory):
    class Meta:
        model = User
    role = "member"

class AdminFactory(UserFactory):
    role = "admin"
```

## Callbacks - Hooks for Complex Setup

FactoryBot provides callbacks for advanced scenarios:

```ruby
FactoryBot.define do
  factory :user do
    name { "Alice" }

    # Runs after building (before saving)
    after(:build) do |user|
      user.generate_api_token
    end

    # Runs after creating (after saving)
    after(:create) do |user|
      create(:profile, user: user)
    end

    # Runs before stubbing
    before(:stub) do |user|
      user.id = 1001
    end
  end
end
```

Available callbacks:
- `before(:build)`
- `after(:build)`
- `before(:create)`
- `after(:create)`
- `before(:stub)`
- `after(:stub)`

**Python comparison:**
```python
class UserFactory(factory.Factory):
    @factory.post_generation
    def setup_profile(obj, create, extracted, **kwargs):
        if create:
            ProfileFactory.create(user=obj)
```

## Creating Multiple Objects

```ruby
# Create 5 users
users = create_list(:user, 5)
users.count  # => 5

# Build 3 posts
posts = build_list(:post, 3)

# With overrides
admins = create_list(:user, 3, role: :admin)

# With traits
users_with_posts = create_list(:user, 2, :with_posts)
```

**Python comparison:**
```python
users = UserFactory.create_batch(5)
```

## Transient Attributes

Transient attributes are helper values not assigned to the model:

```ruby
FactoryBot.define do
  factory :user do
    transient do
      posts_count { 3 }
    end

    name { "Alice" }

    after(:create) do |user, evaluator|
      create_list(:post, evaluator.posts_count, user: user)
    end
  end
end

# Usage
user = create(:user, posts_count: 5)
user.posts.count  # => 5
```

**Python comparison:**
```python
class UserFactory(factory.Factory):
    class Params:
        posts_count = 3
    
    @factory.post_generation
    def create_posts(obj, create, extracted, **kwargs):
        if create:
            PostFactory.create_batch(obj.posts_count, user=obj)
```

## Dynamic Attributes with Faker

Combine with Faker gem for realistic test data:

```ruby
# Gemfile
gem 'faker'

# Factory
FactoryBot.define do
  factory :user do
    name { Faker::Name.name }
    email { Faker::Internet.email }
    phone { Faker::PhoneNumber.phone_number }
    bio { Faker::Lorem.paragraph }
  end
end

# Each user gets unique, realistic data
user1 = create(:user)  # name: "John Smith", email: "john.smith@example.org"
user2 = create(:user)  # name: "Jane Doe", email: "jane.doe@example.net"
```

**Python comparison:**
```python
from faker import Faker
fake = Faker()

class UserFactory(factory.Factory):
    name = factory.LazyFunction(fake.name)
    email = factory.LazyFunction(fake.email)
```

## Best Practices

### 1. Keep Factories Simple
```ruby
# GOOD - Minimal, valid object
factory :user do
  name { "Alice" }
  email { "alice@example.com" }
end

# BAD - Too much setup
factory :user do
  name { "Alice" }
  posts { create_list(:post, 10) }  # Slow!
  followers { create_list(:user, 20) }  # Even slower!
end
```

Use traits for complex scenarios, keep base factory minimal.

### 2. One Factory Per Model

```ruby
# GOOD
factory :user do
  # base user
end

factory :admin, parent: :user do
  role { :admin }
end

# BAD - Separate factory for what should be a trait
factory :user do
end

factory :user_admin do
  role { :admin }
end
```

### 3. Use `build` Over `create` When Possible

```ruby
# GOOD - Faster, no DB hit
describe User do
  it "validates name presence" do
    user = build(:user, name: nil)
    expect(user).not_to be_valid
  end
end

# SLOWER - Unnecessary DB access
describe User do
  it "validates name presence" do
    user = create(:user, name: nil)  # Will fail before save anyway
  end
end
```

### 4. Avoid Callbacks in Factories

```ruby
# AVOID - Hidden complexity
factory :user do
  after(:create) do |user|
    create(:profile, user: user)
    create_list(:post, 5, user: user)
    EmailService.send_welcome(user)
  end
end

# BETTER - Explicit trait
factory :user do
  trait :with_complete_setup do
    after(:create) do |user|
      create(:profile, user: user)
    end
  end
end
```

## Testing with FactoryBot

### RSpec Example

```ruby
describe User do
  describe '#full_name' do
    it 'combines first and last name' do
      user = build(:user, first_name: "Alice", last_name: "Smith")
      expect(user.full_name).to eq("Alice Smith")
    end
  end

  describe '.admins' do
    it 'returns only admin users' do
      create_list(:user, 3)
      create_list(:user, 2, :admin)
      
      expect(User.admins.count).to eq(2)
    end
  end
end
```

### Minitest Example

```ruby
class UserTest < Minitest::Test
  def test_full_name
    user = build(:user, first_name: "Alice", last_name: "Smith")
    assert_equal "Alice Smith", user.full_name
  end

  def test_admins_scope
    create_list(:user, 3)
    create_list(:user, 2, :admin)
    
    assert_equal 2, User.admins.count
  end
end
```

## Debugging Factories

```ruby
# See what attributes will be used
puts attributes_for(:user)
# => {:name=>"Alice", :email=>"alice@example.com", ...}

# Check if factory is valid
FactoryBot.build(:user).valid?

# Lint all factories (finds invalid factories)
FactoryBot.lint

# Lint specific traits
FactoryBot.lint traits: true
```

## Exercises

1. **Create User Factory**: Build a comprehensive User factory with:
   - Sequences for email and username
   - Traits for :admin, :inactive, :with_profile
   - Use Faker for realistic names and bios

2. **Association Practice**: Create factories for a blog system:
   - User (author)
   - Post (belongs_to :user)
   - Comment (belongs_to :post, belongs_to :user)
   - Tag (has_and_belongs_to_many :posts)

3. **Convert Fixtures**: Take existing Rails fixtures and convert them to FactoryBot factories.

4. **Performance Test**: Compare test suite speed using:
   - Hard-coded fixtures
   - FactoryBot with `create`
   - FactoryBot with `build`
   - FactoryBot with `build_stubbed`

## Summary

FactoryBot eliminates the pain of test data management. By defining blueprints with sensible defaults, you can create test objects with minimal code while keeping tests flexible and maintainable.

**Python developers:** If you've used factory_boy, FactoryBot will feel immediately familiar. The philosophy and API are nearly identical.

**Key Takeaways:**
- Define factories with sensible defaults
- Use sequences for unique values
- Leverage traits for variations
- Prefer `build` over `create` for speed
- Use associations for related objects
- Keep factories simple, use traits for complexity

**Next Tutorial:** Integration Testing with Capybara - learn to test web applications by simulating real user interactions in a browser.
