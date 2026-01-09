from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from courses.models import Lesson, Course, Subscription
from users.models import User


class LessonSubscriptionTest(APITestCase):
    def setUp(self):
        """Создаем значения"""
        self.user = User.objects.create(email="admin_3@mail.ru")
        self.course = Course.objects.create(name="Английский", owner=self.user)
        self.lesson = Lesson.objects.create(
            title="Elementary",
            course=self.course,
            owner=self.user,
            link="https://youtube.com/video1",
            description="Elementary",
        )
        self.client.force_authenticate(user=self.user)

    def test_lesson_retrieve(self):
        url = reverse("courses:lesson_retrieve", args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data.get("title"), self.lesson.title)

    def test_lesson_create(self):
        url = reverse("courses:lesson_create")
        data = {
            "title": "Испанский",
            "course": self.course.pk,
            "link": "http://youtube.com/video",
        }
        response = self.client.post(url, data)
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
            msg=f"Response data: {response.data}",
        )

        self.assertEqual(Lesson.objects.count(), 2)

    def test_lesson_update(self):
        url = reverse("courses:lesson_update", args=(self.lesson.pk,))
        data = {
            "title": "Китайский",
        }
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lesson.refresh_from_db()
        self.assertEqual(response.data.get("title"), "Китайский")

    def test_lesson_delete(self):
        url = reverse("courses:lesson_delete", args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.count(), 0)

    def test_lesson_list(self):
        url = reverse("courses:lesson_list")
        response = self.client.get(url)
        data = response.json()
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.lesson.pk,
                    "courses": [self.course.name],
                    "link": self.lesson.link,
                    "title": self.lesson.title,
                    "description": self.lesson.description,
                    "preview": None,
                    "course": self.course.pk,
                    "owner": self.user.pk,
                }
            ],
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("count", data)
        self.assertIn("results", data)
        self.assertIsInstance(data["results"], list)
        self.assertEqual(data, result)

    def test_subscription(self):
        url = reverse("courses:subscription-list")
        data = {"course_id": self.course.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Новая подписка добавлена")
        self.assertTrue(
            Subscription.objects.filter(user=self.user, course=self.course).exists()
        )

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Подписка удалена")
        self.assertFalse(
            Subscription.objects.filter(user=self.user, course=self.course).exists()
        )
