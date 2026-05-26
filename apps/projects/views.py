from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Prefetch
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views import View
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


# ---------------------------------------------------------------------------
# HTMX views — return HTML fragments, no full page reloads
# ---------------------------------------------------------------------------


class ProjectHtmxCreateView(LoginRequiredMixin, View):
    """GET: return inline form card; POST: create project and return project_card.html."""

    def get(self, request):
        form = ProjectForm()
        return render(
            request, "projects/partials/project_inline_form.html", {"form": form}
        )

    def post(self, request):
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = create_project(owner=request.user, name=form.cleaned_data["name"])
            # Prefetch tasks (empty for new project) for template compatibility
            project.tasks_list = []
            return render(
                request, "projects/partials/project_card.html", {"project": project}
            )
        return render(
            request,
            "projects/partials/project_inline_form.html",
            {"form": form},
        )


class ProjectHtmxUpdateView(LoginRequiredMixin, View):
    """GET: return inline edit form; POST: save and return updated project_card.html."""

    def _get_project(self, request, pk):
        return get_object_or_404(Project, pk=pk, owner=request.user)

    def get(self, request, pk):
        project = self._get_project(request, pk)
        form = ProjectForm(instance=project)
        return render(
            request,
            "projects/partials/project_inline_form.html",
            {"form": form, "object": project},
        )

    def post(self, request, pk):
        project = self._get_project(request, pk)
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            updated = update_project(project=project, name=form.cleaned_data["name"])
            tasks = updated.tasks.order_by("order")
            return render(
                request,
                "projects/partials/project_card.html",
                {"project": updated, "tasks": tasks},
            )
        return render(
            request,
            "projects/partials/project_inline_form.html",
            {"form": form, "object": project},
        )


class ProjectHtmxDeleteView(LoginRequiredMixin, View):
    """POST: delete project, return empty response (HTMX removes the card)."""

    def post(self, request, pk):
        project = get_object_or_404(Project, pk=pk, owner=request.user)
        delete_project(project)
        return HttpResponse("")


# ---------------------------------------------------------------------------
# Classic full-page fallback views (kept for non-JS environments)
# ---------------------------------------------------------------------------


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
