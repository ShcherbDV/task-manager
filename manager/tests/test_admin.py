from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from manager.models import Position


class AdminSiteTests(TestCase):
    def setUp(self):
        self.admin_user = get_user_model().objects.create_superuser(
            username="superuser", password="testadmin", email="test@gmail.com"
        )
        self.client.force_login(self.admin_user)
        position = Position.objects.create(name="test")
        self.worker = get_user_model().objects.create_user(
            username="testuser",
            password="test1234",
            position=position,
            email="driver@gmail.com",
        )

    def test_worker_position_listed(self):
        url = reverse("admin:manager_worker_changelist")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, self.worker.position_id)
