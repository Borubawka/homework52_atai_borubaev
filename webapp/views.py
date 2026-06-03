from django.shortcuts import render, redirect, get_object_or_404
from webapp.models import Task

def index_view(request):
    tasks = Task.objects.all()

    context = {
        'tasks': tasks
    }

    return render(request, 'index.html', context)

def create_task_view(request):
    if request.method == 'GET':
        return render(request, 'create_task.html')

    description = request.POST.get('description')
    details = request.POST.get('details')
    status = request.POST.get('status')
    due_date = request.POST.get('due_date')

    task = Task.objects.create(
        description=description,
        details=details,
        status=status,
        due_date=due_date if due_date else None
    )

    return redirect('task_detail', task_id=task.id)

def delete_task_view(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if request.method == 'GET':
        return render(
            request,
            'delete_task.html',
            {
                'task': task
            }
        )

    task.delete()

    return redirect('index')

def task_detail_view(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    context = {
        'task': task
    }

    return render(request, 'task_detail.html', context)

def edit_task_view(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if request.method == 'GET':
        return render(
            request,
            'edit_task.html',
            {
                'task': task
            }
        )

    task.description = request.POST.get('description')
    task.details = request.POST.get('details')
    task.status = request.POST.get('status')

    due_date = request.POST.get('due_date')
    task.due_date = due_date if due_date else None

    task.save()

    return redirect('task_detail', task_id=task.id)