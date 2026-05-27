# API Reference

All endpoints require authentication. Unauthenticated requests redirect to `/accounts/login/`.

HTMX endpoints return HTML fragments and are the primary interface for the UI. Classic endpoints (full-page fallback) exist for non-JS environments.

---

## Projects

### List — main page

| | |
|---|---|
| **URL** | `GET /projects/` |
| **Auth** | Required |
| **Returns** | Full HTML page — all user projects with tasks |
| **Template** | `projects/list.html` |

---

### HTMX Create

| | |
|---|---|
| **URL** | `GET /projects/htmx/create/` |
| **Returns** | Inline form fragment |
| **Template** | `projects/partials/project_inline_form.html` |

| | |
|---|---|
| **URL** | `POST /projects/htmx/create/` |
| **Body** | `name` (string, required) |
| **Returns — valid** | New project card fragment |
| **Returns — invalid** | Form with inline errors |
| **Template** | `projects/partials/project_card.html` |

---

### HTMX Edit

| | |
|---|---|
| **URL** | `GET /projects/htmx/<pk>/edit/` |
| **Returns** | Inline edit form for the project |
| **Template** | `projects/partials/project_inline_form.html` |

| | |
|---|---|
| **URL** | `POST /projects/htmx/<pk>/edit/` |
| **Body** | `name` (string, required) |
| **Returns — valid** | Updated project card fragment |
| **Returns — invalid** | Form with inline errors |
| **Template** | `projects/partials/project_card.html` |

---

### HTMX Card (Cancel)

| | |
|---|---|
| **URL** | `GET /projects/htmx/<pk>/card/` |
| **Returns** | Project card fragment — used by the Cancel button to restore the card after entering edit mode |
| **Template** | `projects/partials/project_card.html` |

---

### HTMX Delete

| | |
|---|---|
| **URL** | `POST /projects/htmx/<pk>/delete/` |
| **Returns** | Empty `200` response — HTMX removes the card from the DOM |

---

### Classic Fallback (full-page)

| URL | Method | Action |
|-----|--------|--------|
| `/projects/create/` | GET / POST | Create project, redirect to `/projects/` |
| `/projects/<pk>/edit/` | GET / POST | Edit project, redirect to `/projects/` |
| `/projects/<pk>/delete/` | GET / POST | Delete project, redirect to `/projects/` |

---

## Tasks

All task endpoints are scoped to the authenticated user via `project__owner=request.user`. A wrong `pk` or a `pk` belonging to another user returns `404`.

### Create

| | |
|---|---|
| **URL** | `POST /tasks/<project_pk>/create/` |
| **Body** | `title` (string, required) |
| **Returns — valid** | New `<tr>` row fragment |
| **Returns — invalid** | Error fragment |
| **Template** | `tasks/partials/task_item.html` |

---

### Edit

| | |
|---|---|
| **URL** | `GET /tasks/<pk>/edit/` |
| **Returns** | Inline edit form row |
| **Template** | `tasks/partials/task_edit_form.html` |

| | |
|---|---|
| **URL** | `POST /tasks/<pk>/edit/` |
| **Body** | `title`, `description`, `priority` (1/2/3), `deadline` (YYYY-MM-DD, optional) |
| **Returns — valid** | Updated `<tr>` row |
| **Returns — invalid** | Form with inline errors |
| **Template** | `tasks/partials/task_item.html` |

---

### Delete

| | |
|---|---|
| **URL** | `POST /tasks/<pk>/delete/` |
| **Returns** | Empty `200` response — HTMX removes the row from the DOM |

---

### Toggle Done

| | |
|---|---|
| **URL** | `POST /tasks/<pk>/toggle/` |
| **Returns** | Updated `<tr>` row with flipped checkbox state |
| **Template** | `tasks/partials/task_item.html` |

---

### Move Up / Move Down

| | |
|---|---|
| **URL** | `POST /tasks/<pk>/move-up/` |
| **URL** | `POST /tasks/<pk>/move-down/` |
| **Returns** | Full task list for the project — all rows re-rendered in new order |
| **Template** | `tasks/partials/task_list.html` |

Unified variant:

| | |
|---|---|
| **URL** | `POST /tasks/<pk>/move/<direction>/` |
| **Path param** | `direction`: `up` or `down` |

---

## Auth

Handled by `django-allauth` mounted at `/accounts/`.

| URL | Action |
|-----|--------|
| `/accounts/login/` | Login form |
| `/accounts/signup/` | Registration form |
| `/accounts/logout/` | Logout (POST) |

---

## System Routes

| URL | Behavior |
|-----|---------|
| `/` | Redirects to `/projects/` |
| `/admin/` | Django admin panel (superuser only) |
| `/__debug__/` | django-debug-toolbar (available when `DEBUG=True`) |
