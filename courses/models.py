from django.db import models

class Course(models.Model):
    "Модель Курса"

    name = models.CharField(max_length=150, unique=True, help_text="Название")
    preview = models.ImageField(
        upload_to="courses/images", blank=True, null=True, help_text="Изображение"
    )
    description = models.TextField(
        max_length=300, blank=True, null=True, help_text="Введите описание"
    )
    owner = models.ForeignKey('users.User', null = True, on_delete=models.CASCADE, related_name='courses')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


class Lesson(models.Model):
    "Модель Урок"

    title = models.CharField(max_length=150, unique=True, help_text="Название")
    description = models.TextField(
        max_length=300, blank=True, null=True, help_text="Введите описание"
    )
    preview = models.ImageField(
        upload_to="courses/images", blank=True, null=True, help_text="Изображение"
    )
    link = models.URLField(blank=True, null=True, help_text="Видео")
    course = models.ForeignKey(Course, related_name="lessons", on_delete=models.CASCADE)
    owner = models.ForeignKey('users.User', null = True, on_delete=models.CASCADE, related_name='lesson')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
