from bs4 import BeautifulSoup
from database_class import *
# from main import parse_job_card
from parse_items import *
from greq_open import local_file_open, single_url_open

from main import parse_job_card


def tests():

    """
    Attention!!!
    Running tests will drop existing database

    """

    db = StorageDatabase(SQL_BUILDER['new'])
    db.sql_exec("SHOW TABLES" ,"s")
    print(db.__table_find_row__('departments', 'name', "some dept 5"))
    db.__table_add_row__('departments', {'name' : "some dept 5"})
    db.__table_add_row__('departments', {'name' : "some dept 6"})
    db.__table_add_row__('departments', {'name' : "some dept 7"})
    assert db.table_update_row_return_id('departments', 'name', "some dept 5", {'name' : "some dept 9"})  == 1
    db.__table_add_row__('category', {'title' : "some category 7"})
    db.__table_add_row__('professional_area', {'title' : "some professional area", 'category_id' : 1})
    print(db.sql_exec("SELECT * FROM professional_area", 's') )
    assert db.table_get_value('departments', 1, 'name') == {'name': 'some dept 5'}
    assert db.table_get_value('professional_area', 1, 'num_records')['num_records'] == 0

    # soup = single_url_open("https://www.usajobs.gov/job/683987500")
    # titles = parse_card_header(soup)
    # print(titles)


    soup = local_file_open('test_job_card.html')
    titles = parse_card_header(soup)
    print(titles)
    assert titles == {'department': 'Department of the Army', 'agency': 'U.S. Army Corps of Engineers', 'title': 'Project Manager (Interdisciplinary)'}

    print(parse_overview(soup))


if __name__ == '__main__':
    tests()
