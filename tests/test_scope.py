"""Tests for biblewise.scope."""

import pytest

from biblewise.scope import scope_label, scope_where_sql


def test_scope_where_sql_all():
    clause, params = scope_where_sql("all", None)
    assert clause == ""
    assert params == []


def test_scope_where_sql_ot():
    clause, params = scope_where_sql("ot", None)
    assert "BETWEEN" in clause and "1" in clause
    assert params == [39]


def test_scope_where_sql_nt():
    clause, params = scope_where_sql("nt", None)
    assert "BETWEEN" in clause and "66" in clause
    assert params == [40]


def test_scope_where_sql_book():
    clause, params = scope_where_sql("book", 43)
    assert "=" in clause
    assert params == [43]


def test_scope_label():
    assert scope_label("all", None) == "All (whole Bible)"
    assert scope_label("ot", None) == "Old Testament"
    assert scope_label("nt", None) == "New Testament"
    assert scope_label("book", 43) == "John"
