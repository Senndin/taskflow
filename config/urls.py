"""URL configuration for taskflow project."""

from django.conf import settings
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

if settings.DEBUG:
    try:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
    except ImportError:
        pass
