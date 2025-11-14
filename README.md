# Fixed Flask App — Email Async & Tests

This repository demonstrates a small Flask application using the application-factory pattern, SQLAlchemy, and Flask-Mail, with safe asynchronous email sending.

Root problems addressed:
- Original code imported proxies incorrectly and passed current_app instead of real app to background threads, causing "Working outside of application context" exceptions.
- Background threads used the app-scoped SQLAlchemy session without handling contexts, leading to session lifecycle and race conditions.
- Tests were flaky — they started threads that outlived test teardown and popped contexts while background threads still ran.
- Package import mismatches caused environment import errors in certain environments.

What I changed (high level):
- Implemented a proper app factory in `app/__init__.py`; imports of optional packages are guarded to avoid breaking systems with mismatched versions.
- Added an `EmailLog` model in `app/models.py` to track emails sent.
- Fixed `app/email.py` to accept the real `app` object and push a context inside background tasks; also added a test-friendly synchronous mode.
- Improved tests to run deterministically and assert that the message was recorded in Flask-Mail and logged in the database.
- Added `requirements.txt`, `setup.sh`, `run_test.sh`, `run_test.bat`, a `Dockerfile` placeholder, and `config.py`.

How to run locally:
- Linux/macOS:
  - ./setup.sh
  - source .venv/bin/activate
  - ./run_test.sh

- Windows (PowerShell):
  - ./run_test.bat

Known limitations:
- The project uses a file-based sqlite database for tests. In production a proper DB should be used.
- The test suite is minimal — it focuses on deterministic validation of asynchronous email handling and DB session safety.

If you want, I can extend the test suite further to add integration tests with a mock SMTP server and to improve logging and error handling.
