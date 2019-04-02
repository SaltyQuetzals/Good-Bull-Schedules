from django.test import TestCase, Client
from scraper.models import Course, Section


class CourseRetrievalTestCase(TestCase):
    def setUp(self):
        self.course = Course(
            id="DEPT-CRS",
            dept="DEPT",
            course_num="CRS",
            name="An informative name",
            description="",
            prerequisites="",
            corequisites="",
            min_credits=0.0,
            max_credits=4.0,
            distribution_of_hours="",
        )
        self.course.save()

        self.section = Section(
            id="123456_123456",
            name="",
            term_code=123456,
            crn=123456,
            dept="DEPT",
            course_num="CRS",
            section_num="101",
            min_credits=0.0,
            max_credits=4.0,
            instructor="John Doe",
        )

        self.section2 = Section(
            id="123456_654321",
            name="",
            term_code=654321,
            crn=123456,
            dept="DEPT",
            course_num="CRS",
            section_num="101",
            min_credits=0.0,
            max_credits=4.0,
            instructor="Jane Doe",
        )

        self.section.save()
        self.section2.save()

        self.client = Client()

        self.dept = "DEPT"
        self.course_num = "CRS"

    def test_retrieves_correct_course(self):
        json = self.client.get(f"/api/data/{self.dept}/{self.course_num}/123456").json()

        self.assertEqual(json["dept"], self.dept)
        self.assertEqual(json["course_num"], self.course_num)

    def test_retrieves_sections(self):
        json = self.client.get(f"/api/data/{self.dept}/{self.course_num}/123456").json()
        self.assertGreater(len(json["sections"]), 0)

    def test_retrieves_only_sections_in_term_code(self):
        json = self.client.get(f"/api/data/{self.dept}/{self.course_num}/123456").json()
        self.assertEqual(len(json["sections"]), 1)
        self.assertEqual(json["sections"][0]["term_code"], 123456)

    def test_retrieves_empty_list_if_no_relevant_sections(self):
        json = self.client.get(f"/api/data/{self.dept}/{self.course_num}/222222").json()
        self.assertIn("sections", json)
        self.assertEqual(len(json["sections"]), 0)
