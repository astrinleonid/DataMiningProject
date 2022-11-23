import requests
from bs4 import BeautifulSoup
from main import parse_summary, html_open, parse_overview


file = open("test-travel.html", 'r')
page = file.read()
soup = BeautifulSoup(page, "html.parser")

print(parse_overview(soup))