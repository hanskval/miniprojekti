from flask import redirect, render_template, request, jsonify, flash
from db_helper import reset_db
from repositories.todo_repository import get_todos, create_todo, set_done
from config import app, test_env
from util import validate_todo
from db_helper import reset_db, init_db_if_needed

from repositories import citations

with app.app_context():
    init_db_if_needed()

@app.route("/")
def index():
    return render_template("index.html", citations=citations.get_citations())

@app.route("/new_citation")
def new():
    return render_template("new_citation.html")

@app.route("/create_book_citation", methods=["POST"])
def book_citation_creation():
    fields = ("type", "author", "title", "year", "publisher")
    citation = {field: request.form.get(field, "").strip() for field in fields}

    if not all(citation.values()):
        flash("All fields are required.")
        return redirect("/new_citation")

    if citation["type"] != "book":
        flash("Unsupported citation type.")
        return redirect("/new_citation")

    try:
        year = int(citation["year"])
    except ValueError:
        flash("Year must be a number.")
        return redirect("/new_citation")

    citations.create_book_citation(
        citation["type"],
        citation["author"],
        citation["title"],
        year,
        citation["publisher"],
    )
    return redirect("/") # tää myöhemmi nii et siirtää siihe kirjaan tai listaan yms citationiin eikä etusivulle



# testausta varten oleva reitti
if test_env:
    @app.route("/reset_db")
    def reset_database():
        reset_db()
        return jsonify({ 'message': "db reset" })