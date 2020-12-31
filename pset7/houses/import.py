from cs50 import SQL
from csv import reader
from sys import argv

# opening the database
db = SQL("sqlite:///students.db")

# check that we launched the code with proper arguments, otherwise it exits
if len(argv) < 2:
    print("usage error, import.py characters.csv")
    exit()

# open the csv file containing the students info and copy the content into a list
with open(argv[1], newline='') as charactersFile:
    characters = reader(charactersFile)
    for character in characters:
        if character[0] == 'name':
            continue

        fullName = character[0].split()
        # insert the name and the other infos in the database
        if len(fullName) < 3:
            db.execute("INSERT INTO students(first, middle, last, house, birth) VALUES(?, ?, ?, ?, ?)",
                       fullName[0], None, fullName[1], character[1], character[2])

        else:
            db.execute("INSERT INTO students(first, middle, last, house, birth) VALUES(?, ?, ?, ?, ?)",
                       fullName[0], fullName[1], fullName[2], character[1], character[2])
