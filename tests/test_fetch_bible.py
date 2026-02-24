"""Tests for biblewise.fetch_bible."""

import sqlite3

import pytest

from biblewise.db import init_schema
from biblewise.fetch_bible import import_data

MINI_JSON = {
    "resultset": {
        "row": [
            {"field": [1001001, 1, 1, 1, "In the beginning God created the heaven and the earth."]},
            {"field": [1001002, 1, 1, 2, "And the earth was without form."]},
            {"field": [1002001, 1, 2, 1, "Thus the heavens and the earth were finished."]},
        ]
    }
}


def test_import_data_creates_verses():
    conn = sqlite3.connect(":memory:")
    init_schema(conn)
    count = import_data(conn, MINI_JSON)
    conn.close()
    assert count == 3


def test_import_data_content():
    conn = sqlite3.connect(":memory:")
    init_schema(conn)
    import_data(conn, MINI_JSON)
    row = conn.execute(
        "SELECT book_position, chapter, verse, text FROM verses WHERE book_position = 1 AND chapter = 1 AND verse = 1"
    ).fetchone()
    conn.close()
    assert row is not None
    assert row[0] == 1 and row[1] == 1 and row[2] == 1
    assert "beginning" in row[3]


def test_import_data_idempotent():
    conn = sqlite3.connect(":memory:")
    init_schema(conn)
    import_data(conn, MINI_JSON)
    count1 = conn.execute("SELECT COUNT(*) FROM verses").fetchone()[0]
    import_data(conn, MINI_JSON)
    count2 = conn.execute("SELECT COUNT(*) FROM verses").fetchone()[0]
    conn.close()
    assert count1 == count2 == 3
