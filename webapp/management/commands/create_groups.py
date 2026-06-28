from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from webapp.models import Project, Task

class Command(BaseCommand):

    help = 'Создает группы пользователей и назначает им права'

    def handle(self, *args, **options):

        manager_group, created = Group.objects.get_or_create(
            name='Manager'
        )

        developer_group, created = Group.objects.get_or_create(
            name='Developer'
        )

        manager_group.permissions.clear()
        developer_group.permissions.clear()

        project_content_type = ContentType.objects.get_for_model(
            Project
        )

        task_content_type = ContentType.objects.get_for_model(
            Task
        )

        manager_permissions = Permission.objects.filter(
            content_type__in=[
                project_content_type,
                task_content_type,
            ]
        )

        manager_group.permissions.set(
            manager_permissions
        )

        developer_permissions = Permission.objects.filter(
            content_type=task_content_type,
            codename__in=[
                'view_task',
                'add_task',
                'change_task',
            ]
        )

        developer_group.permissions.set(
            developer_permissions
        )

        self.stdout.write(
            self.style.SUCCESS(
                'Группы успешно созданы.'
            )
        )