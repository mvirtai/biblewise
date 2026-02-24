"""Tests for biblewise.search."""

import pytest

from biblewise.search import (
    get_verse,
    parse_reference,
    random_verse,
    search_by_reference,
    search_by_text,
)


class TestParseReference:
    def test_john_3_16(self):
        assert parse_reference("John 3:16") == (43, 3, 16)

    def test_genesis_1_1(self):
        assert parse_reference("Genesis 1:1") == (1, 1, 1)

    def test_one_john(self):
        assert parse_reference("1 John 2:3") == (62, 2, 3)

    def test_lowercase(self):
        assert parse_reference("john 3:16") == (43, 3, 16)

    def test_whitespace(self):
        assert parse_reference("  Romans  8  :  28  ") == (45, 8, 28)

    def test_space_instead_of_colon(self):
        assert parse_reference("John 3 16") == (43, 3, 16)

    def test_invalid_garbage(self):
        assert parse_reference("not a ref") is None
        assert parse_reference("") is None


class TestGetVerse:
    def test_existing_verse(self, conn):
        v = get_verse(conn, 1, 1, 1)
        assert v is not None
        assert v["book_name"] == "Genesis"
        assert v["reference"] == "Genesis 1:1"
        assert "beginning" in v["text"]

    def test_missing_verse(self, conn):
        assert get_verse(conn, 1, 99, 99) is None


class TestSearchByReference:
    def test_found(self, conn):
        v = search_by_reference(conn, "Genesis 1:1")
        assert v is not None
        assert v["reference"] == "Genesis 1:1"

    def test_not_found_invalid_ref(self, conn):
        assert search_by_reference(conn, "NoBook 1:1") is None

    def test_not_found_valid_ref_missing_verse(self, conn):
        v = search_by_reference(conn, "Genesis 2:99")
        assert v is None


class TestSearchByText:
    def test_finds_substring(self, conn):
        results = search_by_text(conn, "begotten", limit=5)
        assert len(results) >= 1
        refs = [r["reference"] for r in results]
        assert "Genesis 3:16" in refs

    def test_limit(self, conn):
        results = search_by_text(conn, "the", limit=2)
        assert len(results) <= 2

    def test_no_match(self, conn):
        results = search_by_text(conn, "xyznonexistent123", limit=5)
        assert results == []

    def test_case_insensitive(self, conn):
        results = search_by_text(conn, "BEGINNING", limit=5)
        assert len(results) >= 1
        assert any("beginning" in r["text"].lower() for r in results)


class TestRandomVerse:
    def test_returns_verse(self, conn):
        v = random_verse(conn)
        assert v is not None
        assert "reference" in v
        assert "text" in v
        assert "book_name" in v

    def test_all_from_fixture_eventually(self, conn):
        seen = set()
        for _ in range(30):
            v = random_verse(conn)
            seen.add((v["book_position"], v["chapter"], v["verse"]))
        assert len(seen) >= 2
