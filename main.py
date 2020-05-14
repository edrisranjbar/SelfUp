import os
import platform
from builtins import staticmethod
from category import *
from result import *
from task import *


class App:
    """ EVALUATOR ANALYZE YOUR DATA """
    @staticmethod
    def display_menu():
        """ display a menu to choose operations """
        response = input(f"""    1) SHOW TASKS
    2) DELETE TASK
    3) ADD A NEW TASK
    4) SHOW LAST RESULTS 
    5) GET AND ADD TODAY RESULTS
    6) DELETE LAST RESULT
    7) CATEGORY MANAGEMENT
    {danger}8) Exit{end_part}
    {header}{bold}PLEASE CHOOSE ONE ITEM: (1-7) {end_part}""")

        if response == "1":
            Task.show_all(10)
        elif response == "2":
            Task.delete()
        elif response == "3":
            task = input(f"TYPE YOUR TASK TITLE: {warning}(Enter b to back){end_part} ")
            if task != "b":
                Task.add(task)
        elif response == "4":
            Result.show_lasts(10)
        elif response == "5":
            Result.add_today_results()
        elif response == "6":
            Result.delete_last_result()
        elif response == "7":
            Category.show_menu()
        elif response == "8" or response == "exit":
            global continue_app
            continue_app = False
            print(f"{header}Goodbye!{end_part}")
        else:
            print(f"{warning}Your response does not match any item; so choose again!{end_part}")
            App.display_menu()

    @staticmethod
    def clean_table(table):
        connection = sqlite3.connect(config.db_file)
        cursor = connection.cursor()
        query = f'DELETE FROM {table}'
        cursor.execute(query)
        connection.commit()
        connection.close()

    @staticmethod
    def clear():
        """ CLEAR THE TERMINAL SCREEN """
        if platform.system() == "Windows":
            os.system('cls')
        elif platform.system() == "Linux":
            os.system('clear')


if __name__ == "__main__":
    Task.create_table()
    Result.create_table()
    Task.tasks_count = Task.get_count()
    continue_app = True
    plt.rcdefaults()
    while continue_app:
        App.display_menu()
        print()
