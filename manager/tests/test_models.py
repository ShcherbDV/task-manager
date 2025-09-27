from django.contrib.auth import get_user_model
from django.test import TestCase

from manager.models import Task, TaskType, Position


class ModelsTests(TestCase):
    def test_task_str(self):
        task_type = TaskType.objects.create(name="test_name")
        task = Task.objects.create(
            name="test",
            deadline="2035-09-29 19:55:55",
            priority="urgent",
            task_type=task_type,
        )
        self.assertEqual(str(task), f"{task.name} ({task.get_priority_display()})")

    def test_task_type_str(self):
        task_type = TaskType.objects.create(name="test_name")
        self.assertEqual(str(task_type), task_type.name)

    def test_worker_str(self):
        position = Position.objects.create(name="test")
        worker = get_user_model().objects.create_user(
            username="test_user",
            first_name="test_name",
            last_name="test_last_name",
            email="test@gmail.com",
            password="test1234",
            position=position,
        )
        self.assertEqual(
            str(worker),
            f"{worker.username} ({worker.first_name} {worker.last_name} - {worker.position})",
        )
