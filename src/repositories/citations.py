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
