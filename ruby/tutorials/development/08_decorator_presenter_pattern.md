# Tutorial 8: Decorator/Presenter Pattern - Keeping Logic Out of Views

## Overview

The Decorator (or Presenter) pattern wraps model objects to add view-specific logic without polluting the model. Instead of putting formatting, conditional display logic, or helper methods in models or views, you create a decorator that handles presentation concerns.

## Python Comparison

**Decorators are universal!** Both languages use them, though Python has more built-in decorator syntax:

**Python (with decorator library):**
```python
# presenters/user_presenter.py
class UserPresenter:
    def __init__(self, user):
        self.user = user
    
    def display_name(self):
        if self.user.is_admin:
            return f"👑 {self.user.name} (Admin)"
        return self.user.name
    
    def member_since(self):
        return self.user.created_at.strftime("%B %Y")
    
    def status_badge(self):
        return "🟢 Active" if self.user.active else "🔴 Inactive"

# Usage in template
user_presenter = UserPresenter(user)
print(user_presenter.display_name())
```

**Ruby (Draper gem):**
```ruby
# app/decorators/user_decorator.rb
class UserDecorator < Draper::Decorator
  delegate_all

  def display_name
    if object.admin?
      "👑 #{object.name} (Admin)"
    else
      object.name
    end
  end

  def member_since
    object.created_at.strftime("%B %Y")
  end

  def status_badge
    object.active? ? "🟢 Active" : "🔴 Inactive"
  end
end

# Usage in view
<%= user.decorate.display_name %>
```

Same concept! Keep presentation logic separate from business logic.

## The Problem: View Logic in Models or Templates

### Bad Approach #1: Logic in Models

```ruby
# BAD - Presentation logic in model
class User < ApplicationRecord
  def display_name
    admin? ? "#{name} (Admin)" : name
  end

  def formatted_phone
    phone.gsub(/(\d{3})(\d{3})(\d{4})/, '(\1) \2-\3')
  end

  def membership_badge_html
    if premium?
      '<span class="badge badge-gold">Premium</span>'
    else
      '<span class="badge badge-silver">Free</span>'
    end
  end
end
```

Problems:
- ❌ Model knows about HTML
- ❌ Can't reuse model outside web context (API, CLI)
- ❌ Violates Single Responsibility
- ❌ Hard to test view logic separately

### Bad Approach #2: Logic in Views

```erb
<!-- BAD - Complex logic in template -->
<h1>
  <%= if user.admin? %>
    👑 <%= user.name %> (Admin)
  <% else %>
    <%= user.name %>
  <% end %>
</h1>

<p>
  Member since: 
  <%= user.created_at.strftime("%B %Y") %>
</p>

<p>
  Status: 
  <%= if user.active? %>
    🟢 Active
  <% else %>
    🔴 Inactive
  <% end %>
</p>
```

Problems:
- ❌ Templates become unreadable
- ❌ Logic scattered across views
- ❌ Hard to test
- ❌ Duplicate code

**Python comparison:** Same issues exist in Django templates or Jinja2!

## Solution: Decorator Pattern

### Using Draper Gem (Recommended)

```ruby
# Gemfile
gem 'draper'

# Generate decorator
rails generate decorator User
```

```ruby
# app/decorators/user_decorator.rb
class UserDecorator < Draper::Decorator
  delegate_all  # Delegate undefined methods to model

  def display_name
    if object.admin?
      h.content_tag :span, "👑 #{object.name}", class: 'admin-badge'
    else
      object.name
    end
  end

  def member_since
    object.created_at.strftime("%B %Y")
  end

  def status_badge
    if object.active?
      h.content_tag :span, '🟢 Active', class: 'badge badge-success'
    else
      h.content_tag :span, '🔴 Inactive', class: 'badge badge-danger'
    end
  end

  def formatted_phone
    return 'No phone provided' if object.phone.blank?
    object.phone.gsub(/(\d{3})(\d{3})(\d{4})/, '(\1) \2-\3')
  end

  def avatar_url(size: 100)
    if object.avatar.attached?
      h.url_for(object.avatar.variant(resize: "#{size}x#{size}"))
    else
      "https://ui-avatars.com/api/?name=#{h.url_encode(object.name)}&size=#{size}"
    end
  end
end
```

**Key features:**
- `delegate_all`: Pass undefined methods to wrapped model
- `object`: Access the wrapped model
- `h`: Access view helpers (content_tag, link_to, etc.)

### Using in Controllers

```ruby
class UsersController < ApplicationController
  def show
    @user = User.find(params[:id]).decorate
  end

  def index
    @users = User.all.decorate  # Decorates collection
  end
end
```

### Using in Views

```erb
<!-- app/views/users/show.html.erb -->
<h1><%= @user.display_name %></h1>
<p>Member since: <%= @user.member_since %></p>
<p><%= @user.status_badge %></p>
<p>Phone: <%= @user.formatted_phone %></p>
<img src="<%= @user.avatar_url(size: 200) %>" />
```

Clean and readable!

**Python comparison (Django):**
```python
# views.py
def user_detail(request, user_id):
    user = User.objects.get(id=user_id)
    presenter = UserPresenter(user)
    return render(request, 'user.html', {'user': presenter})

# Template
<h1>{{ user.display_name }}</h1>
<p>{{ user.member_since }}</p>
```

## Plain Ruby Decorator (No Gems)

You don't need Draper! Here's a plain Ruby approach:

```ruby
# app/decorators/base_decorator.rb
class BaseDecorator
  def initialize(object, view_context = nil)
    @object = object
    @view_context = view_context
  end

  def method_missing(method, *args, &block)
    if @object.respond_to?(method)
      @object.send(method, *args, &block)
    else
      super
    end
  end

  def respond_to_missing?(method, include_private = false)
    @object.respond_to?(method) || super
  end

  private

  attr_reader :object, :view_context
  alias_method :h, :view_context
end

# app/decorators/user_decorator.rb
class UserDecorator < BaseDecorator
  def display_name
    object.admin? ? "#{object.name} (Admin)" : object.name
  end

  def member_since
    object.created_at.strftime("%B %Y")
  end

  def status_badge
    object.active? ? "🟢 Active" : "🔴 Inactive"
  end
end

# Usage
user = User.first
decorated = UserDecorator.new(user, view_context)
decorated.display_name  # => "Alice (Admin)"
decorated.email  # => delegated to user.email
```

**Python comparison:**
```python
class BasePresenter:
    def __init__(self, obj):
        self._obj = obj
    
    def __getattr__(self, name):
        return getattr(self._obj, name)

class UserPresenter(BasePresenter):
    def display_name(self):
        if self._obj.is_admin:
            return f"{self._obj.name} (Admin)"
        return self._obj.name
```

## Real-World Examples

### Example 1: Product Decorator

```ruby
class ProductDecorator < Draper::Decorator
  delegate_all

  def price_with_currency
    h.number_to_currency(object.price)
  end

  def discount_percentage
    return nil unless object.discount_price

    percentage = ((object.price - object.discount_price) / object.price * 100).round
    "#{percentage}% OFF"
  end

  def availability_badge
    if object.in_stock?
      h.content_tag :span, '✓ In Stock', class: 'badge badge-success'
    else
      h.content_tag :span, '✗ Out of Stock', class: 'badge badge-danger'
    end
  end

  def thumbnail_url
    if object.images.any?
      h.url_for(object.images.first.variant(resize: '200x200'))
    else
      '/images/product-placeholder.png'
    end
  end

  def short_description(length: 100)
    if object.description.length > length
      "#{object.description.truncate(length)}..."
    else
      object.description
    end
  end
end
```

### Example 2: Order Decorator

```ruby
class OrderDecorator < Draper::Decorator
  delegate_all

  def status_label
    case object.status
    when 'pending'
      h.content_tag :span, '⏳ Pending', class: 'badge badge-warning'
    when 'processing'
      h.content_tag :span, '🔄 Processing', class: 'badge badge-info'
    when 'shipped'
      h.content_tag :span, '📦 Shipped', class: 'badge badge-primary'
    when 'delivered'
      h.content_tag :span, '✓ Delivered', class: 'badge badge-success'
    when 'cancelled'
      h.content_tag :span, '✗ Cancelled', class: 'badge badge-danger'
    end
  end

  def total_with_shipping
    h.number_to_currency(object.total + object.shipping_cost)
  end

  def placed_at
    object.created_at.strftime("%B %d, %Y at %I:%M %p")
  end

  def estimated_delivery
    return nil unless object.shipped_at

    delivery_date = object.shipped_at + 5.days
    delivery_date.strftime("%B %d, %Y")
  end

  def items_summary
    count = object.items.count
    "#{count} #{count == 1 ? 'item' : 'items'}"
  end
end
```

### Example 3: Blog Post Decorator

```ruby
class PostDecorator < Draper::Decorator
  delegate_all

  def published_at
    object.created_at.strftime("%B %d, %Y")
  end

  def reading_time
    words = object.content.split.size
    minutes = (words / 200.0).ceil
    "#{minutes} min read"
  end

  def author_with_avatar
    h.content_tag :div, class: 'author-info' do
      h.concat h.image_tag(object.author.avatar_url, class: 'avatar')
      h.concat h.content_tag(:span, object.author.name)
    end
  end

  def tags_list
    object.tags.map { |tag| 
      h.link_to tag.name, h.tag_path(tag), class: 'tag-badge'
    }.join(' ').html_safe
  end

  def social_share_links
    url = h.post_url(object)
    
    h.content_tag :div, class: 'social-share' do
      h.concat twitter_share_link(url)
      h.concat facebook_share_link(url)
      h.concat linkedin_share_link(url)
    end
  end

  private

  def twitter_share_link(url)
    h.link_to "Tweet", 
              "https://twitter.com/intent/tweet?text=#{object.title}&url=#{url}",
              target: '_blank',
              class: 'btn btn-twitter'
  end

  def facebook_share_link(url)
    h.link_to "Share",
              "https://www.facebook.com/sharer/sharer.php?u=#{url}",
              target: '_blank',
              class: 'btn btn-facebook'
  end

  def linkedin_share_link(url)
    h.link_to "Share",
              "https://www.linkedin.com/sharing/share-offsite/?url=#{url}",
              target: '_blank',
              class: 'btn btn-linkedin'
  end
end
```

## Collections

Decorate entire collections:

```ruby
# Controller
def index
  @users = User.all.decorate
end

# View
<% @users.each do |user| %>
  <%= user.display_name %>
<% end %>
```

Or create a collection decorator:

```ruby
class UsersDecorator < Draper::CollectionDecorator
  def total_admins
    object.count(&:admin?)
  end

  def average_age
    ages = object.map(&:age).compact
    ages.sum / ages.size
  end
end

# Usage
@users = UsersDecorator.new(User.all)
@users.total_admins  # => 5
@users.average_age   # => 32
```

## Testing Decorators

Decorators are easy to test!

```ruby
# spec/decorators/user_decorator_spec.rb
RSpec.describe UserDecorator do
  let(:user) { create(:user, name: 'Alice', admin: true, created_at: Date.new(2022, 1, 15)) }
  let(:decorator) { described_class.new(user) }

  describe '#display_name' do
    context 'when user is admin' do
      it 'includes admin badge' do
        expect(decorator.display_name).to include('Admin')
        expect(decorator.display_name).to include('Alice')
      end
    end

    context 'when user is not admin' do
      before { user.admin = false }

      it 'returns plain name' do
        expect(decorator.display_name).to eq('Alice')
      end
    end
  end

  describe '#member_since' do
    it 'formats created_at' do
      expect(decorator.member_since).to eq('January 2022')
    end
  end

  describe '#status_badge' do
    context 'when active' do
      before { user.active = true }

      it 'returns active badge' do
        expect(decorator.status_badge).to include('Active')
      end
    end

    context 'when inactive' do
      before { user.active = false }

      it 'returns inactive badge' do
        expect(decorator.status_badge).to include('Inactive')
      end
    end
  end
end
```

**Python comparison:**
```python
import pytest

class TestUserPresenter:
    def test_display_name_for_admin(self):
        user = User(name="Alice", is_admin=True)
        presenter = UserPresenter(user)
        assert "Admin" in presenter.display_name()
        assert "Alice" in presenter.display_name()
    
    def test_display_name_for_regular_user(self):
        user = User(name="Bob", is_admin=False)
        presenter = UserPresenter(user)
        assert presenter.display_name() == "Bob"
```

## View Components Alternative

Rails 6.1+ introduced ViewComponent as an alternative:

```ruby
# app/components/user_card_component.rb
class UserCardComponent < ViewComponent::Base
  def initialize(user:)
    @user = user
  end

  def display_name
    @user.admin? ? "#{@user.name} (Admin)" : @user.name
  end

  def member_since
    @user.created_at.strftime("%B %Y")
  end
end

# app/components/user_card_component.html.erb
<div class="user-card">
  <h3><%= display_name %></h3>
  <p>Member since: <%= member_since %></p>
</div>

# Usage in view
<%= render UserCardComponent.new(user: @user) %>
```

Components combine decorator logic with templates.

## When to Use Decorators

### Use Decorators When:
- ✅ Formatting data for display (dates, currency, phone numbers)
- ✅ Conditional presentation logic
- ✅ Generating HTML snippets
- ✅ Combining multiple attributes
- ✅ View-specific helpers

### Don't Use Decorators For:
- ❌ Business logic (use service objects)
- ❌ Validations (belongs in models)
- ❌ Database queries (use models/scopes)
- ❌ API responses (use serializers)

## Best Practices

1. **Keep decorators focused on presentation**
2. **Don't put business logic in decorators**
3. **Use semantic method names** (not `decorated_name`, just `display_name`)
4. **Test decorators independently**
5. **Consider ViewComponents for complex UI**
6. **Use plain Ruby if you don't need view helpers**

## Alternative Gems

- **Draper**: Most popular, feature-rich
- **SimpleDelegator**: Built into Ruby, no dependencies
- **ViewComponent**: Rails 6.1+, combines decorators with templates
- **Cells**: More complex, includes caching and testing

## Exercises

1. **Create User Decorator**: Build a decorator with:
   - Formatted phone number
   - Avatar with fallback
   - Role badge
   - Join date

2. **Product Catalog**: Create a product decorator with:
   - Price formatting
   - Discount calculation
   - Stock status
   - Image thumbnails

3. **Refactor View**: Take a complex ERB template and extract logic into a decorator.

4. **Compare Approaches**: Implement the same presentation logic using:
   - Helper methods
   - Decorator
   - ViewComponent
   
   Compare readability and testability.

## Summary

Decorators keep your models clean and your views simple by providing a dedicated place for presentation logic. They follow the Single Responsibility Principle and make your code more maintainable and testable.

**Key Takeaways:**
- Decorators handle presentation logic
- Keep view logic out of models and templates
- Draper is the most popular gem
- Easy to test in isolation
- Use `delegate_all` to proxy to model
- Access view helpers via `h`

**Next Tutorial:** Essential Gems - master Bundler, Pry, Sidekiq, and Bullet for professional Ruby development.
