"""Search verses by reference or text; get random verse.

Reference parsing supports formats like 'John 3:16', '1 John 2:3', 'John 3 16'.
Text search is LIKE-based (substring). All functions accept scope (OT/NT/book).
"""

import re
import sqlite3

from biblewise.books import BOOKS, book_name_by_position
from biblewise.scope import ScopeKind, scope_where_sql

# Optional digits, then book name (letters), then chapter and verse (with optional colon).
REF_PATTERN = re.compile(
    r"^\s*(\d?\s*[A-Za-z]+)\s+(\d+)\s*:\s*(\d+)\s*$",
    re.IGNORECASE,
)

# Map various book name forms (full, short, lowercase) to 1-based position.
BOOK_NAME_TO_POSITION = {}
for pos, _id, name in BOOKS:
    BOOK_NAME_TO_POSITION[name.lower()] = pos
    if name not in BOOK_NAME_TO_POSITION:
        BOOK_NAME_TO_POSITION[name] = pos
    short = name.split()[-1] if " " in name else name
    if short.lower() not in BOOK_NAME_TO_POSITION:
        BOOK_NAME_TO_POSITION[short.lower()] = pos


def parse_reference(ref: str) -> tuple[int, int, int] | None:
    """Parse 'John 3:16' or '1 John 2:3' or 'John 3 16' into (book_position, chapter, verse).

    Tries exact match first, then prefix/suffix match on book name. Returns None if invalid.
    """
    ref = ref.strip()
    ref = re.sub(r"\s+(\d+)\s+(\d+)\s*$", r" \1:\2", ref)
    m = REF_PATTERN.match(ref)
    if not m:
        return None
    book_part, chapter_str, verse_str = m.group(1), m.group(2), m.group(3)
    book_key = book_part.strip().lower().replace(" ", " ")
    if " " in book_part:
        book_key = book_part.strip().lower()
    pos = BOOK_NAME_TO_POSITION.get(book_key)
    if pos is None:
        for name_lower, p in BOOK_NAME_TO_POSITION.items():
            if name_lower.startswith(book_key) or book_key.startswith(name_lower):
                pos = p
                break
    if pos is None:
        return None
    return (pos, int(chapter_str), int(verse_str))


def get_verse(conn: sqlite3.Connection, book_position: int, chapter: int, verse: int) -> dict | None:
    """Fetch a single verse by book position, chapter, and verse number.

    Returns a dict with book_position, chapter, verse, text, book_name, reference; or None.
    """
    row = conn.execute(
        """
        SELECT v.book_position, v.chapter, v.verse, v.text, b.name
        FROM verses v
        JOIN books b ON b.position = v.book_position
        WHERE v.book_position = ? AND v.chapter = ? AND v.verse = ?
        """,
        (book_position, chapter, verse),
    ).fetchone()
    if not row:
        return None
    return {
        "book_position": row[0],
        "chapter": row[1],
        "verse": row[2],
        "text": row[3],
        "book_name": row[4],
        "reference": f"{row[4]} {row[1]}:{row[2]}",
    }


def search_by_reference(conn: sqlite3.Connection, ref: str) -> dict | None:
    """Parse ref and return the matching verse dict, or None if not found or invalid."""
    parsed = parse_reference(ref)
    if not parsed:
        return None
    return get_verse(conn, *parsed)


def search_by_text(
    conn: sqlite3.Connection,
    query: str,
    limit: int = 20,
    scope_kind: ScopeKind = "all",
    book_position: int | None = None,
) -> list[dict]:
    """Search verse text with case-insensitive LIKE %query%. Respects scope. Returns list of verse dicts."""
    q = f"%{query.strip()}%"
    where_extra, where_params = scope_where_sql(scope_kind, book_position)
    rows = conn.execute(
        f"""
        SELECT v.book_position, v.chapter, v.verse, v.text, b.name
        FROM verses v
        JOIN books b ON b.position = v.book_position
        WHERE v.text LIKE ? COLLATE NOCASE{where_extra}
        ORDER BY v.book_position, v.chapter, v.verse
        LIMIT ?
        """,
        (q, *where_params, limit),
    ).fetchall()
    return [
        {
            "book_position": r[0],
            "chapter": r[1],
            "verse": r[2],
            "text": r[3],
            "book_name": r[4],
            "reference": f"{r[4]} {r[1]}:{r[2]}",
        }
        for r in rows
    ]


def random_verse(
    conn: sqlite3.Connection,
    scope_kind: ScopeKind = "all",
    book_position: int | None = None,
) -> dict | None:
    """Return a random verse within the given scope, or None if no verses match."""
    where_extra, where_params = scope_where_sql(scope_kind, book_position)
    row = conn.execute(
        f"""
        SELECT v.book_position, v.chapter, v.verse, v.text, b.name
        FROM verses v
        JOIN books b ON b.position = v.book_position
        WHERE 1=1{where_extra}
        ORDER BY RANDOM()
        LIMIT 1
        """,
        where_params,
    ).fetchone()
    if not row:
        return None
    return {
        "book_position": row[0],
        "chapter": row[1],
        "verse": row[2],
        "text": row[3],
        "book_name": row[4],
        "reference": f"{row[4]} {row[1]}:{row[2]}",
    }
