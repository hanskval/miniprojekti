from sqlalchemy import text
from config import db



COMMON_FIELDS = ("title", "author", "year")
OPTIONAL_FIELDS = ("month", "note")
CITATION_FIELDS = {
    "book": ("publisher",),
    "article": ("journal", "volume", "issue", "pages"),
    "inproceedings": ("booktitle",),
}
INPROCEEDINGS_OPTIONAL_FIELDS = (
    "editor", "volume", "issue", "series", "pages", "address",
    "organization", "publisher",
)


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
    citation_type = str(data.get("type", "")).strip().lower()
    if citation_type not in CITATION_FIELDS:
        raise ValueError("Citation type must be book, article or inproceedings.")

    optional_fields = OPTIONAL_FIELDS
    if citation_type == "inproceedings":
        optional_fields = (*INPROCEEDINGS_OPTIONAL_FIELDS, *OPTIONAL_FIELDS)
    fields = (*COMMON_FIELDS, *CITATION_FIELDS[citation_type], *optional_fields)
    unexpected_fields = {
        name for name, value in data.items()
        if name not in {"type", *fields} and str(value).strip()
    }
    if unexpected_fields:
        raise ValueError("The submitted fields do not match the citation type.")

    citation = {"type": citation_type}
    for name in (*COMMON_FIELDS, *CITATION_FIELDS[citation_type]):
        value = str(data.get(name, "")).strip()
        if not value:
            raise ValueError(f"{name} is required.")
        if name == "year":
            try:
                value = int(value)
            except ValueError as exc:
                raise ValueError("year must be a number.") from exc
        citation[name] = value

    for name in optional_fields:
        value = str(data.get(name, "")).strip()
        if value:
            citation[name] = value

    names = ", ".join(f'"{name}"' for name in citation)
    placeholders = ", ".join(f":{name}" for name in citation)
    db.session.execute(
        text(f"INSERT INTO citations ({names}) VALUES ({placeholders})"),
        citation,
    )
    db.session.commit()


def remove_book_citation(citation_id):
    sql = text("DELETE FROM citations WHERE id = ?")
    db.session.execute(sql, [citation_id])
    db.session.commit()


def create_book_citation(citation_type, author, title, year, publisher):
    create_citation({
        "type": citation_type,
        "author": author,
        "title": title,
        "year": year,
        "publisher": publisher,
    })


def _select_citations(where_clause="", parameters=None):
    names_with_id = ["id", *get_column_names()]
    sql = "SELECT " + ", ".join(f'"{name}"' for name in names_with_id)
    sql += " FROM citations"
    if where_clause:
        sql += " WHERE " + where_clause
    sql += " ORDER BY id"
    return db.session.execute(text(sql), parameters or {}).fetchall()


def get_citations():
    return _select_citations()


def get_citations_by_type(citation_type):
    if citation_type not in CITATION_FIELDS:
        raise ValueError("Citation type must be book, article or inproceedings.")
    return _select_citations("type = :type", {"type": citation_type})


def get_citation(citation_id):
    names_with_id = ["id", *get_column_names()]
    sql = text(
        "SELECT " +
        ", ".join(f'"{name}"' for name in names_with_id) +
        " FROM citations WHERE id = :id"
    )
    return db.session.execute(sql, {"id": citation_id}).fetchone()


def update_citation(citation_id, data):
    existing_citation = get_citation(citation_id)
    if not existing_citation:
        raise ValueError("Citation not found.")

    citation_type = str(data.get("type", "")).strip().lower()
    if citation_type not in CITATION_FIELDS:
        raise ValueError("Citation type must be book, article or inproceedings.")

    optional_fields = OPTIONAL_FIELDS
    if citation_type == "inproceedings":
        optional_fields = (*INPROCEEDINGS_OPTIONAL_FIELDS, *OPTIONAL_FIELDS)
    fields = (*COMMON_FIELDS, *CITATION_FIELDS[citation_type], *optional_fields)
    unexpected_fields = {
        name for name, value in data.items()
        if name not in {"type", *fields} and str(value).strip()
    }
    if unexpected_fields:
        raise ValueError("The submitted fields do not match the citation type.")

    citation = {"type": citation_type}
    for name in (*COMMON_FIELDS, *CITATION_FIELDS[citation_type]):
        value = str(data.get(name, "")).strip()
        if not value:
            raise ValueError(f"{name} is required.")
        if name == "year":
            try:
                value = int(value)
            except ValueError as exc:
                raise ValueError("year must be a number.") from exc
        citation[name] = value

    for name in optional_fields:
        value = str(data.get(name, "")).strip()
        citation[name] = value or None

    set_clause = ", ".join(f'"{name}" = :{name}' for name in citation)
    sql = text(f"UPDATE citations SET {set_clause} WHERE id = :id")

    try:
        db.session.execute(sql, {**citation, "id": citation_id})
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise
