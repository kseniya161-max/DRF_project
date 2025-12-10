from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from courses.models import Lesson, Course
from users.models import User


class LessonSubscriptionTest(APITestCase):
    def setUp(self):
        """Создаем значения"""
        self.user = User.objects.create(email="admin_3@mail.ru")
        self.course = Course.objects.create(name="Английский", owner=self.user)
        self.lesson = Lesson.objects.create(title="Elementary", course=self.course, owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_lesson_retrieve(self):
        url = reverse("courses:lesson_retrieve", args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
            )

        self.assertEqual(
            response.data.get("title"), self.lesson.title

            )




