"""Views for HTMX-powered task CRUD."""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views import View

from apps.projects.models import Project

from .forms import TaskForm, TaskQuickCreateForm
from .models import Task
from .services import (
    create_task,
    delete_task,
    move_task_down,
    move_task_up,
    toggle_done,
    update_task,
)


class TaskCreateView(LoginRequiredMixin, View):
    """POST: create task, return a single <tr> fragment."""

    def post(self, request, project_pk: int):
        project = get_object_or_404(Project, pk=project_pk, owner=request.user)
        form = TaskQuickCreateForm(request.POST)
        if form.is_valid():
            task = create_task(project=project, title=form.cleaned_data["title"])
            return render(request, "tasks/partials/task_item.html", {"task": task})
        return HttpResponse(status=422)


class TaskUpdateView(LoginRequiredMixin, View):
    """GET: return inline edit form row; POST: save and return updated <tr>."""

    def _get_task(self, request, pk: int) -> Task:
        return get_object_or_404(Task, pk=pk, project__owner=request.user)

    def get(self, request, pk: int):
        task = self._get_task(request, pk)
        form = TaskForm(instance=task)
        return render(
            request, "tasks/partials/task_edit_form.html", {"task": task, "form": form}
        )

    def post(self, request, pk: int):
        task = self._get_task(request, pk)
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            updated = update_task(task, **{k: v for k, v in form.cleaned_data.items()})
            return render(request, "tasks/partials/task_item.html", {"task": updated})
        return render(
            request, "tasks/partials/task_edit_form.html", {"task": task, "form": form}
        )


class TaskDeleteView(LoginRequiredMixin, View):
    """POST: delete task, return empty response (HTMX removes the row)."""

    def post(self, request, pk: int):
        task = get_object_or_404(Task, pk=pk, project__owner=request.user)
        delete_task(task)
        return HttpResponse("")


class TaskToggleView(LoginRequiredMixin, View):
    """POST: toggle is_done, return updated <tr> fragment."""

    def post(self, request, pk: int):
        task = get_object_or_404(Task, pk=pk, project__owner=request.user)
        task = toggle_done(task)
        return render(request, "tasks/partials/task_item.html", {"task": task})


class TaskMoveView(LoginRequiredMixin, View):
    """POST: move task up or down, return full task list for the project."""

    def post(self, request, pk: int, direction: str):
        task = get_object_or_404(Task, pk=pk, project__owner=request.user)
        if direction == "up":
            move_task_up(task)
        elif direction == "down":
            move_task_down(task)
        tasks = task.project.tasks.order_by("order")
        return render(request, "tasks/partials/task_list.html", {"tasks": tasks})


class TaskMoveUpView(LoginRequiredMixin, View):
    """POST: move task one position up → return updated task list."""

    def post(self, request, pk: int):
        task = get_object_or_404(Task, pk=pk, project__owner=request.user)
        move_task_up(task)
        tasks = task.project.tasks.order_by("order")
        return render(request, "tasks/partials/task_list.html", {"tasks": tasks})


class TaskMoveDownView(LoginRequiredMixin, View):
    """POST: move task one position down → return updated task list."""

    def post(self, request, pk: int):
        task = get_object_or_404(Task, pk=pk, project__owner=request.user)
        move_task_down(task)
        tasks = task.project.tasks.order_by("order")
        return render(request, "tasks/partials/task_list.html", {"tasks": tasks})
