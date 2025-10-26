def holdbook(conn, pr, title, author):
    db_cursor = conn.cursor()
    db_cursor.execute("""SELECT id, free FROM books WHERE title=? AND author=?""", (title, author))
    book = db_cursor.fetchone()
    if not book or book[1] <= 0:
        print("нет свободных экземпляров")
        return
    book_id = book[0]
    db_cursor.execute("""SELECT COUNT(*) FROM holds WHERE pr=?""", (pr,))
    if db_cursor.fetchone()[0] >= 5:
        print("у читателя уже 5 броней")
        return
    db_cursor.execute("""INSERT INTO holds (pr, book_id, date) VALUES (?, ?, CURRENT_DATE)""", (pr, book_id))
    db_cursor.execute("""UPDATE books SET free=free-1 WHERE id=?""", (book_id,))
    conn.commit()
    print("книга забронирована")


def unholdbook(conn, pr, title, author):
    db_cursor = conn.cursor()
    db_cursor.execute("""SELECT id FROM books WHERE title=? AND author=?""", (title, author))
    book = db_cursor.fetchone()
    if not book:
        print("книга не найдена")
        return
    book_id = book[0]
    db_cursor.execute("""DELETE FROM holds WHERE pr=? AND book_id=?""", (pr, book_id))
    db_cursor.execute("""UPDATE books SET free=free+1 WHERE id=?""", (book_id,))
    conn.commit()
    print("бронь снята")


def loanbook(conn, pr, title, author, date):
    db_cursor = conn.cursor()
    db_cursor.execute("""SELECT id, free FROM books WHERE title=? AND author=?""", (title, author))
    book = db_cursor.fetchone()
    if not book or book[1] <= 0:
        print("нет свободных экземпляров")
        return
    book_id = book[0]

    db_cursor.execute("""SELECT COUNT(*) FROM holds WHERE pr=? AND book_id=?""", (pr, book_id))
    has_hold = db_cursor.fetchone()[0] > 0

    if not has_hold:
        print("читатель не бронировал эту книгу")
        return

    db_cursor.execute("""SELECT COUNT(*) FROM loans WHERE pr=?""", (pr,))
    if db_cursor.fetchone()[0] >= 5:
        print("у читателя уже 5 книг")
        return

    db_cursor.execute("""DELETE FROM holds WHERE pr=? AND book_id=?""", (pr, book_id))
    db_cursor.execute("""INSERT INTO loans (pr, book_id, date) VALUES (?,?,?)""", (pr, book_id, date))
    db_cursor.execute("""UPDATE books SET free=free-1 WHERE id=?""", (book_id,))
    conn.commit()
    print("книга выдана")


def returnbook(conn, pr, title, author):
    db_cursor = conn.cursor()
    db_cursor.execute("""SELECT id FROM books WHERE title=? AND author=?""", (title, author))
    book = db_cursor.fetchone()
    if not book:
        print("книга не найдена")
        return

    book_id = book[0]
    db_cursor.execute("""DELETE FROM loans WHERE pr=? AND book_id=?""", (pr, book_id))
    db_cursor.execute("""UPDATE books SET free=free+1 WHERE id=?""", (book_id,))
    conn.commit()
    print("книга возвращена")


def prosroch(conn):
    db_cursor = conn.cursor()
    db_cursor.execute("""
        SELECT readers.pr, readers.full_name, books.title, books.author, loans.date AS date_return
        FROM loans
        JOIN books ON loans.book_id = books.id
        JOIN readers ON loans.pr = readers.pr
        WHERE date("now") > date(loans.date, "+14 day") """)
    return db_cursor.fetchall()


def holdsreader(conn, pr):
    db_cursor = conn.cursor()
    db_cursor.execute("""
    SELECT books.title, books.author, holds.date, date(holds.date, '+5 days') as unhold_date
    FROM holds JOIN books ON holds.book_id=books.id
    WHERE holds.pr=?
    """, (pr,))
    return db_cursor.fetchall()


def loansreader(conn, pr):
    db_cursor = conn.cursor()
    db_cursor.execute("""
    SELECT books.title, books.author, loans.date, date(loans.date, '+14 days') as return_date
    FROM loans JOIN books ON loans.book_id=books.id
    WHERE loans.pr=?
    """, (pr,))

    return db_cursor.fetchall()

def search(conn, title=None, author=None, genre=None):
    db_cursor=conn.cursor()
    db_cursor.execute("""
    SELECT title, author, genre, total, free 
    FROM books WHERE (title=? OR ? IS NULL) AND (author=? OR ? IS NULL) AND (genre=? OR ? IS NULL)
    """, (title, title, author, author, genre, genre,))
    return db_cursor.fetchall()

def autosbros(conn):
    db_cursor = conn.cursor()
    db_cursor.execute("""
        DELETE FROM holds
        WHERE date("now") > date(date, "+5 day") """)
    conn.commit()