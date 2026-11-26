import unittest
from repositories.bib import bibfile, safe_bib

class TestBib(unittest.TestCase):
    def test_plain_text_is_unchanged(self):
        self.assertEqual(safe_bib("Clean Code"), "Clean Code")

    def test_bibfile_makes_book_entry(self):
        entry = {"id": 1, "type": "book", "title": "Clean Code",
                 "author": "Martin", "year": 2008, "publisher": "PH"}
        expected = ("@book{citation1,\n"
                    "  title = {Clean Code},\n"
                    "  author = {Martin},\n"
                    "  year = {2008},\n"
                    "  publisher = {PH}\n"
                    "}")
        self.assertEqual(bibfile([entry])[0], expected)

    def test_empty_fields_are_skipped(self):
        entry = {"id": 2, "type": "book", "title": "X", "author": "Y",
                 "year": 2000, "publisher": "Z", "note": ""}
        self.assertNotIn("note", bibfile([entry])[0])

    def test_id_and_type_are_not_fields(self):
        entry = {"id": 3, "type": "book", "title": "X", "author": "Y",
                 "year": 2000, "publisher": "Z"}
        result = bibfile([entry])[0]
        self.assertNotIn("id =", result)
        self.assertNotIn("type =", result)

    def test_special_characters_are_escaped(self):
        self.assertEqual(safe_bib("A & B"), r"A \& B")
        self.assertEqual(safe_bib("50%"), r"50\%")
        self.assertEqual(safe_bib("my_file"), r"my\_file")

    def test_backslash_is_escaped_once(self):
        self.assertEqual(safe_bib("a\\b"), r"a\textbackslash{}b")
