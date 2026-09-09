# AGENTS.md

## Project

This is a Python application for working with DBF data.

## Repository structure

- `src/dbf_reports/` — application source code
- `src/dbf_reports/database/` — database-related code
- `src/dbf_reports/dbf/` — DBF-related code
- `src/dbf_reports/maintenance_utils/` — maintenance utilities
- `src/dbf_reports/dbf_pipeline.py` — DBF processing pipeline
- `src/dbf_reports/winguiapp.py` — GUI application
- `src/dbf_reports/config.py` — configuration handling
- `src/dbf_reports/utils.py` — common utilities
- `checkings/` — checks / verification scripts
- `data/` — application data
- `logs/` — logs

## Environment

- Python project
- Dependencies are managed with `uv`
- `uv.lock` must be kept in sync with `pyproject.toml`

## Rules

- Do not make unrelated refactoring.
- Preserve the existing architecture unless the task explicitly requires changing it.
- Before changing behavior, inspect the existing implementation and its callers.
- Do not modify generated or runtime data unless explicitly required.
- Do not commit secrets or local configuration.

## Validation

Before considering a change complete:

1. Run the relevant tests/checks.
2. Run formatting/linting if configured.
3. Verify that the application still starts.
4. Report what was changed and what was verified.