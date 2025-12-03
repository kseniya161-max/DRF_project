from django.contrib.auth.models import AbstractUser
from django.db import models

from courses.models import Course, Lesson


class User(AbstractUser):
    "Модель Пользователя"

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

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Payments(models.Model):
    """Модель Платежей"""

    username = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="payments",
        help_text="Пользователь",
    )
    payment_date = models.DateTimeField(auto_now_add=True)
    paid_course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        help_text="Оплаченый курс",
    )
    paid_lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        help_text="Оплаченый курс урок",
    )
    sum = models.DecimalField(max_digits=10, decimal_places=2, help_text="Сумма оплаты")
    payment_detail = models.CharField(
        max_length=100, help_text="Наличные или перевод на счет"
    )

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"
        unique_together = ("username", "paid_course", "paid_lesson")

    def __str__(self):
        return f"{self.username} - {self.sum} - {self.payment_date}"
