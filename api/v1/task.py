import sqlite3
import config
from typing import List, Any


class Task:
    """ handle tasks """
    @staticmethod
    def is_task_name_valid(task_name):
        if task_name is None or len(task_name) > 100:
            return False
        else:
            return True

    @staticmethod
    def add(task, category_id, user_id):
        """ ADD A SINGLE TASK """
        connection = sqlite3.connect(config.db_file)
        cursor = connection.cursor()
        query = f'INSERT INTO tasks (name, category_id, user_id) VALUES ("{task}",{category_id}, {user_id})'
        cursor.execute(query)
        connection.commit()
        connection.close()
        return True

    @staticmethod
    def get_count(user_id):
        """ RETURNS COUNT OF ALL OF THE TASKS """
        conn = sqlite3.connect(config.db_file)
        query = f"SELECT count(*) FROM tasks WHERE user_id = {user_id}"
        count = conn.execute(query).fetchone()[0]
        conn.close()
        return count

    @staticmethod
    def show_all(user_id, limit=None):
        """ RETURNS ALL TASKS """
        conn = sqlite3.connect(config.db_file)
        if limit is not None:
            query = "SELECT * FROM tasks WHERE user_id={user_id} LIMIT {}".format(
                limit, user_id)
        else:
            query = "SELECT * FROM tasks"
        tasks = conn.execute(query).fetchall()
        counter = 0
        for task in tasks:
            counter += 1
        conn.close()
        if counter < 1:
            print("There is no task available!")
            return False
        return True

    @staticmethod
    def get_all(user_id, limit=None):
        """ RETURNS ALL TASKS """
        connection = sqlite3.connect(config.db_file)
        if limit is not None:
            query = "SELECT * FROM tasks WHERE user_id={user_id} LIMIT {limit}".format(
                limit=limit, user_id=user_id)
        else:
            query = "SELECT * FROM tasks WHERE user_id={user_id}".format(
                user_id=user_id)
        tasks: List[Any] = connection.execute(query).fetchall()
        connection.close()
        the_tasks = []
        for task in tasks:
            task_dict = {'id': task[0],
                         'name': task[1], 'category_id': task[2], 'user_id': task[3]}
            the_tasks.append(task_dict)
        return the_tasks

    @staticmethod
    def delete(task_id, user_id):
        """ DELETE A SINGLE TASK BASED ON ID """
        there_is_task = Task.show_all(user_id)
        if there_is_task:
            connection = sqlite3.connect(config.db_file)
            cursor = connection.cursor()
            query = f'DELETE FROM tasks WHERE id={task_id} AND user_id = {user_id}'
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
                    (id integer PRIMARY KEY, name TEXT, category_id integer, user_id integer, FOREIGN KEY(category_id) REFERENCES category(id) FOREIGN KEY(user_id) REFERENCES user(user_id))""")
            connection.close()
            print("Table created successfuly")
            return True
        except sqlite3.DatabaseError:
            print("Can't create tasks table")
            return False

    @staticmethod
    def insert_task(task, user_id):
        connection = sqlite3.connect(config.db_file)
        cursor = connection.cursor()
        query = f'INSERT INTO tasks (name) VALUES ("{task}", {user_id})'
        cursor.execute(query)
        connection.commit()
        connection.close()

    @staticmethod
    def get(task_id, user_id):
        """ gets a atsk id and returns task details """
        conn = sqlite3.connect(config.db_file)
        query = f"SELECT * FROM tasks WHERE id={task_id} AND user_id = {user_id}"
        task = conn.execute(query).fetchone()
        conn.close()
        task_dict = {'id': task[0], 'name': task[1]}
        return task_dict

    @staticmethod
    def exist(task_id, user_id):
        conn = sqlite3.connect(config.db_file)
        query = f"SELECT COUNT (*) FROM tasks WHERE id={task_id} AND user_id = {user_id}"
        count = conn.execute(query).fetchone()[0]
        conn.close()
        if count > 0:
            return True
        else:
            return False

    @staticmethod
    def update(task_id, task_name, user_id):
        connection = sqlite3.connect(config.db_file)
        cursor = connection.cursor()
        query = f"UPDATE tasks SET name='{task_name}' WHERE id={task_id} AND user_id = {user_id}"
        cursor.execute(query)
        connection.commit()
        return True
