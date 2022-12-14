from bs4 import BeautifulSoup
from database_class import *
import json
from parse_items import *
from text_items_afterparsing import *
from greq_open import local_file_open, single_url_open
from USJscrape import parse_job_card

def tests():

    """
    Attention!!!
    Running tests will drop existing database

    """

    db = StorageDatabase('new','from_file')
    db.sql_exec("SHOW TABLES" ,"s")
    print(db.__table_find_row__('departments', 'name', "some dept 5"))
    db.table_add_row('departments', {'name' : "some dept 5"})
    db.table_add_row('departments', {'name' : "some dept 6"})
    db.table_add_row('departments', {'name' : "some dept 7"})
    assert db.table_update_row_return_id('departments', 'name', "some dept 5", {'name' : "some dept 9"})  == 1
    db.table_add_row('category', {'title' : "some category 7"})
    db.table_add_row('professional_area', {'title' : "some professional area", 'category_id' : 1})
    print(db.sql_exec("SELECT * FROM professional_area", 's') )
    assert db.table_get_value_with_ID('departments', 1, 'name') == {'name': 'some dept 5'}
    assert db.table_get_value_with_ID('professional_area', 1, 'num_records')['num_records'] == 0

    soup = single_url_open("https://www.usajobs.gov/job/683987500")
    titles = parse_card_header(soup)
    assert titles == {'department': 'Department of the Navy', 'agency': 'Naval Sea Systems Command',
                      'title': 'ENGINEER/SCIENTIST'}


    soup = local_file_open('test_job_card.html')
    titles = parse_card_header(soup)
    print(titles)



    assert titles == {'department': 'Department of the Army', 'agency': 'U.S. Army Corps of Engineers',
                      'title': 'Project Manager (Interdisciplinary)'}

    print(parse_overview(soup))
    parse_job_card(soup, 1, db)

    assert db.sql_exec("SELECT * FROM departments WHERE ID = 4" , 's')  == [{'ID': 4, 'name': 'Department of the Army'}]
    assert db.sql_exec("SELECT name FROM agencies", 's') == [{'name': 'U.S. Army Corps of Engineers'}]
    assert db.sql_exec("SELECT * FROM promotion_potential", 's') == [{'ID': 1, 'text': 'None', 'level': None}]
    assert db.sql_exec("SELECT text FROM security_clearance", 's') == [{'text': 'Not Required'}]
    assert db.sql_exec("SELECT salary FROM job_card LIMIT 10", 's' ) == [{'salary': '$79,363 - $114,702 per year'}]
    assert db.sql_exec("SELECT * FROM summary", 's') == [
        {'ID': 1,
         'text': 'About the Position: Serves as a Project Manager for the Corps of Engineers assigned to the Planning, Programs and Project Management Division within the Huntington, Louisville, or Chicago Districts. Works under general supervision of the Section Chief, who makes assignments in terms of overall objectives and any limitations on the scope of projects. Incumbent plans and carries out assignments independently, setting own priorities and coordinating work, as necessary.'}
    ]

    soup = local_file_open('locations_section.html')
    result = parse_locations(soup)

    print(result[0])
    assert result[0] == {'city': 'Mobile', 'state_ID': 'AL'}


def test_sal(salary):
    print(parce_salary_text(salary))


if __name__ == '__main__':
    with open("config.json", "r") as config_file:
        config = json.load(config_file)
    print(config['overview_fields']['TABLE_LIST'][5])
    # tests()
    test_sal("""$89,076 - $115,803 per year
                                            PLEASE NOTE: In addition to the salary shown above, the salary for this position will also include a COLA of 2.48% (2022) for Juneau, Alaska.""")
