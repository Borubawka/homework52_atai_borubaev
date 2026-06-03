from django.urls import path
from webapp.views import (
    index_view,
    create_task_view,
    delete_task_view,
    task_detail_view,
    edit_task_view,
)

urlpatterns = [
    path('', index_view, name='index'),
    path('add/', create_task_view, name='task_add'),
    path('delete/<int:task_id>/', delete_task_view, name='task_delete'),
    path('task/<int:task_id>/', task_detail_view, name='task_detail'),

    path('task/<int:task_id>/edit/', edit_task_view, name='task_edit'),
]