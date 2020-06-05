from sqlite3 import *
from typing import List, Any

import config


class Category:
    """ To manage task categories """

    def __init__(self):
        self.create_table()

    @staticmethod
    def create_table():
        connection = connect(config.db_file)
        connection.execute("""CREATE TABLE IF NOT EXISTS category
                (id integer PRIMARY KEY, name TEXT, description TEXT)""")
        connection.close()
        return True

    @staticmethod
    def add(name, description):
        """ Add a new category with some details """
        try:
            connection = connect(config.db_file)
            cursor = connection.cursor()
            cursor.execute(f'INSERT INTO category (name,description) VALUES ("{name}","{description}")')
            connection.commit()
            connection.close()
            return True
        except Error:
            return False

    @staticmethod
    def delete(category_id):
        """ Delete a specific category with id """
        connection = connect(config.db_file)
        try:
            query = f"DELETE FROM category WHERE id='{category_id}'"
            cursor = connection.cursor()
            cursor.execute(query)
            connection.commit()
        except Error:
            return False
        finally:
            connection.close()
        return True

    @staticmethod
    def get_all():
        """ Get all of categories and returns an Array """
        connection = connect(config.db_file)
        query = "SELECT * FROM category"
        try:
            categories: List[Any] = connection.execute(query).fetchall()
        except Error:
            return False
        finally:
            connection.close()
        return categories
