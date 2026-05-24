from django.urls import path
from webapp.views import (
    index_view,
    create_task_view,
    delete_task_view
)
urlpatterns = [
    path('', index_view),
    path('add/', create_task_view),
    path('delete/', delete_task_view),
]