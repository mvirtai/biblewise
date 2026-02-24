# Deployment and CI/CD

**Purpose**: Notes on GitHub Actions, Docker, and future deployment options.

---

## GitHub Actions (CI)

**File**: `.github/workflows/ci.yml`

### Jobs

1. **test** (matrix: Python 3.10, 3.11, 3.12)
   - Checkout code
   - Install uv
   - Install dependencies (`uv sync --extra dev`)
   - Run pytest (`uv run pytest tests/ -v`)
   - Basic import check (ensure modules load)

2. **lint** (Python 3.12)
   - Install ruff (optional linter)
   - Run `ruff check` on biblewise/ and tests/ (continue-on-error)

### Triggers

- Push to `main`
- Pull requests to `main`

### Notes

- Tests run in ~30s per Python version (3 versions = ~90s total)
- No real `bible.db` needed (tests use in-memory fixture)
- Linting is optional (ruff not required; can add later)

---

## Docker

**Files**: `Dockerfile`, `docker-compose.yml`, `.dockerignore`

### Dockerfile

- Base: `python:3.12-slim` (~150 MB)
- Copies `pyproject.toml`, `requirements.txt`, `biblewise/`
- Installs package with `pip install -e .`
- **Runs `fetch_bible` during build** → image includes `bible.db` (~10 MB)
- CMD: `biblewise` (interactive menu)

### docker-compose.yml

- Service: `biblewise` (builds from Dockerfile)
- `stdin_open: true` + `tty: true` for interactive terminal
- Volume: `bible-data:/app` (persists DB if you want to rebuild without re-fetching)

### Build and run

```bash
docker build -t biblewise .
docker run -it biblewise
```

Or:
```bash
docker-compose up --build
```

### Image size

- Base image: ~150 MB
- + Python deps (rich, click, requests): ~10 MB
- + biblewise code: <1 MB
- + bible.db: ~10 MB
- **Total**: ~170 MB

### Notes

- `.dockerignore` excludes `.venv/`, `tests/`, `.plans/` to keep image small
- `fetch_bible` runs during build (requires network); if build fails, check network or comment out RUN line and fetch manually in container

---

## Future deployment options

### 1. PyPI package

**Steps**:
1. Add `[project.urls]` to pyproject.toml (homepage, repository)
2. Build: `uv build` or `python -m build`
3. Upload: `twine upload dist/*` or `uv publish`

**Users install**: `pip install biblewise` or `uv pip install biblewise`

**Trade-off**: Users must run `biblewise-fetch` (or `python -m biblewise.fetch_bible`) separately to download Bible. Or bundle `bible.db` in package (adds ~10 MB to wheel).

### 2. Standalone binary (PyInstaller / Nuitka)

**Steps**:
1. Install: `pip install pyinstaller`
2. Build: `pyinstaller --onefile --name biblewise biblewise/main.py`
3. Distribute: `dist/biblewise` (single executable, ~50 MB)

**Trade-off**: Large binary; must bundle `bible.db` or fetch on first run.

### 3. Snap / Flatpak (Linux)

**Steps**: Create `snapcraft.yaml` or `flatpak manifest`; publish to Snap Store or Flathub.

**Benefits**: Easy install on Linux (`snap install biblewise`); sandboxed.

### 4. Homebrew (macOS / Linux)

**Steps**: Create Homebrew formula; submit to homebrew-core or personal tap.

**Users install**: `brew install biblewise`

### 5. Web version (Flask / FastAPI)

**Architecture**:
- Backend: FastAPI with same `db.py`, `search.py`, `games.py` logic
- Frontend: HTMX (simple) or React (rich)
- Deploy: Heroku, Fly.io, Railway, or self-hosted

**Benefits**: No install; accessible from any device; can add user accounts, progress tracking.

**Trade-off**: Requires server; more complex than CLI.

### 6. GitHub Releases (binaries)

**Steps**:
1. Build binaries for Linux/macOS/Windows (PyInstaller or Nuitka)
2. Create GitHub release: `gh release create v0.1.0 dist/*`
3. Users download from Releases page

**Benefits**: Easy distribution; no PyPI needed.

---

## CI/CD enhancements (future)

- **Code coverage**: Add `pytest-cov`; upload to Codecov or Coveralls
- **Linting**: Add `ruff` or `flake8` as required (currently optional)
- **Type checking**: Add `mypy` to CI
- **Docker image push**: Build and push to Docker Hub or GitHub Container Registry on release
- **Release automation**: Use `semantic-release` or manual tags to trigger builds

---

## Current CI status

- ✅ Tests run on 3 Python versions
- ✅ Basic import check
- ⚠️ No coverage reporting
- ⚠️ Linting optional (ruff not required)
- ⚠️ No type checking (mypy)

---

*Refer to this when setting up deployment or improving CI pipeline.*
