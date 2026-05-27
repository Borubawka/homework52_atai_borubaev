from django.db import models

STATUS_CHOICES = [
    ('new', 'Новая'),
    ('in_progress', 'В процессе'),
    ('done', 'Сделано')
]

class Task(models.Model):
    description = models.TextField(
        verbose_name='Описание'
    )

    details = models.TextField(
        blank=True,
        verbose_name='Подробное описание'
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='new',
        verbose_name='Статус'
    )

    due_date = models.DateField(
        blank=True,
        null=True,
        verbose_name='Дата выполнения'
    )

    def __str__(self):
        return self.description