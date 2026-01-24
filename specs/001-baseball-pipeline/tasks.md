# Tasks: LMU Baseball Practice Data Pipeline & Performance Dashboard

**Input**: Design documents from `/specs/001-baseball-pipeline/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/cli-contract.md

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- Database schema: `data/schema.sql`
- GitHub Actions: `.github/workflows/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create src/ directory structure with __init__.py files per plan.md
- [ ] T002 Create tests/ directory structure with unit/, integration/, fixtures/ subdirectories
- [ ] T003 [P] Create requirements.txt with pinned dependencies: pandas, sqlalchemy, pymysql, openpyxl, python-dotenv, pytest, pytest-cov
- [ ] T004 [P] Create .env.example with DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME, LOG_LEVEL placeholders
- [ ] T005 [P] Add .env to .gitignore to prevent credential commits
- [ ] T006 [P] Create data/ directory and add sample_batting_practice.xlsx fixture file

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T007 Implement config.py with environment variable loading using python-dotenv in src/config.py
- [ ] T008 Implement database connection factory with SQLAlchemy engine creation in src/config.py
- [ ] T009 Create SQLAlchemy models for players, practice_sessions, batting_records, upload_logs in src/models.py
- [ ] T010 [P] Create database schema DDL script with tables and indexes in data/schema.sql
- [ ] T011 [P] Create database views (player_metrics_summary, session_metrics_summary, recent_upload_status) in data/schema.sql
- [ ] T012 Implement init-db CLI command to create schema in src/pipeline.py
- [ ] T013 Configure Python logging with structured format (timestamp, level, module, message) in src/config.py

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 - Automated Data Upload (Priority: P1) 🎯 MVP

**Goal**: Process Excel batting practice files automatically with validation, cleaning, and database storage

**Independent Test**: Run `python -m src.pipeline process data/sample_batting_practice.xlsx` and verify data appears in database with success log

### Implementation for User Story 1

- [ ] T014 [US1] Implement Excel file reading with openpyxl via pandas in src/extract.py
- [ ] T015 [US1] Implement schema validation (required columns check) in src/extract.py
- [ ] T016 [US1] Implement file hash computation (SHA-256) for duplicate detection in src/extract.py
- [ ] T017 [US1] Implement row-level data type validation in src/transform.py
- [ ] T018 [US1] Implement date format normalization (YYYY-MM-DD and MM/DD/YYYY) in src/transform.py
- [ ] T019 [US1] Implement numeric range validation (exit_velocity 0-130, launch_angle -90 to 90) in src/transform.py
- [ ] T020 [US1] Implement validation error collection with row/column details in src/transform.py
- [ ] T021 [US1] Implement player upsert (create if not exists) in src/load.py
- [ ] T022 [US1] Implement practice_session upsert (create if not exists) in src/load.py
- [ ] T023 [US1] Implement batting_records bulk insert with transaction in src/load.py
- [ ] T024 [US1] Implement upload_logs recording (filename, hash, status, counts) in src/load.py
- [ ] T025 [US1] Implement duplicate file detection using file_hash lookup in src/load.py
- [ ] T026 [US1] Implement main pipeline orchestration (extract → transform → load) in src/pipeline.py
- [ ] T027 [US1] Implement process CLI command with --dry-run, --verbose, --force options in src/pipeline.py
- [ ] T028 [US1] Implement validate CLI command for validation-only mode in src/pipeline.py
- [ ] T029 [US1] Implement status CLI command to show recent upload_logs in src/pipeline.py
- [ ] T030 [US1] Add comprehensive logging throughout pipeline operations in src/pipeline.py
- [ ] T031 [US1] Implement exit codes per CLI contract (0=success, 1=partial, 2=failed, etc.) in src/pipeline.py

**Checkpoint**: User Story 1 complete - pipeline processes Excel files and stores validated data in MySQL

---

## Phase 4: User Story 2 - View Key Performance Metrics (Priority: P2)

**Goal**: Looker Studio dashboard homepage with KPI cards showing team metrics

**Independent Test**: Open Looker Studio dashboard and verify KPI cards display average exit velocity, hard-hit %, average launch angle

**Note**: This phase involves Looker Studio configuration, not Python code. Tasks document the dashboard setup steps.

### Implementation for User Story 2

- [ ] T032 [US2] Create Looker Studio data source connected to MySQL database
- [ ] T033 [US2] Create KPI scorecard for Average Exit Velocity using session_metrics_summary view
- [ ] T034 [US2] Create KPI scorecard for Hard-Hit Percentage using player_metrics_summary view
- [ ] T035 [US2] Create KPI scorecard for Average Launch Angle using session_metrics_summary view
- [ ] T036 [US2] Add trend sparklines or comparison indicators to KPI cards
- [ ] T037 [US2] Add metric tooltips/descriptions explaining each KPI (e.g., "Hard-Hit %: Exit velocity ≥ 95 mph")
- [ ] T038 [US2] Configure dashboard auto-refresh to reflect new data uploads

**Checkpoint**: User Story 2 complete - coaches can view team KPIs on dashboard homepage

---

## Phase 5: User Story 3 - Player Performance Profiles (Priority: P3)

**Goal**: Individual player drill-down views showing personal metrics and trends

**Independent Test**: Select a player from dropdown and verify individual metrics, trend chart, and drill-type breakdown display

### Implementation for User Story 3

- [ ] T039 [US3] Create player dropdown/selector control in Looker Studio
- [ ] T040 [US3] Create player profile section with individual metrics (EV, LA, hard-hit %, quality distribution)
- [ ] T041 [US3] Create trend line chart showing player metrics over time (by session_date)
- [ ] T042 [US3] Create drill-type filter to segment metrics by Tee Work, Live BP, Soft Toss
- [ ] T043 [US3] Create quality-of-contact distribution chart (pie or bar) for selected player

**Checkpoint**: User Story 3 complete - coaches can view individual player performance profiles

---

## Phase 6: User Story 4 - Compare Players Side-by-Side (Priority: P4)

**Goal**: Multi-player comparison view for lineup decisions

**Independent Test**: Select 2-3 players and verify side-by-side metric comparison displays with highlighting

### Implementation for User Story 4

- [ ] T044 [US4] Create multi-select player control allowing 2-5 player selection
- [ ] T045 [US4] Create comparison table showing all players' metrics in aligned columns
- [ ] T046 [US4] Add conditional formatting to highlight best values in each metric
- [ ] T047 [US4] Enable PDF/image export for comparison view

**Checkpoint**: User Story 4 complete - coaches can compare multiple players for lineup decisions

---

## Phase 7: User Story 5 - Filter by Date and Session (Priority: P5)

**Goal**: Date range and session filtering across all dashboard views

**Independent Test**: Apply date filter and verify all charts/KPIs update to show only filtered data

### Implementation for User Story 5

- [ ] T048 [US5] Create date range picker control in Looker Studio
- [ ] T049 [US5] Create practice session dropdown filter
- [ ] T050 [US5] Connect filters to all dashboard components (KPIs, charts, tables)
- [ ] T051 [US5] Add "Clear Filters" / "Reset" button to return to all-data view

**Checkpoint**: User Story 5 complete - coaches can filter dashboard by date/session

---

## Phase 8: User Story 6 - Practice-to-Game Correlation Insights (Priority: P6)

**Goal**: Callout boxes correlating practice trends with game performance

**Independent Test**: View player with improved practice metrics and verify correlation callout appears

**Note**: Requires game data from The PAW site. This phase may be deferred if game data integration is not yet available.

### Implementation for User Story 6

- [ ] T052 [US6] Design game_stats table schema for PAW site data in data/schema.sql
- [ ] T053 [US6] Create manual game data import process or API integration
- [ ] T054 [US6] Create correlation query joining practice trends with game stats
- [ ] T055 [US6] Create callout text box component showing correlation insights
- [ ] T056 [US6] Implement logic to surface meaningful correlations (e.g., "EV increase → higher slugging %")

**Checkpoint**: User Story 6 complete - coaches see practice-to-game correlation insights

---

## Phase 9: Automation & Polish

**Purpose**: GitHub Actions automation and final improvements

- [ ] T057 Create GitHub Actions workflow file at .github/workflows/pipeline.yml
- [ ] T058 Configure workflow with schedule trigger (cron) and manual dispatch
- [ ] T059 Add GitHub Secrets documentation for DB_HOST, DB_USER, DB_PASSWORD, DB_NAME
- [ ] T060 [P] Update README.md with project overview, setup instructions, and usage examples
- [ ] T061 [P] Validate quickstart.md instructions work end-to-end
- [ ] T062 [P] Create coach user guide for Looker Studio dashboard
- [ ] T063 Review and ensure all Constitution principles are satisfied in implementation

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Story 1 (Phase 3)**: Depends on Foundational - MVP target
- **User Stories 2-6 (Phases 4-8)**: Depend on US1 (need data in database)
- **Automation & Polish (Phase 9)**: Can start after US1; complete after all stories

### User Story Dependencies

```
Phase 1: Setup
    ↓
Phase 2: Foundational (database, config, models)
    ↓
Phase 3: US1 - Automated Data Upload (MVP - pipeline works)
    ↓
    ├── Phase 4: US2 - KPI Dashboard (needs data from US1)
    │       ↓
    │   Phase 5: US3 - Player Profiles (builds on US2 dashboard)
    │       ↓
    │   Phase 6: US4 - Player Comparison (builds on US3 profiles)
    │       ↓
    │   Phase 7: US5 - Date Filtering (enhances all views)
    │       ↓
    │   Phase 8: US6 - Correlation Insights (advanced feature)
    ↓
Phase 9: Automation & Polish
```

### Within Each User Story

1. Models/schema before services
2. Core logic before CLI commands
3. Main functionality before edge cases
4. Logging and error handling integrated throughout

### Parallel Opportunities

- **Phase 1**: T003, T004, T005, T006 can all run in parallel
- **Phase 2**: T010, T011 can run in parallel with T007-T009
- **Phase 3**: Extract (T014-T016), Transform (T017-T020), Load (T021-T025) are sequential
- **Phases 4-8**: Dashboard tasks within each phase are mostly sequential (Looker Studio)
- **Phase 9**: T060, T061, T062 can run in parallel

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational
3. Complete Phase 3: User Story 1 (Automated Data Upload)
4. **STOP and VALIDATE**: Process sample file, verify data in MySQL
5. Demo to stakeholders - pipeline is functional!

### Incremental Delivery

1. **Week 1-2**: Setup + Foundational + US1 → MVP pipeline working
2. **Week 3-4**: US2 + US3 → Basic dashboard with KPIs and player profiles
3. **Week 5-6**: US4 + US5 → Comparison and filtering features
4. **Week 7-8**: US6 + Polish → Correlation insights and automation

### Suggested MVP Scope

**Minimum Viable Product = Phases 1-3 (Tasks T001-T031)**

This delivers:
- Working ETL pipeline
- Excel file validation
- MySQL database storage
- CLI commands (process, validate, status, init-db)
- Logging and error handling

Coaches can then manually query MySQL or wait for dashboard phases.

---

## Summary

| Phase | User Story | Tasks | Parallel Tasks |
|-------|------------|-------|----------------|
| 1 | Setup | T001-T006 | 4 |
| 2 | Foundational | T007-T013 | 2 |
| 3 | US1 - Data Upload | T014-T031 | 0 (sequential) |
| 4 | US2 - KPI Dashboard | T032-T038 | 0 |
| 5 | US3 - Player Profiles | T039-T043 | 0 |
| 6 | US4 - Player Comparison | T044-T047 | 0 |
| 7 | US5 - Date Filtering | T048-T051 | 0 |
| 8 | US6 - Correlations | T052-T056 | 0 |
| 9 | Polish | T057-T063 | 3 |
| **Total** | | **63 tasks** | **9 parallel** |

---

## Notes

- [P] tasks = different files, no dependencies
- [USn] label maps task to specific user story for traceability
- Each user story is independently testable after completion
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Dashboard tasks (US2-US6) are Looker Studio configuration, not Python code
