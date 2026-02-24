"""Download KJV from bibleapi/bibleapi-bibles-json and import into SQLite."""

import json
import sqlite3
import urllib.request
from pathlib import Path

from biblewise.books import BOOKS
from biblewise.db import get_db_path, init_schema

KJV_JSON_URL = "https://raw.githubusercontent.com/bibleapi/bibleapi-bibles-json/master/kjv.json"


def download_json() -> dict:
    with urllib.request.urlopen(KJV_JSON_URL) as resp:
        return json.load(resp)


def import_data(conn: sqlite3.Connection, data: dict) -> int:
    """Insert books and verses from bibleapi JSON into an already-schema-ready conn. Returns verse count."""
    conn.execute("DELETE FROM verses")
    conn.execute("DELETE FROM books")
    for pos, id_, name in BOOKS:
        conn.execute(
            "INSERT INTO books (position, id, name) VALUES (?, ?, ?)",
            (pos, id_, name),
        )
    rows = data["resultset"]["row"]
    for row in rows:
        field = row["field"]
        book_position = field[1]
        chapter = field[2]
        verse = field[3]
        text = field[4].strip() if isinstance(field[4], str) else str(field[4])
        conn.execute(
            "INSERT INTO verses (book_position, chapter, verse, text) VALUES (?, ?, ?, ?)",
            (book_position, chapter, verse, text),
        )
    conn.commit()
    return conn.execute("SELECT COUNT(*) FROM verses").fetchone()[0]


def run() -> None:
    db_path = get_db_path()
    db_path.parent.mkdir(parents=True, exist_ok=True)

    print("Downloading KJV from bibleapi/bibleapi-bibles-json...")
    data = download_json()

    conn = sqlite3.connect(db_path)
    init_schema(conn)
    count = import_data(conn, data)
    conn.close()
    print(f"Done. {count} verses in {db_path}")


if __name__ == "__main__":
    run()
