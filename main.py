from typing import List, Any

import numpy as np
import matplotlib.pyplot as plt
import sqlite3
from datetime import datetime

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
            task = input("TYPE YOUR TASK TITLE: ")
            self.add_task(task)
        elif response == "4":
            self.show_last_results(10)
        elif response == "5":
            self.add_today_results()
        elif response == "6":
            self.delete_last_result()
        elif response == "7":
            global continue_app
            continue_app = False
            print(f"{Styles.header}Goodbye!{Styles.end_part}")
        else:
            print(f"{Styles.warning}Your response does not match any item; so choose again!{Styles.end_part}")
            self.display_menu()


    def create_tasks_table(self):
        try:
            connection = sqlite3.connect(self.db_file)
            connection.execute("""CREATE TABLE IF NOT EXISTS tasks
                    (id integer PRIMARY KEY, name TEXT)""")
            connection.close()
            return True
        except:
            print(f"{Styles.danger}Can't create tasks table{Styles.end_part}")
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
            print(f"{Styles.danger}Can't create tasks table{Styles.end_part}")
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
            print(f"{Styles.danger}There is no task available!{Styles.end_part}")
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
            print(f"{Styles.warning}There is no result to display!{Styles.end_part}")


    def get_tasks_count(self):
        """ RETURNS COUNT OF ALL OF THE TASKS """
        conn = sqlite3.connect(self.db_file)
        query = "SELECT count(*) FROM tasks"
        count = conn.execute(query).fetchone()[0]
        conn.close()
        return count


    def add_today_results(self):
        """ this method will add toda's analyze results """
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
                    print(f"{Styles.warning}please answer with y or n!{Styles.end_part}")
                    answer = input(f"{Styles.info}Did you " + task + "? " + "(y or n) {Styles.end_part}")
        rank = round(rank, 2)
        print(f"{Styles.success}You've done {str(rank)} % of your tasks!{Styles.end_part}")
        if rank > 80:
            print(f"{Styles.success}Well done! you did great!{Styles.end_part}")
        else:
            print(f"{Styles.warning}OOPS! Your rank is not good! tomorrow try more!{Styles.end_part}")
        # insert result into results table
        date = datetime.now().strftime("%Y/%m/%d")
        self.insert_result(rank, date)


    def add_task(self, task):
        """ ADD A SINGLE TASK """
        connection = sqlite3.connect(self.db_file)
        cursor = connection.cursor()
        query = f'INSERT INTO tasks (name) VALUES ("{task}")'
        try:
            cursor.execute(query)
            connection.commit()
            print(f"{Styles.success}Task added successfully!{Styles.end_part}")
        except:
            print(f"{Styles.danger}Can not add new task{Styles.end_part}")
        finally:
            connection.close()
        return True


    def delete_task(self):
        """ DELETE A SINGLE TASK BASED ON ID """
        # Show tasks and their ids
        there_is_task = self.show_tasks()
        if there_is_task:
            task_id = input("TYPE TASK ID TO REMOVE: ")
            connection = sqlite3.connect(self.db_file)
            cursor = connection.cursor()
            query = f'DELETE FROM tasks WHERE id="{task_id}"'
            try:
                cursor.execute(query)
                connection.commit()
                print(f"{Styles.success}Task delete successfully!{Styles.end_part}")
            except:
                print(f"{Styles.danger}Can not delete task with id {task_id}{Styles.end_part}")
            finally:
                connection.close()


    def delete_last_result(self):
        """ Delete last result """
        if self.do_we_have_result():
            connection = sqlite3.connect(self.db_file)
            cursor = connection.cursor()
            query = "delete from results where id= (select id from results order by id desc limit 1);"
            try:
                cursor.execute(query)
                connection.commit()
                print(f"{Styles.success} Last result deleted successfully!{Styles.end_part}")
            except Exception as error:
                print(f"{Styles.danger} Sorry; can't delete last result. {error}{Styles.end_part}")
        else:
            print(f"{Styles.warning} There is no result to delete!{Styles.end_part}")


class Styles:
    """ IN ORDER TO USE Styles WE SHOULD USE THESE CONSTANTS EASILY! """
    header = '\033[95m'
    info = '\033[94m'
    success = '\033[92m'
    warning = '\033[93m'
    danger = '\033[91m'
    end_part = '\033[0m'
    bold = '\033[1m'
    underline = '\033[4m'


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
