import grequests
from bs4 import BeautifulSoup

# URL_NAME = 'https://www.usajobs.gov/?c=opportunities'
header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36"}

def single_url_open(url_name = 'https://www.usajobs.gov/?c=opportunities'):
    """
    Opens web page at url_name
    Returns the soup of the whole page
    """
    print(f"Opening {url_name}")
    pages = open_with_grequests([url_name])
    return BeautifulSoup(pages[0],"html.parser")

def multiple_urls_open(url_list):
    """
    Opens web page at url_name
    Returns the soup of the whole page
    """
    print(f"Opening a batch of urls")
    pages = open_with_grequests(url_list)
    return [BeautifulSoup(page,"html.parser") for page in pages]

def open_with_grequests(urls):
    """
    Opens the batch of hrefs with grequests and returns the list of pages paired with their numbers
    """
    print(f"Opening list of URLs : {urls}")
    rs = (grequests.get(href, headers = header) for href in urls)
    # print(rs)
    pages = grequests.map(rs)
    return [page.content for page in pages]


# print(single_url_open())