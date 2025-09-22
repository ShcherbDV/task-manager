from django.contrib.auth import get_user_model
from django.shortcuts import render

from manager.models import Task


User = get_user_model()

def index(request):
    num_of_tasks = Task.objects.count()
    num_of_workers = User.objects.count()

    context = {
        "num_of_tasks": num_of_tasks,
        "num_of_workers": num_of_workers,
    }

    return render(request, "manager/index.html", context=context)
