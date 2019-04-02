from django.test import TestCase
from rest_framework import status
from django.contrib.auth import models as auth_models
from rest_framework.test import APIClient
from scheduler import views

# Create your tests here.
class SchedulerViewsTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.user_creds = {"username": "test", "password": "12345"}
        self.user = auth_models.User.objects.create_user(**self.user_creds)

    def test_cant_create_schedule_without_auth(self):
        response = self.client.post(
            "/api/schedules/", {"name": "Schedule Name", "term_code": 201931}
        )
        self.assertTrue(not status.is_success(response.status_code))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_can_create_schedule_with_auth(self):
        self.client.login(**self.user_creds)
        response = self.client.post(
            "/api/schedules/", {"name": "Schedule Name", "term_code": 201931}
        )
        self.assertTrue(status.is_success(response.status_code))
