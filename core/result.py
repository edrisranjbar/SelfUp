from sqlite3 import *
from datetime import datetime
from matplotlib import pyplot as plt
import numpy as np
from core.task import Task
from core import config


class Result:
    @staticmethod
    def do_we_have_result():
        """ returns True or False """
        connection = connect(config.db_file)
        query = "SELECT COUNT(*) FROM results"
        cursor = connection.cursor()
        results = cursor.execute(query).fetchone()
        for result_count in results:
            if result_count > 0:
                return True
            else:
                return False

    @staticmethod
    def show_lasts(limit):
        """RETURNS A GRAPHICAL CHART OF LAST RESULTS"""
        conn = connect(config.db_file)
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

    @staticmethod
    def add_today_results():
        """ this method will add today's analyze results """
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
                    print("please answer with y or n!")
                    answer = input(f"Did you {task} ? (y or n)")
        rank = round(rank, 2)
        print(f"You've done {str(rank)}% of your tasks!")
        # insert result into results table
        date = datetime.now().strftime("%Y/%m/%d")
        Result.insert_result(rank, date)

    @staticmethod
    def create_table():
        connection = connect(config.db_file)
        cursor = connection.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS results (id integer PRIMARY KEY, result TEXT, date DATE)""")
        connection.close()
        return True

    @staticmethod
    def insert_result(result, date):
        connection = connect(config.db_file)
        cursor = connection.cursor()
        query = f'INSERT INTO results (result,date) VALUES ("{result}","{date}")'
        cursor.execute(query)
        connection.commit()
        connection.close()

    @staticmethod
    def delete_last_result():
        """ Delete last result """
        if Result.do_we_have_result():
            connection = connect(config.db_file)
            cursor = connection.cursor()
            query = "delete from results where id= (select id from results order by id desc limit 1);"
            cursor.execute(query)
            connection.commit()
        else:
            print("There is no result to delete!")
