import pymysql
from password import PASSWORD
SQL_BUILDER = {
'new' : "usajobs_db.sql",
'keep' : "usajobs_db_keepdb.sql"}

TABLE_LIST = {

    'telework_eligible',
    'travel_required',
    'relocation_expenses_reimbursed',
    'appointment_type','work_schedule',
    'service',
    'promotion_potential',
    'security_clearance',
    'position_sensitivity_and_risk',
    'trust_determination_process',
    'requirements',
    'duties',
    'summary',
    'pay_scale_grade',
    'job_family_series',

}


# 'open_closing_dates',

TEXT_FIELDS = """
    
    'salary',
    'announcement_number',
    'open_closing_dates'
 """

NUMERIC_FIELDS = """
        'control_number'

"""

BINARY_FIELDS = """
    'supervisory_status',
    'drug_test'

"""



def text_prepare(value):
    """
    Prepare text field in such a vay that it will not cause problems whe inserted into SQL quiery
    """

    if type(value) == str:
        return value.replace('"',"'").strip()
    else:
        return value

class StorageDatabase:

    def __init__(self,filename = "usajobs_db.sql"):
        self.__connection__ = pymysql.connect(host='localhost',
                                     user='root',
                                     password=PASSWORD,
                                     cursorclass=pymysql.cursors.DictCursor)

        self.__USE__ = "USE mydb"
        self.__SH_T__ = "SHOW TABLES"

        with open(filename) as file:
             sql_script = file.read().strip('; \n')
             sqls = sql_script.split(';')

        with self.__connection__.cursor() as cursor:
            for sql in sqls:
                cursor.execute(sql)

        print("Database created sucsessfully")

        # with self.__connection__.cursor() as cursor:
        #     cursor.execute(self.__USE__)
        #     cursor.execute(self.__SH_T__)
        #     result = cursor.fetchall()
        #     for item in result:
        #         print(item)


    def sql_exec(self,sql,show = 'n', *kwargs):
        """
        execute SQL quierty. if show == 'y' print the result to the standard output
        """

        with self.__connection__.cursor() as cursor:
            cursor.execute(self.__USE__)
            try:
                cursor.execute(sql)
            except pymysql.err.ProgrammingError as er:
                print(f"\n\n SQL failed on \n {sql}")
                raise pymysql.err.ProgrammingError(er)
            result = cursor.fetchall()
            res = []
            for item in result:
                res.append(item)
                if show == 's':
                    print(item)
            return res


    def __table_add_row__(self, table, data_items):
        """
        Add row into the table
        """

        names = []
        values = []
        for key, value in data_items.items():
            names.append(key)
            values.append(value)
        col_names = "".join([f'{name}, ' for name in names]).strip(', ')
        col_values = "".join([f'"{text_prepare(value)}", ' for value in values]).strip(', ')
        sql = f"INSERT INTO {table} ({col_names}) VALUES ({col_values})"

        self.sql_exec(sql)


    def table_update_row_return_id(self, table, column, value, data_items):
        """
        If the row with given value in given column does not exist,
        adds the row to the table with the given set of values and returns its ID.
        Otherwise returns the ID of the existing row.
        Does NOT update existing rows

        """
        row = self.__table_find_row__(table, column, value)
        if len(row) > 0:
            return row[0]['ID']
        else:
            self.__table_add_row__(table, data_items)
            sql = f"SELECT MAX(ID) AS ID FROM {table}"
            return self.sql_exec(sql)[0]['ID']


    def __table_find_row__(self, table, column, value):
        """
        Finds row in the table with given value in the given row, returns ID
        """
        sql = f'SELECT ID FROM {table}  WHERE {column} = "{text_prepare(value)}"'
        res = self.sql_exec(sql)
        return res

    def table_get_value(self, table, ID, column):
        """
        Returns value in the row by ID

        """
        sql = f'SELECT {column} FROM {table}  WHERE ID = {ID}'
        res = self.sql_exec(sql)
        if len(res) > 0:
            return res[0]
        else:
            return []

    def current_no_of_records(self):
        """
        Returns the number of the job announcements recorded in the database at the moment
        """
        sql = f"SELECT MAX(ID) AS ID FROM job_card"
        return self.sql_exec(sql)[0]['ID']

    def table_update_row(self, table, ID, column, value):
        """
        Updates the row with the given value by ID

        """
        sql = f'UPDATE {table} SET {column} = {value} WHERE ID = {ID}'
        res = self.sql_exec(sql)
        if len(res) > 0:
            return res[0]
        else:
            return []

    def db_commit(self):
        self.__connection__.commit()


if __name__ == "__main__":

    db = StorageDatabase(FILE)
    db.sql_exec("SHOW TABLES","s")
    print(db.__table_find_row__('departments', 'name', "some dept 5"))
    db.__table_add_row__('departments', {'name' : "some dept 5"})
    db.__table_add_row__('departments', {'name' : "some dept 6"})
    db.__table_add_row__('departments', {'name' : "some dept 7"})
    print(db.table_add_row_return_id('departments', {'name' : "some dept 9"}))
    print(db.table_find_row_return_id('departments', 'name', "some dept 5"))
    db.sql_exec("SELECT * FROM departments", 's')