"""Verse scope (filter): All, OT, NT, or a single book."""

from typing import Literal

from biblewise.books import BOOKS, book_name_by_position

OT_LAST = 39
NT_FIRST = 40

ScopeKind = Literal["all", "ot", "nt", "book"]


def scope_where_sql(scope_kind: ScopeKind, book_position: int | None) -> tuple[str, list]:
    """Return (suffix WHERE clause, params) for verses. Clause includes leading space and AND if needed."""
    if scope_kind == "all":
        return "", []
    if scope_kind == "ot":
        return " AND v.book_position BETWEEN 1 AND ?", [OT_LAST]
    if scope_kind == "nt":
        return " AND v.book_position BETWEEN ? AND 66", [NT_FIRST]
    if scope_kind == "book" and book_position is not None:
        return " AND v.book_position = ?", [book_position]
    return "", []


def scope_label(scope_kind: ScopeKind, book_position: int | None) -> str:
    if scope_kind == "all":
        return "All (whole Bible)"
    if scope_kind == "ot":
        return "Old Testament"
    if scope_kind == "nt":
        return "New Testament"
    if scope_kind == "book" and book_position is not None:
        name = book_name_by_position(book_position)
        return name or f"Book {book_position}"
    return "All"


def book_list_for_picker() -> list[tuple[int, str]]:
    """(position, display name) for scope picker."""
    return [(pos, name) for pos, _id, name in BOOKS]
