from django.shortcuts import (render, redirect, get_object_or_404)
from django.urls import reverse
from django.db.models import Q
from django.views import View
from django.views.generic import (
    ListView,
    DetailView,
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

class TaskDetailView(DetailView):

    model = Task

    template_name = 'task_detail.html'

    context_object_name = 'task'

    pk_url_kwarg = 'task_id'

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

class TaskUpdateView(UpdateView):

    model = Task

    form_class = TaskForm

    template_name = 'edit_task.html'

    context_object_name = 'task'

    pk_url_kwarg = 'task_id'

    def get_success_url(self):

        return reverse(
            'task_detail',
            kwargs={
                'task_id': self.object.id
            }
        )

class TaskDeleteView(DeleteView):

    model = Task

    template_name = 'delete_task.html'

    context_object_name = 'task'

    pk_url_kwarg = 'task_id'

    def get_success_url(self):

        return reverse(
            'project_detail',
            kwargs={
                'project_id': self.object.project.id
            }
        )