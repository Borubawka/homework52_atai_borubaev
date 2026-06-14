from django import forms
from django.core.exceptions import ValidationError
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

    def clean_summary(self):

        summary = self.cleaned_data['summary']

        if len(summary) < 5:

            raise ValidationError(
                'Название задачи должно содержать минимум 5 символов'
            )

        return summary

    def clean(self):

        cleaned_data = super().clean()

        summary = cleaned_data.get('summary')
        description = cleaned_data.get('description')

        if summary and description:

            if summary.lower() == description.lower():

                raise ValidationError(
                    'Описание не должно полностью совпадать с названием'
                )

        return cleaned_data