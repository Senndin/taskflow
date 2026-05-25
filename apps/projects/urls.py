"""URL patterns for the projects app."""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import path
from django.views.generic import TemplateView


class ProjectListPlaceholder(LoginRequiredMixin, TemplateView):
    """Temporary placeholder view — will be replaced in Milestone 1.7."""

    template_name = "projects/list.html"


app_name = "projects"

urlpatterns = [
    path("", ProjectListPlaceholder.as_view(), name="list"),
]
