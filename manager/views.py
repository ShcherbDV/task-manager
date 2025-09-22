from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from manager.models import Task, Position

User = get_user_model()

def index(request):
    num_of_tasks = Task.objects.count()
    num_of_workers = User.objects.count()

    context = {
        "num_of_tasks": num_of_tasks,
        "num_of_workers": num_of_workers,
    }

    return render(request, "manager/index.html", context=context)


class PositionListView(generic.ListView):
    model = Position


class PositionCreateView(generic.CreateView):
    model = Position
    fields = "__all__"
    success_url = reverse_lazy("manager:position-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["previous_url"] = self.request.META.get(
            "HTTP_REFERER", reverse_lazy("manager:position-list")
        )
        return context


class PositionUpdateView(generic.UpdateView):
    model = Position
    fields = "__all__"
    success_url = reverse_lazy("manager:position-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["previous_url"] = self.request.META.get(
            "HTTP_REFERER", reverse_lazy("manager:position-list")
        )
        return context


class PositionDeleteView(generic.DeleteView):
    model = Position
    success_url = reverse_lazy("manager:position-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["previous_url"] = self.request.META.get(
            "HTTP_REFERER", reverse_lazy("manager:position-list")
        )
        return context


