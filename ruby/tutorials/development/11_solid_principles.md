# Tutorial 11: SOLID Principles in Ruby

## Overview

SOLID is a set of five design principles that make software designs more understandable, flexible, and maintainable. While these principles apply to all object-oriented languages, Ruby's dynamic nature offers unique ways to implement them. This tutorial shows how to apply SOLID principles in Ruby with practical examples.

## Python Comparison

SOLID principles are **language-agnostic** and apply equally to Python and Ruby. The implementations differ slightly due to language features, but the concepts are identical.

## The SOLID Principles

1. **S**ingle Responsibility Principle
2. **O**pen/Closed Principle
3. **L**iskov Substitution Principle
4. **I**nterface Segregation Principle
5. **D**ependency Inversion Principle

## 1. Single Responsibility Principle (SRP)

**A class should have only one reason to change.**

### Bad Example: Multiple Responsibilities

```ruby
# BAD - User class doing too much
class User
  attr_accessor :name, :email

  def initialize(name, email)
    @name = name
    @email = email
  end

  # Responsibility 1: User data
  def valid?
    email.include?('@')
  end

  # Responsibility 2: Persistence
  def save
    Database.execute("INSERT INTO users...")
  end

  # Responsibility 3: Email notification
  def send_welcome_email
    EmailService.send(email, "Welcome #{name}!")
  end

  # Responsibility 4: Report generation
  def generate_report
    "User Report: #{name}, #{email}"
  end
end
```

Problems:
- Too many reasons to change
- Hard to test
- Tight coupling

**Python comparison:**
```python
# Same anti-pattern exists in Python
class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email
    
    def is_valid(self):
        return '@' in self.email
    
    def save(self):
        Database.execute("INSERT...")
    
    def send_welcome_email(self):
        EmailService.send(self.email, f"Welcome {self.name}!")
```

### Good Example: Separated Responsibilities

```ruby
# GOOD - Single responsibility per class

class User
  attr_accessor :name, :email

  def initialize(name, email)
    @name = name
    @email = email
  end

  def valid?
    email.include?('@')
  end
end

class UserRepository
  def save(user)
    Database.execute("INSERT INTO users (name, email) VALUES (?, ?)", user.name, user.email)
  end

  def find(id)
    # Database logic
  end
end

class UserNotifier
  def send_welcome_email(user)
    EmailService.send(user.email, "Welcome #{user.name}!")
  end
end

class UserReportGenerator
  def generate(user)
    "User Report: #{user.name}, #{user.email}"
  end
end

# Usage
user = User.new('Alice', 'alice@example.com')
UserRepository.new.save(user)
UserNotifier.new.send_welcome_email(user)
```

**Benefits:**
- Each class has one reason to change
- Easy to test in isolation
- Reusable components

## 2. Open/Closed Principle (OCP)

**Software entities should be open for extension but closed for modification.**

### Bad Example: Modification Required

```ruby
# BAD - Need to modify class to add new payment types
class PaymentProcessor
  def process(payment)
    case payment.type
    when :credit_card
      process_credit_card(payment)
    when :paypal
      process_paypal(payment)
    when :bitcoin
      process_bitcoin(payment)
    # Adding new type requires modifying this class!
    end
  end

  def process_credit_card(payment)
    # Logic
  end

  def process_paypal(payment)
    # Logic
  end

  def process_bitcoin(payment)
    # Logic
  end
end
```

**Python comparison:**
```python
# Same anti-pattern
class PaymentProcessor:
    def process(self, payment):
        if payment.type == 'credit_card':
            self.process_credit_card(payment)
        elif payment.type == 'paypal':
            self.process_paypal(payment)
        # Must modify to add new types!
```

### Good Example: Extension via Polymorphism

```ruby
# GOOD - Extend via new classes, don't modify existing

class PaymentProcessor
  def initialize(strategy)
    @strategy = strategy
  end

  def process(payment)
    @strategy.process(payment)
  end
end

class CreditCardPaymentStrategy
  def process(payment)
    # Credit card logic
    puts "Processing credit card payment: #{payment.amount}"
  end
end

class PayPalPaymentStrategy
  def process(payment)
    # PayPal logic
    puts "Processing PayPal payment: #{payment.amount}"
  end
end

class BitcoinPaymentStrategy
  def process(payment)
    # Bitcoin logic
    puts "Processing Bitcoin payment: #{payment.amount}"
  end
end

# Adding new payment type: just create new class!
class ApplePayStrategy
  def process(payment)
    puts "Processing Apple Pay payment: #{payment.amount}"
  end
end

# Usage
payment = Payment.new(amount: 100)
processor = PaymentProcessor.new(CreditCardPaymentStrategy.new)
processor.process(payment)

# Switch strategy
processor = PaymentProcessor.new(BitcoinPaymentStrategy.new)
processor.process(payment)
```

**Benefits:**
- Add new payment types without modifying existing code
- Each strategy is independently testable
- Follows Strategy pattern

**Python comparison:**
```python
# Same approach with Strategy pattern
from abc import ABC, abstractmethod

class PaymentStrategy(ABC):
    @abstractmethod
    def process(self, payment):
        pass

class CreditCardPaymentStrategy(PaymentStrategy):
    def process(self, payment):
        print(f"Processing credit card: {payment.amount}")

class PaymentProcessor:
    def __init__(self, strategy):
        self.strategy = strategy
    
    def process(self, payment):
        self.strategy.process(payment)
```

## 3. Liskov Substitution Principle (LSP)

**Subtypes must be substitutable for their base types without altering correctness.**

### Bad Example: Broken Substitution

```ruby
# BAD - Square breaks Rectangle's contract
class Rectangle
  attr_accessor :width, :height

  def initialize(width, height)
    @width = width
    @height = height
  end

  def area
    width * height
  end
end

class Square < Rectangle
  def width=(value)
    @width = value
    @height = value  # Violates LSP!
  end

  def height=(value)
    @width = value
    @height = value  # Violates LSP!
  end
end

# Usage breaks:
rect = Rectangle.new(5, 10)
rect.width = 3
rect.area  # => 30 ✓

square = Square.new(5, 5)
square.width = 3
square.area  # => 9 (expected 15 if truly a Rectangle!) ✗
```

**Python comparison:**
```python
# Same LSP violation
class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height
    
    def area(self):
        return self.width * self.height

class Square(Rectangle):
    @property
    def width(self):
        return self._width
    
    @width.setter
    def width(self, value):
        self._width = value
        self._height = value  # Violates LSP!
```

### Good Example: Proper Abstraction

```ruby
# GOOD - Don't inherit if substitution breaks
class Shape
  def area
    raise NotImplementedError
  end
end

class Rectangle < Shape
  attr_accessor :width, :height

  def initialize(width, height)
    @width = width
    @height = height
  end

  def area
    width * height
  end
end

class Square < Shape
  attr_accessor :size

  def initialize(size)
    @size = size
  end

  def area
    size * size
  end
end

# Both are Shapes, but not substitutable for each other
```

**Or use composition:**
```ruby
class Rectangle
  attr_reader :width, :height

  def initialize(width, height)
    @width = width
    @height = height
  end

  def area
    width * height
  end
end

class Square
  attr_reader :size

  def initialize(size)
    @size = size
  end

  def area
    size * size
  end

  def to_rectangle
    Rectangle.new(size, size)
  end
end
```

## 4. Interface Segregation Principle (ISP)

**Clients should not be forced to depend on interfaces they don't use.**

### Bad Example: Fat Interface

```ruby
# BAD - All workers must implement all methods
class Worker
  def work
    raise NotImplementedError
  end

  def eat
    raise NotImplementedError
  end

  def sleep
    raise NotImplementedError
  end
end

class Human < Worker
  def work
    puts "Working"
  end

  def eat
    puts "Eating"
  end

  def sleep
    puts "Sleeping"
  end
end

class Robot < Worker
  def work
    puts "Working"
  end

  def eat
    # Robots don't eat!
    raise "Robots don't eat"
  end

  def sleep
    # Robots don't sleep!
    raise "Robots don't sleep"
  end
end
```

**Python comparison:**
```python
# Same anti-pattern
from abc import ABC, abstractmethod

class Worker(ABC):
    @abstractmethod
    def work(self):
        pass
    
    @abstractmethod
    def eat(self):
        pass
    
    @abstractmethod
    def sleep(self):
        pass
```

### Good Example: Segregated Interfaces

```ruby
# GOOD - Small, focused interfaces
module Workable
  def work
    raise NotImplementedError
  end
end

module Eatable
  def eat
    raise NotImplementedError
  end
end

module Sleepable
  def sleep
    raise NotImplementedError
  end
end

class Human
  include Workable
  include Eatable
  include Sleepable

  def work
    puts "Working"
  end

  def eat
    puts "Eating"
  end

  def sleep
    puts "Sleeping"
  end
end

class Robot
  include Workable  # Only implements what it needs!

  def work
    puts "Working"
  end
end
```

**Benefits:**
- Each class only implements what it needs
- More flexible, easier to maintain

**Python comparison:**
```python
from abc import ABC, abstractmethod

class Workable(ABC):
    @abstractmethod
    def work(self):
        pass

class Eatable(ABC):
    @abstractmethod
    def eat(self):
        pass

class Human(Workable, Eatable):
    def work(self):
        print("Working")
    
    def eat(self):
        print("Eating")

class Robot(Workable):  # Only implements needed interface
    def work(self):
        print("Working")
```

## 5. Dependency Inversion Principle (DIP)

**Depend on abstractions, not concretions.**

### Bad Example: Tight Coupling

```ruby
# BAD - Depends on concrete class
class UserNotifier
  def initialize
    @email_service = EmailService.new  # Tight coupling!
  end

  def notify(user, message)
    @email_service.send(user.email, message)
  end
end

class EmailService
  def send(email, message)
    puts "Sending email to #{email}: #{message}"
  end
end

# Can't easily switch to SMS without modifying UserNotifier
```

**Python comparison:**
```python
# Same tight coupling
class UserNotifier:
    def __init__(self):
        self.email_service = EmailService()  # Concrete dependency
    
    def notify(self, user, message):
        self.email_service.send(user.email, message)
```

### Good Example: Dependency Injection

```ruby
# GOOD - Depends on abstraction (duck typing)
class UserNotifier
  def initialize(notification_service)
    @notification_service = notification_service  # Injected dependency
  end

  def notify(user, message)
    @notification_service.send(user, message)
  end
end

# Concrete implementations
class EmailNotificationService
  def send(user, message)
    puts "Email to #{user.email}: #{message}"
  end
end

class SmsNotificationService
  def send(user, message)
    puts "SMS to #{user.phone}: #{message}"
  end
end

class SlackNotificationService
  def send(user, message)
    puts "Slack to #{user.slack_handle}: #{message}"
  end
end

# Usage - easily swap implementations!
user = User.new(email: 'alice@example.com')

notifier = UserNotifier.new(EmailNotificationService.new)
notifier.notify(user, 'Hello!')

notifier = UserNotifier.new(SmsNotificationService.new)
notifier.notify(user, 'Hello!')
```

**Benefits:**
- Easy to test with mocks
- Easy to swap implementations
- Loose coupling

**Python comparison:**
```python
# Dependency Injection
class UserNotifier:
    def __init__(self, notification_service):
        self.notification_service = notification_service
    
    def notify(self, user, message):
        self.notification_service.send(user, message)

# Can inject any service with send() method
notifier = UserNotifier(EmailNotificationService())
notifier = UserNotifier(SmsNotificationService())
```

## Real-World Example: SOLID Together

```ruby
# Applying all SOLID principles

# 1. SRP - Each class has single responsibility
class Order
  attr_reader :id, :items, :total

  def initialize(id, items)
    @id = id
    @items = items
    @total = calculate_total
  end

  private

  def calculate_total
    items.sum(&:price)
  end
end

# 2. OCP - Open for extension via strategies
class OrderProcessor
  def initialize(payment_strategy, notification_strategy)
    @payment_strategy = payment_strategy
    @notification_strategy = notification_strategy
  end

  def process(order)
    @payment_strategy.charge(order)
    @notification_strategy.notify(order)
  end
end

# 3. LSP - All payment strategies are substitutable
class CreditCardPayment
  def charge(order)
    puts "Charging credit card: #{order.total}"
  end
end

class PayPalPayment
  def charge(order)
    puts "Charging PayPal: #{order.total}"
  end
end

# 4. ISP - Small interfaces
module Chargeable
  def charge(order)
    raise NotImplementedError
  end
end

module Notifiable
  def notify(order)
    raise NotImplementedError
  end
end

# 5. DIP - Depend on abstractions, inject dependencies
class EmailNotification
  def notify(order)
    puts "Email sent for order #{order.id}"
  end
end

# Usage
order = Order.new(1, [item1, item2])
processor = OrderProcessor.new(
  CreditCardPayment.new,
  EmailNotification.new
)
processor.process(order)

# Easy to swap implementations!
processor = OrderProcessor.new(
  PayPalPayment.new,
  SmsNotification.new
)
```

## Testing SOLID Code

SOLID code is easier to test:

```ruby
RSpec.describe OrderProcessor do
  let(:order) { instance_double(Order, id: 1, total: 100) }
  let(:payment) { instance_double(CreditCardPayment) }
  let(:notifier) { instance_double(EmailNotification) }
  let(:processor) { described_class.new(payment, notifier) }

  describe '#process' do
    it 'charges payment' do
      expect(payment).to receive(:charge).with(order)
      allow(notifier).to receive(:notify)
      
      processor.process(order)
    end

    it 'sends notification' do
      allow(payment).to receive(:charge)
      expect(notifier).to receive(:notify).with(order)
      
      processor.process(order)
    end
  end
end
```

Easy to test with mocks because dependencies are injected!

## Exercises

1. **Refactor for SRP**: Take a "God class" and split it into multiple single-responsibility classes.

2. **Strategy Pattern**: Implement a discount calculator using OCP with different discount strategies.

3. **LSP Violation**: Find an LSP violation in existing code and fix it.

4. **Interface Segregation**: Create a file storage system with segregated interfaces for reading, writing, and deleting.

5. **Dependency Injection**: Refactor a tightly-coupled class to use dependency injection.

## Summary

SOLID principles lead to more maintainable, testable, and flexible code. Ruby's dynamic nature (duck typing, modules) makes implementing these principles elegant and natural.

**Key Takeaways:**
- **SRP**: One class, one responsibility
- **OCP**: Extend via new classes, not modifications
- **LSP**: Subtypes must be substitutable
- **ISP**: Small, focused interfaces (modules in Ruby)
- **DIP**: Inject dependencies, depend on abstractions

**Next Tutorial:** Secrets Management and Security Best Practices - learn to handle sensitive data securely in Ruby applications.
