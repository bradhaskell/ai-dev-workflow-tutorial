# Implementation Plan: LMU Baseball Practice Data Pipeline & Performance Dashboard

**Branch**: `001-baseball-pipeline` | **Date**: 2026-01-24 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-baseball-pipeline/spec.md`

## Summary

Build an automated ETL pipeline to process Excel batting practice files, store validated data in MySQL, and visualize performance metrics in Looker Studio for LMU Baseball coaching staff. The system reduces manual data processing by 80% and enables data-informed coaching decisions through KPI dashboards, player profiles, and trend analysis.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: pandas, sqlalchemy, pymysql, openpyxl, python-dotenv
**Storage**: MySQL (LMU's existing server)
**Testing**: pytest with pytest-cov for coverage
**Target Platform**: GitHub Actions (Linux runners), local Windows/Mac development
**Project Type**: Single project (ETL pipeline + CLI)
**Performance Goals**: Process 50-200 row files in <30 seconds; 95%+ pipeline success rate
**Constraints**: Dashboard load <4 seconds; no data corruption on failures
**Scale/Scope**: ~30 players, daily/weekly practice sessions, single team

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Requirement | Status | Implementation |
|-----------|-------------|--------|----------------|
| I. Data Integrity First | Validate before storage, reject invalid data, log failures | ✅ PASS | `transform.py` validates schema/types; `load.py` uses transactions |
| II. Robust Error Handling | Catch exceptions, use transactions, comprehensive logs | ✅ PASS | Try/except blocks; SQLAlchemy transactions; Python logging module |
| III. Coach-Friendly Visualizations | Clear labels, 4s load, intuitive filtering | ✅ PASS | Looker Studio with descriptive metric names and tooltips |
| IV. Clean, Maintainable Code | Type hints, docstrings, PEP 8, modular design | ✅ PASS | ETL modules: extract.py, transform.py, load.py; type hints throughout |
| V. Secure Credential Management | No hardcoded secrets, use env vars/GitHub Secrets | ✅ PASS | python-dotenv for local; GitHub Secrets for Actions; .env in .gitignore |
| VI. Environment Isolation | Virtual environment, pinned requirements.txt | ✅ PASS | venv for local dev; requirements.txt with version pins |

**Gate Result**: ✅ All principles satisfied. Proceed to Phase 0.

## Project Structure

### Documentation (this feature)

```text
specs/001-baseball-pipeline/
├── plan.md              # This file
├── research.md          # Phase 0: Technology decisions
├── data-model.md        # Phase 1: Database schema design
├── quickstart.md        # Phase 1: Setup and usage guide
├── contracts/           # Phase 1: API/CLI contracts
│   └── cli-contract.md  # Command-line interface specification
└── tasks.md             # Phase 2: Implementation tasks (via /speckit.tasks)
```

### Source Code (repository root)

```text
src/
├── __init__.py
├── extract.py           # Excel file reading and initial parsing
├── transform.py         # Data validation, cleaning, normalization
├── load.py              # Database operations with transactions
├── pipeline.py          # Main orchestration: extract → transform → load
├── config.py            # Configuration and environment variable handling
└── models.py            # SQLAlchemy ORM models

tests/
├── __init__.py
├── unit/
│   ├── test_extract.py
│   ├── test_transform.py
│   └── test_load.py
├── integration/
│   └── test_pipeline.py
└── fixtures/
    └── sample_batting_practice.xlsx

data/
├── sample_batting_practice.xlsx  # Sample input for testing
└── schema.sql                    # Database schema DDL

.github/
└── workflows/
    └── pipeline.yml     # GitHub Actions workflow for scheduled runs

.env.example             # Template for environment variables
requirements.txt         # Pinned Python dependencies
README.md               # Project documentation
```

**Structure Decision**: Single project structure selected. This is an ETL pipeline with CLI execution, not a web application. The `src/` directory contains modular ETL components following the extract-transform-load pattern specified in the constitution.

## Complexity Tracking

> No constitution violations requiring justification. Design follows all principles.

| Aspect | Decision | Rationale |
|--------|----------|-----------|
| No ORM abstractions | Direct SQLAlchemy Core + simple models | YAGNI: single table writes don't need repository pattern |
| No API layer | CLI-only execution | Pipeline runs via cron/Actions, not REST API |
| Single database | MySQL only | Looker Studio connects directly; no intermediate storage needed |
