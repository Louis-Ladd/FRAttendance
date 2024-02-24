from sqlite3 import connect, Error 
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
        self.connection = connect(self.db_name)
        self.cursor = self.connection.cursor()

    def __del__(self):
        self.connection.close()

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
    
    def get_classes(self):
        try:
            result = self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            result = result.fetchall()
            for i in range(0,len(result)):
                result[i] = result[i][0]

            return result
        except Error as e:
            traceback.print_tb(e.__traceback__)
            print(f"{e.sqlite_errorname}: {e}")

    def create_class(self, class_name: str):
        try:
            self.cursor.execute(
                f"CREATE TABLE {class_name}(first, last, id, photo_path, tardies)"
            )
            self.connection.commit()
        except Error as e:
            traceback.print_tb(e.__traceback__)
            print(f"{e.sqlite_errorname}: {e}")

    def get_class(self, class_name: str):
        try:
            self.cursor.execute("SELECT * FROM ?")
            return self.cursor.fetchall()
        except Error as e:
            traceback.print_tb(e.__traceback__)
            print(f"{e.sqlite_errorname}: {e}")

    # Parameterized Queries go brrr
    def get_students(self, class_name, student_id=None, first_name=None, last_name=None):
        """
        Retrieve student information based on ID, first name, or last name.
        :param student_id: Student's ID
        :param first_name: Student's first name
        :param last_name: Student's last name
        """
        
        try:

            search_columns = []
            query_by = []

            if student_id != None:
                search_columns.append(f"id = ?")
                query_by.append(student_id)

            if first_name != None:
                search_columns.append(f"first LIKE ?")
                query_by.append(first_name+'%')

            if last_name != None:
                search_columns.append(f"last LIKE ?")
                query_by.append(last_name+'%')

            query = ( 
                f"SELECT * FROM {class_name} WHERE {', '.join(search_columns)}"
            )

            self.cursor.execute(query, tuple(query_by))
            results = self.cursor.fetchall()
            return results
        
        except Error as e:
            traceback.print_tb(e.__traceback__)
            print(f"{e.sqlite_errorname}: {e}")
            return []

    def update_student(self, class_name, student_id, first_name=None, last_name=None, photo_path=None, tardies=None):
        """
        Update a student's information.
        :param student_id: ID of the student to update.
        :param first_name: New first name of the student (optional).
        :param last_name: New last name of the student (optional).
        :param photo_path: New photo path of the student (optional).
        :param tardies: New tardies count of the student (optional).
        """
        try:
            updated_columns = []
            query_by = []

            if first_name != None:
                updated_columns.append("first = ?")
                query_by.append(first_name)
            if last_name != None:
                updated_columns.append("last = ?")
                query_by.append(last_name)
            if photo_path != None:
                updated_columns.append("photo_path = ?")
                query_by.append(photo_path)
            if tardies != None:
                updated_columns.append("tardies = ?")
                query_by.append(tardies)


            query_by.append(student_id)
            query = (
                f"UPDATE {class_name} SET {', '.join(updated_columns)} WHERE id = ?"
            )
            self.cursor.execute(query, tuple(query_by))
            self.connection.commit()

        except Error as e:
            traceback.print_tb(e.__traceback__)
            print(f"{e.sqlite_errorname}: {e}")

    def get_data_in_column(
        self, class_name, column_name, student_id : str = None, first_name : str = None
    ):
        """
        Get data from student
        :param class_name: Name of class being accessed
        :param column_name: Which column to access
        :param student_id: Find student by id
        :param first_name: Find student by first name
        """

        try:
            result = self.cursor.execute(
                f"SELECT {column_name} FROM {class_name}"
            )
            result = result.fetchall()
            for i in range(0,len(result)):
                result[i] = result[i][0]
            return result
        
        except Error as e:
            traceback.print_tb(e.__traceback__)
            print(f"{e.sqlite_errorname}: {e}")

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
            self.cursor.execute(None)
            self.connection.commit()
        except Error as e:
            traceback.print_tb(e.__traceback__)
            print(f"{e.sqlite_errorname}: {e}")

    def create_example_data(self, class_name: str):
        """Adds test data to the specified class"""
        try:
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
                ("Alice", "Bob", 11, "/path/to/photo1", 0),
            ]
            self.cursor.executemany(
                f"INSERT INTO {class_name} VALUES (?, ?, ?, ?, ?)", students
            )
            self.connection.commit()
        except Error as e:
            traceback.print_tb(e.__traceback__)
            print(f"{e.sqlite_errorname}: {e}")


test = ClassDatabase()

print(test.get_classes())