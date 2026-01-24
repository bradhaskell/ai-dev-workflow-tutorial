<!--
=== Sync Impact Report ===
Version change: 0.0.0 → 1.0.0 (Initial ratification)
Modified principles: N/A (initial creation)
Added sections:
  - Core Principles (6 principles)
  - Technology Stack & Constraints
  - Development Workflow
  - Governance
Removed sections: N/A
Templates requiring updates:
  - .specify/templates/plan-template.md: ✅ No changes required (Constitution Check section compatible)
  - .specify/templates/spec-template.md: ✅ No changes required (user story format compatible)
  - .specify/templates/tasks-template.md: ✅ No changes required (phase structure compatible)
Follow-up TODOs: None
========================
-->

# LMU Baseball Practice Data Pipeline & Performance Dashboard Constitution

## Core Principles

### I. Data Integrity First

All data entering the system MUST be validated before storage. The pipeline MUST:
- Validate Excel file structure matches expected schema (date, player_name, drill_type, metrics)
- Reject rows with invalid data types (e.g., non-numeric exit velocity)
- Log all validation failures with specific row/column information
- Handle missing values according to defined rules (reject or default, never silently ignore)
- Prevent duplicate uploads of the same practice session

**Rationale**: Coaches rely on accurate metrics for lineup and strategy decisions. Invalid data leads to incorrect insights and erodes trust in the system.

### II. Robust Error Handling & Logging

Every pipeline operation MUST include comprehensive error handling and logging:
- All exceptions MUST be caught, logged with context, and handled gracefully
- Pipeline failures MUST NOT corrupt existing database state (use transactions)
- Logs MUST include timestamp, operation type, file processed, rows affected, and status
- Success and failure states MUST be clearly distinguishable in logs
- Critical failures MUST be surfaced (via log alerts or GitHub Actions notifications)

**Rationale**: Analysts need visibility into pipeline health. Silent failures lead to missing data and broken dashboards.

### III. Coach-Friendly Visualizations

Dashboard design MUST prioritize usability for non-technical coaches:
- Use clear, descriptive labels (not technical jargon or abbreviations)
- Provide context for metrics (e.g., "Hard-Hit %: Percentage of swings with exit velocity ≥ 95 mph")
- Ensure all visualizations load within 4 seconds
- Support intuitive filtering by date, player, and drill type
- Design for quick scanning: KPI cards for headline numbers, charts for trends

**Rationale**: The primary users are coaches, not analysts. Adoption depends on accessibility.

### IV. Clean, Maintainable Code

Python code MUST follow established best practices:
- Use type hints for function signatures
- Document functions with docstrings explaining purpose, parameters, and return values
- Keep functions focused and under 50 lines where practical
- Use meaningful variable names (e.g., `exit_velocity_avg` not `ev_a`)
- Follow PEP 8 style guidelines
- Organize code into logical modules: `extract.py`, `transform.py`, `load.py`

**Rationale**: This project may be maintained by future students or staff. Clean code reduces onboarding time and bug risk.

### V. Secure Credential Management

Database credentials and secrets MUST NEVER be:
- Hardcoded in source files
- Committed to version control
- Logged or printed to console

Credentials MUST be stored via:
- Environment variables for local development
- GitHub Secrets for GitHub Actions automation
- `.env` files (added to `.gitignore`) for local configuration

**Rationale**: Database access credentials protect LMU's data infrastructure. Leaked credentials create security vulnerabilities.

### VI. Environment Isolation

All development and execution MUST use isolated Python virtual environments:
- Use `venv` or `virtualenv` for dependency isolation
- Maintain `requirements.txt` with pinned versions for reproducibility
- Document setup steps in README or quickstart guide
- Never install project dependencies to system Python

**Rationale**: Isolated environments prevent dependency conflicts and ensure consistent behavior across machines (local dev, GitHub Actions, production).

## Technology Stack & Constraints

**Required Technologies**:
- **Language**: Python 3.11+
- **ETL Libraries**: pandas, sqlalchemy, pymysql, openpyxl
- **Database**: MySQL (LMU's existing server)
- **Dashboard**: Looker Studio (connected to MySQL)
- **Automation**: GitHub Actions
- **Version Control**: GitHub

**Performance Targets**:
- Pipeline MUST process typical practice files (50-200 rows) in under 30 seconds
- Dashboard MUST load within 4 seconds
- Pipeline success rate MUST exceed 95%

**Data Constraints**:
- Input: Excel files (.xlsx) with standardized column structure
- Supported metrics: exit_velocity, launch_angle, distance, hard_hit_percentage, quality_of_contact
- Date format: YYYY-MM-DD or MM/DD/YYYY (auto-detected and normalized)

## Development Workflow

**Branch Strategy**:
- Feature branches: `feature/ECOM-#-description` or `###-feature-name`
- Main branch: `main` (protected, requires review)
- Commit format: `ECOM-#: description`

**Code Quality Gates**:
- All pipeline code MUST include basic unit tests for validation logic
- Manual testing with sample data MUST pass before merging
- Code MUST be reviewed before deployment to production database

**Documentation Requirements**:
- README MUST include setup instructions and quickstart guide
- Data transformations MUST be documented in code comments or separate docs
- Dashboard MUST include user guide for coaches

**Testing Strategy**:
- Test with sample data before connecting to production MySQL
- Validate edge cases: empty files, missing columns, duplicate uploads
- Test dashboard filters and visualizations with realistic data volumes

## Governance

This constitution establishes the non-negotiable standards for the LMU Baseball Practice Data Pipeline & Performance Dashboard project. All contributors MUST adhere to these principles.

**Amendment Process**:
1. Propose changes via pull request with rationale
2. Review impact on existing code and documentation
3. Update version number according to semantic versioning
4. Document changes in Sync Impact Report

**Versioning Policy**:
- MAJOR: Principle removed or fundamentally redefined
- MINOR: New principle added or materially expanded
- PATCH: Clarifications, typo fixes, non-semantic refinements

**Compliance**:
- All pull requests MUST verify code complies with relevant principles
- Reviewers SHOULD check Constitution compliance as part of review
- Violations MUST be justified in code comments or PR description

**Version**: 1.0.0 | **Ratified**: 2026-01-24 | **Last Amended**: 2026-01-24
