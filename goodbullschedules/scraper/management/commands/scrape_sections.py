import asyncio

from django.core.management import base
from django.db import transaction

from scraper import models as scraper_models
from scraper.management.commands import section_parser as parser
from scraper.management.commands import shared_functions
from typing import List
import concurrent


async def scrape_departments(term_code: int, depts: List[str]):
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        loop = asyncio.get_event_loop()
        futures = [
            loop.run_in_executor(executor, shared_functions.sections, term_code, dept)
            for dept in depts
        ]
        parameters = []
        for soup in await asyncio.gather(*futures):
            if not soup:
                continue
            results = parser.parse_sections(soup)
            parameters += results
        return parameters


class Command(base.BaseCommand):
    def handle(self, *args, **options):
        for term_code in shared_functions.term_codes():
            print("----------------------")
            print(term_code)
            print("----------------------")
            loop = asyncio.get_event_loop()
            depts = shared_functions.depts(term_code)
            parameters = loop.run_until_complete(scrape_departments(term_code, depts))
            with transaction.atomic():
                courses = {}
                for section_fields, meeting_fields in parameters:
                    section_id = f"{section_fields['crn']}_{term_code}"
                    course_id = (
                        f"{section_fields['dept']}-{section_fields['course_num']}"
                    )
                    if not course_id in courses:
                        course = scraper_models.Course.objects.filter(
                            id=course_id
                        ).first()
                        if course:
                            courses[course_id] = course
                        else:
                            course = scraper_models.Course(
                                id=course_id,
                                default={
                                    "dept": section_fields["dept"],
                                    "course_num": section_fields["course_num"],
                                    "min_credits": section_fields["min_credits"],
                                    "max_credits": section_fields["max_credits"],
                                    "name": section_fields["name"].title(),
                                },
                            )
                            course.save()
                            courses[course_id] = course
                    section = scraper_models.Section(
                        id=section_id,
                        defaults={"term_code": int(term_code), **section_fields},
                    )
                    section.save()

