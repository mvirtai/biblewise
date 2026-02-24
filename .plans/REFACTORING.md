# Refactoring opportunities

**Purpose**: Technical improvements that don't add features but make the code cleaner, more testable, or more maintainable.

---

## 1. Scope as a dataclass

**Current**: Scope is `tuple[ScopeKind, int | None]` passed as two params everywhere.

**Refactor**:
```python
from dataclasses import dataclass

@dataclass
class Scope:
    kind: ScopeKind
    book_position: int | None = None
    
    def where_sql(self) -> tuple[str, list]:
        return scope_where_sql(self.kind, self.book_position)
    
    def label(self) -> str:
        return scope_label(self.kind, self.book_position)
```

**Benefits**: Single param instead of two; methods on Scope instead of free functions; easier to extend (e.g. add verse length filter).

---

## 2. Shared Console instance

**Current**: `games.py` has `_console = Console()`; `ui.py` has `console = Console()`. Two instances.

**Refactor**: Use one console from `ui.py` everywhere:
```python
# games.py
from biblewise.ui import console
# Remove _console = Console()
```

**Benefits**: Consistent output; easier to mock for tests (one place).

---

## 3. DB connection as context manager

**Current**: `get_connection()` returns Connection; never explicitly closed.

**Refactor**:
```python
from contextlib import contextmanager

@contextmanager
def get_connection():
    conn = sqlite3.connect(get_db_path())
    try:
        yield conn
    finally:
        conn.close()

# Usage in main.py
with get_connection() as conn:
    do_search(conn, ...)
```

**Benefits**: Explicit cleanup; safer for long-running sessions or future threading.

---

## 4. Reference parsing: explicit abbreviations

**Current**: `BOOK_NAME_TO_POSITION` built from BOOKS with heuristic (last word, lowercase, startswith).

**Refactor**: Add explicit abbreviation map:
```python
ABBREVIATIONS = {
    "gen": 1, "gn": 1,
    "exo": 2, "ex": 2,
    "ps": 19, "psa": 19, "psalm": 19,
    "jn": 43, "john": 43,
    "1jn": 62, "1 jn": 62, "1john": 62,
    # ... all 66 books
}
```

**Benefits**: Predictable; no ambiguity; easier to document supported abbreviations.

---

## 5. Game logic extraction (testability)

**Current**: `run_hangman()` mixes game logic (word selection, masking, guess checking) with I/O (Prompt.ask, console.print).

**Refactor**: Extract pure logic:
```python
def hangman_logic(target_word: str, guess: str, guessed: set, masked: str) -> tuple[str, bool]:
    """Returns (new_masked, is_correct). Pure function."""
    # ... logic only, no I/O
    
def run_hangman(conn, scope_kind, book_position):
    # ... verse selection, then:
    for round in game_loop:
        guess = Prompt.ask(...)
        masked, correct = hangman_logic(target_word, guess, guessed, masked)
        console.print(...)
```

**Benefits**: Test `hangman_logic()` with deterministic inputs; no mocking needed.

---

## 6. Verse dict as a dataclass

**Current**: Verses are `dict` with keys `reference`, `text`, `book_name`, etc.

**Refactor**:
```python
@dataclass
class Verse:
    book_position: int
    chapter: int
    verse: int
    text: str
    book_name: str
    
    @property
    def reference(self) -> str:
        return f"{self.book_name} {self.chapter}:{self.verse}"
```

**Benefits**: Type safety; autocomplete; clear structure; easier to extend (e.g. add `translation_id`).

---

## 7. Config file support

**Current**: DB path, game defaults (pairs=4, max_wrong=6) are hardcoded.

**Refactor**: Optional `~/.biblewise/config.toml`:
```toml
[database]
path = "~/Documents/bible.db"

[games]
hangman_max_wrong = 6
memory_default_pairs = 3
quiz_num_options = 4

[ui]
theme = "dark"  # or "light"
```

Load with `tomllib` (Python 3.11+) or `tomli` (backport). Fallback to defaults if missing.

**Benefits**: User customization without code changes.

---

## 8. Logging instead of print for errors

**Current**: Errors use `console.print("[red]...")` or `print(...)`.

**Refactor**: Use `logging` module:
```python
import logging
logger = logging.getLogger("biblewise")

# In fetch_bible
logger.info("Downloading KJV...")
logger.error("Failed to download: %s", e)
```

**Benefits**: Can redirect to file; control verbosity; standard Python practice.

---

## 9. Async for future web version

**Current**: All DB calls are synchronous (sqlite3).

**Refactor** (if building web version): Use `aiosqlite` for async queries; FastAPI endpoints can `await db.random_verse()`.

**Benefits**: Non-blocking for web; better concurrency.

---

## 10. Separate game modules

**Current**: All games in `games.py` (248 lines).

**Refactor**: `games/hangman.py`, `games/memory.py`, `games/quiz.py`; `games/__init__.py` exports `run_hangman`, etc.

**Benefits**: Easier to navigate; each game is self-contained; can add more games without bloating one file.

---

## Priority (if refactoring)

1. **Scope dataclass** (high impact, low effort)
2. **Shared console** (trivial, good cleanup)
3. **Explicit abbreviations** (improves UX, moderate effort)
4. **Verse dataclass** (type safety, moderate effort)
5. **Config file** (nice-to-have, low priority for CLI)

---

*These are suggestions, not requirements. The current code is clean and functional.*
