# CHITTI — Personal AI Assistant (MVP)

10-day modular voice assistant. See `docs/ARCHITECTURE.md` for the full design document, day-by-day schedule, and Phase 1/Phase 2 scope.

## Setup (Windows, Python 3.12+)

```powershell
# 1. Create and activate a virtual environment
python -m venv .venv
.venv\\Scripts\\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure secrets
copy configs\\.env.example .env
# then open .env and paste in your real ANTHROPIC\_API\_KEY

# 4. Run
python scripts\\run\_jarvis.py
```

You should see log output ending in `JARVIS online.` — that's Day 1's definition of done.

## Running tests

```powershell
pytest
```

## Project layout

See `docs/ARCHITECTURE.md` for the full annotated folder structure and module responsibilities. Quick map:

* `core/` — orchestrator, app bootstrap, logging
* `llm/` — Claude API client (abstracted behind an interface)
* `memory/` — conversation memory (abstracted behind an interface)
* `voice/` — wake word, STT, TTS (Day 6-7)
* `skills/` — every pluggable capability (open app, search, YouTube, browser automation, PDF summarizer, etc.)
* `automation/` — shared low-level browser/OS drivers used by skills
* `configs/` — the *only* place env vars / secrets are read
* `tests/` — unit tests, mirrors the source tree

## Status

**Day 1 — Foundation: done.**
Repo skeleton, config loading (`pydantic-settings` + `.env`), structured logging (console + rotating file), and an app that boots cleanly and fails fast on missing config.

Next: Day 2 — LLM client + basic memory + first real conversation loop.

