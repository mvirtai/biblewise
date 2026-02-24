# Improvements and future work

**Date**: 2026-02-25  
**Status**: Post-review notes after initial implementation

---

## Code quality observations

### Good
- **Scope works well**: OT/NT/single book filter is clean and applied consistently.
- **Rich UI**: Panels, tables, prompts look professional; color feedback (green/red/yellow) is clear.
- **Reference parsing**: Accepts "John 3 16" (space) and "John 3:16" (colon); flexible for user.
- **Games submenu**: Cleaner main menu; games grouped logically.
- **Tests**: 31+ tests (books, db, search, scope, fetch, games); in-memory fixture is fast.

### Issues fixed during review
- Removed unused imports: `book_list_for_picker` from main, `Text` from games.
- Memory pairs: Added message when user quits early ("Matched X/Y pairs").
- Reference quiz: Added fallback when scope has < 4 unique verses (e.g. Philemon has 1 chapter).
- Curly quotes in ui.py title strings → replaced with straight quotes for consistency.

---

## Maalaisjärki (common sense) improvements to consider

### UX / usability

1. **Scope visibility in games**
   - Currently scope is shown in main menu but not repeated in game panels.
   - Suggestion: Add scope to game panel title or subtitle (e.g. "Hangman (scope: Psalms)").

2. **Memory pairs: default count**
   - 4 pairs = 8 cards; might be overwhelming on small terminals.
   - Suggestion: Prompt user "How many pairs? (2–4)" or add difficulty setting.

3. **Hangman: show full verse earlier**
   - User sees reference but not the verse until game ends.
   - Suggestion: Option to "peek" at verse (costs 1 wrong guess) or show first/last word as hint.

4. **Reference quiz: plausible distractors**
   - Wrong options are random; could be Genesis vs Revelation (too easy to rule out).
   - Suggestion: For NT scope, only pick NT wrong answers; for OT, only OT. Or pick from nearby chapters (e.g. John 3 vs John 5).

5. **Search: case-insensitive text search**
   - Currently `LIKE %query%` is case-sensitive in SQLite (default).
   - Suggestion: Use `LIKE %query% COLLATE NOCASE` or lowercase both sides.

6. **Quit confirmation**
   - User might hit 'q' by accident.
   - Suggestion: "Are you sure? (y/n)" or just accept it (current behavior is fine for CLI).

7. **Empty input handling**
   - Prompt.ask with default="1" means pressing Enter → choice 1. Good for main menu.
   - In search, default="" means Enter → empty search → no results. Consider "Press Enter to cancel" message.

### Architecture / code

8. **Console instances**
   - `games.py` uses `_console = Console()`; `ui.py` uses `console = Console()`. Two separate instances.
   - Suggestion: Share one console from ui.py in games (import console from ui), or accept console as param.

9. **DB connection lifecycle**
   - Connection opened in `run()` for each menu action; not closed explicitly (Python GC handles it).
   - Suggestion: Use `with get_connection() as conn:` context manager (requires wrapping Connection) or close explicitly. Current approach is fine for small CLI.

10. **Scope state in main**
    - Scope is a tuple `(scope_kind, book_position)` passed everywhere.
    - Suggestion: Create a `Scope` dataclass with `.where_sql()` and `.label()` methods; cleaner than tuple + two params.

11. **Reference parsing: abbreviations**
    - "Jn" or "Jhn" for John not supported; "Gen" works (matches "genesis" via startswith).
    - Suggestion: Add explicit abbreviation map (e.g. "Jn" → 43, "1Jn" → 62, "Gen" → 1, "Ps" → 19).

12. **Error messages: Finnish vs English**
    - All UI is English; user rules say "code in English" but conversation can be Finnish.
    - Suggestion: Keep UI English for consistency with codebase (current); or add i18n later if needed.

### Testing

13. **Game I/O tests**
    - Games use Prompt.ask (blocking); hard to test without mocking.
    - Suggestion: Inject console or use `unittest.mock.patch` for Prompt.ask in tests.

14. **Integration test for fetch**
    - `test_fetch_bible.py` tests `import_data()` with a fixture; doesn't test `download_json()`.
    - Suggestion: Mock `urllib.request.urlopen` to return fixture JSON; test full `run()`.

15. **Scope in tests**
    - Tests for search/games don't test scope filtering (they use default "all").
    - Suggestion: Add tests for `search_by_text(conn, "love", scope_kind="nt")` → only NT results.

---

## Feature ideas (future)

16. **Scoring / progress**
    - Track correct/wrong per game; save to `~/.biblewise/stats.json` or in DB.
    - Leaderboard or "streak" (days in a row).

17. **More games**
    - **Fill-in-the-blank**: Show verse with one word `___`; user types the word.
    - **Order the verse**: Scrambled words; user reorders them.
    - **Verse completion**: Show first half; user types or chooses second half.
    - **Book quiz**: "Which book has the most chapters?" (trivia).

18. **Translations**
    - Support ASV, WEB, etc. from same GitHub repo.
    - Schema: Add `translation` column to verses or separate DB per translation.
    - UI: "Set translation" in menu.

19. **CLI subcommands (Click)**
    - `biblewise search "John 3:16"` → print verse and exit (no menu).
    - `biblewise random --scope nt` → print one NT verse.
    - `biblewise quiz --scope psalms` → one quiz round.
    - Useful for scripting or quick lookups.

20. **Verse length filter**
    - In addition to scope, filter by verse length (e.g. "short verses only" for memory).
    - UI: "Set filters" → Scope + Length (short/medium/long).

21. **Bookmarks / favorites**
    - User can save verses to a favorites list; quick access or focused drills.
    - Schema: Add `favorites` table with `(user_id, book_position, chapter, verse)`.

22. **Daily verse**
    - Show a "verse of the day" (deterministic based on date, or from a curated list).

23. **Study mode**
    - Read a chapter sequentially; quiz on each verse or section.

24. **Export / share**
    - Export search results or favorites to text/JSON.

---

## Performance notes

- **31,103 verses**: All queries are fast (<10ms) on modern hardware.
- **Random verse**: `ORDER BY RANDOM()` is O(n) but acceptable for 31k rows.
- **Text search**: `LIKE %query%` with index on `text` is reasonably fast; for large queries consider FTS5 (full-text search).

---

## Deployment / distribution ideas

- **PyPI**: Package as `biblewise` on PyPI; users install with `pip install biblewise` or `uv pip install biblewise`.
- **Docker**: Dockerfile with Python + biblewise; `docker run -it biblewise` (fetch_bible in entrypoint or volume).
- **Binary**: Use PyInstaller or Nuitka to create standalone executable (no Python required).
- **Web version**: Flask/FastAPI backend + HTMX or React frontend; same DB/logic, browser UI.

---

*Review these notes when planning next steps or refactoring.*
