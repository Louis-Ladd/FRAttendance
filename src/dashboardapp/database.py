import sqlite3
import traceback


# TODO:
#   Follow object oreintated programming paradigms
#   Check if .db file exists, then check if table exists within sql.
#   STRUCTURE Plan:
#   Databases hold every class which are tables,
#   The students have the columns: first name, last name, UUID (generated at student(row) creation), path to photo(s), tardies


class ClassDatabase:
    def __init__(self):
        self.db_name = "database.db"

    def sanitise_input(self, input: str) -> str:
        """
        :param input Sanitise untrusted string for SQL qeuries
        :returns: empty string if non alpha numeric or contains SQL commands
        """
        for i in input:
            if not (i.isalnum() or i == " "):
                print("illegal character")
                return ""
        return input

    def create_class(self, class_name: str):
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute(
                f"CREATE TABLE {class_name}(first, last, id, photo_path, tardies)"
            )
            conn.commit()
        except sqlite3.Error as e:
            traceback.print_tb(e.__traceback__)
            print(f"{e.sqlite_errorname}: {e}")
        finally:
            if conn:
                conn.close()

    # Parameterized Queries go brrr
    def get_student(self, student_id=None, first_name=None, last_name=None):
        """
        Retrieve student information based on ID, first name, or last name.
        :param student_id: Student's ID
        :param first_name: Student's first name
        :param last_name: Student's last name
        """
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()

            query = "SELECT * FROM {table_name} WHERE"
            params = []

            if student_id != None:
                query += " id = ?"
                params.append(student_id)
            elif first_name != None:
                query += " AND" if params else ""
                query += " first = ?"
                params.append(first_name)
            elif last_name != None:
                query += " AND" if params else ""
                query += " last = ?"
                params.append(last_name)

            else:
                raise ValueError("student_id, first_name, last_name cannot be empty")

            cursor.execute(
                query.format(table_name="your_class_table_name"), tuple(params)
            )
            results = cursor.fetchall()
            return results
        except sqlite3.Error as e:
            traceback.print_tb(e.__traceback__)
            print(f"{e.sqlite_errorname}: {e}")
            return []
        finally:
            if conn:
                conn.close()

    def update_student(
        self, student_id, first_name=None, last_name=None, photo_path=None, tardies=None
    ):
        """
        Update a student's information.
        :param student_id: ID of the student to update.
        :param first_name: New first name of the student (optional).
        :param last_name: New last name of the student (optional).
        :param photo_path: New photo path of the student (optional).
        :param tardies: New tardies count of the student (optional).
        """
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()

            updates = []
            params = []

            if first_name != None:
                updates.append("first = ?")
                params.append(first_name)
            elif last_name != None:
                updates.append("last = ?")
                params.append(last_name)
            elif photo_path != None:
                updates.append("photo_path = ?")
                params.append(photo_path)
            elif tardies != None:
                updates.append("tardies = ?")
                params.append(tardies)

            else:
                raise ValueError("At least one field to update must be provided")

            params.append(student_id)
            query = (
                f"UPDATE your_class_table_name SET {', '.join(updates)} WHERE id = ?"
            )
            cursor.execute(query, tuple(params))
            conn.commit()
        except sqlite3.Error as e:
            traceback.print_tb(e.__traceback__)
            print(f"{e.sqlite_errorname}: {e}")
        finally:
            if conn:
                conn.close()

    def get_data_in_column(
        self, class_name, column_name, student_id : str = None, first_name : str = None
    ):
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
            sql_cmd = (
                f"SELECT {column_name} FROM {class_name} WHERE id = {student_id}"
                if student_id != None
                else f"SELECT {column_name} FROM {class_name} WHERE first = {first_name}"
            )
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            result = cursor.execute(sql_cmd)
            return result.fetchone()
        except sqlite3.Error as e:
            traceback.print_tb(e.__traceback__)
            print(f"{e.sqlite_errorname}: {e}")
        finally:
            if conn:
                conn.close()

    def set_data_in_column(
        self, class_name, column_name, data, student_id="", first_name=""
    ):
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

    def create_example_data(self, class_name: str):
        """Adds test data to the specified class"""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            students = [
                ("Alice", "Smith", 1, "/path/to/photo1", 0),
                ("Bob", "Johnson", 2, "/path/to/photo2", 1),
                ("Charlie", "Brown", 3, "/path/to/photo3", 2),
                ("David", "Wilson", 4, "/path/to/photo4", 0),                
                ("Ella", "Martinez", 5, "/path/to/photo5", 1),
                ("Frank", "Miller", 6, "/path/to/photo6", 3),
                ("Grace", "Davis", 7, "/path/to/photo7", 0),
                ("Henry", "Garcia", 8, "/path/to/photo8", 2),
                ("Isabel", "Lopez", 9, "/path/to/photo9", 1),
                ("Jack", "Hall", 10, "/path/to/photo10", 0),
            ]
            cursor.executemany(
                f"INSERT INTO {class_name} VALUES (?, ?, ?, ?, ?)", students
            )
            conn.commit()
        except sqlite3.Error as e:
            traceback.print_tb(e.__traceback__)
            print(f"{e.sqlite_errorname}: {e}")
        finally:
            if conn:
                conn.close()




test = ClassDatabase()

print(test.get_data_in_column("Test", "tardies", student_id=1115))
