"""SQLite database path, schema, and connection helpers."""

import sqlite3
from pathlib import Path


def get_db_path() -> Path:
    """Path to bible.db next to the project root (where pyproject.toml lives)."""
    root = Path(__file__).resolve().parent.parent
    return root / "bible.db"


def get_connection() -> sqlite3.Connection:
    path = get_db_path()
    if not path.exists():
        raise FileNotFoundError(
            f"Database not found at {path}. Run: uv run python -m biblewise.fetch_bible"
        )
    return sqlite3.connect(path, check_same_thread=False)


def init_schema(conn: sqlite3.Connection) -> None:
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS books (
            position INTEGER PRIMARY KEY,
            id TEXT NOT NULL,
            name TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS verses (
            book_position INTEGER NOT NULL,
            chapter INTEGER NOT NULL,
            verse INTEGER NOT NULL,
            text TEXT NOT NULL,
            PRIMARY KEY (book_position, chapter, verse),
            FOREIGN KEY (book_position) REFERENCES books(position)
        );
        CREATE INDEX IF NOT EXISTS idx_verses_text ON verses(text);
    """)
    conn.commit()


def verse_count(conn: sqlite3.Connection) -> int:
    cur = conn.execute("SELECT COUNT(*) FROM verses")
    return cur.fetchone()[0]
