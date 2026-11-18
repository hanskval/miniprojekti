from config import db
from sqlalchemy import text


def create_book_citation(citation_type, author, title, year, publisher):
    sql = text(
        "INSERT INTO citations (type, author, title, year, publisher) "
        "VALUES (:type, :author, :title, :year, :publisher)"
    )
    db.session.execute(
        sql,
        {
            "type": citation_type,
            "author": author,
            "title": title,
            "year": year,
            "publisher": publisher,
        },
    )
    db.session.commit()

def get_citations():
    sql = text("SELECT id, type, author, title, year, publisher FROM citations ORDER BY id")
<<<<<<< HEAD
    return db.session.execute(sql).fetchall()
=======
    return db.session.execute(sql).fetchall()

def get_column_names():
    sql = text("PRAGMA table_info(citations)")
    result = db.session.execute(sql).fetchall()
    return [row[1] for row in result]
>>>>>>> c9b688f14a2d4c17d5819c0e499474d2d4d71a2c
