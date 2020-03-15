import sqlite3
from datetime import datetime
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt


# Configs
db_file = "database.db"

def display_menu():
    """
        HERE WE DISPLAY A MENU;
        USER SHOULD BE ABLE TO CHOOSE AN ITEM IN MENU
        AND WE SHOULD DISPLAY SOMETHING IN EXCHANGE!
    """
    response = input("""PLEASE CHOOS ONE ITEM: (1-5)
    1) SHOW TASKS
    2) DELETE TASK
    3) ADD A NEW TASK
    4) SHOW LAST RESULTS 
    5) GET AND ADD TODAY RESULTS
    """)

    if response == "1":
        show_tasks(10)
    elif response == "2":
        delete_task()
    elif response == "3":
        task = input("TYPE YOUR TASK TITLE: ")
        add_task(task)
    elif response == "4":
        show_last_results(10)
    elif response == "5":
        add_today_results()
    else:
        print("Your response does not match any item; so choose again!")
        display_menu()

def create_tasks_table():
    conn = sqlite3.connect(db_file)
    try:
        conn.execute("""CREATE TABLE IF NOT EXISTS tasks
                 (id integer PRIMARY KEY, name TEXT)""")
        return True
    except:
        return False
    conn.close()

def insert_task(task):
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    query = f'INSERT INTO tasks (name) VALUES ("{task}")'
    conn.execute(query)
    conn.commit()
    conn.close()

def create_results_table():
    conn = sqlite3.connect(db_file)
    try:
        conn.execute("""CREATE TABLE IF NOT EXISTS results
                 (id integer PRIMARY KEY, result TEXT, date DATE)""")
        return True
    except:
        return False
    conn.close()

def insert_result(result,date):
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    query = f'INSERT INTO results (result,date) VALUES ("{result}","{date}")'
    conn.execute(query)
    conn.commit()
    conn.close()

def clean_table(table):
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    query = f'DELETE FROM {table}'
    conn.execute(query)
    conn.commit()
    conn.close()

def show_tasks(limit=None,show_id=False):
    """ RETURNS ALL TASKS """
    conn = sqlite3.connect(db_file)
    if limit != None:
        query = "SELECT * FROM tasks LIMIT {}".format(limit)
    else:
        query = "SELECT * FROM tasks"
    tasks = conn.execute(query).fetchall()
    for id,name in tasks:
        print(id,name)
    conn.close()

def get_tasks(limit=None):
    """ RETURNS ALL TASKS """
    conn = sqlite3.connect(db_file)
    if limit != None:
        query = "SELECT * FROM tasks LIMIT {}".format(limit)
    else:
        query = "SELECT * FROM tasks"
    tasks = conn.execute(query).fetchall()
    conn.close()
    return tasks

def show_last_results(limit):
    """RETURNS A GRAPHICAL CHART OF LAST RESULTS"""
    conn = sqlite3.connect(db_file)
    query = "SELECT * FROM results LIMIT {}".format(limit)
    results = conn.execute(query).fetchall()
    ranks = []
    dates = []
    for id,rank,date in results:
        ranks.append(rank)
        dates.append(date)
    conn.close()
    # DISPLAY RESULTS IN A CHART
    y_pos = np.arange(len(results))

    plt.bar(y_pos, ranks, align='center', alpha=0.5)
    plt.xticks(y_pos, dates)
    plt.ylabel('LAST RESULTS')
    plt.title('last results')
    plt.show()

def get_tasks_count():
    """ RETURNS COUNT OF ALL OF THE TASKS """
    conn = sqlite3.connect(db_file)
    query = "SELECT count(*) FROM tasks"
    count = conn.execute(query).fetchone()[0]
    conn.close()
    return count


def add_today_results():
    answers = []
    rank = 0
    percentage_per_task = 100 / tasks_count
    tasks = get_tasks()
    for id,name in tasks:
        task = name
        answer = input("Did you " + task + "? " + "(y or n) ")
        answers.append(answer)
        if answer == "y":
            rank += percentage_per_task
        elif answer is not "y" and answer is not "n":
            while answer is not "y" and answer is not "n":
                print("please answer with y or n!")
                answer = input("Did you " + task + "? " + "(y or n) ")
    rank = round(rank,2)
    print("You've done " + str(rank) + "% of your tasks!")
    if rank > 80:
        print("Well done! you did great!")
    else:
        print("OOPS! Your rank is not good! tomorrow try more!")
    # insert result into results table
    date = datetime.now().strftime("%Y/%m/%d")
    insert_result(rank, date)


def add_task(task):
    """ ADD A SINGLE TASK """
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    query = f'INSERT INTO tasks (name) VALUES ("{task}")'
    try:
        conn.execute(query)
        conn.commit()
        print("task added successfuly!")
    except:
        print("ERROR: can not add new task")
    finally:
        conn.close()
    return True


def delete_task():
    """ DELETE A SINGLE TASK BASED ON ID """
    # Show tasks and their ids
    show_tasks(show_id=True)
    task_id = input("TYPE TASK ID TO REMOVE: ")
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    query = f'DELETE FROM tasks WHERE id="{task_id}"'
    try:
        conn.execute(query)
        conn.commit()
    except:
        print("ERROR: can not delete task with id {}".format(task_id))
    finally:
        conn.close()

# IF NOT EXISTS
create_tasks_table()
create_results_table()
tasks_count = get_tasks_count()
display_menu()