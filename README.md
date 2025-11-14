# Flask Email Refactor

## What was wrong
- The original factory and email helpers misused Flask proxies and left asynchronous threads running without application contexts.
- Background threads committed to the database after the context/session had been torn down, which made tests flaky and unreliable.
- There was no reproducible environment, documentation, or automated test setup.

## What changed
- Added a proper application factory with SQLAlchemy, Flask-Mail, and login/migration extensions wired through a real app instance.
- Implemented `EmailLog`, ensured `send_email` uses `current_app._get_current_object()`, pushes contexts inside threads, and exposes a synchronous mode for tests.
- Replaced the fragile unit test with deterministic pytest-based coverage that records mail outputs and verifies `EmailLog` entries.
- Added configuration, dependency tracking, OS-aware setup/test scripts, a README, and an optional Dockerfile so every environment can reproduce the fixes.

## Project structure
- `app/`: application package with factory, models, and email helpers.
- `config.py`: base and test-specific Flask configuration.
- `tests/`: pytest fixtures and cases exercising `send_email`.
- `requirements.txt`: pinned Python dependencies.
- `setup.sh` / `run_test.sh`: one-click setup/testing for Linux/mac.
- `run_test.bat`: Windows test runner.
- `Dockerfile`: optional containerized execution (runs setup and tests).

## Setup & testing

### Linux / macOS
1. Ensure `python3` is available.
2. Run `./setup.sh`.
3. Run `./run_test.sh` to install requirements and execute `pytest tests`.

### Windows
1. Run `run_test.bat`; it will create a virtual environment, install dependencies, and launch `pytest tests`.

### Docker (optional)
1. Build the image with `docker build -t flask-email-refactor .`
2. Run it: `docker run --rm flask-email-refactor` (it already executes `./run_test.sh`).

## Known limitations
- Asynchronous email dispatch requires a configured SMTP server in production (`EMAIL_ASYNC` defaults to `True`). In tests we run synchronously to avoid threading races.
- The sample setup does not expose web routes or CLI commands because the original task focused on the email helper and its tests.
