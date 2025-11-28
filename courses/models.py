from django.db import models

class Course(models.Model):
    "Модель Курса"
    name = models.CharField(max_length=150, unique=True, help_text='Название')
    preview = models.ImageField(upload_to='courses/images', help_text='Изображение')
    description = models.TextField(max_length=300, blank=True, null=True, help_text='Введите описание')

    def __str__(self):
        return self.name


class Meta:
    verbose_name = "Курс"
    verbose_name_plural = "Курсы"