from django.shortcuts import render, redirect
from webapp.models import Task

def index_view(request):
    tasks = Task.objects.all()

    context = {
        'tasks': tasks
    }

    return render(request, 'index.html', context)

def create_task_view(request):

    if request.method == 'POST':
        description = request.POST.get('description')
        status = request.POST.get('status')
        due_date = request.POST.get('due_date')

        Task.objects.create(
            description=description,
            status=status,
            due_date=due_date if due_date else None
        )

        return redirect('/')

    return render(request, 'create_task.html')

def delete_task_view(request):

    task_id = request.GET.get('pk')

    task = Task.objects.get(pk=task_id)

    task.delete()

    return redirect('/')