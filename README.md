# Fixed Flask App and Deterministic Tests

Overview
- This project reproduces issues with asynchronous email sending and Flask application context misuse. The original problem included: threads using Flask proxy objects, uncaptured contexts, database operations in background threads after the session was removed, and flaky tests.

What I changed
- Restructured the app to be a package `app` with `__init__.py` creating extensions and `create_app` factory.
- Added `app/models.py` with `EmailLog` model.
- Fixed `app/email.py` to properly pass the real app instance into threads and push the app context in background threads before using `db` or `mail`.
- Added a synchronous mode for tests using `EMAIL_SEND_ASYNC=False` to avoid flakiness.
- Rewrote tests to use deterministic behavior and to join threads in the async test.
- Added `config.py` with `TestConfig` to use a file-based sqlite DB for multithread safety.

Run tests
- Linux/macOS: `./setup.sh` then `./run_test.sh`
- Windows: `run_test.bat`

Known limitations
- This is small demo code for tests. In production, use a real mail server and background job processing system such as Celery or RQ.

