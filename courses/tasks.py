
from datetime import timedelta, timezone
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings



@shared_task
def send_information(email):
    print(f"Получен email для отправки: {email}")
    if not email:
        raise ValueError("Email не может быть пустым")
    send_mail(
        'Новая подписка',
        'Вы обновили подписку',
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False,
    )


@shared_task
def check_user_activity():
    print("Задача check_user_activity запущена.")
    from users.models import User
    now = timezone.now()
    inactive_users = User.objects.filter(last_login__lt=now - timezone.timedelta(days=30), is_active=True)

    for user in inactive_users:
        user.is_active = False
        user.save()
        print(f"Пользователь {user.username} был заблокирован.")


