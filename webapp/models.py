from django.db import models

class TaskType(models.Model):
    title = models.CharField(
        max_length=100,
        verbose_name='Тип задачи'
    )

    def __str__(self):
        return self.title

class TaskStatus(models.Model):
    title = models.CharField(
        max_length=100,
        verbose_name='Статус'
    )

    def __str__(self):
        return self.title


class Task(models.Model):
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