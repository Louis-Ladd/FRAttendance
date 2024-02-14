# hewwow :3
import sqlite3


class Database:
    def create_table(db_name, create_table_sql):
        """
        Create a table from the create_table_sql statement.
        :param db_name: Name of the database.
        :param create_table_sql: a CREATE TABLE statement.
        """
        try:
            conn = sqlite3.connect(db_name)
            cursor = conn.cursor()
            cursor.execute(create_table_sql)
            conn.commit()
        except sqlite3.Error as e:
            print(e)
        finally:
            if conn:
                conn.close()

    def insert_data(db_name, table, data):
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
            conn = sqlite3.connect(db_name)
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()
        except sqlite3.Error as e:
            print(e)
        finally:
            if conn:
                conn.close()

    def query_data(db_name, query):
        """
        Query data from the database.
        :param db_name: Name of the database.
        :param query: SELECT query.
        :return: List of tuples containing the query results.
        """
        try:
            conn = sqlite3.connect(db_name)
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

    def add_column(db_name, table_name, new_column, column_type):
        """
        Add a new column to an existing table.
        :param db_name: Name of the database.
        :param table_name: Name of the table to add the column to.
        :param new_column: Name of the new column.
        :param column_type: Data type of the new column.
        """
        sql = f"ALTER TABLE {table_name} ADD COLUMN {new_column} {column_type}"
        try:
            conn = sqlite3.connect(db_name)
            cursor = conn.cursor()
            cursor.execute(sql)
            conn.commit()
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
        finally:
            if conn:
                conn.close()

    def insert_data_into_column(db_name, table_name, column_name, data, row_id):
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
            conn = sqlite3.connect(db_name)
            cursor = conn.cursor()
            cursor.execute(sql, (data, row_id))
            conn.commit()
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
        finally:
            if conn:
                conn.close()

    def __init__(self):
        print("hewwow wowd :3")
