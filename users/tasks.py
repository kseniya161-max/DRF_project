from celery import shared_task
from datetime import timedelta
from users.models import User
from django.utils import timezone


@shared_task
def check_user_activity():
    print("Задача check_user_activity запущена.")
    inactive_users = User.objects.filter(
        last_login__lt=timezone.now() - timedelta(days=30), is_active=True
    )

    for user in inactive_users:
        user.is_active = False
        user.save()
        print(f"Пользователь {user.username} был заблокирован.")
