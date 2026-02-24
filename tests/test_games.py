"""Tests for biblewise.games."""

import pytest

from biblewise.games import get_random_verse_for_game


def test_get_random_verse_for_game_returns_verse(conn):
    v = get_random_verse_for_game(conn, min_words=1)
    assert v is not None
    assert "reference" in v
    assert "text" in v


def test_get_random_verse_for_game_prefers_long_verses(conn):
    for _ in range(20):
        v = get_random_verse_for_game(conn, min_words=5)
        assert v is not None
        word_count = len(v["text"].split())
        if word_count >= 5:
            assert word_count >= 5
            return
    v = get_random_verse_for_game(conn, min_words=5)
    assert v is not None


def test_get_random_verse_for_game_fallback_when_no_long_verses(conn):
    v = get_random_verse_for_game(conn, min_words=100)
    assert v is not None
