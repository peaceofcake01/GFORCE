import sys
import csv
from cs50 import SQL
db = SQL("sqlite:///students.db")

# Import all important things and also check that the correct format and number of command line arguments are input
if len(sys.argv) != 2:
    sys.exit("Usage: python roster.py house")

# get elements that are necessary into student's roster variable that can be locally tracked down

house_choice = sys.argv[1]
students_roster = db.execute("SELECT first, middle, last, birth FROM students WHERE house = ? ORDER BY last, first", house_choice)

# Then print the correct statement based on the middle name or not
for student in students_roster:
    name1 = student["first"]
    name2 = student["middle"]
    name3 = student["last"]
    birth = student["birth"]
    if name2 == None:
        print(f"{name1} {name3}, born {birth}")
    else:
        print(f"{name1} {name2} {name3}, born {birth}")