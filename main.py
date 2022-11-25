import requests
import argparse
from bs4 import BeautifulSoup
import sys
from database_class import StorageDatabase, TABLE_LIST, TEXT_FIELDS
from parse_items import *
from url_open import *
from tests import *

def parse_job_card(details, professional_area_id, db):
    """
    Parse individual page of the job announcement
    Store the proceeds to the database
    """

    # Parsing the records from the page into the job_card dictionary
    job_card = {**parse_card_header(details), **parse_overview(details),
                **parse_requirements(details), **parse_duties(details), **parse_summary(details) }

    # Getting the agency and department, if new store to the database
    department_name = str(job_card['department'])
    agency_name = str(job_card['agency'])
    print(f"Department: {department_name}")
    department_id = db.table_update_row_return_id('departments', 'name', department_name, {'name' : department_name})
    print(f"Agency: {agency_name}")
    agency_id = db.table_update_row_return_id('agencies', 'name', agency_name, {'name' : agency_name, 'department' : department_id})


    # Creating the record for writing it into the database
    job_card_record = {'name': job_card['title'],
                       'agency_id': agency_id,
                       'professional_area': professional_area_id}

    # Filling the record with the items parsed from the webpage.
    # If the item has to be stored in the separate table, the record in that table is made and
    # its ID is stored in the job_card_items with corresponding key.

    for key, value in job_card.items():

        if key in TABLE_LIST:
            print(f"Updating table {key}")
            item_id = db.table_find_row_return_id(key, 'text', value)
            if item_id == 0:
                item_id = db.table_add_row_return_id(key, {'text' : value})
            job_card_record.update({key + '_id': item_id})
        if key in TEXT_FIELDS:
            job_card_record.update({key: value})

    # Writing the record into the database
    job_card_id = db.table_update_row_return_id('job_card', 'announcement_number',
                                                job_card_record['announcement_number'],
                                                job_card_record)

    print(f"Job announcement card added/found , ID: {job_card_id}")
    return job_card

def open_prof_area_page(url_name, old_count):
    soup = html_open(url_name)
    count = int(soup.find(class_="usajobs-search-controls__results-count").text.split()[0].strip())
    changes_on_page = count != old_count
    if changes_on_page:
        print("New records found on the page")
    return (soup, count, changes_on_page)

def parse_job_cards(url_name, db, professional_area_id, limit=-1):
    """
    Parses the page with list of the cards.
    Returns list of dictionaries (each card is represented by a dictionary)
    """
    # v_counter = Value_Counter(OVERVIEW_ITEMS) - initial data study tool

    old_count = db.table_get_value('professional_area', professional_area_id, 'num_records')['num_records']
    (soup, count, changes_on_page) = open_prof_area_page(url_name, old_count)
    print("Cards on page: ",count)

    page_number = 1
    jobs = []
    j = 0
    details_urls = []
    while True:
        j += 1
        if j == limit: #limiting output for debugging
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
            details_urls.append(details_url)

        if number_of_cards < 25:
            break

    print("List of urls formed, starting parsing")
    print(details_urls)

    for url in details_urls:
        details = html_open(url)
        job_card = parse_job_card(details, professional_area_id, db)
        # v_counter.add_card(job_card)
        jobs.append(job_card)



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
    category_title = ""
    current_index = 0

    out_file = ""
    i = 0
    for title in titles:
        i += 1
        if i == limit:
            break
        class_name = title['class'][0]

        if class_name == class_of_category:
            category_title = title.text.strip()
            print("Category title =",category_title)

            category_id = db.table_update_row_return_id('category', 'title', category_title,
                                                        {'title': category_title })
            sections.append({category_title:[]})
            out_file += "\n\n" + category_title + "\n"
            current_index = len(sections)-1
        elif class_name == class_of_prof_area:
            professional_area = title.text.strip()
            print(professional_area)
            card_url = ("https://www.usajobs.gov" + title.find("a", href=True)["href"])
            print("Parsing: ",card_url)
            professional_area_id = db.table_update_row_return_id('professional_area', 'title',
                                                                 professional_area,
                                                                {'title': professional_area,
                                                                'category_id': category_id})

            cards = parse_job_cards(card_url, db, professional_area_id ,limit)
            sections[current_index][category_title].append({title.text.strip() : cards})

    # db.sql_exec("SELECT * FROM departments", 's')
    # db.sql_exec("SELECT * FROM agencies", 's')
    # db.sql_exec("SELECT * FROM promotion_potential", 's')
    # db.sql_exec("SELECT * FROM trust_determination_process", 's')
    # db.sql_exec("SELECT * FROM security_clearance", 's')
    db.sql_exec("SELECT * FROM job_card", 's')
    db.db_commit()

def main(limit):

    try:
        soup = html_open(URL_NAME)
    except FileNotFoundError as er:
        print(f"Failed to open URL, error : {er}")
        return
        # soup = BeautifulSoup(file,"html-parser")
    sections = parse_sections(soup, limit)

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('-s', dest='section_name', type=str, default='')
    parser.add_argument('-l', type=int, default=-1)
    parser.add_argument('--check', action='store_true', default=False)

    args = parser.parse_args()
    print(args.l)
    print(args.section_name)
    print(args.check)
    # tests()
    main(args.l)






