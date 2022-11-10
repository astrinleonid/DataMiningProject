import requests
from bs4 import BeautifulSoup
from main import html_open, parse_card_header, parse_job_card

URL_NAME = "https://www.usajobs.gov/job/683987500"


def run_tests():

    soup = html_open("https://www.usajobs.gov/job/683987500")
    titles = parse_card_header(soup)
    print(titles)
    assert parse_card_header(soup) == {'Department': 'Department of the Navy', 'Agency': 'Naval Sea Systems Command', 'Title': 'ENGINEER/SCIENTIST'}
    job_card = parse_job_card(soup)
    for key, value in job_card.items():
        print(key, value)

if __name__ == "__main__":
    run_tests()