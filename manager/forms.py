from datetime import datetime

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from manager.models import Task

User = get_user_model()


class WorkerCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + (
            "position",
            "first_name",
            "last_name",
        )


class WorkerPositionUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ("position",)


class TaskNameSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by name..."}),
    )


class TaskForm(forms.ModelForm):
    assignees = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )
    deadline = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))

    class Meta:
        model = Task
        fields = "__all__"


class WorkerUsernameSearchForm(forms.Form):
    username = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by username..."}),
    )