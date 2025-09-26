from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from manager.forms import (
    WorkerCreationForm,
    WorkerPositionUpdateForm,
    TaskNameSearchForm,
    WorkerUsernameSearchForm,
    TaskForm,
)
from manager.models import Task, Position, TaskType

User = get_user_model()


@login_required
def index(request):
    num_of_tasks = Task.objects.count()
    num_of_complete_tasks = Task.objects.filter(is_completed=True).count()
    num_of_uncompleted_tasks = Task.objects.filter(is_completed=False).count()
    queryset = Task.objects.all().order_by("deadline")[:5]
    num_of_workers = User.objects.count()

    context = {
        "num_of_tasks": num_of_tasks,
        "num_of_complete_tasks": num_of_complete_tasks,
        "num_of_uncompleted_tasks": num_of_uncompleted_tasks,
        "num_of_workers": num_of_workers,
        "queryset": queryset,
    }

    return render(request, "manager/index.html", context=context)


class PositionListView(LoginRequiredMixin, generic.ListView):
    model = Position


class PositionCreateView(LoginRequiredMixin, generic.CreateView):
    model = Position
    fields = "__all__"
    success_url = reverse_lazy("manager:position-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["previous_url"] = self.request.META.get(
            "HTTP_REFERER", reverse_lazy("manager:position-list")
        )
        return context


class PositionUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Position
    fields = "__all__"
    success_url = reverse_lazy("manager:position-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["previous_url"] = self.request.META.get(
            "HTTP_REFERER", reverse_lazy("manager:position-list")
        )
        return context


class PositionDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Position
    success_url = reverse_lazy("manager:position-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["previous_url"] = self.request.META.get(
            "HTTP_REFERER", reverse_lazy("manager:position-list")
        )
        return context


class TaskTypeListView(LoginRequiredMixin, generic.ListView):
    model = TaskType
    template_name = "manager/task_type_list.html"
    context_object_name = "task_type_list"


class TaskTypeCreateView(LoginRequiredMixin, generic.CreateView):
    model = TaskType
    template_name = "manager/task_type_form.html"
    fields = "__all__"
    success_url = reverse_lazy("manager:task-type-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["previous_url"] = self.request.META.get(
            "HTTP_REFERER", reverse_lazy("manager:task-type-list")
        )
        return context


class TaskTypeUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = TaskType
    template_name = "manager/task_type_form.html"
    fields = "__all__"
    success_url = reverse_lazy("manager:task-type-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["previous_url"] = self.request.META.get(
            "HTTP_REFERER", reverse_lazy("manager:task-type-list")
        )
        return context


class TaskTypeDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = TaskType
    template_name = "manager/task_type_confirm_delete.html"
    success_url = reverse_lazy("manager:task-type-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["previous_url"] = self.request.META.get(
            "HTTP_REFERER", reverse_lazy("manager:task-type-list")
        )
        return context


class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    paginate_by = 5

    def get_queryset(self):
        form = TaskNameSearchForm(self.request.GET)
        queryset = Task.objects.all().select_related("task_type")
        if form.is_valid():
            return queryset.filter(name__icontains=form.cleaned_data["name"])
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TaskListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name")
        context["search_form"] = TaskNameSearchForm(initial={"name": name})
        return context


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("manager:task-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["previous_url"] = self.request.META.get(
            "HTTP_REFERER", reverse_lazy("manager:task-list")
        )
        return context


class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("manager:task-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["previous_url"] = self.request.META.get(
            "HTTP_REFERER", reverse_lazy("manager:task-list")
        )
        return context


class TaskDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Task
    success_url = reverse_lazy("manager:task-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["previous_url"] = self.request.META.get(
            "HTTP_REFERER", reverse_lazy("manager:task-list")
        )
        return context


class WorkerListView(LoginRequiredMixin, generic.ListView):
    model = User
    paginate_by = 5

    def get_queryset(self):
        form = WorkerUsernameSearchForm(self.request.GET)
        queryset = User.objects.all()
        if form.is_valid():
            return queryset.filter(username__icontains=form.cleaned_data["username"])
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(WorkerListView, self).get_context_data(**kwargs)
        username = self.request.GET.get("username")
        context["search_form"] = WorkerUsernameSearchForm(
            initial={"username": username}
        )
        return context


class WorkerDetailView(LoginRequiredMixin, generic.DetailView):
    model = User
    context_object_name = "worker"
    queryset = User.objects.all().select_related("position")


class WorkerCreateView(LoginRequiredMixin, generic.CreateView):
    model = User
    form_class = WorkerCreationForm
    success_url = reverse_lazy("manager:worker-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["previous_url"] = self.request.META.get(
            "HTTP_REFERER", reverse_lazy("manager:worker-list")
        )
        return context


class WorkerUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = User
    form_class = WorkerPositionUpdateForm
    success_url = reverse_lazy("manager:worker-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["previous_url"] = self.request.META.get(
            "HTTP_REFERER", reverse_lazy("manager:worker-list")
        )
        return context


class WorkerDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = User
    context_object_name = "worker"
    success_url = reverse_lazy("manager:worker-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["previous_url"] = self.request.META.get(
            "HTTP_REFERER", reverse_lazy("manager:worker-list")
        )
        return context
