from rest_framework.test import APITestCase

from courses.models import Lesson, Course
from users.models import User


class LessonSubscriptionTest(APITestCase):
    def setUp(self):
        """Создаем значения"""
        self.user = User.objects.create(email="admin_3@mail.ru")
        self.lesson = Lesson.objects.create(title="Elementary")
        self.course = Course.objects.create(name="Английский", owner=self.user)
        self.client.force_authenticate(user=self.user)



