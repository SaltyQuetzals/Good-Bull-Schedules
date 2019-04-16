import asyncio
import concurrent
import re
import time
from typing import Dict, List, Set, Tuple

import bs4
import requests
from django.core.management import base
from django.db import transaction

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


def parse_courseblocktitle(courseblocktitle: bs4.BeautifulSoup) -> Tuple[str, str, str]:
    """Parses the course number and course name from a .courseblocktitle element.
    
    Args:
        courseblocktitle: A BeautifulSoup instance around the .courseblocktitle element of a .courseblock elem.
    Returns:
        A tuple of format (Course number, Course name).
    """
    COURSE_NUM_NAME_PATTERN = re.compile(
        "(?P<dept>[a-zA-Z]{3,4}[0-9]?) (?P<course_num>[0-9]{3,4}[a-zA-Z]?) (?P<name>.*)"
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
        A triple of format (min_credits, max_hours, Number of hours in lecture, lab, etc.)
    """
    CREDITS_PATTERN = re.compile(
        r"Credits? (?P<min>[\d.]{1,3})(?:(?:-| to | or )(?P<max>[\d.]{1,3}))?.(?P<distribution>$|.*)"
    )
    hours_text = hours.select_one("strong").text
    hours_text = sanitize(hours_text)
    results = re.findall(CREDITS_PATTERN, hours_text)[0]
    min_credits = max_hours = distribution = None
    min_credits, max_hours, distribution = results
    distribution = distribution.strip()
    min_credits = float(min_credits)
    if max_hours:
        max_hours = float(max_hours)
    else:
        max_hours = min_credits
    return (min_credits, max_hours, distribution)


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
    dept, course_num, name = results
    hours = courseblock.select_one(".hours")
    min_credits, max_credits, distribution_of_hours = parse_hours(hours)
    courseblockdesc = courseblock.select_one(".courseblockdesc")
    description, prerequsites, corequisites = parse_description(courseblockdesc)
    return {
        "dept": dept,
        "course_num": course_num,
        "name": name,
        "min_credits": min_credits,
        "max_credits": max_credits,
        "distribution_of_hours": distribution_of_hours,
        "description": description if description else None,
        "prerequisites": prerequsites,
        "corequisites": corequisites,
    }


async def scrape_departments(url_dept_pairs: List[Tuple[str, str]]):
    with concurrent.futures.ProcessPoolExecutor() as executor:
        loop = asyncio.get_event_loop()
        futures = [
            loop.run_in_executor(executor, requests.get, BASE_URL + url)
            for url, _ in url_dept_pairs
        ]
        parameters = []
        for response in await asyncio.gather(*futures):
            soup = bs4.BeautifulSoup(response.text, "lxml")
            for courseblock in soup.select(".courseblock"):
                results = parse_courseblock(courseblock)
                if results:
                    dept, course_num = results["dept"], results["course_num"]
                    _id = "%s-%s" % (dept, course_num)
                    parameters.append((_id, results))
        return parameters


class Command(base.BaseCommand):
    help = "Scrapes course data from catalog.tamu.edu"

    def handle(self, *args, **options):
        start = time.time()
        for level in EDUCATION_LEVELS:
            level_start = time.time()
            description_url = DEPARTMENT_LIST_URL % level
            course_description_html = request_html(description_url)
            url_dept_pairs = collect_departments(course_description_html)
            loop = asyncio.get_event_loop()
            parameters = loop.run_until_complete(scrape_departments(url_dept_pairs))
            with transaction.atomic():
                for params in parameters:
                    _id, rest = params
                    course = scraper_models.Course(id=_id, **rest)
                    course.save()
        end = time.time()
        print("Finished scraping courses in %s seconds" % (end - start))
