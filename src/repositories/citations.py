from config import db
from sqlalchemy import text
import re


def get_column_metadata():
    rows = db.session.execute(text("PRAGMA table_info(citations)")).fetchall()
    return [
        {
            "name": row[1],
            "type": row[2].upper(),
            "required": bool(row[3] and row[5] == 0 and row[1] != "type"),
        }
        for row in rows
        if row[1] != "id" and row[5] == 0
    ]


def get_column_names():
    return [column["name"] for column in get_column_metadata()]


def create_citation(data):
    columns = get_column_metadata()
    allowed = {column["name"]: column for column in columns}
    citation = {}

    for name, column in allowed.items():
        if name not in data:
            if name == "type":
                citation[name] = "misc"
                continue
            if column["required"]:
                raise ValueError(f"{name} is required.")
            continue

        value = str(data[name]).strip()
        if not value:
            if name == "type":
                citation[name] = "misc"
                continue
            if column["required"]:
                raise ValueError(f"{name} is required.")
            continue

        if "INT" in column["type"]:
            try:
                value = int(value)
            except ValueError as exc:
                raise ValueError(f"{name} must be a number.") from exc

        if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", name):
            raise ValueError("Invalid citation field.")
        citation[name] = value

    if not citation:
        raise ValueError("At least one citation field is required.")

    names = ", ".join(f'"{name}"' for name in citation)
    placeholders = ", ".join(f":{name}" for name in citation)
    db.session.execute(
        text(f"INSERT INTO citations ({names}) VALUES ({placeholders})"),
        citation,
    )
    db.session.commit()


def create_book_citation(citation_type, author, title, year, publisher):
    create_citation({
        "type": citation_type,
        "author": author,
        "title": title,
        "year": year,
        "publisher": publisher,
    })

def get_citations():
    names = get_column_names()
    names_with_id = ["id", *names]
    sql = text(
        "SELECT " +
        ", ".join(f'"{name}"' for name in names_with_id) +
        " FROM citations ORDER BY id"
    )
    return db.session.execute(sql).fetchall()

def get_citation(citation_id):
    names = get_column_names()
    names_with_id = ["id", *names]
    sql = text(
        "SELECT " +
        ", ".join(f'"{name}"' for name in names_with_id) +
        " FROM citations WHERE id = :id"
    )
    return db.session.execute(sql, {"id": citation_id}).fetchone()

