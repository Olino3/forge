# Tutorial 7: Service Objects Pattern - Organizing Complex Business Logic

## Overview

In Ruby (especially Rails), it's tempting to put all business logic in Models or Controllers. But as applications grow, this leads to "fat models" and "fat controllers." Service Objects are plain Ruby classes that do one thing well - they encapsulate complex business logic into dedicated, testable units.

## Python Comparison

**Service Objects are universal!** Both Python and Ruby use them:

**Python (Django/Flask):**
```python
# services/user_registration.py
class UserRegistrationService:
    def __init__(self, email, password):
        self.email = email
        self.password = password
    
    def call(self):
        user = User.objects.create(
            email=self.email,
            password=self.make_password(password)
        )
        self.send_welcome_email(user)
        self.create_default_profile(user)
        return user
    
    def send_welcome_email(self, user):
        # Email logic
        pass

# Usage
service = UserRegistrationService("alice@example.com", "password123")
user = service.call()
```

**Ruby:**
```ruby
# app/services/user_registration_service.rb
class UserRegistrationService
  def initialize(email, password)
    @email = email
    @password = password
  end

  def call
    user = User.create!(
      email: @email,
      password: @password
    )
    send_welcome_email(user)
    create_default_profile(user)
    user
  end

  private

  def send_welcome_email(user)
    # Email logic
  end

  def create_default_profile(user)
    # Profile logic
  end
end

# Usage
service = UserRegistrationService.new('alice@example.com', 'password123')
user = service.call
```

Nearly identical! The pattern transcends language boundaries.

## Why Service Objects?

### The Problem: Fat Controllers

```ruby
# BAD - All logic in controller
class UsersController < ApplicationController
  def create
    @user = User.new(user_params)
    
    if @user.save
      # Send welcome email
      UserMailer.welcome_email(@user).deliver_later
      
      # Create default profile
      Profile.create!(
        user: @user,
        bio: "New user",
        avatar_url: DEFAULT_AVATAR
      )
      
      # Award signup bonus
      @user.wallet.add_credits(100)
      
      # Track analytics
      Analytics.track('user_signup', user_id: @user.id)
      
      # Notify admins
      AdminNotifier.new_user(@user)
      
      redirect_to @user, notice: 'Welcome!'
    else
      render :new
    end
  end
end
```

Problems:
- ❌ Controller is too complex
- ❌ Hard to test
- ❌ Business logic mixed with HTTP concerns
- ❌ Can't reuse logic elsewhere (API, console, background jobs)

**Python comparison:** Same issue in Django views or Flask routes!

### The Solution: Service Objects

```ruby
# GOOD - Service object
class UserRegistrationService
  def initialize(params)
    @params = params
  end

  def call
    ActiveRecord::Base.transaction do
      create_user
      send_welcome_email
      create_default_profile
      award_signup_bonus
      track_analytics
      notify_admins
    end
    
    @user
  end

  private

  attr_reader :params

  def create_user
    @user = User.create!(params)
  end

  def send_welcome_email
    UserMailer.welcome_email(@user).deliver_later
  end

  def create_default_profile
    Profile.create!(user: @user, bio: 'New user', avatar_url: DEFAULT_AVATAR)
  end

  def award_signup_bonus
    @user.wallet.add_credits(100)
  end

  def track_analytics
    Analytics.track('user_signup', user_id: @user.id)
  end

  def notify_admins
    AdminNotifier.new_user(@user)
  end
end

# Controller becomes thin!
class UsersController < ApplicationController
  def create
    service = UserRegistrationService.new(user_params)
    @user = service.call
    
    redirect_to @user, notice: 'Welcome!'
  rescue ActiveRecord::RecordInvalid => e
    @user = e.record
    render :new
  end
end
```

Benefits:
- ✅ Single Responsibility Principle
- ✅ Easy to test in isolation
- ✅ Reusable (controller, API, console, background jobs)
- ✅ Clear, self-documenting code
- ✅ Transaction handling in one place

## Service Object Conventions

### 1. Naming Convention

```ruby
# Format: [Verb][Noun]Service
CreateInvoiceService
SendReminderEmailService
ProcessPaymentService
CalculateShippingCostService
ImportUsersFromCsvService

# Or use plain verb+noun
CreateInvoice
SendReminderEmail
ProcessPayment
```

**Python comparison:** Same convention works well!

### 2. Single Public Method: `call`

```ruby
class CreateInvoice
  def initialize(order)
    @order = order
  end

  def call
    # Main logic here
  end

  private
  # Helper methods
end

# Usage
CreateInvoice.new(order).call
```

Some teams use `.call` as a class method:

```ruby
class CreateInvoice
  def self.call(order)
    new(order).call
  end

  def initialize(order)
    @order = order
  end

  def call
    # Logic
  end

  private
  # ...
end

# Usage (more concise)
CreateInvoice.call(order)
```

**Python comparison:**
```python
# Python often uses __call__
class CreateInvoice:
    def __init__(self, order):
        self.order = order
    
    def __call__(self):
        # Logic
        pass

# Usage
CreateInvoice(order)()
```

### 3. Return Values

Be explicit about what you return:

```ruby
class CreateInvoice
  def call
    invoice = Invoice.create!(
      order: @order,
      amount: @order.total
    )
    
    send_invoice_email(invoice)
    
    invoice  # Return the created invoice
  end
end

# Or return a result object
class CreateInvoice
  Result = Struct.new(:success?, :invoice, :errors)

  def call
    invoice = Invoice.create(order: @order)
    
    if invoice.persisted?
      Result.new(true, invoice, [])
    else
      Result.new(false, nil, invoice.errors.full_messages)
    end
  end
end

# Usage
result = CreateInvoice.call(order)
if result.success?
  puts "Invoice created: #{result.invoice.id}"
else
  puts "Errors: #{result.errors.join(', ')}"
end
```

**Python comparison:**
```python
from dataclasses import dataclass
from typing import Optional, List

@dataclass
class Result:
    success: bool
    invoice: Optional[Invoice]
    errors: List[str]

class CreateInvoice:
    def call(self) -> Result:
        # Logic
        return Result(success=True, invoice=invoice, errors=[])
```

## Real-World Examples

### Example 1: Payment Processing

```ruby
class ProcessPayment
  def self.call(order, payment_method)
    new(order, payment_method).call
  end

  def initialize(order, payment_method)
    @order = order
    @payment_method = payment_method
  end

  def call
    ActiveRecord::Base.transaction do
      charge_payment
      update_order_status
      send_receipt
      fulfill_order
    end
    
    @payment
  rescue Stripe::CardError => e
    @order.update(payment_error: e.message)
    raise
  end

  private

  def charge_payment
    @payment = Stripe::Charge.create(
      amount: (@order.total * 100).to_i,
      currency: 'usd',
      source: @payment_method,
      description: "Order ##{@order.id}"
    )
  end

  def update_order_status
    @order.update!(status: :paid, paid_at: Time.current)
  end

  def send_receipt
    OrderMailer.receipt(@order).deliver_later
  end

  def fulfill_order
    FulfillmentService.call(@order)
  end
end
```

**Python comparison:**
```python
import stripe
from django.db import transaction

class ProcessPayment:
    def __init__(self, order, payment_method):
        self.order = order
        self.payment_method = payment_method
    
    @transaction.atomic
    def call(self):
        self.charge_payment()
        self.update_order_status()
        self.send_receipt()
        self.fulfill_order()
        return self.payment
    
    def charge_payment(self):
        self.payment = stripe.Charge.create(
            amount=int(self.order.total * 100),
            currency='usd',
            source=self.payment_method,
            description=f"Order #{self.order.id}"
        )
```

### Example 2: CSV Import

```ruby
class ImportUsersFromCsv
  def initialize(file_path)
    @file_path = file_path
    @imported_count = 0
    @errors = []
  end

  def call
    CSV.foreach(@file_path, headers: true) do |row|
      import_user(row)
    end
    
    {
      imported: @imported_count,
      errors: @errors
    }
  end

  private

  def import_user(row)
    User.create!(
      email: row['email'],
      name: row['name'],
      role: row['role']
    )
    @imported_count += 1
  rescue ActiveRecord::RecordInvalid => e
    @errors << { row: row.to_h, error: e.message }
  end
end

# Usage
result = ImportUsersFromCsv.call('users.csv')
puts "Imported: #{result[:imported]}, Errors: #{result[:errors].count}"
```

### Example 3: Report Generation

```ruby
class GenerateSalesReport
  def initialize(start_date, end_date)
    @start_date = start_date
    @end_date = end_date
  end

  def call
    {
      total_sales: calculate_total_sales,
      total_orders: count_orders,
      average_order_value: calculate_average_order,
      top_products: find_top_products,
      sales_by_day: group_sales_by_day
    }
  end

  private

  def orders
    @orders ||= Order.where(created_at: @start_date..@end_date)
  end

  def calculate_total_sales
    orders.sum(:total)
  end

  def count_orders
    orders.count
  end

  def calculate_average_order
    total = calculate_total_sales
    count = count_orders
    count.zero? ? 0 : total / count
  end

  def find_top_products
    OrderItem.joins(:order)
             .where(orders: { created_at: @start_date..@end_date })
             .group(:product_id)
             .order('sum_quantity DESC')
             .limit(10)
             .sum(:quantity)
  end

  def group_sales_by_day
    orders.group_by_day(:created_at).sum(:total)
  end
end
```

## Testing Service Objects

Service objects are incredibly easy to test!

```ruby
# spec/services/create_invoice_service_spec.rb
RSpec.describe CreateInvoiceService do
  describe '#call' do
    let(:order) { create(:order, total: 100) }
    let(:service) { described_class.new(order) }

    it 'creates an invoice' do
      expect { service.call }.to change(Invoice, :count).by(1)
    end

    it 'sets the correct amount' do
      invoice = service.call
      expect(invoice.amount).to eq(100)
    end

    it 'sends email' do
      expect(InvoiceMailer).to receive(:invoice_created).and_call_original
      service.call
    end

    context 'when order is invalid' do
      let(:order) { build(:order, total: nil) }

      it 'raises an error' do
        expect { service.call }.to raise_error(ActiveRecord::RecordInvalid)
      end
    end
  end
end
```

**Python comparison:**
```python
import pytest
from unittest.mock import patch

class TestCreateInvoice:
    def test_creates_invoice(self, order):
        service = CreateInvoice(order)
        invoice = service.call()
        assert invoice.id is not None
    
    def test_sends_email(self, order):
        with patch('services.InvoiceMailer.invoice_created') as mock:
            service = CreateInvoice(order)
            service.call()
            mock.assert_called_once()
```

## Advanced Patterns

### 1. Callable Modules (Dry-rb Approach)

```ruby
class CreateInvoice
  include Dry::Transaction

  step :validate_order
  step :create_invoice
  step :send_email

  def validate_order(order)
    order.valid? ? Success(order) : Failure("Invalid order")
  end

  def create_invoice(order)
    invoice = Invoice.create(order: order)
    Success(invoice)
  end

  def send_email(invoice)
    InvoiceMailer.created(invoice).deliver_later
    Success(invoice)
  end
end
```

### 2. Service Objects with Callbacks

```ruby
class BaseService
  def self.call(*args, &block)
    new(*args, &block).call
  end

  def call
    run_callbacks :execute do
      execute
    end
  end

  private

  def execute
    raise NotImplementedError
  end
end

class CreateUser < BaseService
  set_callback :execute, :after, :send_welcome_email

  def initialize(params)
    @params = params
  end

  private

  def execute
    @user = User.create!(@params)
  end

  def send_welcome_email
    UserMailer.welcome(@user).deliver_later
  end
end
```

### 3. Form Objects (Special Service Objects)

```ruby
class UserRegistrationForm
  include ActiveModel::Model

  attr_accessor :email, :password, :password_confirmation, :terms_accepted

  validates :email, presence: true, format: { with: URI::MailTo::EMAIL_REGEXP }
  validates :password, presence: true, length: { minimum: 8 }
  validates :password_confirmation, presence: true
  validates :terms_accepted, acceptance: true
  validate :passwords_match

  def save
    return false unless valid?

    user = User.create!(
      email: email,
      password: password
    )
    
    send_welcome_email(user)
    user
  end

  private

  def passwords_match
    return if password == password_confirmation
    errors.add(:password_confirmation, "doesn't match password")
  end

  def send_welcome_email(user)
    UserMailer.welcome(user).deliver_later
  end
end

# Usage in controller
def create
  @form = UserRegistrationForm.new(user_params)
  
  if @form.save
    redirect_to root_path
  else
    render :new
  end
end
```

## When NOT to Use Service Objects

Don't overuse them! Not everything needs a service object:

```ruby
# OVERKILL - Simple CRUD doesn't need a service
class CreatePost
  def call(params)
    Post.create(params)
  end
end

# JUST USE RAILS
def create
  @post = Post.create(post_params)
  # ...
end

# USE SERVICE OBJECTS when:
# - Multiple models involved
# - External API calls
# - Complex business logic
# - Background job coordination
# - Multi-step processes
```

## Best Practices

1. **One responsibility per service**
2. **Keep them small** (< 100 lines)
3. **Name them clearly** (verb + noun)
4. **Return explicit values**
5. **Use transactions when needed**
6. **Test in isolation**
7. **Don't couple to framework** (can be plain Ruby)

## Exercises

1. **Refactor Controller**: Take a fat controller action and extract logic into a service object.

2. **Payment Service**: Create a `ProcessRefund` service that:
   - Refunds payment via Stripe
   - Updates order status
   - Sends refund confirmation email
   - Creates refund record

3. **Background Job**: Create a service that coordinates multiple background jobs for a complex workflow.

4. **Form Object**: Create a complex registration form with validations that spans multiple models.

## Summary

Service Objects keep your codebase maintainable by extracting complex business logic into dedicated, testable classes. They're a universal pattern used in both Ruby and Python. Master them to write professional, scalable code.

**Key Takeaways:**
- Service Objects = Single Responsibility Principle in action
- Use `call` as the primary public method
- Keep controllers thin, services fat
- Easy to test in isolation
- Reusable across controllers, APIs, background jobs
- Don't overuse - simple CRUD doesn't need services

**Next Tutorial:** Decorator/Presenter Pattern - learn to keep view logic out of models and templates.
