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
            {"username": "admin", "first_name": "Admin", "last_name": "User", "is_superuser": True, "is_staff": True},
            {"username": "User1", "first_name": "Иван", "last_name": "Иванов"},
            {"username": "User2", "first_name": "Мария", "last_name": "Петрова"},
            {"username": "User3", "first_name": "Алексей", "last_name": "Сидоров"},
        ]
        created_users = {}
        for u in users_data:
            user, created = User.objects.get_or_create(username=u["username"], defaults=u)
            if created:
                if u.get("is_superuser"):
                    user.set_password("admin123")
                    user.save()
                    self.stdout.write(f"Created superuser {u['username']}/admin123")
                else:
                    user.set_password("123")
                    user.save()
                    self.stdout.write(f"Created user {u['username']}/123")
            created_users[u["username"]] = user

        admin_user = created_users["admin"]

        # -------------------- STATUSES --------------------
        status_names = ["Новая", "В процессе", "Завершена"]
        statuses = []
        for s in status_names:
            status, _ = Status.objects.get_or_create(name=s)
            statuses.append(status)
        self.stdout.write("Created statuses")

        # -------------------- LABELS --------------------
        label_names = ["важно", "желательно", "Umbrella", "SpaceX"]
        labels = []
        for l in label_names:
            label, _ = Label.objects.get_or_create(name=l)
            labels.append(label)
        self.stdout.write("Created labels")

        # -------------------- TASKS --------------------
        for username, user in created_users.items():
            if username == "admin":
                continue  # не создаем задачи для админа
            task_name = f"Задача для {username}"
            if not Task.objects.filter(name=task_name).exists():
                task = Task.objects.create(
                    name=task_name,
                    description=f"Это пример задачи для {username}",
                    status=random.choice(statuses),
                    author=admin_user,
                    executor=user,
                    deadline=timezone.now() + timezone.timedelta(days=random.randint(1, 10))
                )
                # случайные метки (1-3 на задачу)
                task.labels.set(random.sample(labels, k=random.randint(1, 3)))
                task.save()
                self.stdout.write(f"Created task for {username}")
