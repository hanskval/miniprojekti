from flask import Response, redirect, render_template, request, jsonify, flash
from repositories import bib
from repositories.todo_repository import get_todos, create_todo, set_done
from config import app, test_env
from util import validate_todo
from db_helper import reset_db, init_db_if_needed

from repositories import citations

with app.app_context():
    init_db_if_needed()

@app.route("/")
def index():
    return render_template(
        "index.html",
        citations=citations.get_citations(),
        columns=[name for name in citations.get_column_names() if name not in ("id", "type")],
    )

@app.route("/make_bibtex")
def make_bibtex():
    entries = bib.bibfile(citations.get_citations())

    return Response(
            "\n\n".join(entries) + ("\n" if entries else ""),
            mimetype="application/x-bibtex",
            headers={"Content-Disposition": 'attachment; filename="citations.bib"'},
        )

@app.route("/citation_list")
def citation_list():
    return render_template(
        "citation_list.html",
        citations=citations.get_citations(),
        columns=[name for name in citations.get_column_names() if name not in ("id", "type")],
    )

@app.route("/make_bib/<int:citation_id>")
def make_bib(citation_id):
    citation = citations.get_citation(citation_id)
    if not citation:
        return "Citation not found", 404

    entries = bib.bibfile([citation])
    return Response(
            "\n\n".join(entries) + ("\n" if entries else ""),
            mimetype="application/x-bibtex",
            headers={"Content-Disposition": 'attachment; filename="citations.bib"'},
        )
    ## if not citation:
    ##    return "Citation not found", 404
    ## return render_template("citation.html", citation=citation)

@app.route("/new_citation")
def new():
    return render_template(
        "new_citation.html",
        columns=citations.get_column_metadata(),
    )

@app.route("/create_citation", methods=["POST"])
def create_citation():
    citation = request.form.to_dict(flat=True)
    try:
        citations.create_citation(citation)
    except ValueError as exc:
        flash(str(exc))
        return redirect("/new_citation")
    return redirect("/citation_list")

@app.route("/reset_db")
def reset_db_route():
    reset_db()
    return jsonify({ 'message': "db reset" })



# testausta varten oleva reitti
if test_env:
    @app.route("/reset_db")
    def reset_database():
        reset_db()
        return jsonify({ 'message': "db reset" })