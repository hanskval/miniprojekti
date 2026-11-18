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
    return [
        f"@{citation.type}{{citation{citation.id},\n"
        f"  author = {{{safe_bib(citation.author)}}},\n"
        f"  title = {{{safe_bib(citation.title)}}},\n"
        f"  year = {{{citation.year}}},\n"
        f"  publisher = {{{safe_bib(citation.publisher)}}}\n"
        f"}}"
        for citation in entries
    ]
    