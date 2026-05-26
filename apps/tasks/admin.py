from django.contrib import admin

from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "project", "priority", "is_done", "order", "deadline")
    list_filter = ("is_done", "priority", "project")
    search_fields = ("title", "project__name")
    ordering = ("project", "order")
    list_editable = ("is_done", "order")
