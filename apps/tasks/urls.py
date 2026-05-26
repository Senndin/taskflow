"""URL patterns for the tasks app."""

from django.urls import path

from . import views

app_name = "tasks"

urlpatterns = [
    path("<int:project_pk>/create/", views.TaskCreateView.as_view(), name="create"),
    path("<int:pk>/edit/", views.TaskUpdateView.as_view(), name="edit"),
    path("<int:pk>/delete/", views.TaskDeleteView.as_view(), name="delete"),
    path("<int:pk>/toggle/", views.TaskToggleView.as_view(), name="toggle"),
    path("<int:pk>/move/<str:direction>/", views.TaskMoveView.as_view(), name="move"),
    path("<int:pk>/move-up/", views.TaskMoveUpView.as_view(), name="move_up"),
    path("<int:pk>/move-down/", views.TaskMoveDownView.as_view(), name="move_down"),
]
