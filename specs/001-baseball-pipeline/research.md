# Research: LMU Baseball Practice Data Pipeline

**Feature**: 001-baseball-pipeline
**Date**: 2026-01-24
**Status**: Complete

## Technology Decisions

### 1. Python ETL Framework

**Decision**: Use pandas + SQLAlchemy (no dedicated ETL framework like Airflow/Luigi)

**Rationale**:
- Simple single-file processing workflow doesn't require DAG orchestration
- pandas provides robust Excel reading via openpyxl and data manipulation
- SQLAlchemy provides database abstraction and transaction management
- Lower complexity aligns with Constitution Principle IV (Clean, Maintainable Code)
- Future maintainers (students/staff) more likely to know pandas than Airflow

**Alternatives Considered**:
- Apache Airflow: Overkill for single-step pipeline; adds operational complexity
- Luigi: Similar concerns; better suited for multi-step dependencies
- Raw Python + mysql-connector: Less robust than SQLAlchemy for transactions

### 2. Database Connection Strategy

**Decision**: SQLAlchemy with pymysql driver, connection pooling disabled

**Rationale**:
- SQLAlchemy provides ORM flexibility if needed, but allows raw SQL when simpler
- pymysql is pure Python (no C dependencies), easier to install across platforms
- Connection pooling unnecessary for batch job that runs and exits
- Transaction support critical for atomic uploads (Constitution Principle II)

**Alternatives Considered**:
- mysql-connector-python: Oracle-maintained but heavier; pymysql is lighter
- mysqlclient: Faster but requires MySQL C libraries (installation friction)
- Direct SQL without ORM: Loses transaction convenience and parameterized queries

### 3. Configuration Management

**Decision**: python-dotenv for environment variables with .env files

**Rationale**:
- Industry standard for 12-factor app configuration
- Seamless transition between local (.env file) and CI/CD (environment variables)
- Aligns with Constitution Principle V (Secure Credential Management)
- Simple setup with `load_dotenv()` in config module

**Alternatives Considered**:
- YAML/JSON config files: Risk of accidentally committing secrets
- OS environment only: Poor local development experience
- configparser: Less modern, doesn't integrate with shell environment

### 4. Logging Strategy

**Decision**: Python standard logging module with structured format

**Rationale**:
- Built-in, no additional dependencies
- Supports multiple handlers (console + file) for development and production
- Can output JSON format for future log aggregation if needed
- Constitution Principle II requires comprehensive logging

**Log Format**:
```
%(asctime)s | %(levelname)s | %(name)s | %(message)s
```

**Log Levels**:
- INFO: Successful operations (file processed, rows inserted)
- WARNING: Recoverable issues (duplicate file skipped, invalid row rejected)
- ERROR: Failures requiring attention (database connection failed, file read error)

**Alternatives Considered**:
- structlog: More features but additional dependency
- loguru: Popular but non-standard; harder for future maintainers
- print statements: Insufficient for production monitoring

### 5. Data Validation Approach

**Decision**: pandas-based validation in transform.py with explicit error collection

**Rationale**:
- Validate each row independently; collect all errors before failing
- Return both valid DataFrame and list of validation errors
- Allows partial success (valid rows proceed, invalid logged and skipped)
- Aligns with Constitution Principle I (Data Integrity First)

**Validation Rules**:
| Field | Required | Type | Validation |
|-------|----------|------|------------|
| date | Yes | date | Parse as datetime; accept YYYY-MM-DD or MM/DD/YYYY |
| player_name | Yes | string | Non-empty after trim |
| drill_type | No | string | If present, must be in allowed list |
| exit_velocity | Yes | float | Numeric, range 0-130 mph |
| launch_angle | No | float | Numeric, range -90 to 90 degrees |
| distance | No | int | Numeric, range 0-600 feet |
| hard_hit_percentage | No | float | Numeric, range 0-100% |
| quality_of_contact | No | string | If present, must be Weak/Medium/Hard |

**Alternatives Considered**:
- Pydantic models: More robust but adds complexity for simple validation
- Great Expectations: Enterprise-grade but overkill for this scope
- SQL constraints only: Doesn't provide detailed error feedback

### 6. Duplicate Detection Strategy

**Decision**: Hash-based detection using file content hash + filename

**Rationale**:
- Compute SHA-256 hash of file contents
- Store hash in upload_logs table with filename and timestamp
- Check hash before processing; reject if already exists
- Prevents both exact duplicates and renamed duplicates

**Alternatives Considered**:
- Filename only: Doesn't catch renamed duplicates
- Database unique constraints: Doesn't prevent processing overhead
- Timestamp-based: Doesn't catch true duplicates uploaded at different times

### 7. GitHub Actions Workflow

**Decision**: Scheduled workflow with manual trigger option

**Rationale**:
- Cron schedule for automated daily/weekly runs
- workflow_dispatch for manual execution when needed
- Secrets stored in GitHub repository settings
- Ubuntu runner for consistency with production-like environment

**Workflow Triggers**:
- `schedule: cron: '0 6 * * *'` (daily at 6 AM UTC)
- `workflow_dispatch` (manual trigger via GitHub UI)

**Alternatives Considered**:
- Local cron only: No centralized execution or logging
- External scheduler (AWS Lambda, etc.): Adds infrastructure complexity
- Webhook-triggered: No external system to trigger from

### 8. Excel File Handling

**Decision**: openpyxl via pandas read_excel with explicit dtype handling

**Rationale**:
- openpyxl is pandas' recommended engine for .xlsx files
- Specify dtypes to prevent pandas from inferring incorrectly
- Handle both .xlsx (openpyxl) formats; reject .xls (legacy)
- Read specific sheet by name or index

**Alternatives Considered**:
- xlrd: Deprecated for .xlsx; only supports legacy .xls
- openpyxl directly: Loses pandas DataFrame convenience
- CSV export from Excel: Adds manual step for users

## Integration Points

### MySQL Database

**Connection String Format**:
```
mysql+pymysql://{user}:{password}@{host}:{port}/{database}
```

**Required Permissions**:
- SELECT, INSERT, UPDATE on practice data tables
- CREATE TABLE for initial schema setup (one-time)

### Looker Studio

**Integration Method**: Direct MySQL connection
- Looker Studio connects to MySQL using native connector
- No intermediate data warehouse needed
- Dashboard queries run against live data
- Refresh controlled by Looker Studio settings (auto or manual)

**Considerations**:
- Read-only access recommended for Looker service account
- Index tables on commonly filtered columns (date, player_name)

### The PAW Site (Game Data)

**Integration Method**: Manual data export or future API integration
- Initial release: Manual correlation by analysts
- Future enhancement: Automated import if API available
- Store game stats in separate table for correlation queries

## Performance Considerations

### Pipeline Performance

**Target**: Process 50-200 row files in <30 seconds

**Optimizations**:
- Bulk insert using pandas to_sql with chunksize
- Single transaction per file (not per row)
- Index on (date, player_name) for duplicate checks

### Dashboard Performance

**Target**: All visualizations load in <4 seconds

**Optimizations**:
- Pre-aggregate metrics in database views if needed
- Index on filter columns (date, player_name, drill_type)
- Limit date range in default dashboard view

## Security Considerations

### Credential Storage

| Environment | Storage Method |
|-------------|----------------|
| Local Development | .env file (in .gitignore) |
| GitHub Actions | Repository Secrets |
| Production Server | Environment variables |

### Database Access

- Use dedicated service account for pipeline
- Minimum required permissions only
- No admin/DDL permissions after initial setup
- Separate read-only account for Looker Studio

## Open Questions Resolved

| Question | Resolution |
|----------|------------|
| Which MySQL driver? | pymysql (pure Python, cross-platform) |
| How to handle partial failures? | Process valid rows, log invalid, continue |
| Duplicate detection method? | SHA-256 content hash |
| Scheduling mechanism? | GitHub Actions with cron |
| Configuration management? | python-dotenv with .env files |
