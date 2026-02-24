# PR: Add docstrings and explanatory comments

## Summary

Add consistent, English docstrings and brief explanatory comments across the codebase. No behaviour or public API changes. Fixes two scope tests that asserted literal values in SQL instead of parameterised queries.

## Changes

- **Module docstrings** for all packages and modules (`__init__.py`, `books`, `db`, `fetch_bible`, `scope`, `search`, `games`, `ui`, `main`) describing purpose and usage.
- **Function docstrings** for all public functions: one-line summary and, where useful, Args/Returns.
- **Comments** for non-obvious bits: `REF_PATTERN` / `BOOK_NAME_TO_POSITION` in `search.py`, OT/NT constants in `scope.py`, KJV JSON URL in `fetch_bible.py`, memory-game verse length in `games.py`.
- **Tests**: `test_scope.py` — OT/NT tests now assert `BETWEEN` and `params` instead of literal `"39"` / `"40"` in the SQL string (implementation uses placeholders).

## Testing

- `uv run pytest tests/ -v` — 36 tests passing.

## Notes

- Style kept consistent (short summary + optional Args/Returns). No refactors or external behaviour changes.
