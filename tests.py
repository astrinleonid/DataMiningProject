from database_class import *

def tests():

    db = StorageDatabase(FILE)
    db.sql_exec("SHOW TABLES" ,"s")
    print(db.__table_find_row__('departments', 'name', "some dept 5"))
    db.__table_add_row__('departments', {'name' : "some dept 5"})
    db.__table_add_row__('departments', {'name' : "some dept 6"})
    db.__table_add_row__('departments', {'name' : "some dept 7"})
    assert db.table_add_row_return_id('departments', {'name' : "some dept 9"}) == 4
    assert db.table_find_row_return_id('departments', 'name', "some dept 5") == 1
    assert db.table_update_row_return_id('departments', 'name', "some dept 5", {'name' : "some dept 9"})  == 1
    db.__table_add_row__('category', {'title' : "some category 7"})
    db.__table_add_row__('professional_area', {'title' : "some professional area", 'category_id' : 1})
    print(db.sql_exec("SELECT * FROM professional_area", 's') )
    assert db.table_get_value('departments', 1, 'name') == {'name': 'some dept 5'}
    assert db.table_get_value('professional_area', 1, 'num_records')['num_records'] == 0



if __name__ == '__main__':
    tests()
