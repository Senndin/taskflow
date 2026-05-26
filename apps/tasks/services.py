"""
Task service layer.
All business logic for tasks lives here — views stay thin.
"""

from django.db import transaction
from django.db.models import Max

from .models import Task


def create_task(
    project,
    title: str,
    description: str = "",
    priority: int = Task.Priority.MEDIUM,
) -> Task:
    """Create a new task at the bottom of the project list."""
    last_order = project.tasks.aggregate(max_order=Max("order"))["max_order"]
    order = (last_order or 0) + 1
    return Task.objects.create(
        project=project,
        title=title,
        description=description,
        priority=priority,
        order=order,
    )


def update_task(task: Task, **data) -> Task:
    """Update allowed task fields and save."""
    allowed = {"title", "description", "priority", "deadline", "is_done"}
    for field, value in data.items():
        if field in allowed:
            setattr(task, field, value)
    task.save(update_fields=list(data.keys()))
    return task


def toggle_done(task: Task) -> Task:
    """Flip the is_done flag."""
    task.is_done = not task.is_done
    task.save(update_fields=["is_done"])
    return task


def delete_task(task: Task) -> None:
    """Delete a task."""
    task.delete()


@transaction.atomic
def move_task_up(task: Task) -> None:
    """Swap task with the one directly above it (lower order value)."""
    predecessor = (
        Task.objects.filter(project=task.project, order__lt=task.order)
        .order_by("-order")
        .first()
    )
    if predecessor is None:
        return  # Already at the top
    task.order, predecessor.order = predecessor.order, task.order
    Task.objects.bulk_update([task, predecessor], ["order"])


@transaction.atomic
def move_task_down(task: Task) -> None:
    """Swap task with the one directly below it (higher order value)."""
    successor = (
        Task.objects.filter(project=task.project, order__gt=task.order)
        .order_by("order")
        .first()
    )
    if successor is None:
        return  # Already at the bottom
    task.order, successor.order = successor.order, task.order
    Task.objects.bulk_update([task, successor], ["order"])
