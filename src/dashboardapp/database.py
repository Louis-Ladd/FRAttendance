import sqlite3


#TODO: 
#   Add student lookup
#   Follow object oreintated programming paradigms
#   Check if .db file exists, then check if table exists within sql.
#   STRUCTURE Plan: 
#   Databases hold every class which are tables, 
#   The students have the columns: first name, last name, UUID (generated at student(row) creation), path to photo(s)

class ClassDatabase:
    def __init__(self, bruh):
        self.db_name = "database.db"

    def create_class(self, class_name : str):
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute(f"CREATE TABLE {class_name}(first, last, id, photo_path)")
            conn.commit()
        except sqlite3.Error as e:
            print(e)
        finally:
            if conn:
                conn.close()

    def insert_data(self, table, data):
        """
        Insert data into a table.
        :param db_name: Name of the database.
        :param table: Table name to insert data into.
        :param data: Dictionary of column-value pairs to insert.
        """
        columns = ", ".join(data.keys())
        placeholders = ":" + ", :".join(data.keys())
        sql = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"

        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()
        except sqlite3.Error as e:
            print(e)
        finally:
            if conn:
                conn.close()

    def query_data(self, query):
        """
        Query data from the database.
        :param db_name: Name of the database.
        :param query: SELECT query.
        :return: List of tuples containing the query results.
        """
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute(query)
            results = cursor.fetchall()
            return results
        except sqlite3.Error as e:
            print(e)
            return []
        finally:
            if conn:
                conn.close()

    def add_column(self, table_name, new_column, column_type):
        """
        Add a new column to an existing table.
        :param db_name: Name of the database.
        :param table_name: Name of the table to add the column to.
        :param new_column: Name of the new column.
        :param column_type: Data type of the new column.
        """
        sql = f"ALTER TABLE {table_name} ADD COLUMN {new_column} {column_type}"
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute(sql)
            conn.commit()
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
        finally:
            if conn:
                conn.close()

    def insert_data_into_column(self, table_name, column_name, data, row_id):
        """
        Insert data into a specific column for a specific row.
        :param db_name: Name of the database.
        :param table_name: Name of the table.
        :param column_name: Name of the column to insert data into.
        :param data: Data to be inserted.
        :param row_id: The ID of the row to insert the data into.
        """
        sql = f"UPDATE {table_name} SET {column_name} = ? WHERE id = ?"
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute(sql, (data, row_id))
            conn.commit()
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
        finally:
            if conn:
                conn.close()

test = ClassDatabase()

print(type(test))