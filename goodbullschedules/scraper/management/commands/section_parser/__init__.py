import collections
from datetime import time
from typing import Dict, List, Tuple, Any
import re

import bs4


from .body_functions import (
    has_primary_indicator,
    is_tba,
    parse_dddefault,
    strip_primary_indicator,
)
from .title_functions import parse_ddtitle


def reduce_whitespace(string: str) -> str:
    return re.sub(r"\s+", " ", string)


def merge_trs(outer_datadisplaytable: bs4.element.Tag) -> List[bs4.BeautifulSoup]:
    """Poorly-designed HTML means TRs need to be merged.
    Args:
        outer_datadisplaytable: A bs4.BeautifulSoup instance
    Returns:
        A list of BeautifulSoup instances representing the merged TRs.
    """
    trs = outer_datadisplaytable.contents[1:]
    trs = [tr for tr in trs if not isinstance(tr, bs4.NavigableString)]
    merged = []
    for tr in trs:
        if tr.select_one("th.ddtitle"):
            merged.append(tr)
        elif tr.select_one("td.dddefault"):
            merged[-1] = bs4.BeautifulSoup(str(merged[-1]) + str(tr), "lxml")
    return merged


def retrieve_instructor(all_mentioned_instructors: List[str]) -> str:
    """Determines which of the instructors mentioned is the primary instructor.
    Args:
        all_mentioned_instructors: Sometimes there are multiple instructors assigned to a section.
    Returns:
        The primary instructor.
    """
    primary_instructor_name = None
    for instructors_mentioned in all_mentioned_instructors:
        instructors_mentioned = instructors_mentioned.split(",")
        for instructor in instructors_mentioned:
            if has_primary_indicator(instructor):
                primary_instructor_name = instructor
                break
    if not primary_instructor_name:
        cnt = collections.Counter(all_mentioned_instructors)
        primary_instructor_name, _ = cnt.most_common(1)[0]
    if is_tba(primary_instructor_name):
        return None
    primary_instructor_name = strip_primary_indicator(primary_instructor_name)
    primary_instructor_name = reduce_whitespace(primary_instructor_name).strip()
    return primary_instructor_name


def parse_tr(tr: bs4.BeautifulSoup) -> Tuple[Dict[Any, Any], List[Dict]]:
    """Extracts the relevant information from a Howdy TR.

    Args:
        tr: A BeautifulSoup instance representing a Howdy table row
    Returns:
        A Section tuple.
    """
    ddtitle = tr.select_one(".ddtitle")
    name, crn, dept, course_num, section_num = parse_ddtitle(ddtitle)
    dddefault = tr.select_one(".dddefault")
    min_hours, max_hours, meeting_fields, all_instructors = parse_dddefault(dddefault)
    instructor = None
    if all_instructors is not None:
        instructor = retrieve_instructor(all_instructors)
    return (
        {
            "name": name,
            "dept": dept,
            "crn": crn,
            "course_num": course_num,
            "section_num": section_num,
            "min_credits": min_hours,
            "max_credits": max_hours,
            "instructor": instructor,
        },
        meeting_fields,
    )


def parse_sections(soup: bs4.BeautifulSoup) -> List[Tuple[Dict, List[Dict]]]:
    outer_datadisplaytable = soup.select_one("table.datadisplaytable")
    if outer_datadisplaytable:
        trs = merge_trs(outer_datadisplaytable)
        results = []
        for tr in trs:
            results.append(parse_tr(tr))
        return results
