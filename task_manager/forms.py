from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from .models import Employee, Task


class TaskForm(forms.ModelForm):
    assignees = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )
    deadline = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))

    class Meta:
        model = Task
        fields = "__all__"


class EmployeeCreationForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    class Meta(UserCreationForm.Meta):
        model = Employee
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "position",
        )


class EmployeePositionUpdateForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ["position"]


class EmployeeSearchForm(forms.Form):
    username = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by username..."}),
    )


class ByNameSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by name..."}),
    )
