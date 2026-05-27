from django.shortcuts import render
from django.shortcuts import redirect
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

    Task.objects.create(
        description=description,
        details=details,
        status=status,
        due_date=due_date or None
    )

    return redirect('index')

def delete_task_view(request, pk):
    task = Task.objects.get(pk=pk)
    task.delete()
    return redirect('index')