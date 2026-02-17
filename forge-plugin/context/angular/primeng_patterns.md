---
id: "angular/primeng_patterns"
domain: angular
title: "PrimeNG Component Patterns"
type: framework
estimatedTokens: 300
loadingStrategy: onDemand
version: "0.3.0-alpha"
lastUpdated: "2026-02-10"
sections:
  - name: "Table Component"
    estimatedTokens: 69
    keywords: [table, component, table]
  - name: "Forms"
    estimatedTokens: 42
    keywords: [forms, forms]
  - name: "Dialog"
    estimatedTokens: 28
    keywords: [dialog, dialog]
  - name: "Accessibility"
    estimatedTokens: 14
    keywords: [accessibility, accessibility]

tags: [angular, primeng, table, forms, dialog, accessibility]
---
# PrimeNG Component Patterns

Best practices for using PrimeNG components in Angular applications.

---

## Table Component {#table}

### Basic Table

```typescript
@Component({
  template: `
    <p-table [value]="products" [loading]="loading">
      <ng-template pTemplate="header">
        <tr>
          <th>Name</th>
          <th>Price</th>
          <th>Actions</th>
        </tr>
      </ng-template>
      <ng-template pTemplate="body" let-product>
        <tr>
          <td>{{ product.name }}</td>
          <td>{{ product.price | currency }}</td>
          <td>
            <button pButton (click)="edit(product)">Edit</button>
          </td>
        </tr>
      </ng-template>
    </p-table>
  `
})
```

### Virtual Scrolling

```html
<p-table
  [value]="products"
  [scrollable]="true"
  scrollHeight="400px"
  [virtualScroll]="true"
  [virtualScrollItemSize]="50">
</p-table>
```

### Lazy Loading

```typescript
loadData(event: LazyLoadEvent) {
  this.loading = true;
  this.productService.getProducts({
    first: event.first,
    rows: event.rows,
    sortField: event.sortField,
    sortOrder: event.sortOrder
  }).subscribe(data => {
    this.products = data;
    this.loading = false;
  });
}
```

```html
<p-table
  [value]="products"
  [lazy]="true"
  (onLazyLoad)="loadData($event)"
  [totalRecords]="totalRecords">
</p-table>
```

---

## Forms {#forms}

### Reactive Forms with PrimeNG

```typescript
form = this.fb.group({
  name: ['', Validators.required],
  email: ['', [Validators.required, Validators.email]],
  role: ['']
});
```

```html
<form [formGroup]="form">
  <div class="p-field">
    <label for="name">Name</label>
    <input pInputText id="name" formControlName="name" />
  </div>

  <div class="p-field">
    <label for="email">Email</label>
    <input pInputText id="email" formControlName="email" />
  </div>

  <div class="p-field">
    <label for="role">Role</label>
    <p-dropdown
      [options]="roles"
      formControlName="role"
      optionLabel="name"
      optionValue="code">
    </p-dropdown>
  </div>
</form>
```

---

## Dialog {#dialog}

```typescript
display = false;

showDialog() {
  this.display = true;
}
```

```html
<p-dialog
  [(visible)]="display"
  [modal]="true"
  [style]="{width: '50vw'}">
  <ng-template pTemplate="header">
    Dialog Title
  </ng-template>
  <p>Dialog content</p>
  <ng-template pTemplate="footer">
    <button pButton label="Cancel" (click)="display=false"></button>
    <button pButton label="Save" (click)="save()"></button>
  </ng-template>
</p-dialog>
```

---

## Accessibility {#accessibility}

Always provide ARIA labels:

```html
<button
  pButton
  icon="pi pi-check"
  aria-label="Save">
</button>

<p-table ariaLabel="Product List">
</p-table>
```

---

**Version**: 0.3.0-alpha
