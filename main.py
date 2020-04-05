from typing import List, Any
import os
import platform
import numpy as np
import matplotlib.pyplot as plt
import sqlite3
from datetime import datetime

class Category:
    """ To manage task categories """
    db_file = "database.db"

    def create_table(self):
        try:
            connection = sqlite3.connect(self.db_file)
            connection.execute("""CREATE TABLE IF NOT EXISTS category
                    (id integer PRIMARY KEY, name TEXT, description TEXT)""")
            connection.close()
            return True
        except:
            print(f"{danger}Can't create category table{end_part}")
            return False

    def add(self, name, description):
        """ Add a new category with some details """
        try:
            connection = sqlite3.connect(self.db_file)
            connection.execute('INSERT INTO category (name,description) VALUES ("{name}","{description}")')
            connection.close()
            return True
        except:
            print(f"{danger}Can't insert category{end_part}")
            return False

    def delete(self, id):
        """ Delete a specific category with id """
        pass

    def get_all(self):
        """ Get all of categories and returns an Array """
        pass

    def show_all(self, categories):
        """ Show all of the categories in the list """
        pass

class Evaluator:
    """ EVALUATOR ANALYZE YOUR DATA """
    db_file = "database.db"

    def __init__(self):
        self.tasks_count = self.get_tasks_count()

    def display_menu(self):
        """
            HERE WE DISPLAY A MENU;
            USER SHOULD BE ABLE TO CHOOSE AN ITEM IN MENU
            AND WE SHOULD DISPLAY SOMETHING IN EXCHANGE!
        """
        response = input("""    1) SHOW TASKS
    2) DELETE TASK
    3) ADD A NEW TASK
    4) SHOW LAST RESULTS 
    5) GET AND ADD TODAY RESULTS
    6) DELETE LAST RESULT
    7) Exit
    PLEASE CHOOSE ONE ITEM: (1-7) """)

        if response == "1":
            self.show_tasks(10)
        elif response == "2":
            self.delete_task()
        elif response == "3":
            task = input(f"TYPE YOUR TASK TITLE: {warning}(Enter b to back){end_part} ")
            if task != "b":
                self.add_task(task)
        elif response == "4":
            self.show_last_results(10)
        elif response == "5":
            self.add_today_results()
        elif response == "6":
            self.delete_last_result()
        elif response == "7" or response == "exit":
            global continue_app
            continue_app = False
            print(f"{header}Goodbye!{end_part}")
        else:
            print(f"{warning}Your response does not match any item; so choose again!{end_part}")
            self.display_menu()

    def create_tasks_table(self):
        try:
            connection = sqlite3.connect(self.db_file)
            connection.execute("""CREATE TABLE IF NOT EXISTS tasks
                    (id integer PRIMARY KEY, name TEXT)""")
            connection.close()
            return True
        except:
            print(f"{danger}Can't create tasks table{end_part}")
            return False

    def insert_task(self, task):
        connection = sqlite3.connect(self.db_file)
        cursor = connection.cursor()
        query = f'INSERT INTO tasks (name) VALUES ("{task}")'
        cursor.execute(query)
        connection.commit()
        connection.close()

    def create_results_table(self):
        connection = sqlite3.connect(self.db_file)
        cursor = connection.cursor()
        try:
            cursor.execute("""CREATE TABLE IF NOT EXISTS results
                    (id integer PRIMARY KEY, result TEXT, date DATE)""")
            connection.close()
            return True
        except:
            print(f"{danger}Can't create tasks table{end_part}")
            return False

    def insert_result(self, result, date):
        connection = sqlite3.connect(self.db_file)
        cursor = connection.cursor()
        query = f'INSERT INTO results (result,date) VALUES ("{result}","{date}")'
        cursor.execute(query)
        connection.commit()
        connection.close()

    def clean_table(self, table):
        connection = sqlite3.connect(self.db_file)
        cursor = connection.cursor()
        query = f'DELETE FROM {table}'
        cursor.execute(query)
        connection.commit()
        connection.close()

    def show_tasks(self, limit=None):
        """ RETURNS ALL TASKS """
        clear()
        conn = sqlite3.connect(self.db_file)
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

    def get_tasks(self, limit=None):
        """ RETURNS ALL TASKS """
        connection = sqlite3.connect(self.db_file)
        if limit is not None:
            query = "SELECT * FROM tasks LIMIT {}".format(limit)
        else:
            query = "SELECT * FROM tasks"
        tasks: List[Any] = connection.execute(query).fetchall()
        connection.close()
        return tasks

    def do_we_have_result(self):
        """ returns True or False """
        connection = sqlite3.connect(self.db_file)
        query = "SELECT COUNT(*) FROM results"
        cursor = connection.cursor()
        results = cursor.execute(query).fetchone()
        for result_count in results:
            if result_count > 0:
                return True
            else:
                return False

    def show_last_results(self, limit):
        clear()
        """RETURNS A GRAPHICAL CHART OF LAST RESULTS"""
        conn = sqlite3.connect(self.db_file)
        query = "SELECT * FROM results LIMIT {}".format(limit)
        results = conn.execute(query).fetchall()
        ranks = []
        dates = []
        counter = 0
        for result_id, rank, date in results:
            ranks.append(rank)
            dates.append(date)
            counter += 1
        conn.close()

        if counter > 0:
            # DISPLAY RESULTS IN A CHART
            y_pos = np.arange(len(results))

            plt.bar(y_pos, ranks, align='center', alpha=0.5)
            plt.xticks(y_pos, dates)
            plt.ylabel('LAST RESULTS')
            plt.title('last results')
            plt.show()
        else:
            print(f"{warning}There is no result to display!{end_part}")

    def get_tasks_count(self):
        """ RETURNS COUNT OF ALL OF THE TASKS """
        conn = sqlite3.connect(self.db_file)
        query = "SELECT count(*) FROM tasks"
        count = conn.execute(query).fetchone()[0]
        conn.close()
        return count

    def add_today_results(self):
        """ this method will add toda's analyze results """
        clear()
        user_answer = input(f"Do you wanna coninue? {warning}(y or n){end_part} ")
        if user_answer == "y":
            answers = []
            rank = 0
            percentage_per_task = 100 / self.tasks_count
            tasks = self.get_tasks()
            for task_id, name in tasks:
                task = name
                answer = input("Did you " + task + "? " + "(y or n) ")
                answers.append(answer)
                if answer == "y":
                    rank += percentage_per_task
                elif answer != "y" and answer != "n":
                    while answer != "y" and answer != "n":
                        print(f"{warning}please answer with y or n!{end_part}")
                        answer = input(f"{info}Did you {task} ? (y or n) {end_part}")
            rank = round(rank, 2)
            print(f"{success}You've done {str(rank)} % of your tasks!{end_part}")
            if rank > 80:
                print(f"{success}Well done! you did great!{end_part}")
            else:
                print(f"{warning}OOPS! Your rank is not good! tomorrow try more!{end_part}")
            # insert result into results table
            date = datetime.now().strftime("%Y/%m/%d")
            self.insert_result(rank, date)

    def add_task(self, task):
        """ ADD A SINGLE TASK """
        clear()
        connection = sqlite3.connect(self.db_file)
        cursor = connection.cursor()
        query = f'INSERT INTO tasks (name) VALUES ("{task}")'
        try:
            cursor.execute(query)
            connection.commit()
            print(f"{success}Task added successfully!{end_part}")
        except:
            print(f"{danger}Can not add new task{end_part}")
        finally:
            connection.close()
        return True

    def delete_task(self):
        """ DELETE A SINGLE TASK BASED ON ID """
        # Show tasks and their ids
        clear()
        there_is_task = self.show_tasks()
        if there_is_task:
            task_id = input(f"TYPE TASK ID TO REMOVE: {warning}(Enter b to back){end_part} ")
            if task_id != "b":
                connection = sqlite3.connect(self.db_file)
                cursor = connection.cursor()
                query = f'DELETE FROM tasks WHERE id="{task_id}"'
                try:
                    cursor.execute(query)
                    connection.commit()
                    print(f"{success}Task delete successfully!{end_part}")
                except:
                    print(f"{danger}Can not delete task with id {task_id}{end_part}")
                finally:
                    connection.close()
            else:
                self.display_menu()

    def delete_last_result(self):
        """ Delete last result """
        clear()
        if self.do_we_have_result():
            answer = input(f"{info}Are you sure? {end_part}{warning}(y or n){end_part}")
            if answer == "y":
                connection = sqlite3.connect(self.db_file)
                cursor = connection.cursor()
                query = "delete from results where id= (select id from results order by id desc limit 1);"
                try:
                    cursor.execute(query)
                    connection.commit()
                    print(f"{success} Last result deleted successfully!{end_part}")
                except Exception as error:
                    print(f"{danger} Sorry; can't delete last result. {error}{end_part}")
            else:
                return True
        else:
            print(f"{warning} There is no result to delete!{end_part}")


header = '\033[95m'
info = '\033[94m'
success = '\033[92m'
warning = '\033[93m'
danger = '\033[91m'
end_part = '\033[0m'
bold = '\033[1m'
underline = '\033[4m'

def clear():
    """ CLEAR THE TERMINAL SCREEN """
    if platform.system() == "Windows":
        os.system('cls')
    elif platform.system() == "Linux":
        os.system('clear')

if __name__ == "__main__":
    app = Evaluator()
    # IF NOT EXISTS
    app.create_tasks_table()
    app.create_results_table()

    continue_app = True
    plt.rcdefaults()
    while continue_app:
        app.display_menu()
        print()
