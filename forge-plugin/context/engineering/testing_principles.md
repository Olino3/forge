# Testing Principles

Universal testing strategy guidance for test generation and the `/test` command.

## Test Pyramid

```
        /  E2E  \        Few, slow, expensive
       /----------\
      / Integration \    Moderate count
     /----------------\
    /    Unit Tests     \  Many, fast, cheap
   /--------------------\
```

| Level | Count | Speed | What to Test |
|-------|-------|-------|-------------|
| Unit | Many (70-80%) | Fast (ms) | Individual functions, classes, business logic |
| Integration | Moderate (15-20%) | Medium (s) | Component interactions, API contracts, DB queries |
| E2E | Few (5-10%) | Slow (min) | Critical user flows, smoke tests |

## Coverage Strategy Decision Tree

```
Is it business logic? → YES → Aim for 90%+ coverage
Is it a data transformation? → YES → Aim for 85%+ with edge cases
Is it a CRUD wrapper? → YES → Integration test, 70% unit coverage
Is it UI/presentation? → YES → Component tests, snapshot tests
Is it infrastructure/config? → YES → Integration tests only
```

## Mock vs Integrate Decision

| Mock When | Integrate When |
|-----------|---------------|
| External API (flaky, slow) | Database (if fast, local) |
| Payment processing | File system (simple reads) |
| Email/notification services | In-memory cache |
| Time-dependent logic | Pure function dependencies |
| Third-party SDKs | Internal service interfaces |

## Test Quality Checklist

- [ ] Tests follow AAA pattern (Arrange, Act, Assert)
- [ ] One logical assertion per test (multiple asserts OK if testing one behavior)
- [ ] Tests are independent (no shared mutable state)
- [ ] Test names describe behavior, not implementation
- [ ] Edge cases covered (null, empty, boundary values)
- [ ] Error paths tested (exceptions, validation failures)
- [ ] No test interdependence (order doesn't matter)

## References

- [Martin Fowler - Test Pyramid](https://martinfowler.com/articles/practical-test-pyramid.html)
- [Martin Fowler - Mocks Aren't Stubs](https://martinfowler.com/articles/mocksArentStubs.html)
- [Testing Trophy (Kent C. Dodds)](https://kentcdodds.com/blog/the-testing-trophy-and-testing-classifications)

---

*Last Updated: 2026-02-10*
