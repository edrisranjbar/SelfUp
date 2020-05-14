from sqlite3 import *
from typing import List, Any

import config
from style import *


class Category:
    """ To manage task categories """

    def __init__(self):
        self.create_table()

    @staticmethod
    def show_menu():
        response = input(f"""{header}CATEGORY MANAGEMENT{end_part}
        {info}  1. Show categories
            2. Add category
            3. Delete Category
            Enter 1 to 3 {end_part}{warning}(b to go back): {end_part}""")
        if response == "1":
            Category.show_all()
        elif response == "2":
            category_name = input(f"{bold}Type category name: {end_part}")
            category_description = input(f"{bold}Type category description: {end_part}")
            Category.add(category_name, category_description)
        elif response == "3":
            Category.show_all()
            category_id = input(f"{bold}Type category id to remove: {end_part}")
            Category.delete(category_id)
        elif response == "b":
            return True

    @staticmethod
    def create_table():
        try:
            connection = connect(config.db_file)
            connection.execute("""CREATE TABLE IF NOT EXISTS category
                    (id integer PRIMARY KEY, name TEXT, description TEXT)""")
            connection.close()
            return True
        except Error:
            print(f"{danger}Can't create category table{end_part}")
            return False

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
            print(f"{danger}Can't insert category{end_part}")
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
            print(f"{success}Category deleted successfuly.{end_part}")
        except Error:
            print(f"{danger}Can not delete catrgory with id {category_id}{end_part}")
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
            print(f"{danger}Can not get all categories!{end_part}")
            return False
        finally:
            connection.close()
        return categories

    @staticmethod
    def show_all():
        """ Show all of the categories in the list """
        categories = Category.get_all()
        counter = 0
        for category in categories:
            counter += 1
            print("id: " + str(category[0]) + "\t name: " + str(category[1]))
        if counter < 1:
            print(f"{danger}There is no category to display!{end_part}")
