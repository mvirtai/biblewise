# PR: UX / usability improvements (from .plans/IMPROVEMENTS.md)

## Summary

Implements the UX/usability tickets from the "Maalaisjärki improvements" section: scope visibility in games, memory pairs count prompt, hangman peek, case-insensitive search, quit confirmation, and search cancel hint. Reference quiz distractors were already scope-aware (random_verse uses scope), so no change there.

## Changes

1. **Scope visibility in games** — Game panels (Hangman, Memory pairs, Reference quiz) now show the current scope in the title, e.g. `Hangman — scope: Psalms` or `scope: New Testament`.

2. **Memory pairs: pair count** — Before starting, the user is prompted "How many pairs? (2–4)" with default 4. Invalid or empty input falls back to 4.

3. **Hangman: peek at verse** — User can type `peek` to see the full verse; it counts as one wrong guess. Panel text explains the option.

4. **Reference quiz: plausible distractors** — No code change: wrong options already come from `random_verse(conn, scope_kind=..., book_position=...)`, so OT scope gives only OT options, NT only NT, etc.

5. **Search: case-insensitive text search** — `search_by_text` now uses `LIKE ? COLLATE NOCASE` so e.g. "LOVE" matches "love". New test `test_case_insensitive` covers this.

6. **Quit confirmation** — On menu choice `q`, the app prompts "Are you sure? (y/n)" (default n). Only `y`/`yes` quits; otherwise the menu is shown again.

7. **Empty search input** — Search prompt now says "(Enter to cancel)" so users know empty input is valid and exits search without running a query.

## Testing

- `uv run pytest tests/ -v` — 37 tests (including new `test_case_insensitive`).
- Manual smoke: run app, try scope in games, memory pairs count, hangman peek, search with uppercase, quit confirmation, Enter at search prompt.

## Notes

- Reference quiz improvement #4 was already satisfied by existing scope filtering.
