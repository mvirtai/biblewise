"""Tests for biblewise.books."""

import pytest

from biblewise.books import BOOKS, book_name_by_position


def test_books_has_66_entries():
    assert len(BOOKS) == 66


def test_books_first_and_last():
    assert BOOKS[0] == (1, "GEN", "Genesis")
    assert BOOKS[-1] == (66, "REV", "Revelation")


def test_book_name_by_position():
    assert book_name_by_position(1) == "Genesis"
    assert book_name_by_position(43) == "John"
    assert book_name_by_position(66) == "Revelation"


def test_book_name_by_position_invalid():
    assert book_name_by_position(0) is None
    assert book_name_by_position(67) is None
