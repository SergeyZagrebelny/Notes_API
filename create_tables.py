import sqlite3

connection = sqlite3.connect("data.db")
cursor = connection.cursor()

users_table_creation = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)"
cursor.execute(users_table_creation)

notes_table_creation = "CREATE TABLE IF NOT EXISTS notes (id INTEGER PRIMARY KEY, title text, content real)"
cursor.execute(notes_table_creation)

connection.commit()
connection.close()