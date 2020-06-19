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
    def exist(id):
        conn = connect(config.db_file)
        query = f"SELECT COUNT (*) FROM category WHERE id={id}"
        count = conn.execute(query).fetchone()[0]
        conn.close()
        if count > 0:
            return True
        else:
            return False

    @staticmethod
    def add(name, description):
        """ Add a new category with some details """
        connection = connect(config.db_file)
        cursor = connection.cursor()
        cursor.execute(f'INSERT INTO category (name,description) VALUES ("{name}","{description}")')
        connection.commit()
        connection.close()
        return True


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
    def update(category_id, category_name, description=""):
        connection = connect(config.db_file)
        cursor = connection.cursor()
        if description is None:
            query = f"UPDATE category SET name='{category_name}' WHERE id={category_id}"
        else:
            query = f"UPDATE category SET name='{category_name}', description='{description}' WHERE id={category_id}"
        cursor.execute(query)
        connection.commit()
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
        categories_array = []
        for category in categories:
            category_dict = {'id': category[0], 'name': category[1], 'description': category[2]}
            categories_array.append(category_dict)
        return categories_array
