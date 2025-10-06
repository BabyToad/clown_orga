# Repository Guidelines
## Project Structure & Module Organization
- Core modules live in root: `gui.py` (ttkbootstrap UI), `optimizer.py` (PuLP model), `data_handler.py` (Excel IO), `config.py` (settings).
- Tests sit beside sources as `test_*.py`; reuse `create_test_data.py` when new fixtures are needed.
- Excel samples (`example_students.xlsx`, `test_*.xlsx`) and coverage artefacts (`htmlcov/`) stay in the root; keep generated data out of version control.

## Build, Test, and Development Commands
- `pip install -r requirements.txt` installs runtime + pytest extras; run inside a virtualenv.
- `python gui.py` launches the desktop client; expect settings persistence in `settings.json`.
- `python -m pytest -v` runs the suite; `./run_tests.sh` or `run_tests.bat` add coverage flags.
- `python -m pytest --cov=. --cov-report=html` refreshes `htmlcov/` for manual inspection.
- `python create_test_data.py` regenerates deterministic Excel fixtures for manual QA.

## Coding Style & Naming Conventions
- Follow PEP 8 with four-space indents, module docstrings, and type hints for public functions.
- Use snake_case for functions/variables, CamelCase for classes, and keep GUI copy in German for consistency.
- Keep imports sorted and rely on Black or an equivalent formatter before submitting.

## Testing Guidelines
- Pytest discovery is configured in `pytest.ini`; respect existing markers (`unit`, `integration`, `slow`) and add new ones sparingly.
- Co-locate integration scenarios with `test_integration.py` and use `tmp_path` for Excel round-trips.
- Hold coverage at ≥80% and document new edge cases in `TESTING.md` when they require extra setup.

## Commit & Pull Request Guidelines
- Use short, imperative commit subjects with a scope prefix (`data_handler: normalize columns`); wrap bodies at 72 characters and explain the why.
- Reference issues or school rollouts in the body and call out any new artefacts (spreadsheets, configs).
- PRs should include a concise summary, UI before/after screenshots or GIFs, and the exact test command executed.

## Security & Configuration Tips
- Never commit real student data; `.gitignore` already excludes `settings.json` and ad-hoc spreadsheets—double-check new files honor that.
- Load secrets or API keys via environment variables rather than embedding them in code.
- Scrub PII from coverage exports or sample sheets before attaching them to issues or reviews.
