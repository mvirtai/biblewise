# Architecture notes

**Purpose**: High-level design decisions and rationale for future reference.

---

## Data layer

- **Source**: KJV JSON from GitHub (bibleapi/bibleapi-bibles-json). Public domain, one-time download.
- **Storage**: SQLite (`bible.db`) next to project root. Two tables: `books` (66 rows), `verses` (31,103 rows).
- **Schema**: Composite PK on verses `(book_position, chapter, verse)`. Index on `text` for substring search.
- **Why SQLite**: Zero-config, portable, fast for 31k rows. No server needed. Easy to ship with app or distribute.

---

## Scope (aluerajaus) design

- **Why scope matters**: Bible has 66 books, 31k verses. For focused learning (e.g. "memorize Psalms" or "NT only"), scope is essential.
- **Scope types**: All (no filter), OT (books 1–39), NT (40–66), Single book (one position).
- **Implementation**: `scope_where_sql()` returns WHERE fragment and params. Applied to random_verse, search_by_text, and all game queries.
- **Trade-off**: Scope is passed as two params `(scope_kind, book_position)` everywhere. Could be a dataclass (see REFACTORING.md).

---

## UI layer (Rich)

- **Why Rich**: Professional terminal UI without building curses from scratch. Panels, tables, prompts, colors.
- **Separation**: `ui.py` holds all Rich code (menus, panels, tables). `games.py` uses Rich for output but owns game logic.
- **Console**: Two instances (`ui.console`, `games._console`). Could share one (see REFACTORING.md).
- **Prompts**: `Prompt.ask()` blocks for input; default values for quick navigation (e.g. Enter → choice 1).

---

## Games design

- **Shared pattern**: All games call `get_random_verse_for_game(conn, min_words, scope)` → verse dict. Then game-specific logic.
- **Hangman**: Pick one word (length > 2) from verse; mask it; user guesses letters/word. Max 6 wrong.
- **Memory pairs**: N verses (text 40–120 chars) → 2N cards (ref + text). User matches Ref# to Text#. Shuffled.
- **Reference quiz**: One verse + 4 references (1 correct, 3 random from scope). User picks 1–4.
- **Scope in games**: All games respect scope; wrong quiz options drawn from same scope (more plausible).

---

## Reference parsing

- **Pattern**: `BookName chapter:verse` (regex). Also accepts `BookName chapter verse` (space → colon).
- **Book name resolution**: `BOOK_NAME_TO_POSITION` map built from BOOKS. Includes full name (lowercase), original name, and last word (e.g. "Samuel" for "1 Samuel").
- **Fuzzy match**: If exact key not found, try `startswith` or `in` (e.g. "Joh" → "John"). Not perfect; explicit abbreviations would be better.
- **Trade-off**: Flexible but heuristic. "Jn" doesn't work (no match). Could add explicit abbrev map.

---

## Testing strategy

- **Unit tests**: Pure functions (parse_reference, scope_where_sql, book_name_by_position).
- **DB tests**: In-memory SQLite with fixture (3 books, 5 verses). Fast; no real DB needed.
- **Integration**: `import_data()` with minimal JSON → assert verse count and content.
- **Games**: Test helpers (get_random_verse_for_game) with fixture. Full game I/O not tested (blocking prompts).

---

## Dependency choices

- **requests**: In deps but not used (fetch_bible uses urllib.request). Reserved for future (e.g. API.Bible).
- **rich**: Core dependency for UI. Well-maintained, widely used.
- **click**: In deps but not used. Reserved for CLI subcommands (e.g. `biblewise search "John 3:16"`).
- **pytest**: Dev dependency (optional). Standard testing tool.

---

## Why terminal app (not web)?

- **Simplicity**: No server, no auth, no deployment. Just Python + SQLite.
- **Focus**: Terminal forces focus (no browser tabs, no distractions).
- **Portability**: Runs anywhere Python runs (Linux, macOS, Windows, SSH).
- **Learning**: Good for developer portfolio (shows CLI skills, DB, testing, packaging).

**Future**: Could add web version (Flask/FastAPI + HTMX) with same backend logic.

---

## Why KJV?

- **Public domain**: No licensing issues; can distribute freely.
- **Availability**: bibleapi/bibleapi-bibles-json has KJV as JSON (easy to parse).
- **Familiarity**: Widely known; good for reference training.

**Future**: Add other translations (ASV, WEB, etc. from same repo).

---

## File structure rationale

```
biblewise/
├── books.py       # Data: 66 books (position, id, name)
├── db.py          # DB path, schema, connection
├── fetch_bible.py # One-time: download + import
├── scope.py       # Scope logic (WHERE fragment, label)
├── search.py      # Reference parsing, verse lookup, text search, random
├── games.py       # Three games (hangman, memory, quiz)
├── ui.py          # Rich UI (menus, panels, tables, prompts)
└── main.py        # Entry point (menu loop, scope state, dispatch)
```

**Rationale**: Each module has a clear role; low coupling (scope, search, games don't depend on ui; ui imports from scope/search). Easy to test (db/search/scope are pure logic).

---

*Refer to this when making architectural decisions or explaining design to others.*
