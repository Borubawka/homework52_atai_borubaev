from django.shortcuts import (render, redirect, get_object_or_404)
from django.views import View
from webapp.models import Task
from webapp.forms import TaskForm
class IndexView(View):

    def get(self, request, *args, **kwargs):

        tasks = Task.objects.all()

        context = {
            'tasks': tasks
        }

        return render(
            request,
            'index.html',
            context
        )

class TaskDetailView(View):

    def get(self, request, task_id, *args, **kwargs):

        task = get_object_or_404(
            Task,
            id=task_id
        )

        context = {
            'task': task
        }

        return render(
            request,
            'task_detail.html',
            context
        )

class TaskCreateView(View):

    def get(self, request, *args, **kwargs):

        form = TaskForm()

        return render(
            request,
            'create_task.html',
            {
                'form': form
            }
        )

    def post(self, request, *args, **kwargs):

        form = TaskForm(request.POST)

        if not form.is_valid():

            return render(
                request,
                'create_task.html',
                {
                    'form': form
                }
            )

        task = form.save()

        return redirect(
            'task_detail',
            task_id=task.id
        )

class TaskUpdateView(View):

    def get(self, request, task_id, *args, **kwargs):

        task = get_object_or_404(
            Task,
            id=task_id
        )

        form = TaskForm(instance=task)

        return render(
            request,
            'edit_task.html',
            {
                'form': form,
                'task': task
            }
        )

    def post(self, request, task_id, *args, **kwargs):

        task = get_object_or_404(
            Task,
            id=task_id
        )

        form = TaskForm(
            request.POST,
            instance=task
        )

        if not form.is_valid():

            return render(
                request,
                'edit_task.html',
                {
                    'form': form,
                    'task': task
                }
            )

        task = form.save()

        return redirect(
            'task_detail',
            task_id=task.id
        )

class TaskDeleteView(View):

    def get(self, request, task_id, *args, **kwargs):

        task = get_object_or_404(
            Task,
            id=task_id
        )

        return render(
            request,
            'delete_task.html',
            {
                'task': task
            }
        )

    def post(self, request, task_id, *args, **kwargs):

        task = get_object_or_404(
            Task,
            id=task_id
        )

        task.delete()

        return redirect('index')