"""
Project service layer.
All business logic for projects lives here — views stay thin.
"""

from .models import Project


def create_project(owner, name: str) -> Project:
    """Create a new project for the given user."""
    return Project.objects.create(owner=owner, name=name)


def update_project(project: Project, name: str) -> Project:
    """Rename an existing project."""
    project.name = name
    project.save(update_fields=["name"])
    return project


def delete_project(project: Project) -> None:
    """Delete a project and all its tasks (CASCADE)."""
    project.delete()
