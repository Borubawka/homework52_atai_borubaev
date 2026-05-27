from django.urls import path
from webapp.views import (
    index_view,
    create_task_view,
    delete_task_view,
    task_detail_view
)

urlpatterns = [
    path('', index_view),
    path('add/', create_task_view),
    path('delete/<int:task_id>/', delete_task_view),
    path('task/<int:task_id>/', task_detail_view),
]