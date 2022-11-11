from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Employee, Position, Task, TaskType
from .forms import (
    EmployeeCreationForm,
    EmployeePositionUpdateForm,
    TaskForm,
    EmployeeSearchForm,
    ByNameSearchForm,
)


@login_required
def index(request):
    num_employees = get_user_model().objects.count()
    num_tasks = Task.objects.count()

    context = {
        "num_employees": num_employees,
        "num_tasks": num_tasks,
    }

    return render(request, "task_manager/index.html", context=context)


class TaskTypeListView(LoginRequiredMixin, generic.ListView):
    model = TaskType
    context_object_name = "task_type_list"
    template_name = "task_manager/task_type_list.html"
    paginate_by = 10
    queryset = TaskType.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        name = self.request.GET.get("name", "")

        context["search_form"] = ByNameSearchForm(initial={"name": name})

        return context

    def get_queryset(self):
        if name := self.request.GET.get("name"):
            return self.queryset.filter(name__icontains=name)

        return self.queryset


class TaskTypeCreateView(LoginRequiredMixin, generic.CreateView):
    model = TaskType
    context_object_name = "task_type"
    template_name = "task_manager/task_type_form.html"
    fields = "__all__"
    success_url = reverse_lazy("task_manager:task-type-list")


class TaskTypeUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = TaskType
    context_object_name = "task_type"
    template_name = "task_manager/task_type_form.html"
    fields = "__all__"
    success_url = reverse_lazy("task_manager:task-type-list")


class TaskTypeDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = TaskType
    context_object_name = "task_type"
    template_name = "task_manager/task_type_confirm_delete.html"
    success_url = reverse_lazy("task_manager:task-type-list")


class PositionListView(LoginRequiredMixin, generic.ListView):
    model = Position
    paginate_by = 10
    queryset = Position.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        name = self.request.GET.get("name", "")

        context["search_form"] = ByNameSearchForm(initial={"name": name})

        return context

    def get_queryset(self):
        if name := self.request.GET.get("name"):
            return self.queryset.filter(name__icontains=name)

        return self.queryset


class PositionCreateView(LoginRequiredMixin, generic.CreateView):
    model = Position
    fields = "__all__"
    success_url = reverse_lazy("task_manager:position-list")


class PositionUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Position
    fields = "__all__"
    success_url = reverse_lazy("task_manager:position-list")


class PositionDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Position
    success_url = reverse_lazy("task_manager:position-list")


class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    paginate_by = 10
    queryset = Task.objects.select_related("task_type")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        model = self.request.GET.get("model", "")

        context["search_form"] = ByNameSearchForm(initial={"model": model})

        return context

    def get_queryset(self):
        if model := self.request.GET.get("model"):
            return self.queryset.filter(model__icontains=model)

        return self.queryset


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("task_manager:task-list")


class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("task_manager:task-list")


class TaskDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Task
    success_url = reverse_lazy("task_manager:task-list")


class EmployeeListView(LoginRequiredMixin, generic.ListView):
    model = Employee
    paginate_by = 10
    queryset = Employee.objects.prefetch_related("tasks")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        username = self.request.GET.get("username", "")

        context["search_form"] = EmployeeSearchForm(
            initial={"username": username}
        )

        return context

    def get_queryset(self):
        if username := self.request.GET.get("username"):
            return self.queryset.filter(username__icontains=username)

        return self.queryset


class EmployeeDetailView(LoginRequiredMixin, generic.DetailView):
    model = Employee
    queryset = Employee.objects.prefetch_related("tasks__task_type")


class EmployeeCreateView(LoginRequiredMixin, generic.CreateView):
    model = Employee
    form_class = EmployeeCreationForm


class EmployeePositionUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Employee
    form_class = EmployeePositionUpdateForm

    def get_success_url(self):
        return reverse_lazy(
            "task_manager:employee-detail", kwargs={"pk": self.object.pk}
        )


class EmployeeDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Employee
    success_url = reverse_lazy("task_manager:employee-list")


@login_required
def toggle_assign_to_task(request, pk):
    employee = Employee.objects.get(id=request.user.id)
    if (
        Task.objects.get(id=pk) in employee.tasks.all()
    ):
        employee.tasks.remove(pk)
    else:
        employee.tasks.add(pk)
    return HttpResponseRedirect(reverse_lazy("task_manager:task-detail", args=[pk]))
