# Project status

**Last updated**: 2026-02-25  
**Version**: 0.1.0

---

## Current state: ✅ Functional MVP

The app is **complete and working** for its initial scope:
- ✅ Data pipeline (fetch KJV → SQLite)
- ✅ Search (reference + text, with scope)
- ✅ Random verse (with scope)
- ✅ Three games (Hangman, Memory pairs, Reference quiz)
- ✅ Scope filter (All / OT / NT / Single book)
- ✅ Rich terminal UI (panels, tables, colors)
- ✅ Tests (31+ passing, in-memory fixture)
- ✅ Documentation (README, .plans/)

---

## What works well

- **Scope**: Central feature; applied consistently across search and games.
- **Rich UI**: Professional look; panels and tables are clear.
- **Reference parsing**: Flexible (accepts "John 3:16" and "John 3 16").
- **Games**: Fun and educational; Hangman and quiz are engaging.
- **Tests**: Fast (in-memory DB); good coverage of core logic.

---

## Known limitations

- **No persistence**: No scores, no progress tracking, no favorites.
- **Single translation**: KJV only (ASV/WEB available in same repo but not wired).
- **No CLI args**: Must use interactive menu (Click reserved for future).
- **Reference quiz distractors**: Random; could be more plausible (e.g. same testament).
- **Abbreviations**: "Jn" for John not supported; only full names and some heuristics.

---

## Next steps (if continuing)

### Quick wins (1–2 hours)
1. Shared console (games imports from ui) — cleanup
2. Case-insensitive text search (`COLLATE NOCASE`) — UX improvement
3. Scope in game panel titles (e.g. "Hangman (scope: Psalms)") — visibility

### Medium features (3–5 hours)
4. Explicit abbreviation map (Jn, Gen, Ps, etc.) — better UX
5. Scope dataclass (replace tuple) — cleaner code
6. More games (fill-in-the-blank, order-the-verse) — variety

### Larger features (1–2 days)
7. Scoring / progress (save stats to JSON or DB) — motivation
8. Multiple translations (ASV, WEB) — choice in menu
9. CLI subcommands with Click (`biblewise search "John 3:16"`) — power users
10. Config file (~/.biblewise/config.toml) — customization

### Future directions
- Web version (Flask/FastAPI + HTMX or React)
- Mobile app (Kivy or React Native with same DB)
- PyPI package (distribute as `pip install biblewise`)
- Docker image (for easy deployment)

---

## File count

- **Python files**: 16 (8 in biblewise/, 7 in tests/, 1 root)
- **Lines of code**: ~800 (excluding tests and data)
- **Tests**: 31+ (books, db, search, scope, fetch, games)
- **Documentation**: README.md + 4 files in .plans/

---

## Dependencies

- **Runtime**: requests, rich, click (click not yet used)
- **Dev**: pytest
- **Python**: >=3.10 (for `|` union types, match/case if added later)

---

## Ready for

- ✅ Local use (personal Bible study tool)
- ✅ GitHub (professional-looking repo for portfolio)
- ✅ Extension (scope/games/translations can be added incrementally)
- ⚠️ Distribution (needs PyPI setup or binary build)
- ⚠️ Production (no logging, no config, no error telemetry)

---

*This is a solid foundation. You can use it as-is or extend it based on IMPROVEMENTS.md.*
