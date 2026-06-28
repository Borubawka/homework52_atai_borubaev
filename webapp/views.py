from django.shortcuts import render, redirect, get_object_or_404
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
from django.http import HttpResponseForbidden
from django.contrib.auth.mixins import LoginRequiredMixin

from webapp.models import (
    Task,
    Project,
    ProjectMember,
)

from webapp.forms import (
    TaskForm,
    ProjectForm,
    ProjectMemberForm,
)


def get_member_role(project, user):

    if not user.is_authenticated:
        return None

    member = ProjectMember.objects.filter(
        project=project,
        user=user
    ).first()

    if member:
        return member.role

    return None


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
            'project': project,
            'tasks': project.tasks.filter(
                is_deleted=False
            ),
            'members': project.project_members.select_related(
                'user'
            ),
            'member_form': ProjectMemberForm(),
            'user_role': get_member_role(
                project,
                request.user
            ),
        }

        return render(
            request,
            'project_detail.html',
            context
        )

    def post(self, request, project_id, *args, **kwargs):

        project = get_object_or_404(
            Project,
            id=project_id
        )

        if get_member_role(
            project,
            request.user
        ) not in [
            'manager',
            'lead'
        ]:

            return HttpResponseForbidden()

        form = ProjectMemberForm(request.POST)

        if form.is_valid():

            member = form.save(
                commit=False
            )

            member.project = project

            if ProjectMember.objects.filter(
                project=project,
                user=member.user
            ).exists():

                form.add_error(
                    'user',
                    'Пользователь уже является участником проекта.'
                )

            else:

                member.save()

                return redirect(
                    'project_detail',
                    project_id=project.id
                )

        context = {
            'project': project,
            'tasks': project.tasks.filter(
                is_deleted=False
            ),
            'members': project.project_members.select_related(
                'user'
            ),
            'member_form': form,
            'user_role': get_member_role(
                project,
                request.user
            ),
        }

        return render(
            request,
            'project_detail.html',
            context
        )


class ProjectMemberDeleteView(
    LoginRequiredMixin,
    View
):

    def post(
        self,
        request,
        project_id,
        member_id,
        *args,
        **kwargs
    ):

        project = get_object_or_404(
            Project,
            id=project_id
        )

        if get_member_role(
            project,
            request.user
        ) not in [
            'manager',
            'lead'
        ]:

            return HttpResponseForbidden()

        member = get_object_or_404(
            ProjectMember,
            id=member_id,
            project=project
        )

        member.delete()

        return redirect(
            'project_detail',
            project_id=project.id
        )


class ProjectCreateView(
    LoginRequiredMixin,
    CreateView
):

    model = Project
    form_class = ProjectForm
    template_name = 'project_create.html'

    def form_valid(self, form):

        response = super().form_valid(
            form
        )

        ProjectMember.objects.create(
            project=self.object,
            user=self.request.user,
            role='manager'
        )

        return response

    def get_success_url(self):

        return reverse(
            'project_detail',
            kwargs={
                'project_id': self.object.id
            }
        )


class ProjectUpdateView(
    LoginRequiredMixin,
    UpdateView
):

    model = Project
    form_class = ProjectForm
    template_name = 'project_update.html'
    pk_url_kwarg = 'project_id'

    def dispatch(
        self,
        request,
        *args,
        **kwargs
    ):

        project = self.get_object()

        if get_member_role(
            project,
            request.user
        ) != 'manager':

            return HttpResponseForbidden()

        return super().dispatch(
            request,
            *args,
            **kwargs
        )

    def get_success_url(self):

        return reverse(
            'project_detail',
            kwargs={
                'project_id': self.object.id
            }
        )


class ProjectDeleteView(
    LoginRequiredMixin,
    DeleteView
):

    model = Project
    template_name = 'project_delete.html'
    pk_url_kwarg = 'project_id'

    def dispatch(
        self,
        request,
        *args,
        **kwargs
    ):

        project = self.get_object()

        if get_member_role(
            project,
            request.user
        ) != 'manager':

            return HttpResponseForbidden()

        return super().dispatch(
            request,
            *args,
            **kwargs
        )

    def get_success_url(self):

        return reverse(
            'index'
        )

class TaskDetailView(
    DetailView
):

    model = Task
    template_name = 'task_detail.html'
    context_object_name = 'task'
    pk_url_kwarg = 'task_id'

    def get_queryset(self):

        return Task.objects.filter(
            is_deleted=False
        )


class TaskCreateView(
    LoginRequiredMixin,
    FormView
):

    template_name = 'create_task.html'
    form_class = TaskForm

    def dispatch(
        self,
        request,
        *args,
        **kwargs
    ):

        project = get_object_or_404(
            Project,
            id=self.kwargs['project_id']
        )

        if get_member_role(
            project,
            request.user
        ) not in [
            'manager',
            'lead',
            'developer'
        ]:

            return HttpResponseForbidden()

        return super().dispatch(
            request,
            *args,
            **kwargs
        )

    def form_valid(
        self,
        form
    ):

        project = get_object_or_404(
            Project,
            id=self.kwargs['project_id']
        )

        task = form.save(
            commit=False
        )

        task.project = project

        task.save()

        form.save_m2m()

        return redirect(
            'task_detail',
            task_id=task.id
        )


class TaskUpdateView(
    LoginRequiredMixin,
    UpdateView
):

    model = Task
    form_class = TaskForm
    template_name = 'edit_task.html'
    context_object_name = 'task'
    pk_url_kwarg = 'task_id'

    def dispatch(
        self,
        request,
        *args,
        **kwargs
    ):

        task = self.get_object()

        if get_member_role(
            task.project,
            request.user
        ) not in [
            'manager',
            'lead',
            'developer'
        ]:

            return HttpResponseForbidden()

        return super().dispatch(
            request,
            *args,
            **kwargs
        )

    def get_queryset(self):

        return Task.objects.filter(
            is_deleted=False
        )

    def get_success_url(self):

        return reverse(
            'task_detail',
            kwargs={
                'task_id': self.object.id
            }
        )


class TaskDeleteView(
    LoginRequiredMixin,
    DeleteView
):

    model = Task
    template_name = 'delete_task.html'
    context_object_name = 'task'
    pk_url_kwarg = 'task_id'

    def dispatch(
        self,
        request,
        *args,
        **kwargs
    ):

        task = self.get_object()

        if get_member_role(
            task.project,
            request.user
        ) not in [
            'manager',
            'lead'
        ]:

            return HttpResponseForbidden()

        return super().dispatch(
            request,
            *args,
            **kwargs
        )

    def get_queryset(self):

        return Task.objects.filter(
            is_deleted=False
        )

    def form_valid(
        self,
        form
    ):

        self.object = self.get_object()

        self.object.is_deleted = True

        self.object.save()

        return redirect(
            'project_detail',
            project_id=self.object.project.id
        )