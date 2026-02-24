"""Pytest fixtures: in-memory DB with minimal books and verses."""

import sqlite3

import pytest

from biblewise.books import BOOKS
from biblewise.db import init_schema


@pytest.fixture
def conn():
    """In-memory SQLite with schema and sample data (first 3 books, a few verses)."""
    c = sqlite3.connect(":memory:")
    init_schema(c)
    for pos, id_, name in BOOKS[:3]:
        c.execute(
            "INSERT INTO books (position, id, name) VALUES (?, ?, ?)",
            (pos, id_, name),
        )
    verses = [
        (1, 1, 1, "In the beginning God created the heaven and the earth."),
        (1, 1, 2, "And the earth was without form, and void."),
        (1, 3, 16, "For God so loved the world, that he gave his only begotten Son."),
        (2, 1, 1, "Now these are the names of the children of Israel."),
        (3, 1, 1, "And the LORD called unto Moses."),
    ]
    for bp, ch, vs, text in verses:
        c.execute(
            "INSERT INTO verses (book_position, chapter, verse, text) VALUES (?, ?, ?, ?)",
            (bp, ch, vs, text),
        )
    c.commit()
    yield c
    c.close()
