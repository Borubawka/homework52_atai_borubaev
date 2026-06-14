from django.shortcuts import (render, redirect, get_object_or_404)
from django.urls import reverse
from django.views import View
from django.views.generic import FormView
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

class TaskCreateView(FormView):

    template_name = 'create_task.html'
    form_class = TaskForm

    def form_valid(self, form):

        task = form.save()

        return redirect(
            'task_detail',
            task_id=task.id
        )

class TaskUpdateView(FormView):

    template_name = 'edit_task.html'
    form_class = TaskForm

    def get_form_kwargs(self):

        kwargs = super().get_form_kwargs()

        kwargs['instance'] = get_object_or_404(
            Task,
            id=self.kwargs['task_id']
        )

        return kwargs

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context['task'] = get_object_or_404(
            Task,
            id=self.kwargs['task_id']
        )

        return context

    def form_valid(self, form):

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