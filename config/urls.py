"""URL configuration for taskflow project."""

from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("projects/", include("apps.projects.urls", namespace="projects")),
    path("tasks/", include("apps.tasks.urls", namespace="tasks")),
    path("", RedirectView.as_view(url="/projects/", permanent=False)),
]
