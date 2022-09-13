

import sqlite3


connection = sqlite3.connect('database.db')
print("Opened the database successfully!")

cursor = connection.cursor()

cursor.execute("DROP TABLE IF EXISTS LOGIN")

login_table = """ CREATE TABLE LOGIN (
            Email VARCHAR(255),
            Name CHAR(25),
            Password VARCHAR(50)); """

cursor.execute(login_table)

cursor.execute("DROP TABLE IF EXISTS HABIT")

habit_table = """ CREATE TABLE HABIT (
            Habit CHAR(25),
            Hours int,
            Minutes int); """

cursor.execute(habit_table)

print("Tables are created successfully!")

connection.commit()
connection.close()