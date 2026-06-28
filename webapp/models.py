from django.conf import settings
from django.db import models

class Project(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name='Название'
    )

    description = models.TextField(
        verbose_name='Описание'
    )

    start_date = models.DateField(
        verbose_name='Дата начала'
    )

    end_date = models.DateField(
        blank=True,
        null=True,
        verbose_name='Дата окончания'
    )

    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='ProjectMember',
        related_name='projects',
        verbose_name='Участники'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'

class ProjectMember(models.Model):
    ROLE_CHOICES = (
        ('manager', 'Менеджер'),
        ('lead', 'Капитан'),
        ('developer', 'Разработчик'),
    )

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='project_members',
        verbose_name='Проект'
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='project_members',
        verbose_name='Пользователь'
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='developer',
        verbose_name='Роль'
    )

    class Meta:
        unique_together = (
            'project',
            'user',
        )
        verbose_name = 'Участник проекта'
        verbose_name_plural = 'Участники проекта'

    def __str__(self):
        return (
            f'{self.user} - '
            f'{self.project} '
            f'({self.get_role_display()})'
        )

class TaskType(models.Model):
    title = models.CharField(
        max_length=100,
        verbose_name='Тип задачи'
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Тип задачи'
        verbose_name_plural = 'Типы задач'

class TaskStatus(models.Model):
    title = models.CharField(
        max_length=100,
        verbose_name='Статус'
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Статус'
        verbose_name_plural = 'Статусы'

class Task(models.Model):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='tasks',
        verbose_name='Проект',
        default=1
    )

    summary = models.CharField(
        max_length=255,
        verbose_name='Краткое описание'
    )

    description = models.TextField(
        blank=True,
        verbose_name='Полное описание'
    )

    status = models.ForeignKey(
        TaskStatus,
        on_delete=models.PROTECT,
        verbose_name='Статус'
    )

    task_types = models.ManyToManyField(
        TaskType,
        verbose_name='Типы задач'
    )

    is_deleted = models.BooleanField(
        default=False,
        verbose_name='Удалена'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата изменения'
    )

    def __str__(self):
        return self.summary

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'