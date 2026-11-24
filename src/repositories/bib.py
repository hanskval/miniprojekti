from repositories import citations
from flask import Response
from config import app

def safe_bib(text):
    unsafe_chars = {
        '\\': r'\\textbackslash{}',
        '{': r'\\{',
        '}': r'\\}',
        '$': r'\\$',
        '&': r'\\&',
        '%': r'\\%',
        '#': r'\\#',
        '_': r'\\_',
        '^': r'\\textasciicircum{}',
        '~': r'\\textasciitilde{}',
    }
    for unsafe, safe in unsafe_chars.items():
        text = text.replace(unsafe, safe)
    return text

def bibfile(entries):
    output = []
    for citation in entries:
        values = citation._mapping if hasattr(citation, "_mapping") else citation
        citation_type = values["type"] if "type" in values else "misc"
        fields = []
        for name in values.keys():
            if name in ("id", "type"):
                continue
            value = values[name]
            if value is not None and str(value).strip():
                bib_name = "number" if name == "issue" else name
                fields.append(
                    f"  {bib_name} = {{{safe_bib(str(value))}}}"
                )
        body = ",\n".join(fields)
        output.append(
            f"@{citation_type}{{citation{values['id']},\n"
            f"{body}\n"
            f"}}"
        )
    return output
    