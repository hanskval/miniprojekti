from flask import Response, redirect, render_template, request, jsonify, flash, abort
from config import app, test_env
from db_helper import reset_db, init_db_if_needed
from repositories import bib, citations


with app.app_context():
    init_db_if_needed()

@app.route("/")
def index():
    return render_template(
        "index.html",
        citations=citations.get_citations(),
        columns=["title", "author", "year", "type"],
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
    citation_type = request.args.get("type") or None
    if citation_type is not None and citation_type not in citations.CITATION_FIELDS:
        abort(400)

    entries = (
        citations.get_citations_by_type(citation_type)
        if citation_type
        else citations.get_citations()
    )
    types = {entry.type for entry in entries}
    display_types = types or ({citation_type} if citation_type else {"book"})
    columns = ["title", "author", "year"]
    if citation_type is None and (
        len(types) > 1
        or any(
            entry_type not in citations.CITATION_FIELDS for entry_type in types
        )
    ):
        columns.insert(0, "type")
    if "book" in display_types or any(entry.publisher for entry in entries):
        columns.append("publisher")
    if "article" in display_types or any(entry.journal for entry in entries):
        columns.extend(("journal", "volume", "issue", "pages"))
    for optional_field in ("month", "note"):
        if any(getattr(entry, optional_field) for entry in entries):
            columns.append(optional_field)

    return render_template(
        "citation_list.html",
        citations=entries,
        columns=columns,
        citation_type=citation_type,
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
        # columns=citations.get_column_metadata(),
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
