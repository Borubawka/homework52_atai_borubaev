from django.contrib import admin
from webapp.models import (
    Task,
    TaskStatus,
    TaskType,
    Project
)

admin.site.register(Task)
admin.site.register(TaskStatus)
admin.site.register(TaskType)
admin.site.register(Project)