from django import forms

from .models import Project


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ["name"]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "tf-form-control",
                    "placeholder": "Project name…",
                    "autofocus": True,
                }
            ),
        }
