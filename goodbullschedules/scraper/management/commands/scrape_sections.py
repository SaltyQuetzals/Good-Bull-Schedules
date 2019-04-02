from django.core.management import base
from django.db import transaction

from scraper.management.commands import shared_functions, section_parser as parser
from scraper import models as scraper_models


class Command(base.BaseCommand):
    def handle(self, *args, **options):
        for term_code in shared_functions.term_codes():
            print("----------------------")
            print(term_code)
            print("----------------------")
            for dept in shared_functions.depts(term_code):
                print(dept)
                soup = shared_functions.sections(term_code, dept)
                results = parser.parse_sections(soup)

                with transaction.atomic():
                    for section_fields, meeting_fields in results:
                        section_id = f"{section_fields['crn']}_{term_code}"
                        section, _ = scraper_models.Section.objects.update_or_create(
                            id=section_id,
                            defaults={
                                "term_code": int(term_code),
                                "dept": dept,
                                **section_fields,
                            },
                        )
                        if meeting_fields:
                            for i, m in enumerate(meeting_fields):
                                meeting_id = section_id + "_" + str(i + 1)
                                if len(meeting_id) > 30:
                                    print(meeting_id, len(meeting_id))
                                    return
                                meeting, _ = scraper_models.Meeting.objects.update_or_create(
                                    id=meeting_id, defaults={**m}
                                )
                                section.meetings.add(meeting)
