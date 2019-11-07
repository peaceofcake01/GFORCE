import sys
import csv
from cs50 import SQL
db = SQL("sqlite:///students.db")

# import what is found to be necessary and ensure that the amount of command line arguments is correct
if len(sys.argv) != 2:
    sys.exit("Usage: python import.py file.csv")

# open up data that we need of all the people and their genes
table = open(sys.argv[1], "r")

reader = csv.DictReader(table)

# Use a for loop that goes through and proceeds to split all elements of the name array and relocates them into specific spots
# Then execute everything into the database of students
for element in reader:
    name_array = element["name"].split()
    if len(name_array) == 2:
        first = name_array[0]
        middle = None
        last = name_array[1]
    else:
        first = name_array[0]
        middle = name_array[1]
        last = name_array[2]
    db.execute("INSERT INTO students (first, middle, last, house, birth) VALUES(?, ?, ?, ?, ?)",
               first, middle, last, element["house"], element["birth"])
