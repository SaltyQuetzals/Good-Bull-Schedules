from django.test import TestCase
from rest_framework import status
from django.contrib.auth import models as auth_models
from rest_framework.test import APIClient
from scheduler import views
from scheduler import models as scheduler_models
from scraper import models as scraper_models

# Create your tests here.
class SchedulerViewsTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.user_creds = {"username": "test", "password": "12345"}
        self.user2_creds = {"username": "test2", "password": "54321"}
        self.user = auth_models.User.objects.create_user(**self.user_creds)
        self.user2 = auth_models.User.objects.create_user(**self.user2_creds)

        self.schedule_fields = {"name": "Schedule", "term_code": 201931}

        self.dummy_section_id = "10001_201931"
        self.dummy_section_fields = {
            "id": self.dummy_section_id,
            "name": "",
            "term_code": 201931,
            "crn": 10001,
            "dept": "ACCT",
            "course_num": "209",
            "section_num": "500",
            "min_credits": 0.0,
            "max_credits": 1.0,
        }
        self.dummy_section = scraper_models.Section.objects.create(
            **self.dummy_section_fields
        )

        self.dummy_section2_id = "10001_201831"
        self.dummy_section2_fields = {
            "id": self.dummy_section2_id,
            "name": "",
            "term_code": 201831,
            "crn": 10001,
            "dept": "ACCT",
            "course_num": "209",
            "section_num": "500",
            "min_credits": 0.0,
            "max_credits": 1.0,
        }

        self.dummy_section2 = scraper_models.Section.objects.create(
            **self.dummy_section2_fields
        )

        self.dummy_course = scraper_models.Course.objects.create(
            id="ACCT-209",
            dept="ACCT",
            course_num="209",
            name="",
            description="",
            prerequisites="",
            corequisites="",
            min_credits=0.0,
            max_credits=1.0,
            distribution_of_hours="",
        )

    def create_schedule(self, user, fields):
        schedule = scheduler_models.Schedule.objects.create(**fields, owner=user)
        schedule.full_clean()
        return schedule

    def post_create_schedule(self, creds, fields):
        self.client.login(**self.user_creds)
        response = self.client.post("/api/schedules/", fields)
        self.client.logout()
        return response

    def test_cant_create_schedule_without_auth(self):
        response = self.client.post("/api/schedules/", self.schedule_fields)
        self.assertFalse(status.is_success(response.status_code))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_can_create_schedule_with_auth(self):
        self.post_create_schedule(self.user_creds, self.schedule_fields)
        created_schedule = scheduler_models.Schedule.objects.get(**self.schedule_fields)
        self.assertEqual(created_schedule.name, self.schedule_fields["name"])
        self.assertEqual(created_schedule.term_code, self.schedule_fields["term_code"])

    def test_only_owner_can_access_schedule(self):
        schedule = self.create_schedule(self.user, self.schedule_fields)
        self.client.login(**self.user2_creds)
        response = self.client.get(f"/api/schedules/{schedule.pk}")
        self.assertFalse(status.is_success(response.status_code))
        self.client.logout()

        response = self.client.get(f"/api/schedules/{schedule.pk}")
        self.assertFalse(status.is_success(response.status_code))

        self.client.login(**self.user_creds)
        response = self.client.get(f"/api/schedules/{schedule.pk}")
        self.assertTrue(status.is_success(response.status_code))

    def test_delete_schedule(self):
        schedule = self.create_schedule(self.user, self.schedule_fields)
        self.client.login(**self.user_creds)
        response = self.client.delete(f"/api/schedules/{schedule.pk}")
        self.assertTrue(status.is_success(response.status_code))
        self.assertFalse(
            scheduler_models.Schedule.objects.filter(**self.schedule_fields).exists()
        )

    def test_only_owner_can_delete_schedule(self):
        schedule = self.create_schedule(self.user, self.schedule_fields)
        self.client.login(**self.user2_creds)
        response = self.client.delete(f"/api/schedules/{schedule.pk}")
        self.assertFalse(status.is_success(response.status_code))
        self.client.logout()

        response = self.client.delete(f"/api/schedules/{schedule.pk}")
        self.assertFalse(status.is_success(response.status_code))

    def test_can_add_section_to_schedule(self):
        schedule = self.create_schedule(self.user, self.schedule_fields)
        self.client.login(**self.user_creds)
        response = self.client.patch(
            f"/api/schedules/{schedule.pk}/sections",
            {"section_id": self.dummy_section.id},
        )
        self.assertTrue(status.is_success(response.status_code))

        schedule = scheduler_models.Schedule.objects.get(pk=schedule.pk)

        self.assertEqual(len(schedule.sections.all()), 1)
        self.assertEqual(schedule.sections.first(), self.dummy_section)
        self.assertEqual(schedule.courses.first(), self.dummy_course)

    def test_add_section_with_mismatch_term_code(self):
        schedule = self.create_schedule(self.user, self.schedule_fields)
        self.client.login(**self.user_creds)
        response = self.client.patch(
            f"/api/schedules/{schedule.pk}/sections",
            {"section_id": self.dummy_section2_id},
        )
        self.assertFalse(status.is_success(response.status_code))
        json = response.json()
        self.assertEqual(
            json["msg"], "The section must belong to the same term as the schedule."
        )

    def test_retrieval_after_adding_section(self):
        schedule = self.create_schedule(self.user, self.schedule_fields)
        self.client.login(**self.user_creds)
        self.client.patch(
            f"/api/schedules/{schedule.pk}/sections",
            {"section_id": self.dummy_section_id},
        )
        response = self.client.get(f"/api/schedules/{schedule.pk}")
        json = response.json()
        self.assertIn(self.dummy_course.id, json["courses"])
        self.assertIn(self.dummy_section_id, json["sections"])

    def test_only_owner_can_add_section_to_schedule(self):
        schedule = self.create_schedule(self.user, self.schedule_fields)
        self.client.login(**self.user2_creds)
        response = self.client.patch(
            f"/api/schedules/{schedule.pk}/sections",
            {"section_id": self.dummy_section_id},
        )
        self.assertFalse(status.is_success(response.status_code))
        self.client.logout()

        response = self.client.patch(
            f"/api/schedules/{schedule.pk}/sections",
            {"section_id": self.dummy_section_id},
        )
        self.assertFalse(status.is_success(response.status_code))

    def test_can_delete_section_from_schedule(self):
        schedule = self.create_schedule(self.user, self.schedule_fields)
        schedule.sections.add(self.dummy_section)
        schedule.courses.add(self.dummy_course)
        self.client.login(**self.user_creds)
        response = self.client.delete(
            f"/api/schedules/{schedule.pk}/sections/{self.dummy_section_id}"
        )
        self.assertTrue(status.is_success(response.status_code))
        schedule = scheduler_models.Schedule.objects.get(pk=schedule.pk)
        self.assertEqual(len(schedule.sections.all()), 0)
        self.assertNotEqual(len(schedule.courses.all()), 0)

    def test_only_owner_can_delete_section_from_schedule(self):
        schedule = self.create_schedule(self.user, self.schedule_fields)
        schedule.sections.add(self.dummy_section)
        schedule.courses.add(self.dummy_course)

        self.client.login(**self.user2_creds)
        response = self.client.delete(
            f"/api/schedules/{schedule.pk}/sections/{self.dummy_section_id}"
        )
        self.assertFalse(status.is_success(response.status_code))
        self.client.logout()

        response = self.client.delete(
            f"/api/schedules/{schedule.pk}/sections/{self.dummy_section_id}"
        )
        self.assertFalse(status.is_success(response.status_code))
