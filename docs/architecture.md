# Architecture

## Overview

TaskFlow is a single-page task manager built with Django 5.2. All projects and their tasks render together on one page (`/projects/`). Every mutation — create, edit, delete, reorder — is handled by HTMX without a full-page reload; Alpine.js drives hover-controlled task controls.

## Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Backend | Python 3.13, Django 5.2 | Request handling, ORM, business logic |
| Auth | django-allauth 0.63 | Registration, login, logout |
| Frontend | Bootstrap 5, HTMX, Alpine.js | Layout, partial updates, hover effects |
| Database | PostgreSQL 16 | Primary data store |
| Static files | WhiteNoise | Serves compressed static assets in production |
| Container | Docker + docker-compose | Isolated dev and production environments |
| WSGI server | Gunicorn | Production HTTP server |
| Linting | Ruff | Code style enforcement |

## App Structure

```
apps/
├── core/       # Base templates (base.html, 404.html, 500.html)
├── projects/   # Project model, views, services, forms
└── tasks/      # Task model, views, services, forms
```

Each app follows the same internal layout:

| File | Responsibility |
|------|---------------|
| `models.py` | Fields and `__str__` — no business logic |
| `services.py` | All write operations — the only place that mutates the DB |
| `views.py` | Thin HTTP handlers: validate → call service → render partial |
| `forms.py` | Input validation and cleaning |
| `urls.py` | URL routing |

## Key Design Decisions

### Service Layer

Business logic lives in `services.py`, not in views or models. Views are pure HTTP adapters: parse the request, call a service function, return a rendered template fragment. This keeps views small and each layer independently testable.

```python
# tasks/services.py
@transaction.atomic
def move_task_up(task: Task) -> None:
    predecessor = (
        Task.objects.filter(project=task.project, order__lt=task.order)
        .order_by("-order")
        .first()
    )
    if predecessor is None:
        return
    task.order, predecessor.order = predecessor.order, task.order
    Task.objects.bulk_update([task, predecessor], ["order"])
```

### HTMX Partial Template Pattern

Every mutating view returns a small HTML fragment, not a full page. HTMX swaps that fragment into the DOM. The view decides which partial to render based on the outcome:

- **Success** → return the updated element (e.g., `task_item.html`)
- **Validation error** → return the form with inline errors (same partial, HTTP 400)
- **Delete** → return an empty `HttpResponse("")` — HTMX removes the element via `hx-swap="outerHTML"`

### Zero N+1 Queries

`ProjectListView` loads all data for the main page in exactly two SQL queries — one for projects, one prefetch for tasks — regardless of how many projects the user has:

```python
def get_queryset(self):
    return (
        Project.objects.filter(owner=self.request.user)
        .prefetch_related(
            Prefetch("tasks", queryset=Task.objects.order_by("order"))
        )
        .order_by("-created_at")
    )
```

### Security Model

Every view applies `LoginRequiredMixin`. Every queryset filters by `owner=request.user` or `project__owner=request.user` — one user can never read or mutate another user's data. Object-level lookups use `get_object_or_404` with the owner filter, so a wrong `pk` returns 404.

## Frontend

Three libraries work together on the client without conflict:

| Library | Role |
|---------|------|
| Bootstrap 5 | Layout, typography, form styles (loaded via CDN) |
| HTMX | Sends AJAX requests on user actions, swaps HTML fragments in the DOM |
| Alpine.js | Controls per-row hover state (`x-data="{ hovered: false }"`) |

Alpine manages CSS classes and visibility (`x-show`, `:class`). HTMX manages network requests. They share no state and do not interfere with each other.

Task controls (↑ ↓ ✏ 🗑) are hidden by default and appear only on hover:

```html
<tr x-data="{ hovered: false }"
    @mouseenter="hovered = true"
    @mouseleave="hovered = false"
    :class="{ 'table-warning': hovered }">
  ...
  <td x-show="hovered"><!-- controls --></td>
</tr>
```

## Settings Split

| Module | Environment | Notes |
|--------|-------------|-------|
| `config/settings/base.py` | Shared | Installed apps, auth, static, allauth config |
| `config/settings/local.py` | Development | `DEBUG=True`, SQLite fallback, debug toolbar |
| `config/settings/production.py` | Production | `DEBUG=False`, PostgreSQL via `DATABASE_URL`, HSTS, SSL |

`DJANGO_SETTINGS_MODULE` defaults to `config.settings.local` via `manage.py`.
