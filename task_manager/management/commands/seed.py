from django.core.management.base import BaseCommand
from django.utils import timezone
from task_manager.users.models import User
from task_manager.statuses.models import Status
from task_manager.tasks.models import Task
from task_manager.labels.models import Label
import random

class Command(BaseCommand):
    help = "Create example users, statuses, labels, and tasks"

    def handle(self, *args, **options):
        # -------------------- USERS --------------------
        users_data = [
            {"username": "admin", "first_name": "Admin", "last_name": "User", "is_superuser": True, "is_staff": True, "password": "admin123"},
            {"username": "User1", "first_name": "Иван", "last_name": "Иванов", "password": "123"},
            {"username": "User2", "first_name": "Мария", "last_name": "Петрова", "password": "123"},
            {"username": "User3", "first_name": "Алексей", "last_name": "Сидоров", "password": "123"},
        ]

        created_users = {}
        for u in users_data:
            user, created = User.objects.get_or_create(username=u["username"])
            user.first_name = u["first_name"]
            user.last_name = u["last_name"]
            if u.get("is_superuser"):
                user.is_superuser = True
                user.is_staff = True
            user.set_password(u["password"])
            user.save()
            created_users[u["username"]] = user
            self.stdout.write(f"Ensured user {u['username']} exists")

        admin_user = created_users["admin"]

        # -------------------- STATUSES --------------------
        status_names = ["Новая", "В процессе", "Завершена"]
        statuses = []
        for name in status_names:
            status, _ = Status.objects.get_or_create(name=name)
            statuses.append(status)
        self.stdout.write("Ensured statuses exist")

        # -------------------- LABELS --------------------
        label_names = ["важно", "желательно", "Umbrella", "SpaceX"]
        labels = []
        for name in label_names:
            label, _ = Label.objects.get_or_create(name=name)
            labels.append(label)
        self.stdout.write("Ensured labels exist")

        # -------------------- TASKS --------------------
        for username, user in created_users.items():
            if username == "admin":
                continue  # не создаем задачи для админа
            task_name = f"Задача для {username}"
            task, created = Task.objects.get_or_create(
                name=task_name,
                defaults={
                    "description": f"Это пример задачи для {username}",
                    "status": random.choice(statuses),
                    "author": admin_user,
                    "executor": user,
                    "deadline": timezone.now() + timezone.timedelta(days=random.randint(1, 10))
                }
            )
            # Добавляем случайные метки (1-3 на задачу)
            task.labels.set(random.sample(labels, k=random.randint(1, 3)))
            task.save()
            self.stdout.write(f"Ensured task exists for {username}")

            