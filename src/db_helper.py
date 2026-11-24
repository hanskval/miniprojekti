import os

from sqlalchemy import text

from config import db, app

def init_db_if_needed():
    if "citations" not in tables():
        setup_db()
    elif not {
        "journal", "volume", "issue", "pages", "month", "note"
    }.issubset(citation_columns()):
        migrate_citations()


def citation_columns():
    rows = db.session.execute(text("PRAGMA table_info(citations)")).fetchall()
    return {row[1] for row in rows}


def migrate_citations():
    old_columns = citation_columns()
    selected_columns = ["id", "type", "title", "author", "year"]
    for name in ("publisher", "journal", "volume"):
        selected_columns.append(
            f'"{name}"' if name in old_columns else f"NULL AS {name}"
        )
    if "issue" in old_columns:
        selected_columns.append('"issue"')
    elif "number" in old_columns:
        selected_columns.append('"number" AS issue')
    else:
        selected_columns.append("NULL AS issue")
    for name in ("pages", "month", "note"):
        selected_columns.append(
            f'"{name}"' if name in old_columns else f"NULL AS {name}"
        )

    schema_path = os.path.join(os.path.dirname(__file__), "schema.sql")
    with open(schema_path, "r", encoding="utf-8") as schema_file:
        schema_sql = schema_file.read().strip()
    new_schema = schema_sql.replace(
        "CREATE TABLE citations", "CREATE TABLE citations_new", 1
    )

    db.session.execute(text(new_schema))
    db.session.execute(
        text(
            "INSERT INTO citations_new "
            "(id, type, title, author, year, publisher, journal, volume, issue, "
            "pages, month, note) "
            "SELECT " + ", ".join(selected_columns) + " FROM citations"
        )
    )
    db.session.execute(text("DROP TABLE citations"))
    db.session.execute(text("ALTER TABLE citations_new RENAME TO citations"))
    db.session.commit()

def reset_db():
  print(f"Clearing contents from table citations")
  sql = text(f"DELETE FROM citations")
  db.session.execute(sql)
  db.session.commit()

def tables():
  """Returns all table names from the database"""
  sql = text(
    "SELECT name FROM sqlite_master "
    "WHERE type = 'table' AND name NOT LIKE 'sqlite_%'"
  )

  result = db.session.execute(sql)
  return [row[0] for row in result.fetchall()]

def setup_db():
  """
    Creating the database
    If database tables already exist, those are dropped before the creation
  """
  tables_in_db = tables()
  if len(tables_in_db) > 0:
    print(f"Tables exist, dropping: {', '.join(tables_in_db)}")
    for table in tables_in_db:
      sql = text(f"DROP TABLE {table}")
      db.session.execute(sql)
    db.session.commit()

  print("Creating database")
  
  # Read schema from schema.sql file
  schema_path = os.path.join(os.path.dirname(__file__), 'schema.sql')
  with open(schema_path, 'r') as f:
    schema_sql = f.read().strip()
  
  sql = text(schema_sql)
  db.session.execute(sql)
  db.session.commit()

if __name__ == "__main__":
    with app.app_context():
      setup_db()
