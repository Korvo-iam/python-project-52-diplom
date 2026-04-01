from django.db import models
from django.contrib.auth import get_user_model
from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from django.utils import timezone

# Create your models here.

User = get_user_model()


class Task(models.Model):
    name = models.CharField("Имя", max_length=255)
    description = models.TextField("Описание", blank=True)
    deadline = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Дедлайн"
    )
    status = models.ForeignKey(
        Status,
        on_delete=models.PROTECT,
        verbose_name="Статус",
        related_name='tasks'
    )
    executor = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name="Исполнитель",
        related_name='tasks_assigned'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        verbose_name="Автор",
        related_name='tasks_created'
    )
    labels = models.ManyToManyField(
    Label,
    blank=True,
    related_name='tasks',
    verbose_name="Метки"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")  # noqa: E501
    
    def is_overdue(self):
        return self.deadline and self.deadline < timezone.now()

    def __str__(self):
        return self.name
