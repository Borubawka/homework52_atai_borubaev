from django.contrib import admin
from webapp.models import (
    Task,
    TaskStatus,
    TaskType
)

admin.site.register(Task)
admin.site.register(TaskStatus)
admin.site.register(TaskType)