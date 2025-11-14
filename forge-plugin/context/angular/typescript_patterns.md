# TypeScript Best Practices for Angular

TypeScript patterns, type safety, and best practices for Angular development.

---

## Strict Mode {#strict-mode}

**Enable in tsconfig.json**:
```json
{
  "compilerOptions": {
    "strict": true,
    "strictNullChecks": true,
    "strictPropertyInitialization": true,
    "noImplicitAny": true,
    "noImplicitReturns": true
  }
}
```

---

## Type Safety {#type-safety}

### Avoid `any`

**Bad**:
```typescript
data: any;
process(input: any): any {
  return input;
}
```

**Good**:
```typescript
data: User[];
process(input: User): UserResponse {
  return { /* ... */ };
}
```

### Use Interfaces and Types

```typescript
interface User {
  id: number;
  name: string;
  email: string;
  role: 'admin' | 'user'; // Literal types
}

type UserResponse = {
  user: User;
  token: string;
};
```

---

## Utility Types {#utility-types}

### Partial - Make all properties optional

```typescript
function updateUser(id: number, updates: Partial<User>) {
  // updates can have any subset of User properties
}
```

### Pick - Select specific properties

```typescript
type UserPreview = Pick<User, 'id' | 'name'>;
```

### Omit - Exclude properties

```typescript
type UserWithoutId = Omit<User, 'id'>;
```

### Record - Key-value map

```typescript
type UserMap = Record<number, User>;
const users: UserMap = {
  1: { id: 1, name: 'John' },
  2: { id: 2, name: 'Jane' }
};
```

---

## Generics {#generics}

### Generic Functions

```typescript
function toArray<T>(item: T): T[] {
  return [item];
}

const numbers = toArray<number>(1); // number[]
const strings = toArray('hello'); // string[] (inferred)
```

### Generic Interfaces

```typescript
interface ApiResponse<T> {
  data: T;
  status: number;
  message: string;
}

const userResponse: ApiResponse<User> = {
  data: { id: 1, name: 'John' },
  status: 200,
  message: 'Success'
};
```

---

## Type Guards {#type-guards}

```typescript
function isUser(obj: any): obj is User {
  return obj && typeof obj.id === 'number' && typeof obj.name === 'string';
}

if (isUser(data)) {
  // data is now typed as User
  console.log(data.name);
}
```

---

## Const Assertions {#const-assertions}

```typescript
const config = {
  apiUrl: 'https://api.example.com',
  timeout: 5000
} as const;

// config.apiUrl is type 'https://api.example.com', not string
// config is readonly
```

---

## Null Safety {#null-safety}

```typescript
// Non-null assertion (use sparingly)
const element = document.getElementById('my-id')!;

// Optional chaining
const city = user?.address?.city;

// Nullish coalescing
const name = user?.name ?? 'Unknown';
```

---

**Version**: 1.0.0
