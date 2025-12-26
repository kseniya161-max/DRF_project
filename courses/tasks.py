from celery import shared_task
from config .settings import EMAIL_HOST_USER
from django.conf import settings
from django.core.mail import send_mail



@shared_task
def send_information(email):
    if email:
        send_mail('Новая подписка', 'Вы обновили подписку', EMAIL_HOST_USER, [email])
    else:
        raise ValueError("Email не может быть пустым")