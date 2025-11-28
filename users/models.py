from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    " Модель Пользователя"

    username = None
    email = models.EmailField(max_length=35, unique=True, help_text="Введите email")
    phone = models.CharField(
        max_length=35, blank=True, null=True, help_text="Введите номер телефона"
    )
    location = models.CharField(
        max_length=50, blank=True, null=True, help_text="Введите город"
    )
    avatar = models.ImageField(
        upload_to="users/avatar", blank=True, null=True, help_text="Загрузите аватар"
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
