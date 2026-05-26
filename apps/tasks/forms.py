"""Forms for the tasks app."""

from datetime import date

from django import forms

from .models import Task


class TaskQuickCreateForm(forms.Form):
    """Minimal form for HTMX inline task creation (just a title)."""

    title = forms.CharField(
        max_length=255,
        widget=forms.TextInput(
            attrs={
                "class": "tf-add-task-input",
                "placeholder": "Start typing here to create a task…",
                "autocomplete": "off",
            }
        ),
    )


class TaskForm(forms.ModelForm):
    """Full edit form used for inline task editing."""

    class Meta:
        model = Task
        fields = ["title", "priority", "deadline"]
        widgets = {
            "title": forms.TextInput(
                attrs={"class": "tf-form-control tf-form-control-sm"}
            ),
            "priority": forms.Select(attrs={"class": "form-select form-select-sm"}),
            "deadline": forms.DateInput(
                attrs={"class": "tf-form-control tf-form-control-sm", "type": "date"}
            ),
        }

    def clean_deadline(self):
        """Deadline must not be in the past."""
        deadline = self.cleaned_data.get("deadline")
        if deadline and deadline < date.today():
            raise forms.ValidationError("Deadline cannot be in the past.")
        return deadline
