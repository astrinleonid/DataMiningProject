import pymysql
FILE = "usajobs_db.sql"
TABLE_LIST = {

    'telework_eligible',
    'travel_required',
    'relocation_expenses_reimbursed,',
    'appointment_type','work_schedule',
    'service',
    'promotion_potential',
    'security_clearance',
    'position_sensitivity_and_risk',
    'trust_determination_process',
    'requirements',
    'duties',
    'summary',
    'pay_scale_&_grade',
    'job_family_(series)',

}


# 'open_closing_dates',

TEXT_FIELDS = """
    
    'salary',
    'announcement_number',
    'open_closing_dates'
 """

def text_prepare(value):

    if type(value) == str:
        return value.replace('"',"'").strip()
    else:
        return value

class StorageDatabase:

    def __init__(self,filename = "usajobs_db.sql"):
        self.__connection__ = pymysql.connect(host='localhost',
                                     user='root',
                                     password='yKyw0716',
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

        names = []
        values = []
        for key, value in data_items.items():
            names.append(key)
            values.append(value)
        col_names = "".join([f'{name}, ' for name in names]).strip(', ')
        col_values = "".join([f'"{text_prepare(value)}", ' for value in values]).strip(', ')
        sql = f"INSERT INTO {table} ({col_names}) VALUES ({col_values})"

        self.sql_exec(sql)


    def table_add_row_return_id(self,table,data_items):

        self.__table_add_row__(table, data_items)
        sql = f"SELECT MAX(ID) AS ID FROM {table}"
        return self.sql_exec(sql)[0]['ID']

    def table_find_row_return_id(self, table, column, value):

        row = self.__table_find_row__(table, column, value)
        if len(row) > 0:
            return row[0]['ID']
        else:
            return 0

    def table_update_row_return_id(self, table, column, value, data_items):

        row = self.__table_find_row__(table, column, value)
        if len(row) > 0:
            return row[0]['ID']
        else:
            self.__table_add_row__(table, data_items)
            sql = f"SELECT MAX(ID) AS ID FROM {table}"
            return self.sql_exec(sql)[0]['ID']


    def __table_find_row__(self, table, column, value):

        sql = f'SELECT ID FROM {table}  WHERE {column} = "{text_prepare(value)}"'
        res = self.sql_exec(sql)
        return res

    def table_get_value(self, table, ID, column):
        sql = f'SELECT {column} FROM {table}  WHERE ID = {ID}'
        res = self.sql_exec(sql)
        if len(res) > 0:
            return res[0]
        else:
            return []

    def table_update_row(self, table, ID, column, value):
        sql = f'UPDATE {table} SET {column} = {value} WHERE ID = ID'
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