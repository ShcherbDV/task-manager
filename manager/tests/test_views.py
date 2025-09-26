from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from manager.models import TaskType, Task, Position


class SearchTests(TestCase):
    def setUp(self):
        self.task_type1 = TaskType.objects.create(
            name="Test Type"
        )

        self.task_type2 = TaskType.objects.create(
            name="Another Type"
        )

        self.task1 = Task.objects.create(
            name="Test task", task_type=self.task_type1, deadline="2035-09-29 19:55:55", priority="urgent",
        )
        self.task2 = Task.objects.create(
            name="Another task", task_type=self.task_type2, deadline="2035-09-29 19:55:55", priority="urgent",
        )

        position = Position.objects.create(name="Test Position")

        self.user1 = get_user_model().objects.create_user(
            username="Test User",
            email="test2@mail.com",
            password="test1234!",
            position=position,
        )
        self.user2 = get_user_model().objects.create_user(
            username="Another",
            email="test2@mail.com",
            password="test12345!",
            position=position,
        )

        self.client.force_login(self.user1)

    def test_task_name_search(self):
        url = reverse("manager:task-list")
        response = self.client.get(url, {"name": "Test task"})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test task")
        self.assertNotContains(response, "Another task")

    def test_task_name_search_with_no_data(self):
        url = reverse("manager:task-list")
        response = self.client.get(url, {"name": ""})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test task")
        self.assertContains(response, "Another task")

    def test_worker_username_search(self):
        url = reverse("manager:worker-list")
        response = self.client.get(url, {"username": "Test User"})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test User")
        self.assertNotContains(response, "Another")

    def test_worker_username_search_with_no_search_data(self):
        url = reverse("manager:worker-list")
        response = self.client.get(url, {"username": ""})
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, "Test User")
        self.assertContains(response, "Another")
