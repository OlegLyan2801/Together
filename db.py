import sqlite3

db_connect=sqlite3.connect("reading.db")
db_cursor=db_connect.cursor()
def sozd():
    db_cursor.execute("""CREATE TABLE IF NOT EXISTS readers(
                   pr TEXT PRIMARY KEY,
                   full_name TEXT NOT NULL,
                   phone TEXT NOT NULL,
                   age TEXT NOT NULL)""")
    db_cursor.execute("""CREATE TABLE IF NOT EXISTS books(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   title TEXT NOT NULL,
                   author TEXT NOT NULL,
                   genre TEXT NOT NULL,
                   total INTEGER NOT NULL CHECK(total >= 1),
                   free INTEGER NOT NULL CHECK(free >= 0 and free <= total))""")
    db_cursor.execute("""CREATE TABLE IF NOT EXISTS loans(
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       pr TEXT NOT NULL REFERENCES readers(pr),
                       book_id INTEGER NOT NULL REFERENCES books(id),
                       date TEXT NOT NULL)""")
    db_cursor.execute("""CREATE TABLE IF NOT EXISTS holds(
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       pr TEXT NOT NULL REFERENCES readers(pr),
                       book_id INTEGER NOT NULL REFERENCES books(id),
                       date TEXT NOT NULL)""")
def cl():
    db_cursor.close()

sozd()