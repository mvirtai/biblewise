"""Verse scope (filter): All, OT, NT, or a single book.

Used by search, random verse, and all games to limit which verses are considered.
"""

from typing import Literal

from biblewise.books import BOOKS, book_name_by_position

# KJV book positions: 1–39 Old Testament, 40–66 New Testament.
OT_LAST = 39
NT_FIRST = 40

ScopeKind = Literal["all", "ot", "nt", "book"]


def scope_where_sql(scope_kind: ScopeKind, book_position: int | None) -> tuple[str, list]:
    """Return (suffix WHERE clause, params) for filtering verses by scope.

    The clause includes a leading space and AND so it can be appended to existing WHERE.
    Example: for "ot" returns (" AND v.book_position BETWEEN 1 AND ?", [39]).
    """
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
    """Human-readable label for the current scope (e.g. 'Old Testament', 'Genesis')."""
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
    """List of (position, display name) for the scope picker (all 66 books)."""
    return [(pos, name) for pos, _id, name in BOOKS]
