import sqlite3

def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        #print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


def create_task_table(db_file):
    conn = sqlite3.connect(db_file)
    try:
        conn.execute("""CREATE TABLE tasks
                 (id integer PRIMARY KEY, name TEXT)""")
        return True
    except:
        return False


create_connection("database.db")
if create_task_table("database.db"):
    print("---------------- TASKS TABLE CREATED ----------------")
else:
    print("---------------- ERROR: CAN'T CREATE TASKS TABLE ----------------")
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

# TODO: save the result into sqlite database
# TODO: save tasks into sqlite database