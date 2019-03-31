import datetime
import re
from typing import Dict, List, NewType, Tuple

import bs4
import PyPDF2
import requests

LEN_HEADER_ROW = 38
LEN_OLD_HEADER_ROW = 37
LEN_SECTION_ROW = 20
LEN_COURSE_TOTAL_ROW = LEN_COLLEGE_TOTAL_ROW = LEN_DEPT_TOTAL_ROW = 19

LETTERS = ["A", "B", "C", "D", "F", "I", "S", "U", "Q", "X"]


def generate_year_semesters():
    """Generator function. Generates year_semesters.

    Yields:
        YEAR + SEMESTER CODE
    """
    year = datetime.datetime.now().year
    SPRING, SUMMER, FALL = 1, 2, 3
    while year >= 2013:
        for semester in (SPRING, SUMMER, FALL):
            yield (str(year) + str(semester))
        year -= 1


def is_header_row(string: str) -> bool:
    """Used to identify whether a row is a header row or not in PDFs
    from or after 2017.

    Args:
        string: The first element in the row
    Returns:
        Whether the row is a header row or not.
    """
    return string == "SECTION"


def is_old_header_row(string: str) -> bool:
    """Used to identify whether a row is a header row or not in PDFs
    before 2017.

    Args:
        string: The first element in the row
    Returns:
        Whether the row is a header row or not.
    """
    return string == "COLLEGE:"


def is_course_total_row(string: str) -> bool:
    """Used to identify whether a row is a course total row or not.

    Args:
        string: The first element in the row
    Returns:
        Whether the row is a course total row or not.
    """
    return string == "COURSE TOTAL:"


def is_dept_total_row(string: str) -> bool:
    """Used to identify whether a row is a department total row or not.

    Args:
        string: The first element in the row
    Returns:
        Whether the row is a department total row or not.
    """
    return string == "DEPARTMENT TOTAL:"


def is_college_total_row(string: str) -> bool:
    """Used to identify whether a row is a college total row or not.

    Args:
        string: The first element in the row
    Returns:
        Whether the row is a department total row or not.
    """
    return string == "COLLEGE TOTAL:"


def sanitize_page(page_obj: PyPDF2.pdf.PageObject) -> List[str]:
    """Splits a PageObject's content on any number of newlines, and returns
    the content as a list of strings.
    
    Args:
        page_obj: The content of a PDF page
    Returns:
        A list of strings representing the content on the page.
    """
    text = page_obj.extractText()
    text = re.split(r"\n+", text)
    return [t.strip() for t in text]


def parse_page(
    page_obj: PyPDF2.pdf.PageObject
) -> List[Tuple[Dict, Tuple[str, str, str]]]:
    """Parses a page from a PDF, extracting a list of grade data for each section.

    Args:
        page_obj: A PyPDF2.pdf.PageObject representing the current page
    Returns:
        A list of GradeData (see type definition at the top of the file).
    """
    text = sanitize_page(page_obj)
    i = 0
    grade_data = []
    old_pdf_style = False
    while i < len(text):
        if is_header_row(text[i]):
            i += LEN_HEADER_ROW
        elif is_old_header_row(text[i]):
            i += LEN_OLD_HEADER_ROW
            old_pdf_style = True
        elif is_course_total_row(text[i]):
            i += LEN_COURSE_TOTAL_ROW
        elif is_dept_total_row(text[i]):
            i += LEN_DEPT_TOTAL_ROW
        elif is_college_total_row(text[i]):
            i += LEN_COLLEGE_TOTAL_ROW
        else:
            section_row = text[i : i + LEN_SECTION_ROW]
            try:
                dept, course_num, section_num = section_row[0].split("-")
                ABCDF_SLICE = slice(1, 10, 2)
                ISUQX_SLICE = slice(13, 18)
                if old_pdf_style:
                    ABCDF_SLICE = slice(4, 9)
                    ISUQX_SLICE = slice(10, 15)
                letter_grades = section_row[ABCDF_SLICE] + section_row[ISUQX_SLICE]
                letter_grades = {
                    l: int(grade) for l, grade in zip(LETTERS, letter_grades)
                }
                grade_data.append((letter_grades, (dept, course_num, section_num)))

                i += LEN_SECTION_ROW
            except ValueError:
                i += LEN_SECTION_ROW - 1
    return grade_data


def calculate_gpa(letter_grades: Dict) -> float:
    """Given a series of letter grades, calculates the GPA of the section.

    Args:
        letter_grades: A list of integers representing how many students got
                       each letter grade
    Returns:
        The calculated gpa.
    """
    A = 4.0
    B = 3.0
    C = 2.0
    D = 1.0
    F = 0.0
    WEIGHTS = [A, B, C, D, F]
    grades = [letter_grades[char] for char in ["A", "B", "C", "D", "F"]]
    num_students = sum(grades)

    gpa = 0.0
    for students_with_grade, weight in zip(grades, WEIGHTS):
        gpa += students_with_grade * weight
    return gpa / num_students


def parse_pdf(pdf_path: str) -> List[Tuple[Dict, Tuple[str, str, str], float]]:
    with open(pdf_path, "rb") as f:
        pdf_reader = PyPDF2.PdfFileReader(f)
        pdf_data = []
        for i in range(pdf_reader.getNumPages()):
            page_data = parse_page(pdf_reader.getPage(i))
            for letter_grades, section_tuple in page_data:
                gpa = calculate_gpa(letter_grades)
                datatuple = (letter_grades, section_tuple, gpa)
                pdf_data.append(datatuple)
        return pdf_data
