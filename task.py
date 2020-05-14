import sqlite3
import config
from style import *
from typing import List, Any
from main import App


class Task:
    """ handle tasks """
    @staticmethod
    def add(task):
        """ ADD A SINGLE TASK """
        App.clear()
        connection = sqlite3.connect(config.db_file)
        cursor = connection.cursor()
        query = f'INSERT INTO tasks (name) VALUES ("{task}")'
        cursor.execute(query)
        connection.commit()
        print(f"{success}Task added successfully!{end_part}")
        connection.close()
        return True

    @staticmethod
    def get_count():
        """ RETURNS COUNT OF ALL OF THE TASKS """
        conn = sqlite3.connect(config.db_file)
        query = "SELECT count(*) FROM tasks"
        count = conn.execute(query).fetchone()[0]
        conn.close()
        return count

    @staticmethod
    def show_all(limit=None):
        """ RETURNS ALL TASKS """
        App.clear()
        conn = sqlite3.connect(config.db_file)
        if limit is not None:
            query = "SELECT * FROM tasks LIMIT {}".format(limit)
        else:
            query = "SELECT * FROM tasks"
        tasks = conn.execute(query).fetchall()
        counter = 0
        for task_id, name in tasks:
            counter += 1
            print(task_id, name)
        conn.close()
        if counter < 1:
            print(f"{danger}There is no task available!{end_part}")
            return False
        return True

    @staticmethod
    def get_all(limit=None):
        """ RETURNS ALL TASKS """
        connection = sqlite3.connect(config.db_file)
        if limit is not None:
            query = "SELECT * FROM tasks LIMIT {}".format(limit)
        else:
            query = "SELECT * FROM tasks"
        tasks: List[Any] = connection.execute(query).fetchall()
        connection.close()
        return tasks

    @staticmethod
    def delete():
        """ DELETE A SINGLE TASK BASED ON ID """
        # Show tasks and their ids
        App.clear()
        there_is_task = Task.show_all()
        if there_is_task:
            task_id = input(f"TYPE TASK ID TO REMOVE: {warning}(Enter b to back){end_part} ")
            if task_id != "b":
                connection = sqlite3.connect(config.db_file)
                cursor = connection.cursor()
                query = f'DELETE FROM tasks WHERE id="{task_id}"'
                cursor.execute(query)
                connection.commit()
                print(f"{success}Task delete successfully!{end_part}")
                connection.close()
            else:
                App.display_menu()

    @staticmethod
    def create_table():
        try:
            connection = sqlite3.connect(config.db_file)
            connection.execute("""CREATE TABLE IF NOT EXISTS tasks
                    (id integer PRIMARY KEY, name TEXT)""")
            connection.close()
            return True
        except sqlite3.DatabaseError:
            print(f"{danger}Can't create tasks table{end_part}")
            return False

    @staticmethod
    def insert_task(task):
        connection = sqlite3.connect(config.db_file)
        cursor = connection.cursor()
        query = f'INSERT INTO tasks (name) VALUES ("{task}")'
        cursor.execute(query)
        connection.commit()
        connection.close()
