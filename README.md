# Biblewise

Terminal-based Bible memorization and reference training with a **Rich UI** (panels, tables, colors). Helps users learn verse content and book/chapter/verse references using the King James Version (KJV) stored locally in SQLite. Includes **scope filtering** (All / OT / NT / Single book) and three interactive games.

---

## How it works (application logic)

### Overview

1. **One-time data setup**: A script downloads the full KJV as JSON from [bibleapi/bibleapi-bibles-json](https://github.com/bibleapi/bibleapi-bibles-json), then imports it into a local SQLite database (`bible.db`).
2. **Interactive menu**: The main app opens a single long-lived database connection and shows a looped menu. Every action (search, random verse, games) uses this same connection.
3. **No backend or account**: Everything runs locally. No API keys, no server; the only network use is the initial JSON download.

### Data flow

```
GitHub (kjv.json)  →  fetch_bible  →  bible.db (SQLite)
                                              ↓
User  →  biblewise (menu)  →  db + search/games  →  terminal I/O
```

- **fetch_bible**: Reads `resultset.row[].field` from the JSON. Each `field` is `[verse_id, book_position, chapter, verse, text]`. Book position is 1–66 (canonical order: Genesis=1, Revelation=66). The script creates/overwrites tables `books` and `verses`, then inserts all rows.
- **biblewise**: Expects `bible.db` to exist. If not, it prints an error and tells the user to run `fetch_bible` first.

### Database schema

- **books**: `(position INTEGER PK, id TEXT, name TEXT)` — position 1–66, id e.g. "GEN", name e.g. "Genesis". Used to resolve book names when displaying references.
- **verses**: `(book_position, chapter, verse, text)` with composite primary key. One row per verse. `book_position` matches `books.position`. An index on `text` supports substring search.

All references in the app are displayed as `{book_name} {chapter}:{verse}` (e.g. "John 3:16"), built from a join of `verses` and `books`.

### Search logic

- **Input**: One string from the user — either a reference like "John 3:16" or "1 John 2:3", or a free-text search.
- **Reference path**: `parse_reference()` matches the pattern `BookName chapter:verse`. Book name is resolved via a fixed map (in `search.py`) from full and shortened names (e.g. "Genesis", "genesis", "John", "1 John") to `book_position` 1–66. If parsing succeeds, `get_verse(conn, book_position, chapter, verse)` fetches that single verse.
- **Text path**: If reference parsing fails, the same string is treated as search text. `search_by_text()` runs `LIKE %query%` on `verses.text`, joined with `books`, and returns up to 20 hits in book/chapter/verse order.

So: “looks like a reference” → single-verse lookup; otherwise → full-text search.

### Scope (aluerajaus)

- **Set scope** in the menu: All (whole Bible), Old Testament (books 1–39), New Testament (40–66), or a single book. The current scope is shown in the menu and applied to **random verse**, **text search**, and **all games**. Useful for focused practice (e.g. only Psalms or only NT).

### Random verse

- One SQL query with optional scope filter: `ORDER BY RANDOM() LIMIT 1` on the join of `verses` and `books`. Returns the same dict shape as search (reference + text) for display.

### Games (submenu)

- **Menu → 3. Games** opens a submenu: Hangman, Memory pairs, Reference quiz. All games respect the current scope and use Rich panels/tables.
- **Hangman**: A random verse is chosen (preferring verses with enough words). One word from that verse (length > 2) is picked as the target. The user sees only the reference and a masked word (e.g. `_o_e_`). They guess letters or the full word; up to 6 wrong guesses. Revealing the word ends the round and shows the full verse.
- **Memory pairs**: N random verses (default 4) are chosen with text length 40–120 chars. For each verse we form two “cards”: reference and truncated text (60 chars + "…"). Cards are shuffled and shown as Ref 1…Ref N and Text 1…Text N. The user enters pairs "Ref# Text#". We check whether the chosen reference’s verse text (truncated the same way) matches the chosen text card; matches are counted until all N pairs are correct.
- **Reference quiz**: One random verse is shown (text truncated to 200 chars). Four references are built: the correct one plus three other random verses’ references (no duplicates). Options are shuffled. The user picks 1–4; we compare the choice to the correct index and report right/wrong.

No state is persisted between sessions (no scores, no progress). Each run is independent.

### Module roles

| Module | Role |
|--------|------|
| `biblewise/books.py` | Canonical list of 66 books: (position, id, name). Used by fetch for inserts and by search for reference parsing. |
| `biblewise/db.py` | DB path (next to project root), schema creation, and `get_connection()` that requires `bible.db` to exist. |
| `biblewise/fetch_bible.py` | Download KJV JSON from GitHub, create/clear books and verses, bulk insert. Entry: `python -m biblewise.fetch_bible`. |
| `biblewise/search.py` | Reference parsing (string → book_position, chapter, verse), single-verse fetch, text search (LIKE), random verse. |
| `biblewise/scope.py` | Scope (All/OT/NT/book); returns WHERE fragment and params for verses. |
| `biblewise/ui.py` | Rich UI: welcome, main menu, games submenu, scope menu, verse panels, search table, prompts. |
| `biblewise/games.py` | Hangman, memory pairs, reference quiz; all take scope and use Rich for output. |
| `biblewise/main.py` | Entry point: welcome, loop menu, pass scope to search/games, handle quit. |

---

## Setup

Using **uv** (recommended):

```bash
# Install uv if needed: https://docs.astral.sh/uv/
uv sync
uv run python -m biblewise.fetch_bible   # one-time: download Bible into bible.db
uv run biblewise
```

Or with plain pip:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
python -m biblewise.fetch_bible
python -m biblewise
```

### Docker

Build and run in a container:

```bash
docker build -t biblewise .
docker run -it biblewise
```

Or with docker-compose:

```bash
docker-compose up --build
```

The Dockerfile runs `fetch_bible` during build, so the container includes the full Bible database.

### Task (optional)

If you use [Task](https://taskfile.dev), run `task` to see commands:

```bash
task install    # deps + fetch (first-time)
task run        # run app
task test       # pytest
task docker     # docker-compose up --build
```

### Tests

Install dev dependencies and run tests:

```bash
uv sync --extra dev
uv run pytest
```

Tests use an in-memory SQLite fixture (see `tests/conftest.py`) and cover reference parsing, search, DB schema, fetch import logic, and game helpers. No real `bible.db` is required to run tests.

---

## Features (user-facing)

- **Rich terminal UI** — Panels, tables, and clear prompts (no raw `input()`).
- **Scope (aluerajaus)** — Limit to All, Old Testament, New Testament, or a single book. Applied to search, random verse, and all games.
- **Search verse** — Look up by reference (e.g. John 3:16 or "John 3 16") or by text (substring search). Text search respects scope.
- **Random verse** — One random verse (within current scope).
- **Games** (submenu) — **Hangman** (guess the word from a verse), **Memory pairs** (match reference ↔ snippet), **Reference quiz** (verse → choose reference). All respect scope.

---

## Data and license

- **Source**: KJV from [bibleapi/bibleapi-bibles-json](https://github.com/bibleapi/bibleapi-bibles-json) (public domain).
- **Local store**: `bible.db` (SQLite) in the project root after running `fetch_bible`.
- **License**: Project code/structure: MIT (see LICENSE). Bible text: public domain (KJV).

---

## Developer notes

See `.plans/` folder for internal documentation:
- **INDEX.md** — Overview of all .plans/ files
- **STATUS.md** — Current state, next steps, readiness checklist
- **IMPROVEMENTS.md** — 23 UX/feature/testing ideas from review
- **REFACTORING.md** — 10 code quality improvements (Scope dataclass, shared console, etc.)
- **ARCHITECTURE.md** — Design decisions and rationale
