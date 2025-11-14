# Django Patterns and Best Practices

This file contains Django-specific patterns, anti-patterns, and best practices for code review.

## ORM Best Practices

### N+1 Query Problem

**Problem**:
```python
# INEFFICIENT - N+1 queries
posts = Post.objects.all()  # 1 query
for post in posts:
    print(post.author.name)  # N additional queries!
    print(post.category.name)  # N more queries!
```

**Solution**:
```python
# EFFICIENT - 1 query with JOIN
posts = Post.objects.select_related('author', 'category').all()
for post in posts:
    print(post.author.name)
    print(post.category.name)

# For many-to-many and reverse ForeignKey
posts = Post.objects.prefetch_related('tags', 'comments').all()
```

### QuerySet Evaluation

**Problem**:
```python
# WRONG - Evaluates QuerySet multiple times
posts = Post.objects.filter(published=True)
count = len(posts)  # Evaluates QuerySet
if posts:  # Evaluates again
    first = posts[0]  # Evaluates again
```

**Solution**:
```python
# CORRECT - Use count() for counting
count = Post.objects.filter(published=True).count()

# CORRECT - Use exists() for boolean checks
if Post.objects.filter(published=True).exists():
    pass

# CORRECT - Cache QuerySet if reusing
posts = list(Post.objects.filter(published=True))
count = len(posts)  # Uses cached list
```

### Only/Defer for Large Models

**Problem**:
```python
# INEFFICIENT - Fetches all fields
users = User.objects.all()
for user in users:
    print(user.email)  # Only need email, but fetched everything
```

**Solution**:
```python
# EFFICIENT - Fetch only needed fields
users = User.objects.only('email', 'username')

# Or defer large fields
users = User.objects.defer('bio', 'profile_image')
```

---

## Security Patterns

### SQL Injection Prevention

**Problem**:
```python
# CRITICAL - SQL Injection vulnerability
User.objects.raw(f"SELECT * FROM users WHERE username = '{username}'")

# ALSO WRONG
User.objects.extra(where=[f"status = '{status}'"])
```

**Solution**:
```python
# CORRECT - Parameterized queries
User.objects.raw("SELECT * FROM users WHERE username = %s", [username])

# BETTER - Use ORM
User.objects.filter(username=username)

# For extra(), use params
User.objects.extra(where=["status = %s"], params=[status])
```

### Mass Assignment Vulnerability

**Problem**:
```python
# VULNERABLE - User can set any field
def update_profile(request):
    user = request.user
    for key, value in request.POST.items():
        setattr(user, key, value)  # User could set is_staff=True!
    user.save()
```

**Solution**:
```python
# CORRECT - Whitelist fields
ALLOWED_FIELDS = {'first_name', 'last_name', 'email', 'bio'}

def update_profile(request):
    user = request.user
    for key, value in request.POST.items():
        if key in ALLOWED_FIELDS:
            setattr(user, key, value)
    user.save()

# BETTER - Use forms
from django import forms

class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'bio']

def update_profile(request):
    form = ProfileForm(request.POST, instance=request.user)
    if form.is_valid():
        form.save()
```

### XSS Prevention

**Problem**:
```python
# VULNERABLE - Template
{{ user_input|safe }}  # NEVER use safe with user input!

# VULNERABLE - View
from django.utils.safestring import mark_safe
html = mark_safe(f"<div>{user_input}</div>")  # XSS!
```

**Solution**:
```python
# CORRECT - Django auto-escapes by default
{{ user_input }}  # Automatically escaped

# CORRECT - Explicit escaping
from django.utils.html import escape
safe_input = escape(user_input)

# Only use mark_safe with admin-controlled content
from django.utils.safestring import mark_safe
html = mark_safe(admin_generated_content)
```

### CSRF Protection

**Problem**:
```python
# WRONG - Missing CSRF token in form
<form method="post">
    <input name="email" />
    <button>Submit</button>
</form>

# WRONG - Exempt from CSRF without reason
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def my_view(request):  # Don't do this!
    pass
```

**Solution**:
```python
# CORRECT - Include CSRF token
<form method="post">
    {% csrf_token %}
    <input name="email" />
    <button>Submit</button>
</form>

# For AJAX
<script>
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    fetch('/api/endpoint', {
        method: 'POST',
        headers: {'X-CSRFToken': csrftoken},
        body: data
    });
</script>
```

---

## View Patterns

### Function-Based Views (FBVs)

**Good patterns**:
```python
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

@login_required
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    # Authorization check
    if post.author != request.user and not request.user.is_staff:
        return HttpResponseForbidden()

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post_detail', post_id=post.id)
    else:
        form = CommentForm()

    return render(request, 'post_detail.html', {
        'post': post,
        'form': form
    })
```

### Class-Based Views (CBVs)

**When to use**:
- CRUD operations (CreateView, UpdateView, DeleteView, ListView, DetailView)
- Need to override specific methods
- Want to use mixins for reusable functionality

**Good patterns**:
```python
from django.views.generic import ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

class PostListView(ListView):
    model = Post
    template_name = 'posts/list.html'
    context_object_name = 'posts'
    paginate_by = 20

    def get_queryset(self):
        # Optimize with select_related
        return Post.objects.select_related('author').filter(
            published=True
        ).order_by('-created_at')

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content', 'category']
    template_name = 'posts/create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content', 'category']

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
```

**Anti-patterns**:
```python
# WRONG - Overriding too many methods (use FBV instead)
class MyView(View):
    def get(self, request):
        # Complex custom logic
        pass

    def post(self, request):
        # Complex custom logic
        pass

    def dispatch(self, request):
        # Override
        pass

# Use FBV for complex custom logic
def my_view(request):
    if request.method == 'GET':
        # Custom logic
        pass
    elif request.method == 'POST':
        # Custom logic
        pass
```

---

## Model Patterns

### Model Methods vs Managers

**Good patterns**:
```python
class Post(models.Model):
    title = models.CharField(max_length=200)
    published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    # Instance method - operates on single instance
    def publish(self):
        self.published = True
        self.save(update_fields=['published'])

    # Property - computed value for instance
    @property
    def is_recent(self):
        from django.utils import timezone
        from datetime import timedelta
        return self.created_at >= timezone.now() - timedelta(days=7)

class PostManager(models.Manager):
    # Manager method - operates on queryset
    def published(self):
        return self.filter(published=True)

    def recent(self):
        from django.utils import timezone
        from datetime import timedelta
        cutoff = timezone.now() - timedelta(days=7)
        return self.filter(created_at__gte=cutoff)

class Post(models.Model):
    # ... fields ...
    objects = PostManager()
```

**Usage**:
```python
# Manager methods for filtering
recent_posts = Post.objects.published().recent()

# Instance methods for actions
post.publish()

# Properties for computed values
if post.is_recent:
    pass
```

### Fat Models, Thin Views

**Good pattern**:
```python
# Model - Business logic here
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20)

    def calculate_tax(self):
        return self.total * Decimal('0.08')

    def process_payment(self, payment_method):
        # Payment logic
        if self.status != 'pending':
            raise ValueError("Order already processed")
        # Process payment...
        self.status = 'paid'
        self.save(update_fields=['status'])
        return True

# View - Minimal logic
def checkout(request):
    order = get_object_or_404(Order, id=request.POST['order_id'])
    order.process_payment(request.POST['payment_method'])
    return redirect('order_success')
```

### Using save() Correctly

**Anti-patterns**:
```python
# WRONG - Race condition
post = Post.objects.get(id=1)
post.view_count += 1
post.save()  # Lost updates if concurrent requests!

# WRONG - Saves all fields
post = Post.objects.get(id=1)
post.title = "New Title"
post.save()  # Saves all fields, even unchanged ones
```

**Good patterns**:
```python
# CORRECT - Atomic increment
from django.db.models import F
Post.objects.filter(id=1).update(view_count=F('view_count') + 1)

# CORRECT - Update specific fields
post = Post.objects.get(id=1)
post.title = "New Title"
post.save(update_fields=['title'])

# CORRECT - Use update() for bulk updates
Post.objects.filter(category='tech').update(published=True)
```

---

## Form Patterns

### ModelForm vs Form

**Use ModelForm for model-backed forms**:
```python
from django import forms

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'category']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 10}),
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if 'spam' in title.lower():
            raise forms.ValidationError("Title contains prohibited words")
        return title
```

**Use Form for non-model forms**:
```python
class SearchForm(forms.Form):
    query = forms.CharField(max_length=100)
    category = forms.ChoiceField(choices=CATEGORY_CHOICES, required=False)
    date_from = forms.DateField(required=False)
```

### Form Validation

**Good patterns**:
```python
class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=30)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput)

    # Field-level validation
    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already taken")
        return username

    # Form-level validation (multiple fields)
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Passwords don't match")

        return cleaned_data
```

---

## Middleware Best Practices

**Good pattern**:
```python
class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Code before view
        import time
        start_time = time.time()

        response = self.get_response(request)

        # Code after view
        duration = time.time() - start_time
        logger.info(f"{request.method} {request.path} - {duration:.2f}s")

        return response

    def process_exception(self, request, exception):
        # Handle exceptions
        logger.error(f"Exception: {exception}")
        return None  # Let default exception handling proceed
```

---

## Signals - Use Sparingly

**When to use**:
- Decoupling apps
- Triggering actions from third-party apps

**Anti-pattern**:
```python
# WRONG - Overusing signals
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=Post)
def update_cache(sender, instance, **kwargs):
    cache.set(f'post_{instance.id}', instance)

# WRONG - Circular signal calls
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)  # Triggers more signals!
```

**Good pattern**:
```python
# BETTER - Explicit method call
class Post(models.Model):
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.update_cache()

    def update_cache(self):
        cache.set(f'post_{self.id}', self)

# SIGNALS - Use for decoupling
@receiver(post_save, sender=Order)
def send_order_notification(sender, instance, created, **kwargs):
    if created:
        send_notification.delay(instance.id)  # Celery task
```

---

## Template Best Practices

### Template Inheritance

**Good pattern**:
```django
{# base.html #}
<!DOCTYPE html>
<html>
<head>
    <title>{% block title %}My Site{% endblock %}</title>
    {% block extra_css %}{% endblock %}
</head>
<body>
    <nav>{% include 'navbar.html' %}</nav>
    <main>
        {% block content %}{% endblock %}
    </main>
    <footer>{% include 'footer.html' %}</footer>
    {% block extra_js %}{% endblock %}
</body>
</html>

{# post_detail.html #}
{% extends 'base.html' %}

{% block title %}{{ post.title }} - My Site{% endblock %}

{% block content %}
<article>
    <h1>{{ post.title }}</h1>
    <p>{{ post.content }}</p>
</article>
{% endblock %}
```

### Template Tags vs Context Processors

**Use template tags for**:
- Formatting/transforming data
- Reusable components

**Use context processors for**:
- Global data needed in all templates

```python
# context_processors.py
def site_settings(request):
    return {
        'SITE_NAME': 'My Site',
        'CURRENT_YEAR': datetime.now().year,
    }

# settings.py
TEMPLATES = [{
    'OPTIONS': {
        'context_processors': [
            'myapp.context_processors.site_settings',
        ],
    },
}]
```

---

## Django REST Framework Patterns

### Serializer Best Practices

```python
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    # Read-only computed field
    full_name = serializers.SerializerMethodField()

    # Nested serializer (read-only)
    profile = ProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'full_name', 'profile']
        # Never expose password in serializer!
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True},
        }

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists")
        return value

    def create(self, validated_data):
        # Hash password before saving
        user = User.objects.create_user(**validated_data)
        return user
```

### ViewSet Permissions

```python
from rest_framework import viewsets, permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_queryset(self):
        # Optimize queries
        return Post.objects.select_related('author').prefetch_related('tags')

    def perform_create(self, serializer):
        # Set author automatically
        serializer.save(author=self.request.user)
```

---

## Celery Task Patterns

```python
from celery import shared_task
from django.core.mail import send_mail

@shared_task(bind=True, max_retries=3)
def send_email_task(self, user_id, subject, message):
    try:
        user = User.objects.get(id=user_id)
        send_mail(subject, message, 'from@example.com', [user.email])
    except Exception as exc:
        # Retry with exponential backoff
        raise self.retry(exc=exc, countdown=60 * (2 ** self.request.retries))

# In view
send_email_task.delay(user.id, "Welcome", "Thanks for signing up")
```

---

## Common Django Anti-Patterns to Flag

- [ ] N+1 query problems (missing select_related/prefetch_related)
- [ ] Using len() instead of count() on QuerySets
- [ ] SQL injection in raw() or extra()
- [ ] Mass assignment vulnerabilities
- [ ] Using |safe with user input
- [ ] Missing CSRF tokens in forms
- [ ] Overusing signals
- [ ] Fat views instead of fat models
- [ ] Not using update_fields in save()
- [ ] Using get() without error handling (use get_object_or_404)
- [ ] Exposing sensitive fields in serializers
- [ ] Not optimizing QuerySets in DRF viewsets
- [ ] Circular imports between apps
- [ ] Hardcoded settings instead of using django.conf.settings

## References

- Django Documentation: https://docs.djangoproject.com/
- Django Best Practices: https://django-best-practices.readthedocs.io/
- Two Scoops of Django
- Django ORM Cookbook
