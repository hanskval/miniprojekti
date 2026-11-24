CREATE TABLE citations (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  type TEXT NOT NULL,
  title TEXT NOT NULL,
  author TEXT NOT NULL,
  year INTEGER NOT NULL,
  publisher TEXT,
  journal TEXT,
  volume TEXT,
  issue TEXT,
  pages TEXT,
  month TEXT,
  note TEXT
);
