import requests
from bs4 import BeautifulSoup
from database_class import StorageDatabase
from parse_items import *
from url_open import *

def parse_job_card(details, db):

    job_card = {**parse_card_header(details), **parse_overview(details),
                **parse_requirements(details), **parse_duties(details), **parse_summary(details) }
    department_name = str(job_card['department'])
    agency_name = str(job_card['agency'])
    print(department_name)
    department_id = db.table_find_row('departments', 'name', department_name)
    if len(department_id) == 0:
        department_id = db.table_add_row('departments', {'name' : department_name})
    agency_id = db.table_find_row('agencies', 'name', agency_name)
    if len(agency_id) == 0:
        agency_id = db.table_add_row('agencies', {'name' : agency_name, 'department' : department_id['ID']} )


    return job_card

def parse_job_cards(url_name, db, limit=-1):
    """
    Parses the page with list of the cards.
    Returns list of dictionaries (each card is represented by a dictionary)
    """
    # v_counter = Value_Counter(OVERVIEW_ITEMS)
    soup = html_open(url_name)
    count = int(soup.find(class_="usajobs-search-controls__results-count").text.split()[0].strip())
    print("Cards on page: ",count)
    page_number = 1
    jobs = []
    hashes = []
    duties_number = 0
    j = 0
    while True:
        j += 1
        if j == limit:
            break
        print("Page number = ",page_number)
        url_name_wpage = url_name + "&sort=enddate&page=" + str(page_number)
        print("scraping from url ", url_name_wpage)
        soup = html_open(url_name_wpage)
        job_notices = soup.find_all(class_="usajobs-search-result--card")
        number_of_cards = len(job_notices)
        print("Cards on this page: ",number_of_cards)
        page_number += 1
        for i, job_notice in enumerate(job_notices):
            if i == limit: #limiting output for debugging
                break

            details_url = job_notice.find("a", href=True)["href"]
            details = html_open(details_url)
            job_card = parse_job_card(details, db)

            # v_counter.add_card(job_card)
            jobs.append(job_card )
            for duty, duty_hash in job_card["Duties"]:
                duties_number += 1
                if duty_hash not in hashes:
                    hashes.append(duty_hash)

        if number_of_cards < 25:
            break
    print(f"Total different duties found: {duties_number} from them unique {len(hashes)} ")
    # v_counter.store_values("values.txt",count)
    return jobs

def parse_sections(soup,limit = -1):

    """
    Top level parser, parses the page with the list of the sections opportunities are grouped to topics.
    Return the list of the dictionaries: Name of the section as key, dictionary of embedded sections as value.
    Each embedded dictionary contains subsection names as keys, list of cards as value
    """

    db = StorageDatabase()

    titles_section = soup.find("div",class_="usajobs-landing-find-opportunities__section-container")
    class_of_category = "usajobs-landing-find-opportunities__section-title"
    class_of_prof_area = "usajobs-landing-find-opportunities__job-item"
    titles = soup.find_all("li",class_=[class_of_prof_area,class_of_category])
    sections = []
    current_title = ""
    current_index = 0

    out_file = ""
    i = 0
    for title in titles:
        i += 1
        if i == limit:
            break
        class_name = title['class'][0]

        if class_name == class_of_category:
            current_title = title.text.strip()
            print("Category title =",current_title)
            sections.append({current_title:[]})
            out_file += "\n\n" + current_title + "\n"
            current_index = len(sections)-1
        elif class_name == class_of_prof_area:
            title_string = title.text.strip()
            print(title_string)
            card_url = ("https://www.usajobs.gov" + title.find("a", href=True)["href"])
            print("Parsing: ",card_url)
            cards = parse_job_cards(card_url, db, limit)
            sections[current_index][current_title].append({title.text.strip() : cards})

    db.sql_exec("SELECT * FROM departments", 's')
    db.sql_exec("SELECT * FROM agencies", 's')


if __name__ == "__main__":

    soup = html_open(URL_NAME)
    # soup = BeautifulSoup(file,"html-parser")
    sections = parse_sections(soup, 3)




