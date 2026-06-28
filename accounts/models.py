from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):

    birth_date = models.DateField(
        verbose_name='Дата рождения',
        null=True,
        blank=True
    )

    bio = models.TextField(
        verbose_name='О себе',
        blank=True
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'