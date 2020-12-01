from sqlite3 import *
from typing import List, Any

import config


class Category:
    """ To manage task categories """

    @staticmethod
    def create_table():
        connection = connect(config.db_file)
        connection.execute("""CREATE TABLE IF NOT EXISTS category
                (id integer PRIMARY KEY, name TEXT, description TEXT, user_id integer, FOREIGN KEY(user_id) REFERENCES user(user_id))""")
        connection.close()
        return True

    @staticmethod
    def exist(id, user_id):
        conn = connect(config.db_file)
        query = f"SELECT COUNT (*) FROM category WHERE id={id} AND user_id = {user_id}"
        count = conn.execute(query).fetchone()[0]
        conn.close()
        if count > 0:
            return True
        else:
            return False

    @staticmethod
    def get_count(user_id):
        conn = connect(config.db_file)
        query = f"SELECT count(*) FROM category WHERE user_id = {user_id}"
        count = conn.execute(query).fetchone()[0]
        conn.close()
        return count

    @staticmethod
    def add(name, description, user_id):
        """ Add a new category with some details """
        connection = connect(config.db_file)
        cursor = connection.cursor()
        cursor.execute(
            f'INSERT INTO category (name,description, user_id) VALUES ("{name}","{description}", {user_id})')
        connection.commit()
        connection.close()
        return True

    @staticmethod
    def delete(category_id, user_id):
        """ Delete a specific category with id """
        connection = connect(config.db_file)
        try:
            query = f"DELETE FROM category WHERE id='{category_id}' AND user_id = {user_id}"
            cursor = connection.cursor()
            cursor.execute(query)
            connection.commit()
        except Error:
            return False
        finally:
            connection.close()
        return True

    @staticmethod
    def update(category_id, user_id, category_name, description=""):
        connection = connect(config.db_file)
        cursor = connection.cursor()
        if description == "":
            query = f"UPDATE category SET name='{category_name}' WHERE id={category_id} AND user_id = {user_id}"
        else:
            query = f"UPDATE category SET name='{category_name}', description='{description}' WHERE id={category_id} AND user_id = {user_id}"
        cursor.execute(query)
        connection.commit()
        return True

    @staticmethod
    def get_all(user_id):
        """ Get all of categories and returns an Array """
        connection = connect(config.db_file)
        query = f"SELECT * FROM category WHERE user_id = {user_id}"
        try:
            categories: List[Any] = connection.execute(query).fetchall()
        except Error:
            return False
        finally:
            connection.close()
        categories_array = []
        for category in categories:
            category_dict = {
                'id': category[0], 'name': category[1], 'description': category[2], 'user_id': category[3]}
            categories_array.append(category_dict)
        return categories_array
