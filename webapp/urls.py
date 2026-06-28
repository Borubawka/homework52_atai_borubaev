from django.urls import path
from webapp.views import (
    IndexView,
    ProjectDetailView,
    ProjectMemberDeleteView,
    ProjectCreateView,
    ProjectUpdateView,
    ProjectDeleteView,
    TaskDetailView,
    TaskCreateView,
    TaskUpdateView,
    TaskDeleteView,
)

urlpatterns = [
    path(
        '',
        IndexView.as_view(),
        name='index'
    ),

    path(
        'project/add/',
        ProjectCreateView.as_view(),
        name='project_add'
    ),

    path(
        'project/<int:project_id>/',
        ProjectDetailView.as_view(),
        name='project_detail'
    ),

    path(
        'project/<int:project_id>/edit/',
        ProjectUpdateView.as_view(),
        name='project_edit'
    ),

    path(
        'project/<int:project_id>/delete/',
        ProjectDeleteView.as_view(),
        name='project_delete'
    ),

    path(
        'project/<int:project_id>/member/<int:member_id>/delete/',
        ProjectMemberDeleteView.as_view(),
        name='project_member_delete'
    ),

    path(
        'project/<int:project_id>/task/add/',
        TaskCreateView.as_view(),
        name='task_add'
    ),

    path(
        'task/<int:task_id>/',
        TaskDetailView.as_view(),
        name='task_detail'
    ),

    path(
        'task/<int:task_id>/edit/',
        TaskUpdateView.as_view(),
        name='task_edit'
    ),

    path(
        'task/<int:task_id>/delete/',
        TaskDeleteView.as_view(),
        name='task_delete'
    ),
]