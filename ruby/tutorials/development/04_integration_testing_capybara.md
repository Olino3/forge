# Tutorial 4: Integration Testing with Capybara - Testing Web Applications

## Overview

Capybara is essential for testing web applications in Ruby. It simulates a real user interacting with your app through a browser - clicking buttons, filling forms, navigating pages. While unit tests verify individual components, Capybara tests verify the complete user experience.

## Python Comparison

**Python's Selenium vs Ruby's Capybara:**

**Python (Selenium with pytest):**
```python
from selenium import webdriver
from selenium.webdriver.common.by import By

def test_user_login():
    driver = webdriver.Chrome()
    driver.get("http://localhost:3000/login")
    
    driver.find_element(By.ID, "email").send_keys("user@example.com")
    driver.find_element(By.ID, "password").send_keys("password")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    
    assert "Dashboard" in driver.page_source
    driver.quit()
```

**Ruby (Capybara with RSpec):**
```ruby
feature 'User login' do
  scenario 'successful login' do
    visit '/login'
    
    fill_in 'Email', with: 'user@example.com'
    fill_in 'Password', with: 'password'
    click_button 'Sign In'
    
    expect(page).to have_content('Dashboard')
  end
end
```

Capybara is much more concise and readable! It abstracts away browser driver details and provides a cleaner DSL. Selenium is lower-level and more verbose.

## Installation

```ruby
# Gemfile
group :test do
  gem 'capybara'
  gem 'selenium-webdriver'  # Browser driver
  # Optional but recommended:
  gem 'webdrivers'  # Automatically manages browser drivers
end
```

```bash
bundle install
```

### Setup for RSpec

```ruby
# spec/spec_helper.rb or spec/rails_helper.rb
require 'capybara/rspec'

RSpec.configure do |config|
  config.include Capybara::DSL
end
```

### Setup for Minitest

```ruby
# test/test_helper.rb
require 'capybara/minitest'

class ActionDispatch::IntegrationTest
  include Capybara::DSL
  include Capybara::Minitest::Assertions
end
```

**Python comparison:** With Selenium, you manually create driver instances. Capybara handles driver management automatically.

## Drivers

Capybara supports multiple drivers:

```ruby
# Default driver (Rack::Test - fast but no JavaScript)
Capybara.default_driver = :rack_test

# Selenium with Chrome (real browser, JavaScript support)
Capybara.default_driver = :selenium_chrome

# Headless Chrome (faster, no GUI)
Capybara.default_driver = :selenium_chrome_headless

# Firefox
Capybara.default_driver = :selenium_firefox
```

Configure in your test helper:
```ruby
# spec/spec_helper.rb
Capybara.configure do |config|
  config.default_driver = :selenium_chrome_headless
  config.app_host = 'http://localhost:3000'
  config.default_max_wait_time = 5  # seconds
end
```

**Python comparison:**
```python
driver = webdriver.Chrome()
# Or headless:
options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)
```

## Basic Navigation

### Visiting Pages

```ruby
visit '/'                    # Visit root path
visit '/users/123'           # Visit specific URL
visit user_path(@user)       # Using Rails path helpers
visit 'https://example.com'  # External URL
```

**Python comparison:**
```python
driver.get("http://localhost:3000/")
driver.get("http://localhost:3000/users/123")
```

### Current Page Info

```ruby
current_path        # => "/users/123"
current_url         # => "http://localhost:3000/users/123"
current_host        # => "localhost"
```

## Interacting with Elements

### Clicking

```ruby
click_link 'About Us'               # Click link by text
click_button 'Submit'               # Click button by text
click_on 'Save'                     # Click link or button

# By CSS/ID
find('#submit-button').click
find('.menu-item').click

# With options
click_link 'Edit', match: :first   # First matching link
```

**Python comparison:**
```python
driver.find_element(By.LINK_TEXT, "About Us").click()
driver.find_element(By.ID, "submit-button").click()
```

### Filling Forms

```ruby
fill_in 'Email', with: 'user@example.com'        # By label
fill_in 'user[email]', with: 'user@example.com'  # By name
fill_in 'email', with: 'user@example.com'        # By ID

# Text areas work the same
fill_in 'Description', with: 'Long text here...'
```

**Python comparison:**
```python
driver.find_element(By.ID, "email").send_keys("user@example.com")
```

### Selecting from Dropdowns

```ruby
select 'Option 1', from: 'Category'           # By visible text
select 'option1', from: 'category_id'         # By value

# Multiple select
select 'Red', from: 'Colors'
select 'Blue', from: 'Colors'  # Also selects Blue
```

**Python comparison:**
```python
from selenium.webdriver.support.ui import Select
dropdown = Select(driver.find_element(By.ID, "category"))
dropdown.select_by_visible_text("Option 1")
```

### Checkboxes and Radio Buttons

```ruby
check 'Accept Terms'              # Check checkbox
uncheck 'Accept Terms'            # Uncheck checkbox
choose 'Male'                     # Select radio button

# By ID
check 'terms_acceptance'
```

**Python comparison:**
```python
driver.find_element(By.ID, "accept_terms").click()
```

### File Uploads

```ruby
attach_file 'Profile Picture', '/path/to/image.jpg'
attach_file 'file_upload', File.absolute_path('test/fixtures/file.pdf')
```

**Python comparison:**
```python
driver.find_element(By.ID, "profile_picture").send_keys("/path/to/image.jpg")
```

## Finding Elements

### CSS Selectors

```ruby
find('#user-123')                    # By ID
find('.user-card')                   # By class
find('div.user-card.active')         # Multiple classes
find('input[type="email"]')          # By attribute
find('ul > li:first-child')          # CSS pseudo-selectors

# Multiple matches
all('.user-card')                    # Returns array
first('.user-card')                  # First match
```

### XPath (More Powerful)

```ruby
find(:xpath, '//div[@id="user-123"]')
find(:xpath, '//a[contains(text(), "Edit")]')
```

**Python comparison:**
```python
driver.find_element(By.CSS_SELECTOR, "#user-123")
driver.find_element(By.XPATH, "//div[@id='user-123']")
driver.find_elements(By.CLASS_NAME, "user-card")  # Multiple
```

### Scoped Finding

```ruby
within '.user-card' do
  click_link 'Edit'
  fill_in 'Name', with: 'New Name'
end

# Finding within element
user_card = find('.user-card')
user_card.find('.edit-button').click
```

## Assertions

### Content Assertions

```ruby
# RSpec syntax
expect(page).to have_content('Welcome')
expect(page).not_to have_content('Error')

# Case sensitive
expect(page).to have_text('Welcome', exact: true)

# Using CSS
expect(page).to have_css('.alert-success')
expect(page).to have_css('.user-card', count: 3)

# Using XPath
expect(page).to have_xpath('//div[@class="alert"]')
```

**Minitest syntax:**
```ruby
assert page.has_content?('Welcome')
refute page.has_content?('Error')
assert page.has_css?('.alert-success')
```

**Python comparison:**
```python
assert "Welcome" in driver.page_source
assert driver.find_element(By.CLASS_NAME, "alert-success")
```

### Element Existence

```ruby
expect(page).to have_selector('#user-123')
expect(page).to have_link('Edit')
expect(page).to have_button('Submit')
expect(page).to have_field('Email')
expect(page).to have_checked_field('Accept Terms')
expect(page).to have_unchecked_field('Newsletter')
```

### URL Assertions

```ruby
expect(current_path).to eq('/users/123')
expect(page).to have_current_path('/dashboard')
expect(page).to have_current_path('/users/\d+', url: true)  # Regex
```

## Waiting and Timing

Capybara automatically waits for elements (HUGE advantage over Selenium!):

```ruby
# Capybara automatically waits up to default_max_wait_time (default: 2s)
click_button 'Load More'
expect(page).to have_content('New Content')  # Waits for content to appear

# Custom wait time
using_wait_time(10) do
  expect(page).to have_content('Slow Loading Content')
end
```

**Python comparison (requires explicit waits):**
```python
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

wait = WebDriverWait(driver, 10)
element = wait.until(EC.presence_of_element_located((By.ID, "slow-element")))
```

Capybara's automatic waiting eliminates most timing issues!

## JavaScript Testing

For JavaScript-heavy apps, use JavaScript-enabled driver:

```ruby
feature 'AJAX interactions', js: true do
  scenario 'loading content dynamically' do
    visit '/dashboard'
    
    click_button 'Load More'
    
    # Capybara waits for AJAX to complete
    expect(page).to have_css('.new-item', count: 10)
  end
end
```

### Executing JavaScript

```ruby
# Execute arbitrary JavaScript
page.execute_script('window.scrollTo(0, document.body.scrollHeight)')
page.execute_script('$(".modal").modal("show")')

# Evaluate JavaScript and return result
result = page.evaluate_script('2 + 2')  # => 4
logged_in = page.evaluate_script('currentUser.isLoggedIn()')
```

**Python comparison:**
```python
driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
result = driver.execute_script("return 2 + 2")
```

## Complete Test Examples

### RSpec Feature Test

```ruby
# spec/features/user_login_spec.rb
require 'rails_helper'

feature 'User authentication' do
  let(:user) { create(:user, email: 'alice@example.com', password: 'password123') }

  scenario 'successful login' do
    visit '/login'
    
    fill_in 'Email', with: 'alice@example.com'
    fill_in 'Password', with: 'password123'
    click_button 'Sign In'
    
    expect(page).to have_content('Welcome back, Alice!')
    expect(current_path).to eq('/dashboard')
  end

  scenario 'failed login with wrong password' do
    visit '/login'
    
    fill_in 'Email', with: user.email
    fill_in 'Password', with: 'wrongpassword'
    click_button 'Sign In'
    
    expect(page).to have_content('Invalid email or password')
    expect(current_path).to eq('/login')
  end

  scenario 'logout' do
    # Login first
    visit '/login'
    fill_in 'Email', with: user.email
    fill_in 'Password', with: 'password123'
    click_button 'Sign In'
    
    # Then logout
    click_link 'Logout'
    
    expect(page).to have_content('Signed out successfully')
    expect(current_path).to eq('/')
  end
end
```

### Minitest System Test

```ruby
# test/system/user_login_test.rb
require 'application_system_test_case'

class UserLoginTest < ApplicationSystemTestCase
  def setup
    @user = create(:user, email: 'alice@example.com')
  end

  test 'successful login' do
    visit login_path
    
    fill_in 'Email', with: @user.email
    fill_in 'Password', with: 'password123'
    click_button 'Sign In'
    
    assert_text 'Welcome back, Alice!'
    assert_equal dashboard_path, current_path
  end

  test 'logout' do
    visit login_path
    fill_in 'Email', with: @user.email
    fill_in 'Password', with: 'password123'
    click_button 'Sign In'
    
    click_link 'Logout'
    
    assert_text 'Signed out successfully'
  end
end
```

## Advanced Patterns

### Testing CRUD Operations

```ruby
feature 'Blog posts' do
  scenario 'creating a new post' do
    visit '/posts/new'
    
    fill_in 'Title', with: 'My First Post'
    fill_in 'Content', with: 'This is the content'
    select 'Technology', from: 'Category'
    check 'Published'
    click_button 'Create Post'
    
    expect(page).to have_content('Post created successfully')
    expect(page).to have_content('My First Post')
  end

  scenario 'editing a post' do
    post = create(:post, title: 'Old Title')
    
    visit edit_post_path(post)
    
    fill_in 'Title', with: 'New Title'
    click_button 'Update Post'
    
    expect(page).to have_content('Post updated successfully')
    expect(page).to have_content('New Title')
  end

  scenario 'deleting a post' do
    post = create(:post)
    
    visit post_path(post)
    click_link 'Delete'
    
    # Handle confirm dialog
    accept_alert 'Are you sure?'
    
    expect(page).to have_content('Post deleted')
    expect(current_path).to eq(posts_path)
  end
end
```

### Testing Modals

```ruby
scenario 'opening and closing modal', js: true do
  visit '/users'
  
  click_button 'New User'
  
  within '.modal' do
    expect(page).to have_content('Create New User')
    fill_in 'Name', with: 'Alice'
    click_button 'Save'
  end
  
  expect(page).not_to have_css('.modal')  # Modal closed
  expect(page).to have_content('Alice')
end
```

### Testing Drag and Drop

```ruby
scenario 'reordering items', js: true do
  visit '/tasks'
  
  task = find('.task', text: 'Task 1')
  target = find('.task', text: 'Task 3')
  
  task.drag_to(target)
  
  expect(find('.task:first-child')).to have_content('Task 3')
end
```

## Best Practices

### 1. Use Page Objects for Maintainability

```ruby
# spec/support/pages/login_page.rb
class LoginPage
  include Capybara::DSL

  def visit_page
    visit '/login'
  end

  def login(email, password)
    fill_in 'Email', with: email
    fill_in 'Password', with: password
    click_button 'Sign In'
  end

  def error_message
    find('.alert-error').text
  end
end

# In tests
scenario 'login' do
  page = LoginPage.new
  page.visit_page
  page.login('alice@example.com', 'password')
  
  expect(page).to have_content('Dashboard')
end
```

### 2. Minimize JavaScript Tests

JavaScript tests are slower. Use `js: true` only when necessary:

```ruby
# GOOD - No JS needed
scenario 'viewing user profile' do
  visit '/users/123'
  expect(page).to have_content('Alice')
end

# ONLY when needed
scenario 'AJAX search', js: true do
  fill_in 'Search', with: 'Ruby'
  expect(page).to have_css('.result', count: 10)
end
```

### 3. Use Scoping

```ruby
# GOOD - Scoped, avoids ambiguity
within '#user-form' do
  fill_in 'Email', with: 'alice@example.com'
  click_button 'Save'
end

# RISKY - Might find wrong element
fill_in 'Email', with: 'alice@example.com'  # Which email field?
```

### 4. Be Specific with Selectors

```ruby
# GOOD - Specific
find('#submit-button').click
click_button 'Create User'

# BAD - Too generic
click_button 'Submit'  # Which submit button?
```

## Debugging

```ruby
# Take screenshot
save_screenshot('debug.png')
save_screenshot('debug.png', full: true)  # Full page

# Print page HTML
puts page.html

# Print current URL
puts current_url

# Open page in browser (for debugging)
save_and_open_page

# Pause test execution
binding.pry  # (with pry gem)
```

## Exercises

1. **User Registration Flow**: Write Capybara tests for:
   - Successful registration
   - Validation errors
   - Email confirmation

2. **Shopping Cart**: Test:
   - Adding items to cart
   - Updating quantities
   - Removing items
   - Checkout process

3. **Search Functionality**: Test:
   - Search with results
   - Search with no results
   - Filter and sort results
   - Pagination

4. **Convert Selenium Test**: Take a Python Selenium test and convert it to Capybara, noting the differences in:
   - Syntax clarity
   - Automatic waiting
   - Element finding

## Summary

Capybara makes integration testing enjoyable. Its clean DSL, automatic waiting, and driver abstraction eliminate the pain points of browser automation. While Python's Selenium is powerful, Capybara is more elegant and productive.

**Key Takeaways:**
- Capybara simulates real user interactions
- Automatic waiting eliminates timing issues
- Cleaner syntax than Selenium
- Use `js: true` for JavaScript testing
- Page objects improve maintainability
- Scoping prevents selector ambiguity

**Next Tutorial:** Code Quality with RuboCop - learn to enforce consistent style and catch common mistakes automatically.
