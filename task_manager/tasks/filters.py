from django.db.models import Q
import django_filters
from django import forms
from .models import Task
from django.utils import timezone


class TaskFilter(django_filters.FilterSet):
    status = django_filters.ModelChoiceFilter(
        queryset=Task._meta.get_field('status').related_model.objects.all(),
        empty_label='---------',
        label='Статус'
    )

    executor = django_filters.ModelChoiceFilter(
        queryset=Task._meta.get_field('executor').related_model.objects.all(),
        empty_label='---------',
        label='Исполнитель'
    )

    labels = django_filters.ModelChoiceFilter(
        queryset=Task._meta.get_field('labels').related_model.objects.all(),
        empty_label='---------',
        label='Метка'
    )

    overdue = django_filters.BooleanFilter(
        method='filter_overdue',
        label='Просроченные'
    )

    ASSIGNED_CHOICES = (
        ('to_me', 'Назначенные мне'),
        ('by_me', 'Назначенные мной'),
    )

    assigned = django_filters.ChoiceFilter(
        choices=ASSIGNED_CHOICES,
        method='filter_assigned_tasks',
        label='Назначение',
        empty_label=None,
        widget=forms.RadioSelect(attrs={'class': 'form-check-inline'})
    )

    class Meta:
        model = Task
        fields = ['status', 'executor', 'labels']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form.label_suffix = ''

        self.filters['executor'].field.label_from_instance = \
            lambda obj: obj.username or f"User {obj.pk}"

    def filter_assigned_tasks(self, queryset, name, value):
        user = getattr(self.request, 'user', None)
        if not user or not value:
            return queryset

        if value == 'to_me':
            return queryset.filter(executor=user)
        if value == 'by_me':
            return queryset.filter(author=user)
        return queryset
    
    def filter_overdue(self, queryset, name, value):
        if value:
            return queryset.filter(deadline__lt=timezone.now())
        return queryset
