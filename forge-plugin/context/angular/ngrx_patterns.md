# NgRx State Management Patterns

Best practices for NgRx (and Akita) state management in Angular applications.

---

## NgRx Core Concepts {#core}

### Actions

**Action Best Practices**:
```typescript
import { createAction, props } from '@ngrx/store';

// Good naming: [Source] Event
export const loadUsers = createAction('[User List] Load Users');
export const loadUsersSuccess = createAction(
  '[User API] Load Users Success',
  props<{ users: User[] }>()
);
export const loadUsersFailure = createAction(
  '[User API] Load Users Failure',
  props<{ error: string }>()
);
```

### Reducers (MUST BE PURE)

**Bad - Mutation**:
```typescript
case loadUsersSuccess:
  state.users.push(...action.users); // WRONG - mutates state!
  return state;
```

**Good - Immutable**:
```typescript
import { createReducer, on } from '@ngrx/store';

export const userReducer = createReducer(
  initialState,
  on(loadUsersSuccess, (state, { users }) => ({
    ...state,
    users: [...users],
    loading: false
  })),
  on(loadUsersFailure, (state, { error }) => ({
    ...state,
    error,
    loading: false
  }))
);
```

### Effects

```typescript
import { Injectable } from '@angular/core';
import { Actions, createEffect, ofType } from '@ngrx/effects';
import { catchError, map, switchMap } from 'rxjs/operators';
import { of } from 'rxjs';

@Injectable()
export class UserEffects {
  loadUsers$ = createEffect(() =>
    this.actions$.pipe(
      ofType(loadUsers),
      switchMap(() =>
        this.userService.getUsers().pipe(
          map(users => loadUsersSuccess({ users })),
          catchError(error => of(loadUsersFailure({ error: error.message })))
        )
      )
    )
  );

  constructor(
    private actions$: Actions,
    private userService: UserService
  ) {}
}
```

### Selectors

```typescript
import { createSelector, createFeatureSelector } from '@ngrx/store';

export const selectUserState = createFeatureSelector<UserState>('users');

export const selectAllUsers = createSelector(
  selectUserState,
  state => state.users
);

export const selectUserById = (id: number) => createSelector(
  selectAllUsers,
  users => users.find(user => user.id === id)
);

export const selectLoadingState = createSelector(
  selectUserState,
  state => ({ loading: state.loading, error: state.error })
);
```

---

## Facade Pattern {#facade}

```typescript
@Injectable({ providedIn: 'root' })
export class UserFacade {
  users$ = this.store.select(selectAllUsers);
  loading$ = this.store.select(selectLoadingState);

  constructor(private store: Store) {}

  loadUsers() {
    this.store.dispatch(loadUsers());
  }

  selectUser(id: number) {
    return this.store.select(selectUserById(id));
  }
}

// Component uses facade instead of store directly
export class UserListComponent {
  users$ = this.userFacade.users$;

  constructor(private userFacade: UserFacade) {}

  ngOnInit() {
    this.userFacade.loadUsers();
  }
}
```

---

## Entity Adapter {#entity}

```typescript
import { EntityState, EntityAdapter, createEntityAdapter } from '@ngrx/entity';

export interface UserState extends EntityState<User> {
  loading: boolean;
  error: string | null;
}

export const userAdapter: EntityAdapter<User> = createEntityAdapter<User>();

export const initialState: UserState = userAdapter.getInitialState({
  loading: false,
  error: null
});

export const userReducer = createReducer(
  initialState,
  on(loadUsersSuccess, (state, { users }) =>
    userAdapter.setAll(users, { ...state, loading: false })
  ),
  on(addUserSuccess, (state, { user }) =>
    userAdapter.addOne(user, state)
  ),
  on(updateUserSuccess, (state, { user }) =>
    userAdapter.updateOne({ id: user.id, changes: user }, state)
  ),
  on(deleteUserSuccess, (state, { id }) =>
    userAdapter.removeOne(id, state)
  )
);

// Selectors
const { selectAll, selectEntities, selectIds } = userAdapter.getSelectors();
export const selectAllUsers = selectAll;
export const selectUserEntities = selectEntities;
```

---

**Version**: 1.0.0
