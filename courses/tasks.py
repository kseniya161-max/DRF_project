
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import get_object_or_404

from courses.models import Course, Subscription


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





