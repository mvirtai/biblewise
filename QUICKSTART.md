# Biblewise — Quick start

Terminal Bible memorization with games, search, and scope filtering.

## Install and run

**With uv**:
```bash
uv sync
uv run python -m biblewise.fetch_bible   # One-time: downloads KJV (~10s)
uv run biblewise
```

**With Docker**:
```bash
docker build -t biblewise .
docker run -it biblewise
```

## Features

- **Search**: Type reference (John 3:16) or text (love, faith)
- **Random verse**: One verse from current scope
- **Scope**: Limit to All / OT / NT / Single book (e.g. Psalms)
- **Games**: Hangman, Memory pairs, Reference quiz

## Example

```bash
$ uv run biblewise
# Choose 4 (Set scope) → 3 (New Testament)
# Choose 3 (Games) → 3 (Reference quiz)
# Read verse, pick correct reference from 4 options
```

See README.md for full documentation.
