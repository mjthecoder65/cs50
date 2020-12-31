from cs50 import SQL
from sys import argv

db = SQL("sqlite:///students.db") # opening the database
# Check if the shell arguments are passed properly
if len(argv) < 2:
    print("usage error, roster.py houseName")
    exit()

# Query to the database for all students
students = db.execute("SELECT * FROM students WHERE house = (?) ORDER BY last", argv[1])

for student in students:
    if student['middle'] != None:
        print(f"{student['first']} {student['middle']} {student['last']}, born {student['birth']}")
    else:
        print(f"{student['first']} {student['last']}, born {student['birth']}")
