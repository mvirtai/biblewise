# Demo walkthrough

**Purpose**: Quick guide for showing the app to others or testing all features.

---

## Setup (first time)

```bash
cd /home/vivaldev/code/biblewise
uv sync
uv run python -m biblewise.fetch_bible  # Downloads KJV, creates bible.db (~10s)
```

---

## Demo script (5 minutes)

### 1. Welcome and main menu
```bash
uv run biblewise
```
- Shows welcome panel with blue border
- Main menu: 5 options + current scope

### 2. Search by reference
- Choose **1** (Search)
- Type: `John 3:16`
- Shows verse in green panel with reference as title

### 3. Search by text
- Choose **1** again
- Type: `love`
- Shows table with up to 10 results (reference + text snippet)

### 4. Random verse
- Choose **2** (Random verse)
- Shows one random verse from whole Bible

### 5. Set scope to NT
- Choose **4** (Set scope)
- Choose **3** (New Testament)
- Menu now shows "(current: New Testament)"

### 6. Random verse in NT
- Choose **2** again
- Verse is now from Matthew–Revelation only

### 7. Games submenu
- Choose **3** (Games)
- Shows 3 games + Back option

### 8. Reference quiz
- Choose **3** (Reference quiz)
- Shows verse in italic, 4 reference options in table
- Type a number (1–4)
- Feedback: green "Correct!" or red "Wrong. It was: ..."

### 9. Hangman
- Back to main menu, choose **3** (Games) → **1** (Hangman)
- Shows reference and masked word (e.g. `_o_e_`)
- Type letters or full word
- Feedback: green "Good" or red "No"
- After 6 wrong or correct: shows full verse in panel

### 10. Memory pairs
- Choose **3** (Games) → **2** (Memory pairs)
- Two tables: References (Ref 1–4) and Verse snippets (Text 1–4)
- Type pairs: `1 3` (Ref 1 + Text 3)
- Feedback: green "Match!" or red "No match"
- After all matched: "All pairs matched!"

### 11. Set scope to single book
- Choose **4** (Set scope) → **4** (Single book)
- Shows table of 66 books
- Type: `19` (Psalms)
- Menu shows "(current: Psalms)"
- All games and random verse now use Psalms only

### 12. Quit
- Type **q**
- Shows "Goodbye." and exits

---

## Expected output samples

**Search result (John 3:16)**:
```
╭───────────────────────────────── John 3:16 ──────────────────────────────────╮
│ For God so loved the world, that he gave his only begotten Son, that         │
│ whosoever believeth in him should not perish, but have everlasting life.     │
╰──────────────────────────────────────────────────────────────────────────────╯
```

**Reference quiz**:
```
╭──────────── Reference quiz — Which reference is this verse from? ────────────╮
│ "And I said, Lord, they know that I imprisoned and beat in every synagogue   │
│ them that believed on thee:"                                                 │
╰──────────────────────────────────────────────────────────────────────────────╯
┌──────┬───────────────────┐
│ 1    │ 2 Samuel 1:2      │
│ 2    │ 1 Kings 16:16     │
│ 3    │ Acts 22:19        │  ← Correct
│ 4    │ 2 Chronicles 9:26 │
└──────┴───────────────────┘
```

**Scope menu**:
```
╭───────────────────────────────── Set scope ──────────────────────────────────╮
│   1. All (whole Bible)                                                       │
│   2. Old Testament                                                           │
│   3. New Testament                                                           │
│   4. Single book (pick from list)                                            │
│   b. Back (keep current)                                                     │
╰──────────────────────────────────────────────────────────────────────────────╯
```

---

## Tips for demo

- **Scope is key**: Show how limiting to Psalms or NT makes games more focused.
- **Reference parsing**: Show both "John 3:16" and "John 3 16" work.
- **Games**: Hangman is most visual; reference quiz is quickest.
- **Search**: Text search with "love" or "faith" shows many results.

---

## Recording a demo

If making a GIF or video:
1. Use `asciinema record demo.cast` → `agg demo.cast demo.gif` (or similar tool)
2. Keep terminal 80x24 or 100x30 for readability
3. Show: search → random → scope → one game → quit
4. Total time: 1–2 minutes

---

*Use this script when showing the app to others or testing after changes.*
