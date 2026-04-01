from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'deadline', 'description', 'status', 'executor', 'labels']
        widgets = {
            'deadline': forms.DateTimeInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control'
                }
            ),
        }