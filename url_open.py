import requests
from bs4 import BeautifulSoup



URL_NAME = 'https://www.usajobs.gov/?c=opportunities'

def html_open(url_name):
    """
    Opens web page at url_name
    Returns the soup of the whole page
    """
    page = requests.get(url_name)
    if not page.ok:
        raise FileNotFoundError(f"Couldn't establish connection, status code : {page.status_code}")
    return BeautifulSoup(page.content, "html.parser")
