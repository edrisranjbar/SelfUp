import sqlite3
from core import config
from typing import List, Any


class Task:
    """ handle tasks """

    @staticmethod
    def add(task):
        """ ADD A SINGLE TASK """
        connection = sqlite3.connect(config.db_file)
        cursor = connection.cursor()
        query = f'INSERT INTO tasks (name) VALUES ("{task}")'
        cursor.execute(query)
        connection.commit()
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
            print("There is no task available!")
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
        the_tasks = []
        for task in tasks:
            task_dict = {'id': task[0], 'name': task[1]}
            the_tasks.append(task_dict)
        return the_tasks

    @staticmethod
    def delete(task_id):
        """ DELETE A SINGLE TASK BASED ON ID """
        there_is_task = Task.show_all()
        if there_is_task:
            connection = sqlite3.connect(config.db_file)
            cursor = connection.cursor()
            query = f'DELETE FROM tasks WHERE id="{task_id}"'
            cursor.execute(query)
            connection.commit()
            connection.close()
            return True
        else:
            return False

    @staticmethod
    def create_table():
        try:
            connection = sqlite3.connect(config.db_file)
            connection.execute("""CREATE TABLE IF NOT EXISTS tasks
                    (id integer PRIMARY KEY, name TEXT)""")
            connection.close()
            return True
        except sqlite3.DatabaseError:
            print(f"Can't create tasks table")
            return False

    @staticmethod
    def insert_task(task):
        connection = sqlite3.connect(config.db_file)
        cursor = connection.cursor()
        query = f'INSERT INTO tasks (name) VALUES ("{task}")'
        cursor.execute(query)
        connection.commit()
        connection.close()
