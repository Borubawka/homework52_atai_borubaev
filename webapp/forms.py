from django import forms

from webapp.models import (
    Task,
    TaskStatus,
    TaskType
)

class TaskForm(forms.ModelForm):

    status = forms.ModelChoiceField(
        queryset=TaskStatus.objects.all(),
        label='Статус'
    )

    task_types = forms.ModelMultipleChoiceField(
        queryset=TaskType.objects.all(),
        label='Типы задач',
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Task

        fields = (
            'summary',
            'description',
            'status',
            'task_types'
        )