from django.test import TestCase

from manager.forms import (
    TaskNameSearchForm,
    WorkerUsernameSearchForm,
)


class FormsTests(TestCase):
    def test_task_name_search_form_is_valid(self):
        form_data = {"name": "test"}
        form = TaskNameSearchForm(data=form_data)

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["name"], form_data["name"])

    def test_worker_username_search_form_is_valid(self):
        form_data = {"username": "test_username"}
        form = WorkerUsernameSearchForm(data=form_data)

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["username"], form_data["username"])
