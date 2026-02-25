# PR: UX follow-ups and docs update

## Summary

Hangman improvements (verse visible from start, peek does not reveal answer), .plans/ brought up to date with implemented UX items, and .gitignore updated for private .conversations/ folder.

## Changes

### Hangman (games.py)

- **Verse from start**: Verse is shown from the beginning with the target word blanked (e.g. "...two ______.") so the user has full context to guess the word.
- **Peek**: Peek now shows the verse with the word still blanked (current masked state), so it does not give away the answer; it still costs one wrong guess.

### Documentation (.plans/)

- **STATUS.md**: UX improvements listed in current state; test count 37; quick wins 2–3 marked done; .plans/ vs .conversations/ noted.
- **IMPROVEMENTS.md**: UX section — status line added "All 7 items implemented"; each of 1–7 marked ✅.
- **README.md**: "Improvements done" updated with UX 2026-02 summary.
- **INDEX.md**: IMPROVEMENTS.md description updated (UX implemented).

### Other

- **.gitignore**: Only `.conversations/` ignored (private, Finnish). `.plans/` remains public and tracked.
- **QUICKSTART.md**: Minor update if present.

## Testing

- `uv run pytest tests/ -v` — all tests pass.
- Manual: Hangman shows verse with blank; peek shows verse without revealing word.

## Notes

- .conversations/ is for private Finnish notes (not committed). .plans/ stays public and in English.
