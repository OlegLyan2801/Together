def holdbook(conn, pr, title, author, date):
    db_cursor=conn.cursor()
    db_cursor.execute("""SELECT id, free FROM books WHERE title=? AND author=?""", (title, author))
    book=db_cursor.fetchone()
    if not book or book[1]<=0:
        print("нет свободных экземпляров")
    book_id=book[0]
    db_cursor.execute("""SELECT COUNT(*) FROM holds WHERE pr=?""", (pr,))
    if db_cursor.fetchone()[0]>=5:
        print("у читателя уже 5 броней")
    db_cursor.execute("""INSERT INTO holds (pr, book_id, date) VALUES (?, ?, ?)""", (pr, book_id, date))
    db_cursor.execute("""UPDATE books SET free=free-1 WHERE id=?""", (book_id,))
    conn.commit()
    print("книга забронирована")

def unholdbook(conn, pr, title, author):
    db_cursor=conn.cursor()
    db_cursor.execute("""SELECT id FROM books WHERE title=? AND author=?""", (title, author))
    book=db_cursor.fetchone()
    if not book:
        print("книга не найдена")
    book_id=book[0]
    db_cursor.execute("""DELETE FROM holds WHERE pr=? AND book_id=?""", (pr, book_id))
    db_cursor.execute("""UPDATE books SET free=free+1 WHERE id=?""", (book_id,))
    conn.commit()
    print("бронь снята")