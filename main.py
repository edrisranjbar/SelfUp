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
print("You've done " + str(rank) + "% of your tasks!")

# TODO: to save the result into sqlite database