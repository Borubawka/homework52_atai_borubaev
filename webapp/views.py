from django.shortcuts import render
from webapp.models import Task

def index_view(request):
    tasks = Task.objects.all()

    context = {
        'tasks': tasks
    }

    return render(request, 'index.html', context)