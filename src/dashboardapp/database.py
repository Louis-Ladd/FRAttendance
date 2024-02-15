import sqlite3
import traceback


#TODO: 
#   Add student lookup
#   Follow object oreintated programming paradigms
#   Check if .db file exists, then check if table exists within sql.
#   STRUCTURE Plan: 
#   Databases hold every class which are tables, 
#   The students have the columns: first name, last name, UUID (generated at student(row) creation), path to photo(s), tardies

class ClassDatabase:
    def __init__(self):
        self.db_name = "database.db"

    def create_class(self, class_name : str):
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute(f"CREATE TABLE {class_name}(first, last, id, photo_path, tardies)")
            conn.commit()
        except sqlite3.Error as e:
            traceback.print_tb(e.__traceback__)
            print(f"{e.sqlite_errorname}: {e}")
        finally:
            if conn:
                conn.close()

    def get_student(self, query):
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute(query)
            results = cursor.fetchall()
            return results
        except sqlite3.Error as e:
            traceback.print_tb(e.__traceback__)
            print(f"{e.sqlite_errorname}: {e}")
            return []
        finally:
            if conn:
                conn.close()

    def get_data_in_column(self, class_name, column_name, student_id=None, first_name=None):
        """
        Get data from student
        :param class_name Name of class being accessed
        :param column_name Which column to access
        :param student_id Find student by id
        :param first_name Find student by first name
        """
        if student_id == None and first_name == None:
            raise ValueError("student_id and first_name cannot both be empty")
        try:
            sql_cmd = f"SELECT {column_name} FROM {class_name} WHERE id = {student_id}" if student_id != None else f"SELECT {column_name} FROM {class_name} WHERE first = {first_name}"
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            result = cursor.execute(sql_cmd)
            print(result.fetchone())
            return result
        except sqlite3.Error as e:
            traceback.print_tb(e.__traceback__)
            print(f"{e.sqlite_errorname}: {e}")
        finally:
            if conn:
                conn.close()

    def set_data_in_column(self, class_name, column_name, data, student_id="", first_name=""):
        """
        Insert data into a specific column for a specific row.
        :param db_name: Name of the database.
        :param table_name: Name of the table.
        :param column_name: Name of the column to insert data into.
        :param data: Data to be inserted.
        :param row_id: The ID of the row to insert the data into.
        """
        if student_id == "" and first_name == "":
            raise ValueError("student_id and first_name cannot both be empty")
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute(None)
            conn.commit()
        except sqlite3.Error as e:
            traceback.print_tb(e.__traceback__)
            print(f"{e.sqlite_errorname}: {e}")
        finally:
            if conn:
                conn.close()

test = ClassDatabase()

test.get_data_in_column("bruh", "tardies", "1234")