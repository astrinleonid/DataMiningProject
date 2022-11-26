from bs4 import BeautifulSoup
from database_class import *
# from main import parse_job_card
from parse_items import parse_card_header

from main import parse_job_card


def test_page_scrap(filename = 'test_job_card.html'):

    with open(filename, 'r') as file:
        page = file.read()
        return BeautifulSoup(page)


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

    soup = html_open("https://www.usajobs.gov/job/683987500")
    titles = parse_card_header(soup)
    print(titles)

    assert titles == {'department': 'Department of the Navy', 'agency': 'Naval Sea Systems Command', 'title': 'ENGINEER/SCIENTIST'}
    soup = test_page_scrap()
    # job_card = parse_job_card(soup)
    # for key, value in job_card.items():
    #     print(key, value)


if __name__ == '__main__':
    tests()
