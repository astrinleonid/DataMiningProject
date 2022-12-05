
import argparse
import logging
import json
import sys
from database_class import StorageDatabase
from parse_items import *
from greq_open import single_url_open, multiple_urls_open

with open("config.json", "r") as config_file:
    config = json.load(config_file)

BATCH_SIZE = 7

# TABLE_LIST = {
#
#     'telework_eligible',
#     'travel_required',
#     'relocation_expenses_reimbursed',
#     'appointment_type', 'work_schedule',
#     'service',
#     'promotion_potential',
#     'security_clearance',
#     'position_sensitivity_and_risk',
#     'trust_determination_process',
#     'requirements',
#     'duties',
#     'summary',
#     'pay_scale_grade',
#     'job_family_series',
#
# }

# 'open_closing_dates',
#
# TEXT_FIELDS = """
#
#     'salary',
#     'announcement_number',
#     'open_closing_dates'
#  """
#
# NUMERIC_FIELDS = """
#         'control_number'
#
# """
#
# BINARY_FIELDS = """
#     'supervisory_status',
#     'drug_test'
#
# """


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

        if key in config['overview_fields']['TABLE_LIST']:
            # print(f"Updating table {key}")
            item_id = db.table_update_row_return_id(key, 'text', value, {'text' : value})

            job_card_record.update({key + '_id': item_id})
        if key in config['overview_fields']['TEXT_FIELDS']:
            job_card_record.update({key: value})

        if key in config['overview_fields']['NUMERIC_FIELDS']:
            try:
                numeric_value = int(value)
            except ValueError as er:
                raise ValueError(f"""The field {key} is supposed to be numeric, \n"
                                      non numeric received : {value}""")
            job_card_record.update({key: value})

        if key in config['overview_fields']['BINARY_FIELDS']:
            binary_values = {'Yes' : 1 ,'No' : 0}
            if value not in binary_values:
                raise ValueError(f"""The field {key} is supposed to be binary,  , \n"
                                      Yes/No expected, different value received : {value}""")
            job_card_record.update({key: binary_values[value]})

    job_card_id = db.table_update_row_return_id('job_card', 'announcement_number',
                                                job_card_record['announcement_number'],
                                                job_card_record)


    if 'locations' in job_card:
        for location in job_card['locations']:
            loc_id = db.table_update_row_return_id('locations', 'city', location['city'], location)
            db.table_add_row('pos_at_loc', {'job_card_id' : job_card_id, 'location_id' : loc_id} )

    print(f"Job announcement card added/found , ID: {job_card_id}")
    return job_card

def get_card_list_at_prof_area(url_name, old_count, limit):

    soup = single_url_open(url_name)
    count = int(soup.find(class_=config["tags"]["num_cards_on_page"]).text.split()[0].strip())
    changes_on_page = count != old_count
    print(f"Records in database: {old_count}, records on this page: {count}")
    if changes_on_page:
        print("New records found on the page")

    print("Cards on page: ", count)

    page_number = 1

    j = 0
    details_urls = []
    while True:
        j += 1
        if j == limit:  # limiting output for debugging
            break
        print("Page number = ", page_number)

        url_name_wpage = url_name + config['pathes']['page_num_parameter'] + str(page_number)
        print("scraping from url ", url_name_wpage)
        soup = single_url_open(url_name_wpage)
        job_notices = soup.find_all(class_= config['tags']['cards_in_the_list'])
        number_of_cards = len(job_notices)
        print("Cards on this page: ", number_of_cards)
        page_number += 1

        for i, job_notice in enumerate(job_notices):
            if i == limit:  # limiting output for debugging
                break
            details_url = job_notice.find("a", href=True)["href"]
            details_urls.append(details_url)

        if number_of_cards < 25:
            break

    print("List of urls formed, starting parsing") #TODO: Replace with logging

    # Counting control number
    control_no = 0
    for url in details_urls:
        control_no += int(url.split('/')[-1].strip(' #'))
    control_no = control_no % 1234567
    print(f"Control number :  {control_no}")
    return (details_urls, count, control_no)



def parse_sections(soup,limit = -1, prof_area_param = '',db_mode = 'checkonly', sql_password = 'from_file'):

    """
    Top level parser, parses the page with the list of the sections opportunities are grouped to topics.
    Return the list of the dictionaries: Name of the section as key, dictionary of embedded sections as value.
    Each embedded dictionary contains subsection names as keys, list of cards as value
    """

    db = StorageDatabase(db_mode, sql_password)

    titles_section = soup.find("div",class_ = config['tags']["title_class_teg"])
    class_of_category = config['tags']["category_class_tag"]
    class_of_prof_area = config['tags']["professional_area_class_tag"]
    titles = soup.find_all("li",class_=[class_of_prof_area,class_of_category])
    sections = []
    category_title = ""
    current_index = 0

    out_file = ""
    i = 0
    for title in titles:
        i += 1
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
            if len(prof_area_param) > 0 and prof_area_param != professional_area:
                continue
            card_url = (config['pathes']['target_url'] + title.find("a", href=True)["href"])
            print("Parsing: ",card_url)
            professional_area_id = db.table_update_row_return_id('professional_area', 'title',
                                                                 professional_area,
                                                                {'title': professional_area,
                                                                'category_id': category_id})

            old_count = db.table_get_value('professional_area', professional_area_id, 'num_records')['num_records']
            old_control_no = db.table_get_value('professional_area', professional_area_id, 'control_sum')['control_sum']

            (details_urls, count, control_no) = get_card_list_at_prof_area(card_url, old_count, limit)

            if old_control_no == control_no:
                print("No changes found")
            else:
                print("Changes found")
                if db_mode != 'checkonly':

                    db.table_update_row('professional_area', professional_area_id, 'control_sum', control_no)
                    db.table_update_row('professional_area', professional_area_id, 'num_records', count)
                    jobs = []

                    n = BATCH_SIZE
                    num_urls = len(details_urls)

                    batches = [details_urls[i:i+min(n,num_urls-i)] for i in range(0,num_urls,n)]

                    for batch in batches:
                        details_list = multiple_urls_open(batch)
                        for details in details_list:

                            job_card = parse_job_card(details, professional_area_id, db)
                            # v_counter.add_card(job_card)
                            jobs.append(job_card)

                    sections[current_index][category_title].append({title.text.strip() : jobs})


    db.sql_exec("SELECT * FROM agencies", 's')
    db.sql_exec("SELECT * FROM departments", 's')
    db.sql_exec("SELECT * FROM locations LIMIT 5", 's')
    db.sql_exec("SELECT * FROM states LIMIT 5", 's')
    db.sql_exec("SELECT * FROM professional_area", 's')

    db.db_commit()

def main(limit, prof_area_param, db_mode, sql_password):

    try:
        soup = single_url_open(config['pathes']["start_page"])
    except FileNotFoundError as er:
        # logger.error("Failed to establish connection to the starting page %s")
        print(f"Failed to open URL, error : {er}")
        return
    sections = parse_sections(soup, limit, prof_area_param, db_mode, sql_password)

if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument('-s', dest='section_name', type=str, default='', help='Limit parsing to one section (professional area). Use _ instead of space')
    parser.add_argument('-p', dest='sql_password', type=str, default='from_file', help='Enter your mysql root password')
    parser.add_argument('-l', type=int, default=-1, help='Limit number of cards parsed per section')
    parser.add_argument('-m', choices=['keep','new','checkonly'], default=-1, help='keep to use existing database, new to drop it and start a new one')

    args = parser.parse_args()

    print(args.l)
    print(args.m)
    print(args.section_name)
    print(args.sql_password)
    section_name = " ".join(args.section_name.split('_'))

    main(args.l, section_name, args.m, args.sql_password)






