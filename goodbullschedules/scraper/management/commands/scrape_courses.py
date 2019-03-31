import re
from typing import Dict, List, Set, Tuple

import bs4
from django.core.management import base

from scraper import models as scraper_models
from scraper.management.commands.shared_functions import request_html

BASE_URL = "http://catalog.tamu.edu/"

EDUCATION_LEVELS = ["undergraduate", "graduate"]
DEPARTMENT_LIST_URL = BASE_URL + "%s/course-descriptions"


def sanitize(string: str) -> str:
    string = re.sub(r"\s+", " ", string)
    return "".join([i if ord(i) < 128 else " " for i in string]).strip()


def collect_departments(dept_list_html: bs4.BeautifulSoup) -> List[Tuple[str, str]]:
    """Given html from dept list page, extract all depts listed and their urls.

    Args:
        dept_list_html: The HTML from the department list page, as a BeautifulSoup instance.
    Returns:
        A list of tuples of format (URL path, dept abbreviation)
    """
    a_elements = dept_list_html.select("#atozindex > ul > li > a")
    url_dept_pairs = []
    for a in a_elements:
        try:
            ABBR_PATTERN = re.compile("(?P<dept>^[a-zA-Z]{3,4})")
            dept_abbr = re.findall(ABBR_PATTERN, a.text)[0]
            url_dept_pairs.append((a["href"], dept_abbr))
        except Exception as e:
            raise e
    return url_dept_pairs


def parse_courseblocktitle(courseblocktitle: bs4.BeautifulSoup) -> Tuple[str, str]:
    """Parses the course number and course name from a .courseblocktitle element.
    
    Args:
        courseblocktitle: A BeautifulSoup instance around the .courseblocktitle element of a .courseblock elem.
    Returns:
        A tuple of format (Course number, Course name).
    """
    COURSE_NUM_NAME_PATTERN = re.compile(
        "(?:[a-zA-Z]{3,4}[0-9]?) (?P<course_num>[0-9]{3,4}[a-zA-Z]?) (?P<name>.*)"
    )
    title_text = courseblocktitle.select_one("strong").text
    title_text = sanitize(title_text)
    try:
        return re.findall(COURSE_NUM_NAME_PATTERN, title_text)[0]
    except Exception:
        print(title_text)


def parse_hours(hours: bs4.BeautifulSoup) -> Tuple[int, int, str]:
    """Extracts min, max number of hours, and their distribution, from a .hours element.

    Args:
        hours: A BeautifulSoup instance around the .hours element of a .courseblock elem.
    Returns:
        A triple of format (min_hours, max_hours, Number of hours in lecture, lab, etc.)
    """
    CREDITS_PATTERN = re.compile(
        r"Credits? (?P<min>[\d.]{1,3})(?:(?:-| to | or )(?P<max>[\d.]{1,3}))?.(?P<distribution>$|.*)"
    )
    hours_text = hours.select_one("strong").text
    hours_text = sanitize(hours_text)
    results = re.findall(CREDITS_PATTERN, hours_text)[0]
    min_hours = max_hours = distribution = None
    min_hours, max_hours, distribution = results
    distribution = distribution.strip()
    min_hours = float(min_hours)
    if max_hours:
        max_hours = float(max_hours)
    else:
        max_hours = min_hours
    return (min_hours, max_hours, distribution)


def parse_description(courseblockdesc: bs4.BeautifulSoup) -> Tuple[str, str, str]:
    """Extracts the description, prerequisites, and corequisites of a course from an element.

    Args:
        courseblockdesc: A BeautifulSoup instance around the .courseblockdesc element of a .courseblock elem.
    Returns:
        A triple of format (description, prereqs, coreqs)
    """
    DESCRIPTION_PATTERN = re.compile(
        "(?P<description>.+?(?= Prerequisites?: | Corequisites?: | Cross-Listings?: |$))"
    )
    PREREQS_PATTERN = re.compile(
        " Prerequisites?: (?P<prereqs>.+?(?= Corequisites?: | Cross-Listings?: |$))"
    )
    COREQS_PATTERN = re.compile(
        " Corequisites?: (?P<coreqs>.+?(?= Prerequisites?: | Cross-Listings?: |$))"
    )
    description_text = courseblockdesc.text
    description_text = sanitize(description_text)
    description = re.findall(DESCRIPTION_PATTERN, description_text)
    if description:
        description = description[0].strip()
    prereqs = re.findall(PREREQS_PATTERN, description_text)
    if prereqs:
        prereqs = prereqs[0].strip()
    else:
        prereqs = None
    coreqs = re.findall(COREQS_PATTERN, description_text)
    if coreqs:
        coreqs = coreqs[0].strip()
    else:
        coreqs = None
    return description, prereqs, coreqs


def parse_courseblock(courseblock: bs4.BeautifulSoup):
    """Parses a .courseblock element and returns all important information.

    Args:
        courseblock: A BeautifulSoup instance around a .courseblock element.
    Returns:
        A CourseFields (see above definition)
    """
    courseblocktitle = courseblock.select_one(".courseblocktitle")
    results = parse_courseblocktitle(courseblocktitle)
    if not results:
        return
    course_num, name = results
    hours = courseblock.select_one(".hours")
    min_hours, max_hours, distribution = parse_hours(hours)
    courseblockdesc = courseblock.select_one(".courseblockdesc")
    description, prereqs, coreqs = parse_description(courseblockdesc)
    return (
        course_num,
        name,
        min_hours,
        max_hours,
        distribution,
        description if description else None,
        prereqs,
        coreqs,
    )


class Command(base.BaseCommand):
    help = "Scrapes course data from catalog.tamu.edu"

    def handle(self, *args, **options):
        for level in EDUCATION_LEVELS:
            description_url = DEPARTMENT_LIST_URL % level
            course_description_html = request_html(description_url)
            url_dept_pairs = collect_departments(course_description_html)
            for path, dept in url_dept_pairs:
                print(dept)
                url = BASE_URL + path
                soup = request_html(url)
                courseblocks = soup.select(".courseblock")
                for courseblock in courseblocks:
                    results = parse_courseblock(courseblock)
                    if results:
                        course_num, name, min_hours, max_hours, distribution, description, prereqs, coreqs = (
                            results
                        )
                        _id = "%s-%s" % (dept, course_num)
                        scraper_models.Course.objects.update_or_create(
                            id=_id,
                            defaults={
                                "dept": dept,
                                "course_num": course_num,
                                "name": name,
                                "distribution_of_hours": distribution,
                                "description": description,
                                "prerequisites": prereqs,
                                "corequisites": coreqs,
                                "min_credits": min_hours,
                                "max_credits": max_hours,
                            },
                        )
