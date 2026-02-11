---
id: "python/django_patterns"
domain: python
title: "Django Patterns"
type: framework
estimatedTokens: 950
loadingStrategy: onDemand
version: "1.0.0"
lastUpdated: "2026-02-10"
sections:
  - name: "Common Anti-Patterns"
    estimatedTokens: 126
    keywords: [anti-patterns]
  - name: "Models"
    estimatedTokens: 66
    keywords: [models]
  - name: "Views"
    estimatedTokens: 71
    keywords: [views]
  - name: "Forms"
    estimatedTokens: 60
    keywords: [forms]
  - name: "Security Issues"
    estimatedTokens: 72
    keywords: [security, issues]
  - name: "QuerySet Optimization"
    estimatedTokens: 60
    keywords: [queryset, optimization]
  - name: "Common Detection Patterns"
    estimatedTokens: 79
    keywords: [detection, patterns]
  - name: "Tools"
    estimatedTokens: 20
    keywords: [tools]
  - name: "Official Resources"
    estimatedTokens: 26
    keywords: [official, resources]
tags: [python, django, orm, security, views, forms, queryset]
---

# Django Patterns

Quick reference for Django best practices and common issues. For detailed examples, see [Django documentation](https://docs.djangoproject.com/).

---

## Common Anti-Patterns

| Anti-Pattern | What to Look For | Better Approach | Learn More |
|--------------|------------------|-----------------|------------|
| **N+1 queries** | Loop accessing related objects | Use `select_related()` (ForeignKey) or `prefetch_related()` (ManyToMany) | [QuerySet optimization](https://docs.djangoproject.com/en/stable/topics/db/optimization/) |
| **Using `get()` without exception handling** | `Model.objects.get()` without try/except | Catch `DoesNotExist` or use `get_object_or_404()` | [get() docs](https://docs.djangoproject.com/en/stable/ref/models/querysets/#get) |
| **Unvalidated form data** | Direct `request.POST` access | Use Django forms with `.is_valid()` | [Forms](https://docs.djangoproject.com/en/stable/topics/forms/) |
| **SQL injection risk** | String formatting in `.raw()` or `.extra()` | Use parameterized queries or ORM methods | [SQL injection](https://docs.djangoproject.com/en/stable/topics/security/#sql-injection-protection) |
| **Signals for business logic** | Complex logic in signals | Use model methods or services | [Signals](https://docs.djangoproject.com/en/stable/topics/signals/) |
| **Synchronous code in async views** | Blocking calls in async views | Use `sync_to_async()` wrapper | [Async views](https://docs.djangoproject.com/en/stable/topics/async/) |
| **Not using `F()` for updates** | Load model, modify, save | Use `Model.objects.update(field=F('field') + 1)` | [F() expressions](https://docs.djangoproject.com/en/stable/ref/models/expressions/#f-expressions) |
| **Mutable default in model field** | `JSONField(default={})` | Use callable: `default=dict` | [Field defaults](https://docs.djangoproject.com/en/stable/ref/models/fields/#default) |

---

## Models

| Issue | Detection Pattern | Best Practice |
|-------|-------------------|---------------|
| **Missing `__str__`** | Model without `__str__` method | Add meaningful `__str__` for admin/debugging |
| **Missing indexes** | Frequent queries on unindexed fields | Add `db_index=True` or `indexes` in Meta |
| **Unoptimized queries** | QuerySet inside loop | Use `select_related()`, `prefetch_related()`, `only()`, `defer()` |
| **Large migrations** | Data migration with `.all()` | Use `.iterator()` for large datasets |
| **CharField without max_length** | Missing max_length | Always specify max_length for CharField |

[Model reference](https://docs.djangoproject.com/en/stable/ref/models/)

---

## Views

| Issue | Detection Pattern | Best Practice |
|-------|-------------------|---------------|
| **Function-based views without decorators** | No `@require_http_methods` | Use decorators or switch to CBVs |
| **Missing CSRF protection** | Form without `{% csrf_token %}` | Always include CSRF token in forms |
| **No permission checks** | No `@login_required` or `permission_required` | Add authentication/authorization |
| **Business logic in views** | Complex logic in view functions | Move to model methods or services |
| **Not using CBV mixins** | Repeating code in CBVs | Use LoginRequiredMixin, PermissionRequiredMixin, etc. |

[Views reference](https://docs.djangoproject.com/en/stable/topics/class-based-views/)

---

## Forms

| Issue | Detection Pattern | Best Practice |
|-------|-------------------|---------------|
| **No form validation** | Direct database save without `.is_valid()` | Always validate forms |
| **Using `ModelForm` without `fields` or `exclude`** | Missing Meta.fields | Explicitly list fields or use `'__all__'` |
| **Not cleaning data** | No `clean_<field>` methods | Add custom validation in clean methods |
| **HTML in error messages** | User input in error messages | Escape or use `mark_safe` carefully |

[Forms reference](https://docs.djangoproject.com/en/stable/ref/forms/)

---

## Security Issues

| Issue | Detection Pattern | Recommended Fix |
|-------|-------------------|-----------------|
| **XSS vulnerability** | `|safe` filter on user input | Escape user input, validate/sanitize |
| **CSRF disabled** | `@csrf_exempt` decorator | Remove or use proper CSRF protection |
| **Insecure settings** | `DEBUG = True` in production | Use environment variables |
| **Hardcoded secrets** | Passwords/keys in settings.py | Use environment variables or secrets management |
| **SQL injection** | `.raw()` with f-strings | Use parameterized queries |
| **Mass assignment** | Accepting all POST data | Use forms with explicit fields |

[Security](https://docs.djangoproject.com/en/stable/topics/security/)

---

## QuerySet Optimization

```python
# ❌ N+1 query problem
for book in Book.objects.all():
    print(book.author.name)  # Hits database for each book

# ✅ Use select_related (ForeignKey)
for book in Book.objects.select_related('author'):
    print(book.author.name)  # Single JOIN query

# ❌ N+1 with ManyToMany
for book in Book.objects.all():
    print(book.categories.all())  # Query per book

# ✅ Use prefetch_related (ManyToMany)
for book in Book.objects.prefetch_related('categories'):
    print(book.categories.all())  # Two queries total

# ✅ Use only() to load specific fields
Book.objects.only('title', 'author')

# ✅ Use F() for atomic updates
Entry.objects.update(rating=F('rating') + 1)
```

---

## Common Detection Patterns

```python
# Models
class MyModel(models.Model):
    # ❌ Missing __str__
    # ❌ Missing indexes on frequently queried fields
    name = models.CharField()  # ❌ Missing max_length
    data = models.JSONField(default={})  # ❌ Mutable default

# Views
def my_view(request):
    obj = MyModel.objects.get(pk=1)  # ❌ No exception handling
    # ❌ No permission check
    # ❌ No CSRF check for POST
    MyModel.objects.create(**request.POST)  # ❌ No validation

# Templates
{{ user_input|safe }}  # ❌ XSS risk
<form method="post">  # ❌ Missing {% csrf_token %}

# Queries
for item in Model.objects.all():  # ❌ N+1 query
    print(item.related.name)

# Settings
DEBUG = True  # ❌ In production
SECRET_KEY = 'hardcoded-secret'  # ❌ Hardcoded secret
```

---

## Tools

- **Django Debug Toolbar**: Query profiling - [django-debug-toolbar](https://django-debug-toolbar.readthedocs.io/)
- **django-silk**: Request profiling - [django-silk](https://github.com/jazzband/django-silk)
- **django-extensions**: Development utilities - [django-extensions](https://django-extensions.readthedocs.io/)
- **Bandit**: Security linting - [bandit](https://bandit.readthedocs.io/)

---

## Official Resources

- **Django Documentation**: https://docs.djangoproject.com/
- **Django Best Practices**: https://docs.djangoproject.com/en/stable/misc/design-philosophies/
- **Django Security**: https://docs.djangoproject.com/en/stable/topics/security/
- **QuerySet API**: https://docs.djangoproject.com/en/stable/ref/models/querysets/
- **Two Scoops of Django** (Book): https://www.feldroy.com/books/two-scoops-of-django-3-x

---

**Version**: 1.0.0 (Compacted)
**Last Updated**: 2025-11-14
**Maintained For**: python-code-review skill
