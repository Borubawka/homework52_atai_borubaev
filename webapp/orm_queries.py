from datetime import timedelta
from django.utils import timezone
from webapp.models import Task

closed_tasks_last_month = Task.objects.filter(
    status__title='Done',
    updated_at__gte=timezone.now() - timedelta(days=30)
)

tasks_by_status_and_type = Task.objects.filter(
    status__title__in=[
        'New',
        'In Progress'
    ],
    task_types__title__in=[
        'Task',
        'Bug'
    ]
).distinct()

not_closed_bug_tasks = Task.objects.filter(
    summary__icontains='bug',
    task_types__title='Bug'
).exclude(
    status__title='Done'
)