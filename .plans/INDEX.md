# .plans/ — Developer documentation index

This folder contains **internal developer notes** for the Biblewise project. Not for end users.

---

## Files in this folder

### 📋 README.md
**Main developer reference**. Current design summary, improvements done, possible extensions, technical debt, testing notes, file/dependency notes.

### 📊 STATUS.md
**Project status snapshot** (2026-02-25). What works, known limitations, next steps (quick wins → larger features), file count, dependencies, readiness checklist.

### 💡 IMPROVEMENTS.md
**23 improvement ideas** from maalaisjärki review. Grouped by: UX/usability (7), architecture/code (5), testing (3), features (8). Includes performance notes and deployment ideas.

### 🔧 REFACTORING.md
**10 refactoring opportunities**. Technical improvements that don't add features but make code cleaner: Scope dataclass, shared console, DB context manager, game logic extraction, Verse dataclass, config file, logging, async, separate game modules. Priority ranking included.

### 🏗️ ARCHITECTURE.md
**Design decisions and rationale**. Data layer (why SQLite), scope design, UI layer (why Rich), games pattern, reference parsing, testing strategy, dependency choices, why terminal (not web), why KJV, file structure rationale.

### 🎬 DEMO.md
**Demo walkthrough** (5 min script). Setup, 12-step demo (search, random, scope, games), expected output samples, tips for showing the app, recording instructions.

### 🚀 DEPLOYMENT.md
**CI/CD and deployment notes**. GitHub Actions (test matrix, lint), Docker (Dockerfile, compose, image size), future options (PyPI, binary, Snap, Homebrew, web version), CI enhancements.

---

## How to use these notes

- **Starting a new feature?** → Read STATUS.md (next steps) + IMPROVEMENTS.md (ideas).
- **Refactoring?** → Read REFACTORING.md (priorities).
- **Explaining design to someone?** → Read ARCHITECTURE.md (rationale).
- **General context?** → Read README.md (overview).

---

## Maintenance

Update these files when:
- Architecture changes (new modules, major refactor) → ARCHITECTURE.md
- Feature added → STATUS.md, README.md
- New improvement idea → IMPROVEMENTS.md
- Code quality issue found → REFACTORING.md

Keep STATUS.md date current when making significant changes.

---

*These notes are for you, the developer. They help future-you (or collaborators) understand the project quickly.*
