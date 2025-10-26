def genpr(full_name, phone):
    first, last=full_name.split()
    return first[0].upper()+last[0].upper()+str(len(first))+str(len(last))+phone[-4:]

def addbook(conn,title,author,genre,n=1):
    db_cursor=conn.cursor()
    db_cursor.execute("""SELECT id FROM books WHERE title=? AND author=?""", (title, author))
    row = db_cursor.fetchone()
    if row:
        db_cursor.execute("""UPDATE books SET total=total+?, free=free+? WHERE id=?""", (n, n, row[0]))
        print("книга обновлена")
    else:
        db_cursor.execute(
            """INSERT INTO books (title, author, genre, total, free) VALUES (?,?,?,?,?)""",
            (title, author, genre, n, n)

        )

        print("книга добавлена")
    conn.commit()


def delbook(conn, title, author):
    db_cursor = conn.cursor()
    db_cursor.execute("""
        SELECT b.id, 
               (SELECT COUNT(*) FROM loans WHERE book_id = b.id) as loan_count,
               (SELECT COUNT(*) FROM holds WHERE book_id = b.id) as hold_count
        FROM books b 
        WHERE b.title = ? AND b.author = ?""", (title, author))
    row = db_cursor.fetchone()
    if not row:
        print("книга не найдена")
        return
    book_id, loan_count, hold_count = row

    if loan_count > 0:
        print("книгу уже взяли")
        return

    if hold_count > 0:
        print("книга забронирована")
        return

    db_cursor.execute("DELETE FROM books WHERE id = ?", (book_id,))
    conn.commit()
    print("книга удалена")


def addreader(conn, full_name, phone, age):
    cursor=conn.cursor()
    pr = genpr(full_name, phone)
    cursor.execute("""SELECT 1 FROM readers WHERE pr = ?""", (pr,))
    if cursor.fetchone():
        print("читатель уже существует")
        return pr
    cursor.execute(
        """INSERT INTO readers (pr, full_name, phone, age) VALUES (?,?,?,?)""",
        (pr, full_name, phone, age)
    )
    conn.commit()
    print("читатель добавлен")
    return pr


def delreader(conn, pr):
    db_cursor = conn.cursor()
    db_cursor.execute("""SELECT 
               (SELECT COUNT(*) FROM loans WHERE pr = ?),
               (SELECT COUNT(*) FROM holds WHERE pr = ?)""", (pr, pr))
    row = db_cursor.fetchone()
    if not row:
        print("читатель не найден")
        return
    loan_count, hold_count = row

    if loan_count > 0:
        print("у читателя есть книги")
        return

    if hold_count > 0:
        print("у читателя есть брони")
        return

    db_cursor.execute("DELETE FROM readers WHERE pr = ?", (pr,))
    conn.commit()
    print("читатель удалён")