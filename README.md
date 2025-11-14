## Overview

This project is a minimal Flask application that demonstrates safe asynchronous email delivery with SQLAlchemy logging plus a deterministic automated test suite.

### Original issues
- Background threads accessed `current_app` outside of an application context which triggered `RuntimeError: working outside of application context`.
- Database writes in the async thread reused a torn-down session, causing random `InvalidRequestError` and flaky tests.
- Tests spawned threads but never waited for them, so teardown dropped tables while background work was still running.
- No reproducible tooling (requirements, setup scripts, or runner scripts) existed.

### Fixes
- Rebuilt the factory in `app/__init__.py` to initialize extensions cleanly and register models.
- Added `config.py` with explicit `TestConfig`, isolated in-memory SQLite, and `EMAIL_USE_ASYNC` switch for deterministic tests.
- Reworked `app/email.py` so the background worker receives the real app object, pushes its own context, logs outcomes, and optionally runs synchronously.
- Added the `EmailLog` model with status tracking plus two pytest cases that cover sync and async delivery paths; async tests join the worker before teardown to eliminate flakiness.
- Delivered reproducible tooling: `requirements.txt`, `setup.sh`, `run_test.sh`, `run_test.bat`, and an optional Docker workflow.

### Project structure
```
app/
  __init__.py        # application factory + extensions
  email.py           # safe async helpers
  models.py          # EmailLog ORM model
config.py            # Config and TestConfig definitions
tests/
  conftest.py        # pytest fixtures for app/db
  test_email.py      # sync + async behaviour tests
requirements.txt     # pinned dependencies
setup.sh             # create & populate .venv (Linux/macOS)
run_test.sh          # activate venv and run pytest (Linux/macOS)
run_test.bat         # Windows test runner
```

### Setup
1. Linux/macOS:
   ```
   ./setup.sh
   ```
   This script detects Python, creates `.venv`, and installs dependencies.
2. Windows:
   ```
   python -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   ```

### Running tests
- Linux/macOS: `./run_test.sh`
- Windows (Command Prompt or PowerShell): `run_test.bat`
- Docker (optional):
  ```
  docker build -t flask-email-demo .
  docker run --rm flask-email-demo
  ```

### Known limitations
- The demo relies on SQLite; swap `DATABASE_URL` for production-ready databases.
- Flask-Mail is synchronous per message; consider a task queue (Celery/RQ) for high throughput.
- Docker image is best-effort and not tuned for production deployment.
