import sqlite3

db = sqlite3.connect("database.db")
for row in db.execute("SELECT * FROM users"):
    print(row)