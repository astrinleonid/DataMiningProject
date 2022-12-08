
import argparse
# import logging
import json
# import sys
from database_class import StorageDatabase
from parse_items import *
from greq_open import single_url_open, multiple_urls_open
from service_setup import config, logger
from text_items_afterparsing import *
from api_scraping import get_data



# BATCH_SIZE = 7


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
    department_id = db.table_update_row_return_id('departments', 'name', department_name, {'name' : department_name})
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
            if len(location['state_ID']) > 2:
                location['city'] = ", ".join([location['state_ID'],location['city']])
                location['state_ID'] = 'OS'
            loc_id = db.table_update_row_return_id('locations', 'city', location['city'], location)
            db.table_add_row('pos_at_loc', {'job_card_id' : job_card_id, 'location_id' : loc_id} )

    if 'job_family_series' in job_card:
        for record in job_card['job_family_series']:
            jfs_id = db.table_update_row_return_id('job_family_series', 'name', record['name'], record)
            db.table_add_row('job_family_and_card', {'job_card_id' : job_card_id, 'job_family_series_id' : jfs_id} )

    print(f"Job announcement card added/found , ID: {job_card_id}")
    if job_card_id < db.current_no_of_records():
        logger.info(f"\nCard already in the database, ID: {job_card_id}")
    else:
        logger.info(f"\nJob announcement card added, ID: {job_card_id}, Title : {job_card['title']}")
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
        logger.info(f"scraping from url : {url_name_wpage}")
        soup = single_url_open(url_name_wpage)
        job_notices = soup.find_all(class_= config['tags']['cards_in_the_list'])
        number_of_cards = len(job_notices)
        logger.info(f"Cards on this page : {number_of_cards}")
        page_number += 1

        for i, job_notice in enumerate(job_notices):
            if i == limit:  # limiting output for debugging
                break
            details_url = job_notice.find("a", href=True)["href"]
            details_urls.append(details_url)

        if number_of_cards < 25:
            break

    print("List of urls formed, starting parsing, cards on this page: ", number_of_cards)
    logger.info("\n\nList of urls formed, starting parsing")

    # Counting control number
    control_no = 0
    for url in details_urls:
        control_no += int(url.split('/')[-1].strip(' #'))
    control_no = control_no % 1234567
    logger.info(f"Control number :  {control_no}")
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
            logger.info(f"New category : {category_title}")
            category_id = db.table_update_row_return_id('category', 'title', category_title,
                                                        {'title': category_title })
            sections.append({category_title:[]})
            out_file += "\n\n" + category_title + "\n"
            current_index = len(sections)-1
        elif class_name == class_of_prof_area:
            professional_area = title.text.strip()
            if len(prof_area_param) > 0 and prof_area_param != professional_area:
                continue
            card_url = (config['pathes']['target_url'] + title.find("a", href=True)["href"])
            logger.info(f"Parsing page - professional area : {professional_area}, URL : {card_url}")
            professional_area_id = db.table_update_row_return_id('professional_area', 'title',
                                                                 professional_area,
                                                                {'title': professional_area,
                                                                'category_id': category_id})

            old_count = db.table_get_value('professional_area', professional_area_id, 'num_records')['num_records']
            old_control_no = db.table_get_value('professional_area', professional_area_id, 'control_sum')['control_sum']

            (details_urls, count, control_no) = get_card_list_at_prof_area(card_url, old_count, limit)

            if old_control_no == control_no:
                print(f" {professional_area} : No changes found")
                logger.info(f"No changes")
            else:
                print(f" {professional_area} :Changes found")
                logger.info(f"Changes on page : stored number {old_count},on page : "
                            f"{count}, stored control No : {old_control_no}, on page : {control_no}")
                if db_mode != 'checkonly':

                    db.table_update_row('professional_area', professional_area_id, 'control_sum', control_no)
                    db.table_update_row('professional_area', professional_area_id, 'num_records', count)
                    jobs = []

                    n = config['batch_size']
                    num_urls = len(details_urls)

                    batches = [details_urls[i:i+min(n,num_urls-i)] for i in range(0,num_urls,n)]

                    for batch in batches:
                        details_list = multiple_urls_open(batch)
                        logger.debug(f"Batch open, batch : {batch}")
                        for details in details_list:

                            job_card = parse_job_card(details, professional_area_id, db)
                            # v_counter.add_card(job_card)
                            jobs.append(job_card)

                    sections[current_index][category_title].append({title.text.strip() : jobs})
        db.db_commit()

    len_db = db.current_no_of_records()
    logger.info(f"Number of job card records in the database {len_db}")
    # Afterparsing: splitting the text fields of salary and dates into the respective fields

    for i in range(1,len_db+1):
        date_record = db.table_get_value('job_card', i, 'open_closing_dates')
        (start_date, end_date) = parce_dates_text(date_record)
        db.table_update_row('job_card', i, 'end_date', end_date)
        db.table_update_row('job_card', i, 'start_date', start_date)
        salary_record = db.table_get_value('job_card', i, 'salary')
        (start_salary, max_salary) = parce_salary_text(salary_record)
        db.table_update_row('job_card', i, 'max_salary', max_salary)
        db.table_update_row('job_card', i, 'start_salary', start_salary)

    db.db_commit()
    # Scraping API

    with open('usstates.json', "r") as read_content:
        states_list = json.load(read_content)
    states = states_list['numeric_codes']
    for state in states:
        data = get_data(states[state])
        if data == {}:
            logger.error(f"Request unsucsessfull, breaking the cycle")
            break
        else:
            state_ID = db.table_get_value('states', state, 'state_ID')
            for period, values in data.items():
                period_ID = db.table_update_row_return_id('periods', 'text', period, {'text' : period})

                record = {'state_ID' : state_ID, 'period_id' : period_ID, **values}
                db.table_add_row('stats_data', record)

    db.sql_exec("SELECT * FROM agencies LIMIT 3", 's')
    db.sql_exec("SELECT * FROM departments LIMIT 3", 's')
    db.sql_exec("SELECT * FROM locations LIMIT 3", 's')
    db.sql_exec("SELECT * FROM states LIMIT 3", 's')
    db.sql_exec("SELECT * FROM professional_area LIMIT 3", 's')

    db.db_commit()

def main(limit, prof_area_param, db_mode, sql_password):

    try:
        soup = single_url_open(config['pathes']["start_page"])
    except FileNotFoundError as er:
        # logger.error("Failed to establish connection to the starting page %s")
        print(f"Failed to open URL, error : {er}")
        logger.error(f"Failed to open URL, error : {er}")
        return
    sections = parse_sections(soup, limit, prof_area_param, db_mode, sql_password)



if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument('-s', dest='section_name', type=str, default='', help='Limit parsing to one section (professional area). Use _ instead of space')
    parser.add_argument('-p', dest='sql_password', type=str, default='from_file', help='Enter your mysql root password')
    parser.add_argument('-l', type=int, default=-1, help='Limit number of cards parsed per section')
    parser.add_argument('-m', choices=['keep','new','checkonly'], default='keep', help='keep to use existing database, new to drop it and start a new one, checkonly to track changes without parsing')

    args = parser.parse_args()

    section_name = " ".join(args.section_name.split('_'))
    logger.info(f"Parsing usajobs.gov, section : {section_name} mode : {args.m}")
    main(args.l, section_name, args.m, args.sql_password)






