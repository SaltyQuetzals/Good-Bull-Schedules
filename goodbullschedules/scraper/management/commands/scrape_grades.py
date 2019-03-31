from django.core.management import base
from scraper import models as scraper_models
from scraper.management.commands import shared_functions, pdf_parser

import requests
from typing import List
import bs4
import os


ROOT_URL = "http://web-as.tamu.edu/gradereport/"
PDF_URL = "http://web-as.tamu.edu/gradereport/PDFReports/{}/grd{}{}.pdf"
PDF_DOWNLOAD_DIR = os.path.abspath("documents/pdfs")

SPRING, SUMMER, FALL = "1", "2", "3"


def years() -> List[int]:
    r = requests.get(ROOT_URL)
    r.raise_for_status()

    soup = bs4.BeautifulSoup(r.text, "lxml")
    options = soup.select("#ctl00_plcMain_lstGradYear > option")
    return [int(o["value"]) for o in options]


def colleges() -> List[str]:
    r = requests.get(ROOT_URL)
    r.raise_for_status()

    soup = bs4.BeautifulSoup(r.text, "lxml")
    options = soup.select("#ctl00_plcMain_lstGradCollege > option")
    return [o["value"] for o in options]


def download_pdf(year_semester: str, college: str) -> str:
    """Downloads a PDF from the given URL.

    Args:
        year_semester: A 4-digit year, followed by an integer indicating            semester
        college: The abbreviation for the college, as found on the registrar
    Returns:
        The path to the downloaded PDF file.
    """
    url = PDF_URL.format(year_semester, year_semester, college)
    filename = url.split("/")[-1]
    path = os.path.join(PDF_DOWNLOAD_DIR, filename)

    r = requests.get(url)
    try:
        r.raise_for_status()
        if os.path.isfile(path):
            return path
        with open(path, "wb+") as f:
            f.write(r.content)
            return path
    except requests.exceptions.HTTPError as e:
        if e.response.status_code != 404:
            raise e


def build_term_code(year_semester: str, abbr: str) -> str:
    """Creates a term_code from a year + semester string and an abbreviation.
    Args:
        year_semester: A string in the format "YYYYS" where Y=year and S is in {1, 2, 3}
        abbr: A short code indicating what college is being parsed.
    Returns:
        A 6-char string whose digits are: YYYYSU where U is in {1, 2, 3}
    """
    if abbr != "GV" and abbr != "QT":
        return year_semester + "1"
    else:
        if abbr == "GV":
            return year_semester + "2"
        else:
            return year_semester + "3"


class Command(base.BaseCommand):
    def handle(self, *args, **kwargs):
        yrs = years()
        college_abbrevs = colleges()
        for year in yrs:
            for semester in [SPRING, SUMMER, FALL]:
                year_semester = str(year) + semester
                print(year_semester)
                for college in college_abbrevs:
                    print(college)
                    term_code = build_term_code(year_semester, college)
                    pdf_path = download_pdf(year_semester, college)
                    if pdf_path:
                        distribution_fields = pdf_parser.parse_pdf(pdf_path)

                        for dist in distribution_fields:
                            grades, (dept, course_num, section_num), gpa = dist
                            section = scraper_models.Section.objects.filter(
                                dept=dept,
                                course_num=course_num,
                                section_num=section_num,
                                term_code=int(term_code),
                            ).first()

                            if section:
                                grades, _ = scraper_models.Grades.objects.update_or_create(
                                    section=section, defaults={**grades, "gpa": gpa}
                                )
                                section.grades = grades
