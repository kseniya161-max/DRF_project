from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse


class CourseAPITests(APITestCase):
    def setUp(self):
        self.url = reverse(
            "course-list"
        )  # Используем именно имя маршрута, не маршрут для reverse

    def test_create_and_get_course(self):
        data = {
            "name": "Тестовый курс для теста",
            "description": "Описание тестового курса для теста",
            "owner": 1,
        }

        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, "Тестовый курс для теста")
