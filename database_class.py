import json
import pymysql


SQL_FILE = "usajobs_db_keepdb.sql"
US_STATES = "usstates.json"

def text_prepare(value):
    """
    Prepare text field in such a vay that it will not cause problems whe inserted into SQL quiery
    """

    if type(value) == str:
        return value.replace('"',"'").strip()
    else:
        return value

class StorageDatabase:

    def __init__(self, mode, sql_password):
        if sql_password == 'from_file':
            with open('password.txt') as file:
                sql_password = file.read()
        self.__connection__ = pymysql.connect(host='localhost',
                                              user='root',
                                              password=sql_password,
                                              cursorclass=pymysql.cursors.DictCursor)

        self.__USE__ = "USE mydb"
        self.__SH_T__ = "SHOW TABLES"
        filename = SQL_FILE

        if mode == 'new':
            sql = 'DROP SCHEMA IF EXISTS `mydb`'
            with self.__connection__.cursor() as cursor:
                cursor.execute(sql)

        with open(filename) as file:
             sql_script = file.read().strip('; \n')
             sqls = sql_script.split(';')


        with self.__connection__.cursor() as cursor:
            for sql in sqls:
                cursor.execute(sql)

        print("Database created sucsessfully")

        if mode == 'new':
            with open('usstates.json', "r") as read_content:
                states_list = json.load(read_content)
                for code, state in states_list.items():
                    self.table_add_row('states', {'state_id': code, 'name': state})


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
            except pymysql.err.DataError as er:
                print(f"\n\n SQL failed on \n {sql}")
                raise pymysql.err.DataError(er)
            result = cursor.fetchall()
            res = []
            for item in result:
                res.append(item)
                if show == 's':
                    print(item)
            return res


    def table_add_row(self, table, data_items):
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
            self.table_add_row(table, data_items)
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

    pass