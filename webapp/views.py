from django.shortcuts import (render, redirect, get_object_or_404)
from django.urls import reverse
from django.db.models import Q
from django.views import View
from django.views.generic import (
    ListView,
    FormView,
    CreateView,
    UpdateView,
    DeleteView
)
from webapp.models import (Task, Project)
from webapp.forms import (TaskForm, ProjectForm)

class IndexView(ListView):

    model = Project
    template_name = 'index.html'
    context_object_name = 'projects'
    paginate_by = 5

    def get_queryset(self):

        queryset = Project.objects.all()

        search = self.request.GET.get('search')

        if search:

            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(description__icontains=search)
            )

        return queryset.order_by('id')

class ProjectDetailView(View):

    def get(self, request, project_id, *args, **kwargs):

        project = get_object_or_404(
            Project,
            id=project_id
        )

        context = {
            'project': project
        }

        return render(
            request,
            'project_detail.html',
            context
        )

class ProjectCreateView(CreateView):

    model = Project
    form_class = ProjectForm
    template_name = 'project_create.html'

    def get_success_url(self):

        return reverse(
            'project_detail',
            kwargs={
                'project_id': self.object.id
            }
        )

class ProjectUpdateView(UpdateView):

    model = Project
    form_class = ProjectForm
    template_name = 'project_update.html'

    pk_url_kwarg = 'project_id'

    def get_success_url(self):

        return reverse(
            'project_detail',
            kwargs={
                'project_id': self.object.id
            }
        )

class ProjectDeleteView(DeleteView):

    model = Project
    template_name = 'project_delete.html'

    pk_url_kwarg = 'project_id'

    def get_success_url(self):

        return reverse('index')

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

        project = get_object_or_404(
            Project,
            id=self.kwargs['project_id']
        )

        task = form.save(commit=False)

        task.project = project

        task.save()

        form.save_m2m()

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