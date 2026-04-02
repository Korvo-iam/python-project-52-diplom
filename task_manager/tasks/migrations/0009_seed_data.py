# Generated manually for seeding example data
from django.db import migrations
from django.utils import timezone
import random

def create_seed_data(apps, schema_editor):
    User = apps.get_model('users', 'User')
    Status = apps.get_model('statuses', 'Status')
    Label = apps.get_model('labels', 'Label')
    Task = apps.get_model('tasks', 'Task')

    # ---- Статусы ----
    statuses = ["Новая", "В работе", "На проверке", "Готово"]
    status_objs = []
    for s in statuses:
        obj, _ = Status.objects.get_or_create(name=s)
        status_objs.append(obj)

    # ---- Метки ----
    labels = ["важно", "желательно", "Umbrella", "SpaceX"]
    label_objs = []
    for l in labels:
        obj, _ = Label.objects.get_or_create(name=l)
        label_objs.append(obj)

    # ---- Пользователи ----
    users_data = [
        {"username": "admin", "first_name": "Admin", "last_name": "User", "is_superuser": True, "is_staff": True, "password": "admin123"},
        {"username": "User1", "first_name": "Иван", "last_name": "Иванов", "password": "123"},
        {"username": "User2", "first_name": "Мария", "last_name": "Петрова", "password": "123"},
        {"username": "User3", "first_name": "Алексей", "last_name": "Сидоров", "password": "123"},
    ]
    created_users = {}
    for u in users_data:
        user, created = User.objects.get_or_create(username=u["username"], defaults=u)
        if created:
            user.set_password(u["password"])
            user.save()
        created_users[u["username"]] = user

    admin_user = created_users["admin"]
    all_users = [created_users["User1"], created_users["User2"], created_users["User3"]]

    # ---- Задачи ----
    for user in all_users:
        task_name = f"Пример задачи для {user.username}"
        task, created = Task.objects.get_or_create(
            name=task_name,
            defaults={
                "description": f"Описание задачи для {user.username}",
                "status": random.choice(status_objs),
                "author": admin_user,
                "executor": user,
                "deadline": timezone.now() + timezone.timedelta(days=random.randint(1,10)),
            }
        )
        if created:
            task.labels.set(random.sample(label_objs, k=random.randint(1,3)))
            task.save()

class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0008_task_deadline'),
        ('users', '0001_initial'),
        ('statuses', '0003_alter_status_name'),
        ('labels', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_seed_data),
    ]
