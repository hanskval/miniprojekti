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
    return db.session.execute(sql).fetchall()

def get_column_names():
    sql = text("PRAGMA table_info(citations)")
    result = db.session.execute(sql).fetchall()
    return [row[1] for row in result]

def remove_book_citation(citation_id):
    sql = text("DELETE FROM citations WHERE id = ?")
    db.session.execute(sql, [citation_id])
    db.session.commit()

def update_book_citation(citation_id, citation_type, author, title, year, publisher):
    sql ="""
    UPDATE citations SET type = ?, author = ?, title = ?, year = ?, publisher = ? WHERE id = ?
    """
    db.session.execute(sql, [citation_type, author, title, year, publisher, citation_id])
    db.session.commit()