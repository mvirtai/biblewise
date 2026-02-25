# .plans — developer notes

This folder is for **you (the developer)** only. It is not part of the user-facing product. Use it for future work, extension ideas, and implementation notes. Do not rely on it being kept in sync automatically; treat it as a scratchpad and update it when you change direction.

---

## Current design summary

- **UI**: Rich (panels, tables, prompts). Click in deps, not yet used for CLI.
- **Scope (aluerajaus)**: Menu "Set scope" → All / OT / NT / Single book. Used by random verse, text search, and all games.
- **Games**: Submenu (Menu → 3. Games). All games respect scope.
- **Modules**: `ui.py`, `scope.py`, `main.py`.
- Reference parsing accepts "John 3 16". Tests: `tests/` with pytest; in-memory DB fixture in `conftest.py`. Run with `uv sync --extra dev` then `uv run pytest`. See README “Tests” section.

---

## Improvements done (maalaisjärki)

- **Scope**: Limit to one book or testament so drills are focused.
- **Games submenu**: Main menu cleaner; games grouped.
- **Rich UI**: Panels, tables, green/red/yellow feedback.
- **Search**: "Book c v" without colon accepted; case-insensitive text search (COLLATE NOCASE).
- **Empty scope**: Clear message when no verses in scope.
- **UX (2026-02)**: Scope in game titles; Hangman verse with blank from start; peek (verse shown, word still blanked); Memory pairs prompt 2–4; quit confirmation; search "(Enter to cancel)". See IMPROVEMENTS.md UX section (all 7 items done).

---

## Possible extensions (for later)

- **More games**: Fill-in-the-blank (one word hidden), order-the-verse (scrambled words), “next verse” (show N, guess N+1).
- **Difficulty**: More quiz options (e.g. 6 choices), or only medium-length verses for memory.
- **Scoring and progress**: Persist stats (e.g. correct quiz answers per reference), simple “today’s streak,” or optional local score file.
- **Translations**: Support multiple sources (e.g. ASV from same repo); schema could add `translation_id` or a separate DB per translation.
- **Config**: Optional config file or env for DB path, default game options (e.g. number of pairs, quiz options), or verse length bounds for games.

---

## Technical debt and refactors

- **Reference parsing**: `BOOK_NAME_TO_POSITION` is built from `BOOKS` with ad-hoc variants (last word, lowercase). Consider a small explicit list of accepted abbreviations and aliases to avoid ambiguity (e.g. "Jn" vs "1 Jn").
- **Games I/O**: Games use Rich (console.print, Prompt.ask). Extracting a thin “terminal UI” layer would make it easier to add a simple TUI (e.g. `curses`) or automated tests with mocked I/O.
- **DB lifecycle**: Connection is never explicitly closed on normal exit. Fine for a small CLI; if you add background threads or more complex shutdown, consider a context manager.

---

## Testing (current)

- **tests/conftest.py**: In-memory SQLite with schema + 3 books, 5 verses.
- **tests/test_books.py**: BOOKS length, book_name_by_position.
- **tests/test_db.py**: get_db_path, init_schema, verse_count.
- **tests/test_search.py**: parse_reference (many formats), get_verse, search_by_reference, search_by_text, random_verse.
- **tests/test_fetch_bible.py**: import_data() with minimal JSON fixture (verse count, content, idempotent).
- **tests/test_games.py**: get_random_verse_for_game (returns verse, prefers min_words, fallback).
- **tests/test_scope.py**: scope_where_sql (all/ot/nt/book), scope_label.

Further ideas: mock I/O in run_hangman/run_reference_quiz for deterministic game tests; integration test that runs full fetch with a small JSON and asserts DB state.

---

## File and dependency notes

- **Dependencies**: rich, click (in pyproject.toml). Click not yet used; reserved for optional CLI subcommands. Keep `requirements.txt` in sync for pip users.
- Entry point: `biblewise = biblewise.main:main` so `uv run biblewise` works; `python -m biblewise` also works.
- `fetch_bible` uses `urllib.request` only; `requests` is in deps for potential future use.

---

## See also

- **IMPROVEMENTS.md** — UX ideas, feature suggestions, performance notes, deployment ideas (23 items).
- **REFACTORING.md** — Code quality improvements (Scope dataclass, shared console, game logic extraction, etc.).
- **ARCHITECTURE.md** — Design decisions, rationale, file structure, dependency choices.

---

*Update these files when you change architecture or add features.*
