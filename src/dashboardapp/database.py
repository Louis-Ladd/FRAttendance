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
        self.connection = connect(self.db_name, check_same_thread=False)
        self.cursor = self.connection.cursor()

    def __del__(self):
        self.connection.close()

    def sanitise_input(self, input: str) -> str:
        """
        Sanitises the input string by removing any non-alphanumeric characters or spaces. 

        Args:
            input (str): The input string to be sanitised.

        Returns:
            str: The sanitised input string.
        """
        for i in input:
            if not (i.isalnum() or i == " "):
                print("illegal character")
                return ""
        return input

    def get_classes(self):
        """
        Retrieves the names of all tables (classes) in the SQLite database and returns them as a list.
        """
        try:
            result = self.cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table';"
            )
            result = result.fetchall()
            for i in range(0, len(result)):
                result[i] = result[i][0]

            return result
        except Error as e:
            traceback.print_tb(e.__traceback__)
            print(f"{e.sqlite_errorname}: {e}")

    def create_class(self, class_name: str):
        """
        Create a new table with the given class name in the database.

        Parameters:
            class_name (str): The name of the class for the new table.

        Returns:
            None
        """
        try:
            self.cursor.execute(
                f"CREATE TABLE {self.sanitise_input(class_name)}(first, last, id, photo_path, tardies)"
            )
            self.connection.commit()
        except Error as e:
            traceback.print_tb(e.__traceback__)
            print(f"{e.sqlite_errorname}: {e}")

    def get_class(self, class_name: str, top=None):
        """
        Get the specified class from the database.

        Args:
            class_name (str): The name of the class to retrieve from the database.
            top (int, optional): The number of top records to retrieve.

        Returns:
            list or None: A list of records from the specified class, or None if an error occurs.
        """
        try:
            self.cursor.execute(f"SELECT * FROM {class_name}")

            return self.cursor.fetchall()[:top] if top else self.cursor.fetchall()

        except Error as e:
            traceback.print_tb(e.__traceback__)
            print(f"Error: {e}")
            return None

    def create_student(
        self,
        class_name,
        student_name: str,
        last_name: str,
        student_id: int,
        photo_path: str
    ):
        """
        A function to create a student in the specified class with the given student information.

        Args:
            class_name (str): The name of the class to which the student belongs.
            student_name (str): The first name of the student.
            last_name (str): The last name of the student.
            student_id (int): The unique ID of the student.
            photo_path (str): The file path to the student's photo.

        Returns:
            int or None: The ID of the newly created student, or None if there was an error.
        """
        # TODO: Add check for duplicate students!!! - Louis
        try:
            query = f"INSERT INTO {class_name} (first, last, id, photo_path, tardies) VALUES (?,?,?,?,?)"
            self.cursor.execute(
                query, (student_name, last_name, student_id, photo_path, 0)
            )
            self.connection.commit()
            return self.cursor.lastrowid
        except Exception as e:
            traceback.print_tb(e.__traceback__)
            print(f"Error: {e}")
            return None

    # Parameterized Queries go brrr
    def get_students(
        self, class_name, student_id=None, first_name=None, last_name=None
    ):
        """
        Retrieves students based on class name and optional student ID, first name, and last name.
        Args:
            class_name (str): The name of the class to retrieve students from.
            student_id (int): Optional. The ID of the student to retrieve.
            first_name (str): Optional. The first name of the student to retrieve.
            last_name (str): Optional. The last name of the student to retrieve.
        Returns:
            list: A list of students matching the specified criteria.
        """
        try:

            search_columns = []
            query_by = []

            if student_id != None:
                search_columns.append(f"id = ?")
                query_by.append(student_id)

            if first_name != None:
                search_columns.append(f"first LIKE ?")
                query_by.append(first_name + "%")

            if last_name != None:
                search_columns.append(f"last LIKE ?")
                query_by.append(last_name + "%")

            query = f"SELECT * FROM {self.sanitise_input(class_name)} WHERE {', '.join(search_columns)}"

            self.cursor.execute(query, tuple(query_by))
            results = self.cursor.fetchall()
            return results

        except Error as e:
            traceback.print_tb(e.__traceback__)
            print(f"{e.sqlite_errorname}: {e}")
            return []

    def update_student(
        self,
        class_name,
        student_id,
        first_name=None,
        last_name=None,
        photo_path=None,
        tardies=None,
    ):
        """
        Update student information in the database.

        Args:
            class_name (str): The name of the class.
            student_id (int): The ID of the student.
            first_name (str, optional): The first name of the student. Defaults to None.
            last_name (str, optional): The last name of the student. Defaults to None.
            photo_path (str, optional): The path to the student's photo. Defaults to None.
            tardies (int, optional): The number of tardies. Defaults to None.

        Returns:
            None
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
            query = f"UPDATE {self.sanitise_input(class_name)} SET {', '.join(updated_columns)} WHERE id = ?"
            self.cursor.execute(query, tuple(query_by))
            self.connection.commit()

        except Error as e:
            traceback.print_tb(e.__traceback__)
            print(f"{e.sqlite_errorname}: {e}")

    def get_data_in_column(
        self, class_name, column_name, student_id: str = None, first_name: str = None
    ):
        """
        A function to get data in a specific column from a given class, optionally filtering by student ID or first name.
        
        Args:
            class_name (str): The name of the class/table to retrieve data from.
            column_name (str): The name of the column to retrieve data from.
            student_id (str, optional): The ID of the student to filter by. Defaults to None.
            first_name (str, optional): The first name of the student to filter by. Defaults to None.
        
        Returns:
            list: A list of data from the specified column.
        """
        try:
            result = self.cursor.execute(
                f"SELECT {self.sanitise_input(column_name)} FROM {self.sanitise_input(class_name)}"
            )
            result = result.fetchall()
            for i in range(0, len(result)):
                result[i] = result[i][0]
            return result

        except Error as e:
            traceback.print_tb(e.__traceback__)
            print(f"{e.sqlite_errorname}: {e}")

    def set_data_in_column(
        self, class_name, column_name, data, student_id="", first_name=""
    ):
        """
        Sets data in the specified column for a given class and student. 

        Args:
            class_name (str): The name of the class.
            column_name (str): The name of the column to set the data in.
            data (any): The data to set in the column.
            student_id (str, optional): The ID of the student. Defaults to "".
            first_name (str, optional): The first name of the student. Defaults to "".

        Raises:
            ValueError: If both student_id and first_name are empty.

        Returns:
            None
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
        """
        Create example data for the given class_name using the provided list of students.
        
        Args:
            class_name (str): The name of the class for which the data is created.
        
        Returns:
            None
        """
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

    def createStudent(self, first_name: str, last_name: str):
        """
        Create a new student record in the database.

        Parameters:
            first_name (str): The first name of the student.
            last_name (str): The last name of the student.

        Returns:
            int or None: The ID of the newly created student record, or None if an error occurs.
        """
        try:
            query = "INSERT INTO students (first, last) VALUES (?, ?)"
            self.cursor.execute(query, (first_name, last_name))
            self.connection.commit()
            return self.cursor.lastrowid
        except Exception as e:
            # Log this exception for debugging
            print(f"Error: {e}")
            return None


if __name__ == "__main__":
    test = ClassDatabase()
    print(test.get_classes())
