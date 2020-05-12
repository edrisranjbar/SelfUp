import sqlite3
from datetime import datetime

from style import *
import numpy as np
from task import Task
import config
from main import App


class Result:
    @staticmethod
    def do_we_have_result():
        """ returns True or False """
        connection = sqlite3.connect(config.db_file)
        query = "SELECT COUNT(*) FROM results"
        cursor = connection.cursor()
        results = cursor.execute(query).fetchone()
        for result_count in results:
            if result_count > 0:
                return True
            else:
                return False

    @staticmethod
    def show_lasts(limit, plt=None):
        App.clear()
        """RETURNS A GRAPHICAL CHART OF LAST RESULTS"""
        conn = sqlite3.connect(config.db_file)
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

    @staticmethod
    def add_today_results():
        """ this method will add toda's analyze results """
        App.clear()
        user_answer = input(f"Do you wanna coninue? {warning}(y or n){end_part} ")
        if user_answer == "y":
            answers = []
            rank = 0
            percentage_per_task = 100 / Task.get_count()
            tasks = Task.get_all()
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
            Result.insert_result(rank, date)

    @staticmethod
    def create_table():
        connection = sqlite3.connect(config.db_file)
        cursor = connection.cursor()
        try:
            cursor.execute("""CREATE TABLE IF NOT EXISTS results
                    (id integer PRIMARY KEY, result TEXT, date DATE)""")
            connection.close()
            return True
        except:
            print(f"{danger}Can't create tasks table{end_part}")
            return False

    @staticmethod
    def insert_result(result, date):
        connection = sqlite3.connect(config.db_file)
        cursor = connection.cursor()
        query = f'INSERT INTO results (result,date) VALUES ("{result}","{date}")'
        cursor.execute(query)
        connection.commit()
        connection.close()

    @staticmethod
    def delete_last_result():
        """ Delete last result """
        App.clear()
        if Result.do_we_have_result():
            answer = input(f"{info}Are you sure? {end_part}{warning}(y or n){end_part}")
            if answer == "y":
                connection = sqlite3.connect(config.db_file)
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
