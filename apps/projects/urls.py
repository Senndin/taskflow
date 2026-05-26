"""URL patterns for the projects app."""

from django.urls import path

from . import views

app_name = "projects"

urlpatterns = [
    # Main list
    path("", views.ProjectListView.as_view(), name="list"),
    # HTMX endpoints (return HTML fragments)
    path("htmx/create/", views.ProjectHtmxCreateView.as_view(), name="htmx_create"),
    path(
        "htmx/<int:pk>/edit/", views.ProjectHtmxUpdateView.as_view(), name="htmx_edit"
    ),
    path(
        "htmx/<int:pk>/delete/",
        views.ProjectHtmxDeleteView.as_view(),
        name="htmx_delete",
    ),
    # Classic fallback (full-page, for non-JS environments)
    path("create/", views.ProjectCreateView.as_view(), name="create"),
    path("<int:pk>/edit/", views.ProjectUpdateView.as_view(), name="edit"),
    path("<int:pk>/delete/", views.ProjectDeleteView.as_view(), name="delete"),
]
