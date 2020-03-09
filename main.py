import sqlite3
from datetime import datetime
# Configs
db_file = "database.db"

def display_menu():
    """
        HERE WE DISPLAY A MENU;
        USER SHOULD BE ABLE TO CHOOSE AN ITEM IN MENU
        AND WE SHOULD DISPLAY SOMETHING IN EXCHANGE!
    """
    response = input("""PLEASE CHOOS ONE ITEM: (1-4)
    1) SHOW TASKS
    2) DELETE TASK
    3) ADD A NEW TASK
    4) SHOW LAST RESULTS 
    """)

    if response == "1":
        show_tasks(10)
    elif response == "2":
        delete_tasks()
    elif response == "3":
        add_task()
    elif response == "4":
        show_last_results()
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

def show_tasks(limit):
    """RETURNS A GRAPHICAL CHART OF LAST RESULTS"""
    conn = sqlite3.connect(db_file)
    query = "SELECT * FROM results LIMIT {}".format(limit)
    results = conn.execute(query).fetchall()
    for id,rank,date in results:
        print(id,rank,date)
    conn.close()
    # DISPLAY RESULTS IN A CHART


create_tasks_table()
create_results_table()
clean_table("tasks")
display_menu()

# tasks that I should do every single day
tasks = [
    'Sleep early in the night',
    'Wake up early in the morning',
    'Read Quran and think about it',
    'Drink 1 liter water per day',
    'Eat vegetables',
    'Make a plan for next day',
    'Improve relationships',
    'Stay happy',
    'Learn English',
    'Exercise',
    'Study',
    'Code',
    'Help others'
]
for task in tasks:
    insert_task(task)

answers = []
rank = 0
percentage_per_task = 100 / len(tasks)
for task in tasks:
    answer = input("Did you " + task + "? " + "(y or n) ")
    answers.append(answer)
    if answer == "y":
        rank += percentage_per_task
rank = round(rank,2)
print("You've done " + str(rank) + "% of your tasks!")
if rank > 80:
    print("Well done! you did great!")
else:
    print("OOPS! Your rank is not good! tomorrow try more!")
# insert result into results table
date = datetime.now().strftime("%Y/%m/%d")
insert_result(rank, date)