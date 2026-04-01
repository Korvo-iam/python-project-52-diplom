# task_manager/tasks/apps.py
from django.apps import AppConfig
from django.db.utils import OperationalError, ProgrammingError

class TasksConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'task_manager.tasks'

    def ready(self):
        from task_manager.statuses.models import Status

        initial_statuses = ["Новая", "В работе", "На проверке", "Готово"]

        try:
            for status_name in initial_statuses:
                Status.objects.get_or_create(name=status_name)
        except (OperationalError, ProgrammingError):
            pass