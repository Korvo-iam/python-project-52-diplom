from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Status

@receiver(post_migrate)
def create_initial_statuses(sender, **kwargs):
    # Чтобы выполнялось только для вашего приложения
    if sender.name != 'task_manager.statuses':
        return

    initial_statuses = ["Новая", "В работе", "На проверке", "Готово"]

    for status_name in initial_statuses:
        Status.objects.get_or_create(name=status_name)