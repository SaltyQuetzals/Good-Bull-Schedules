import re
from typing import Tuple


def sanitize(string: str) -> str:
    """Takes a string and replaces Unicode characters with single spaces."""
    string = re.sub(r"\s+", " ", string)
    return "".join([i if ord(i) < 128 else " " for i in string]).strip()


def is_honors(name: str, section_num: str) -> bool:
    try:
        section_num = int(section_num)
        return (section_num >= 200 and section_num < 300) or name.startswith("HNR-")
    except:
        pass
    return name.startswith("HNR-")


def is_sptp(name: str, course_num: str) -> bool:
    """Determines if a function is a Special Topics course.

    Args:
        name: The section name
        course_num: The course number.
    """
    return course_num in ["289", "489", "689"] or name.startswith("SPTP:")


def strip_honors_prefix(name: str) -> str:
    if name.startswith("HNR-"):
        return name[4:].strip()
    return name.strip()


def strip_sptp_prefix(name: str) -> str:
    if name.startswith("SPTP:"):
        return name[5:].strip()
    return name.strip()


def parse_ddtitle(ddtitle) -> Tuple[str, int, str, str]:
    """Extracts the abbreviated name, CRN, and section number from the ddtitle.

    Args:
        ddtitle: A bs4.BeautifulSoup instance
    Returns:
        name: The abbreviated name of the section (used if course doesn't exist)
        CRN: The unique Course Registration Number that identifies this section within a term.
        section_num: The section number that, when combined with a department and course number, uniquely identifies this section.
    """
    title_text = ddtitle.select_one("a").text
    title_text = sanitize(title_text)
    split_text = title_text.split(" - ")
    section_num = split_text[-1]
    crn = int(split_text[-3])
    _, course_num = split_text[-2].split(" ")

    name = " ".join(split_text[0:-3])
    honors = False
    sptp = False
    if is_honors(name, section_num):
        honors = True
        name = strip_honors_prefix(name)
    if is_sptp(name, section_num):
        sptp = True
        name = strip_sptp_prefix(name)

    # TODO: Return sptp and honors status
    return name, crn, course_num, section_num
