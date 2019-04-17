import requests
import bs4
from bs4 import BeautifulSoup
from typing import List, Tuple, Dict

TERM_CODE_URL = "https://compass-ssb.tamu.edu/pls/PROD/bwckschd.p_disp_dyn_sched"
DEPT_LIST_URL = "https://compass-ssb.tamu.edu/pls/PROD/bwckgens.p_proc_term_date"

SECTION_URL = "https://compass-ssb.tamu.edu/pls/PROD/bwckschd.p_get_crse_unsec?term_in={}&sel_subj=dummy&sel_day=dummy&sel_schd=dummy&sel_insm=dummy&sel_camp=dummy&sel_levl=dummy&sel_sess=dummy&sel_instr=dummy&sel_ptrm=dummy&sel_attr=dummy&sel_subj={}&sel_crse=&sel_title=&sel_schd=%25&sel_insm=%25&sel_from_cred=&sel_to_cred=&sel_camp=%25&sel_levl=%25&sel_ptrm=%25&sel_instr=%25&sel_attr=%25&begin_hh=0&begin_mi=0&begin_ap=a&end_hh=0&end_mi=0&end_ap=a"


def request_html(
    url: str, headers: dict = None, form_data: dict = None, post: bool = False
) -> BeautifulSoup:
    """Given URL to webpage, returns a BeautifulSoup containing HTML.

    Args:
        url: The URL of the webpage to request.
        headers: A dictionary containing HTTP headers to send with request.
        form_data: A dictionary of entries for form data
        post: Indicates whether or not to post
    Returns:
        A BeautifulSoup instance containing the webpage HTML.
    """
    r = None
    if not post:
        r = requests.get(url, headers=headers)
    else:
        r = requests.post(url, form_data)
    r.raise_for_status()
    html = r.text
    return BeautifulSoup(html, "lxml")


def term_codes() -> List[str]:
    """Makes a request to retrieve all the term codes offered on Howdy.

    Returns:
        A list of strings, where each element is a term code.
    """
    r = requests.get(TERM_CODE_URL)
    r.raise_for_status()
    soup = bs4.BeautifulSoup(r.text, "lxml")
    options = soup.select("select[name=p_term] > option")

    # Skip the first option, it's blank
    options = options[1:]

    return [o["value"] for o in options]


def depts(term_code: str, depth=0) -> List[str]:
    """Makes a request to retrieve all of the departments offering classes
    during a term.

    Args:
        term_code: A term code to retrieve departments for.
    Returns:
        A list of department abbreviations.
    """
    form_data = {
        "p_calling_proc": "bwckschd.p_disp_dyn_sched",
        "p_term": int(term_code),
    }

    try:
        r = requests.post(DEPT_LIST_URL, data=form_data)
        r.raise_for_status()
        soup = bs4.BeautifulSoup(r.text, "lxml")
        options = soup.select("select[name=sel_subj] > option")
        return [o["value"] for o in options]
    except ConnectionResetError:
        if depth > 5:
            print("Connection reset 5 times, giving up")
            return []
        else:
            return depts(term_code, depth + 1)


def sections(term_code: str, dept: str, retries=0) -> bs4.BeautifulSoup:
    """Requests all of the sections available for a department during a term.

    Args:
        term_code: The term code
        dept: The department to retrieve sections for
        retries: The number of retries performed.
    Returns:
        A BeautifulSoup instance.
    """
    try:
        r = requests.get(SECTION_URL.format(term_code, dept))
        r.raise_for_status()
        soup = bs4.BeautifulSoup(r.text, "lxml")
        return soup
    except (
        requests.exceptions.ConnectionError,
        requests.exceptions.ChunkedEncodingError,
        ConnectionResetError,
        requests.exceptions.HTTPError
    ):
        if retries < 10:
            return sections(term_code, dept, retries + 1)
        print(f"Failed scraping {dept}-{term_code}")
