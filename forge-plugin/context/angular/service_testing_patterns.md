---
id: "angular/service_testing_patterns"
domain: angular
title: "Angular Service Testing Patterns"
type: pattern
estimatedTokens: 500
loadingStrategy: onDemand
version: "0.3.0-alpha"
lastUpdated: "2026-02-10"
sections:
  - name: "Quick Reference"
    estimatedTokens: 72
    keywords: [quick, reference]
  - name: "HTTP Testing"
    estimatedTokens: 42
    keywords: [http, testing]
  - name: "Observable Testing"
    estimatedTokens: 37
    keywords: [observable, testing]
  - name: "Error Handling"
    estimatedTokens: 26
    keywords: [error, handling]
  - name: "Service Dependencies"
    estimatedTokens: 60
    keywords: [service, dependencies]
  - name: "Official Documentation"
    estimatedTokens: 20
    keywords: [official, documentation]
  - name: "Related Context Files"
    estimatedTokens: 16
    keywords: [related, context, files]
tags: [angular, testing, services, http-testing, mocking, observables]
---

# Angular Service Testing Patterns

## Quick Reference

### Basic Service Test (Jest)

```typescript
describe('MyService', () => {
  let service: MyService;
  let httpClient: jest.Mocked<HttpClient>;

  beforeEach(() => {
    httpClient = {
      get: jest.fn(),
      post: jest.fn(),
      put: jest.fn(),
      delete: jest.fn()
    } as any;

    TestBed.configureTestingModule({
      providers: [
        MyService,
        { provide: HttpClient, useValue: httpClient }
      ]
    });

    service = TestBed.inject(MyService);
  });
});
```

### Basic Service Test (Jasmine)

```typescript
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';

describe('MyService', () => {
  let service: MyService;
  let httpMock: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [MyService]
    });

    service = TestBed.inject(MyService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify();
  });
});
```

## HTTP Testing

### Jest Mocking

```typescript
it('should_fetch_data', (done) => {
  const mockData = [{ id: 1, name: 'Test' }];
  httpClient.get.mockReturnValue(of(mockData));

  service.getData().subscribe(data => {
    expect(data).toEqual(mockData);
    expect(httpClient.get).toHaveBeenCalledWith('/api/data');
    done();
  });
});
```

### Jasmine HttpTestingController

```typescript
it('should_fetch_data', () => {
  const mockData = [{ id: 1, name: 'Test' }];

  service.getData().subscribe(data => {
    expect(data).toEqual(mockData);
  });

  const req = httpMock.expectOne('/api/data');
  expect(req.request.method).toBe('GET');
  req.flush(mockData);
});
```

## Observable Testing

```typescript
// Using done callback
it('should_emit_value', (done) => {
  service.data$.subscribe(value => {
    expect(value).toBe('test');
    done();
  });
});

// Using firstValueFrom (modern)
it('should_emit_value', async () => {
  const value = await firstValueFrom(service.data$);
  expect(value).toBe('test');
});

// Testing BehaviorSubject
it('should_update_state', () => {
  service.setState({ value: 'new' });

  service.state$.subscribe(state => {
    expect(state.value).toBe('new');
  });
});
```

## Error Handling

```typescript
it('should_handle_404_error', (done) => {
  const error = { status: 404, message: 'Not Found' };
  httpClient.get.mockReturnValue(throwError(() => error));

  service.getData().subscribe({
    next: () => fail('should have failed'),
    error: (err) => {
      expect(err.status).toBe(404);
      done();
    }
  });
});
```

## Service Dependencies

```typescript
describe('OrderService (with dependencies)', () => {
  let service: OrderService;
  let mockUserService: jest.Mocked<UserService>;
  let mockCartService: jest.Mocked<CartService>;

  beforeEach(() => {
    mockUserService = { getCurrentUser: jest.fn() } as any;
    mockCartService = { getCart: jest.fn(), clearCart: jest.fn() } as any;

    TestBed.configureTestingModule({
      providers: [
        OrderService,
        { provide: UserService, useValue: mockUserService },
        { provide: CartService, useValue: mockCartService }
      ]
    });

    service = TestBed.inject(OrderService);
  });

  it('should_create_order_with_user_data', (done) => {
    mockUserService.getCurrentUser.mockReturnValue(of({ id: '1' }));
    mockCartService.getCart.mockReturnValue(of({ items: [] }));

    service.createOrder().subscribe(order => {
      expect(order.userId).toBe('1');
      done();
    });
  });
});
```

## Official Documentation

- [Angular Service Testing](https://angular.io/guide/testing-services)
- [HttpClient Testing](https://angular.io/guide/http-test-requests)
- [RxJS Testing](https://rxjs.dev/guide/testing)

## Related Context Files

- `jest_testing_standards.md` - Core principles
- `component_testing_patterns.md` - Component mocking
- `testing_utilities.md` - Mocking utilities
- `rxjs_patterns.md` - RxJS operators and patterns
