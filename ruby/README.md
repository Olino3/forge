# Ruby Development Learning Path

A comprehensive, progressive learning path for mastering professional Ruby development, designed specifically for intermediate and advanced Python engineers.

## Overview

This learning path consists of **12 progressive tutorials** and **6 hands-on labs** covering everything from testing frameworks to security best practices. Each tutorial includes Python comparisons to leverage your existing knowledge.

## Structure

```
ruby/
├── tutorials/development/     # 12 comprehensive tutorials
└── README.md                  # This file

../labs/development/           # 6 hands-on lab projects
```

## 📚 Tutorials (In Order)

### Part 1: Testing - The Ruby Heartbeat (Tutorials 1-4)

#### [Tutorial 1: Testing with RSpec](tutorials/development/01_testing_with_rspec.md)
**Duration:** 60-90 min  
**Topics:** RSpec DSL, expectations, hooks, TDD workflow  
**Python Comparison:** pytest vs RSpec

Learn the industry-standard testing framework. RSpec's behavior-driven DSL makes tests self-documenting and expressive.

#### [Tutorial 2: Testing with Minitest](tutorials/development/02_testing_with_minitest.md)
**Duration:** 45-60 min  
**Topics:** Built-in testing, assertions, benchmarking  
**Python Comparison:** unittest (very similar!)

Explore Ruby's built-in testing framework. If you know Python's unittest, Minitest will feel familiar.

#### [Tutorial 3: Test Data with FactoryBot](tutorials/development/03_test_data_with_factorybot.md)
**Duration:** 60 min  
**Topics:** Factories, sequences, traits, associations  
**Python Comparison:** factory_boy (nearly identical API)

Master dynamic test data generation. FactoryBot (and Python's factory_boy) eliminate fixture maintenance nightmares.

#### [Tutorial 4: Integration Testing with Capybara](tutorials/development/04_integration_testing_capybara.md)
**Duration:** 90 min  
**Topics:** Browser automation, web testing, JavaScript testing  
**Python Comparison:** Selenium (but much cleaner API)

Test complete user workflows. Capybara's DSL is far more elegant than raw Selenium.

### Part 2: Code Quality - Consistency and Style (Tutorials 5-6)

#### [Tutorial 5: Code Quality with RuboCop](tutorials/development/05_code_quality_rubocop.md)
**Duration:** 60 min  
**Topics:** Linting, auto-correction, configuration  
**Python Comparison:** flake8 + black + isort (all in one!)

RuboCop combines linting and formatting in one powerful tool. Auto-fix most issues with a single command.

#### [Tutorial 6: StandardRB and Style Guides](tutorials/development/06_standardrb_style_guide.md)
**Duration:** 30-45 min  
**Topics:** Zero-config linting, Ruby Style Guide  
**Python Comparison:** Black (opinionated, no config)

Stop bikeshedding over style. StandardRB enforces one style, no configuration needed.

### Part 3: Architectural Patterns (Tutorials 7-8)

#### [Tutorial 7: Service Objects Pattern](tutorials/development/07_service_objects_pattern.md)
**Duration:** 60-90 min  
**Topics:** Business logic organization, SOLID principles  
**Python Comparison:** Same pattern, universal concept

Keep controllers thin and models focused. Service Objects are essential for professional applications.

#### [Tutorial 8: Decorator/Presenter Pattern](tutorials/development/08_decorator_presenter_pattern.md)
**Duration:** 60 min  
**Topics:** Presentation logic, view helpers, Draper gem  
**Python Comparison:** Presenter pattern (universal)

Keep view logic out of models and templates. Decorators make code cleaner and more testable.

### Part 4: Essential Tools and Practices (Tutorials 9-12)

#### [Tutorial 9: Essential Gems](tutorials/development/09_essential_gems.md)
**Duration:** 90-120 min  
**Topics:** Bundler, Pry, Sidekiq, Bullet  
**Python Comparison:** pip, ipdb, Celery, django-silk

Master the four tools every professional Rubyist needs: dependency management, debugging, background jobs, and performance monitoring.

#### [Tutorial 10: Enumerable Mastery](tutorials/development/10_enumerable_mastery.md)
**Duration:** 60-90 min  
**Topics:** map, select, reduce, lazy evaluation, algorithms  
**Python Comparison:** List comprehensions, functional tools

Write idiomatic Ruby. Professional Rubyists rarely use `for` loops—master Enumerable instead.

#### [Tutorial 11: SOLID Principles in Ruby](tutorials/development/11_solid_principles.md)
**Duration:** 90 min  
**Topics:** SRP, OCP, LSP, ISP, DIP  
**Python Comparison:** Language-agnostic principles

Design maintainable, flexible software. SOLID principles apply to all OOP languages, with Ruby-specific implementations.

#### [Tutorial 12: Secrets Management and Security](tutorials/development/12_secrets_security.md)
**Duration:** 90-120 min  
**Topics:** Environment variables, Rails credentials, password hashing, security vulnerabilities  
**Python Comparison:** dotenv, django-environ

Handle secrets securely and prevent common vulnerabilities. Security is not optional.

## 🧪 Hands-On Labs

Located in `/labs/development/`, each lab is a complete mini-application with Docker environment.

### [Lab 1: RSpec Testing - Mini Blog](../labs/development/lab01_rspec_blog/)
**Duration:** 3-4 hours  
**Prerequisites:** Tutorials 1, 3  
Build a blog using TDD with RSpec and FactoryBot.

### [Lab 2: Minitest - Task Manager](../labs/development/lab02_minitest_tasks/)
**Duration:** 2-3 hours  
**Prerequisites:** Tutorial 2  
Build a task manager with Minitest, compare with RSpec.

### [Lab 3: Background Jobs with Sidekiq](../labs/development/lab03_sidekiq_jobs/)
**Duration:** 3-4 hours  
**Prerequisites:** Tutorial 9  
Implement asynchronous job processing.

### Lab 4: Service Objects Refactoring
**Duration:** 2-3 hours  
**Prerequisites:** Tutorial 7  
Refactor a messy app with Service Objects.

### Lab 5: Code Quality Tools
**Duration:** 2 hours  
**Prerequisites:** Tutorials 5, 6  
Set up RuboCop/StandardRB, integrate with CI.

### Lab 6: Security Best Practices
**Duration:** 3-4 hours  
**Prerequisites:** Tutorial 12  
Find and fix security vulnerabilities.

See [Labs README](../labs/development/README.md) for detailed setup and instructions.

## 🎯 Learning Paths

### Beginner Path (New to Ruby)
1. **Tutorials 1-2** (Testing basics)
2. **Lab 1** (Practice RSpec)
3. **Tutorials 5-6** (Code quality)
4. **Tutorial 9** (Essential tools)

### Intermediate Path (Some Ruby experience)
1. **Tutorial 3-4** (Advanced testing)
2. **Tutorials 7-8** (Design patterns)
3. **Labs 3-4** (Real-world patterns)
4. **Tutorial 11** (SOLID)

### Advanced Path (Experienced developer)
1. **Tutorial 10** (Ruby idioms)
2. **Tutorial 11** (SOLID principles)
3. **Tutorial 12** (Security)
4. **Lab 6** (Security practice)

### Complete Path (Comprehensive mastery)
Complete all tutorials 1-12 in order, then do all labs 1-6.

**Estimated Time:** 25-30 hours total

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone <repository-url>
cd ruby/tutorials/development
```

### 2. Start with Tutorial 1
```bash
cat 01_testing_with_rspec.md
# Or open in your favorite markdown viewer
```

### 3. Do the Exercises
Each tutorial includes exercises to reinforce concepts.

### 4. Complete Labs
After finishing relevant tutorials, complete the corresponding labs:
```bash
cd ../../../labs/development/lab01_rspec_blog
docker-compose up -d
```

## 📖 How to Use These Tutorials

### Format
Each tutorial includes:
- **Overview:** What you'll learn
- **Python Comparison:** Leveraging your Python knowledge
- **Code Examples:** Ruby vs Python side-by-side
- **Best Practices:** Professional patterns
- **Exercises:** Hands-on practice
- **Summary:** Key takeaways

### Study Tips
1. **Read Actively:** Try examples in IRB or Pry
2. **Compare to Python:** Note similarities and differences
3. **Do Exercises:** Essential for retention
4. **Complete Labs:** Apply knowledge to real projects
5. **Take Notes:** Especially on patterns new to you

### Time Investment
- **Tutorials:** ~20 hours total (1-2 hours each)
- **Labs:** ~15 hours total (2-4 hours each)
- **Practice:** Additional time as needed

## 🐍 For Python Engineers

These tutorials are specifically designed for Python developers:

### Similarities You'll Recognize
- Testing frameworks (pytest ↔ RSpec, unittest ↔ Minitest)
- Dependency management (pip ↔ Bundler)
- Debugging tools (ipdb ↔ Pry)
- Background jobs (Celery ↔ Sidekiq)
- Design patterns (Service Objects, Decorators)
- Security practices (universal concepts)

### Key Differences to Note
- Ruby uses 2-space indentation (vs Python's 4)
- Blocks and procs (different from Python lambdas)
- Symbols (`:symbol`) - immutable strings
- Duck typing is more pervasive
- More emphasis on DSLs
- Everything is an object (true OOP)

### Why Ruby?
- **Rails:** Dominant web framework
- **Community:** Strong testing culture
- **Expressiveness:** "Programmer happiness"
- **Metaprogramming:** Powerful when needed
- **Jobs:** High demand, good pay

## 🔗 Additional Resources

### Official Documentation
- [Ruby Docs](https://ruby-doc.org/)
- [Rails Guides](https://guides.rubyonrails.org/)
- [Ruby Style Guide](https://rubystyle.guide/)

### Community
- [Ruby Reddit](https://www.reddit.com/r/ruby/)
- [Ruby Discord](https://discord.gg/ruby)
- [Ruby Weekly Newsletter](https://rubyweekly.com/)

### Books
- *Eloquent Ruby* by Russ Olsen
- *Practical Object-Oriented Design in Ruby* by Sandi Metz
- *The RSpec Book* by David Chelimsky

### Practice
- [Exercism Ruby Track](https://exercism.org/tracks/ruby)
- [Ruby Koans](http://rubykoans.com/)
- [CodeWars Ruby](https://www.codewars.com/)

## ✅ Success Criteria

You've mastered professional Ruby development when you can:

- [ ] Write comprehensive RSpec tests following TDD
- [ ] Choose between RSpec and Minitest appropriately
- [ ] Use FactoryBot effectively for test data
- [ ] Write integration tests with Capybara
- [ ] Configure and use RuboCop/StandardRB
- [ ] Extract business logic into Service Objects
- [ ] Implement Decorator/Presenter patterns
- [ ] Manage dependencies with Bundler
- [ ] Debug with Pry
- [ ] Process background jobs with Sidekiq
- [ ] Write idiomatic Ruby with Enumerable
- [ ] Apply SOLID principles to Ruby code
- [ ] Handle secrets and security properly
- [ ] Complete all 6 labs successfully

## 🎓 What's Next?

After completing this learning path:

1. **Build Projects:** Create your own Ruby/Rails applications
2. **Contribute:** Find Ruby OSS projects to contribute to
3. **Specialize:** Dive deeper into Rails, Sinatra, or Ruby gems
4. **Advanced Topics:** 
   - Metaprogramming
   - Performance optimization
   - Concurrency (Threads, Fibers, Ractors)
   - Building gems

## 📝 Feedback

Found an issue? Have suggestions?
- Open an issue in the repository
- Submit a pull request
- Share your experience

## 📄 License

Part of the Forge project. See main repository LICENSE.

---

**Ready to become a professional Rubyist? Start with [Tutorial 1: Testing with RSpec](tutorials/development/01_testing_with_rspec.md)!**

Happy learning! 💎🚀
