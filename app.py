import db
import repo
import service

def main():
    conn = db.db_connect
    db.sozd()
    repo.addbook(conn, "Война и мир", "Толстой", "Роман", 2)
    repo.addbook(conn, "Преступление и наказание", "Достоевский", "Роман", 1)
    repo.addbook(conn, "Мастер и Маргарита", "Булгаков", "Фантастика", 1)
    repo.addbook(conn, "1984", "Оруэлл", "Антиутопия", 1)
    repo.addbook(conn, "Отцы и дети", "Тургенев", "Роман", 1)
    pr = repo.addreader(conn, "Отсап Сергеевич", "89993452233", 25)
    service.holdbook(conn, pr, "Война и мир", "Толстой", "01/10/25")
    service.unholdbook(conn, pr, "Война и мир", "Толстой")
    service.holdbook(conn, pr, "Преступление и наказание", "Достоевский", "02/10/25")
    service.loanbook(conn, pr, "Преступление и наказание", "Достоевский", "03/10/25")
    service.returnbook(conn, pr, "Преступление и наказание", "Достоевский")
    repo.delreader(conn, pr)
    repo.delbook(conn, "1984", "Оруэлл")
    print(service.prosroch(conn))
    print("книги на руках - ", service.loansreader(conn, pr))
    print("забронированные книги - ", service.holdsreader(conn, pr))
    print(service.search(conn, author="Достоевский"))
    service.autosbros(conn)
    db.cl
main()