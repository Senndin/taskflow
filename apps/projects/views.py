from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Prefetch
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from apps.tasks.models import Task

from .forms import ProjectForm
from .models import Project
from .services import create_project, delete_project, update_project


class ProjectListView(LoginRequiredMixin, ListView):
    """Main page — all projects with tasks, zero N+1 queries."""

    template_name = "projects/list.html"
    context_object_name = "projects"

    def get_queryset(self):
        return (
            Project.objects.filter(owner=self.request.user)
            .prefetch_related(
                Prefetch("tasks", queryset=Task.objects.order_by("order"))
            )
            .order_by("-created_at")
        )


class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = "projects/project_form.html"
    success_url = reverse_lazy("projects:list")

    def form_valid(self, form):
        create_project(owner=self.request.user, name=form.cleaned_data["name"])
        from django.http import HttpResponseRedirect

        return HttpResponseRedirect(self.success_url)


class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = "projects/project_form.html"
    success_url = reverse_lazy("projects:list")

    def get_queryset(self):
        return Project.objects.filter(owner=self.request.user)

    def form_valid(self, form):
        update_project(project=self.object, name=form.cleaned_data["name"])
        from django.http import HttpResponseRedirect

        return HttpResponseRedirect(self.success_url)


class ProjectDeleteView(LoginRequiredMixin, DeleteView):
    model = Project
    template_name = "projects/project_confirm_delete.html"
    success_url = reverse_lazy("projects:list")

    def get_queryset(self):
        return Project.objects.filter(owner=self.request.user)

    def form_valid(self, form):
        delete_project(project=self.object)
        from django.http import HttpResponseRedirect

        return HttpResponseRedirect(self.success_url)
