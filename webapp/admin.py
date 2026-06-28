from django.contrib import admin
from webapp.models import (
    Task,
    TaskStatus,
    TaskType,
    Project,
    ProjectMember,
)

admin.site.register(Task)
admin.site.register(TaskStatus)
admin.site.register(TaskType)
admin.site.register(Project)
admin.site.register(ProjectMember)