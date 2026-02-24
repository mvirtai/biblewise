"""Tests for biblewise.db."""

import sqlite3

import pytest

from biblewise.db import get_db_path, init_schema, verse_count


def test_get_db_path_is_bible_db():
    path = get_db_path()
    assert path.name == "bible.db"
    assert path.is_absolute() or path.resolve().name == "bible.db"


def test_init_schema_creates_tables():
    conn = sqlite3.connect(":memory:")
    init_schema(conn)
    cur = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
    )
    tables = [r[0] for r in cur.fetchall()]
    assert "books" in tables
    assert "verses" in tables
    conn.close()


def test_verse_count_empty():
    conn = sqlite3.connect(":memory:")
    init_schema(conn)
    assert verse_count(conn) == 0
    conn.close()


def test_verse_count_after_insert(conn):
    assert verse_count(conn) == 5
