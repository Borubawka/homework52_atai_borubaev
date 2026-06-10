from django.urls import path
from webapp.views import (
    IndexView,
    TaskDetailView,
    TaskCreateView,
    TaskUpdateView,
    TaskDeleteView,
)

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('add/', TaskCreateView.as_view(), name='task_add'),
    path('task/<int:task_id>/', TaskDetailView.as_view(), name='task_detail'),
    path('task/<int:task_id>/edit/', TaskUpdateView.as_view(), name='task_edit'),
    path('task/<int:task_id>/delete/', TaskDeleteView.as_view(), name='task_delete'),
]