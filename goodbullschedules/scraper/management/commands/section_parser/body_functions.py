import collections
import re
from datetime import datetime, time
from typing import Dict, List, Tuple

import bs4


def is_tba(string: str) -> bool:
    return string.strip() == "TBA"


def has_primary_indicator(instructor: str) -> bool:
    return "(P)" in instructor


def strip_primary_indicator(instructor: str) -> str:
    """Removes the "primary instructor" indicator from an instructor, if present.

    Args:
        instructor: A string (an instructor's name)
    Returns:
        The instructor's name, stripped of its primary indicator.
    """
    if has_primary_indicator(instructor):
        return instructor.replace("(P)", "").strip()
    return instructor


def parse_hours(dddefault: bs4.BeautifulSoup) -> Tuple[float, float]:
    """Extacts the number of hours from dddefault

    Args:
        dddefault: A bs4.BeautifulSoup instance
    Returns:
        min_hours: The minimum number of hours that this section can be worth
        max_hours: The maximum number of hours that this section can be worth
    """
    if "Credit" not in dddefault.text:
        return None, None
    HOURS_PATTERN = re.compile(
        "(?:([\d\.]+)(?:\s+TO\s+|\s+OR\s+))?([\d\.]+)\s+Credits?\n"
    )
    try:
        min_hours, max_hours = re.findall(HOURS_PATTERN, dddefault.text)[0]
        max_hours = float(max_hours)
        if not min_hours:
            min_hours = max_hours
        else:
            min_hours = float(min_hours)
        return min_hours, max_hours
    except Exception as e:
        print(dddefault.text)
        raise e


def parse_duration(duration_string) -> Tuple[float, float]:
    """Parse and calculate the duration of a meeting.

    Args:
        duration_string: A string matching format %I:%M %p (see Python docs on datetime)
    Returns:
        A datetime.timedelta representing the duration of this meeting time, or None if TBA.
    """
    TIME_FORMAT_STRING = "%I:%M %p"
    if is_tba(duration_string):
        return None, None
    start_string, end_string = duration_string.upper().split(" - ")
    start_string = start_string.strip()
    start_time = datetime.strptime(start_string, TIME_FORMAT_STRING)

    end_string = end_string.strip()
    end_time = datetime.strptime(end_string, TIME_FORMAT_STRING)
    return start_time.time(), end_time.time()


def parse_datadisplaytable(
    dddefault: bs4.BeautifulSoup
) -> Tuple[List[Dict], List[str]]:
    """Retieves all of the meetings that this class will be holding. Additionally, determines the instructor.

    Args:
        dddefault: A bs4.BeautifulSoup instance
    Returns:
        A list of Meeting instances, and either an Instructor instance or None
    """
    datadisplaytable = dddefault.select_one(".datadisplaytable")
    if not datadisplaytable:
        return None, None
    # Because TAMU doesn't know what `th` elements are, throw out the first row.
    rows = datadisplaytable.select("tr")[1:]

    all_mentioned_instructors = []
    meeting_fields = []
    for row in rows:
        entries = [td.text.replace(u"\xa0", "") for td in row.select("td")]
        meet_type, duration_string, days, location, _, _, instructor_string = entries
        start_time, end_time = parse_duration(duration_string)
        all_mentioned_instructors.append(re.sub(r"\(\s+P\)", "(P)", instructor_string))

        if is_tba(location):
            location = None
        fields = {
            "location": location,
            "meeting_days": days,
            "start_time": start_time,
            "end_time": end_time,
            "meeting_type": meet_type,
        }
        meeting_fields.append(fields)
    return meeting_fields, all_mentioned_instructors


def parse_dddefault(
    dddefault: bs4.BeautifulSoup
) -> Tuple[float, float, List[Dict], List[str]]:
    """Extracts the number of hours and the meetings from a dddefault element.

    Args:
        dddefault: A dddefault element that contains hours and meeting data.
    Returns:
        min_hours: The minimum number of hours that this section can be worth.
        max_hours: The minimum number of hours that this section can be worth.
        meetings: A list of Meeting instances.
        instructor: An instructor instance (if not TBA)
    """
    min_hours, max_hours = parse_hours(dddefault)
    meetings, all_mentioned_instructors = parse_datadisplaytable(dddefault)
    return min_hours, max_hours, meetings, all_mentioned_instructors
