# CLI Contract: Baseball Pipeline

**Feature**: 001-baseball-pipeline
**Date**: 2026-01-24
**Status**: Complete

## Overview

The pipeline is executed via command-line interface. This document specifies the commands, arguments, and expected behavior.

## Commands

### process

Process an Excel file and upload to the database.

**Usage**:
```bash
python -m src.pipeline process <file_path> [options]
```

**Arguments**:
| Argument | Required | Description |
|----------|----------|-------------|
| file_path | Yes | Path to Excel file (.xlsx) |

**Options**:
| Option | Short | Default | Description |
|--------|-------|---------|-------------|
| --dry-run | -n | false | Validate only, don't insert to database |
| --verbose | -v | false | Enable detailed logging output |
| --force | -f | false | Process even if file hash exists (re-upload) |

**Exit Codes**:
| Code | Meaning |
|------|---------|
| 0 | Success - all rows processed |
| 1 | Partial success - some rows rejected |
| 2 | Failure - no rows processed |
| 3 | Error - file not found or unreadable |
| 4 | Error - database connection failed |
| 5 | Error - duplicate file (use --force to override) |

**Output (stdout)**:
```
Processing: batting_practice_2026-01-24.xlsx
Validating rows... 150 valid, 3 invalid
Inserting records... done
Summary:
  - Rows processed: 150
  - Rows rejected: 3
  - New players created: 2
  - Status: partial
```

**Errors (stderr)**:
```
ERROR: Row 45 - exit_velocity must be numeric, got 'abc'
ERROR: Row 67 - player_name is required
ERROR: Row 89 - date format not recognized: '1/24/26'
```

### validate

Validate an Excel file without uploading.

**Usage**:
```bash
python -m src.pipeline validate <file_path> [options]
```

**Arguments**:
| Argument | Required | Description |
|----------|----------|-------------|
| file_path | Yes | Path to Excel file (.xlsx) |

**Options**:
| Option | Short | Default | Description |
|--------|-------|---------|-------------|
| --verbose | -v | false | Show all validation details |

**Exit Codes**:
| Code | Meaning |
|------|---------|
| 0 | Valid - all rows pass validation |
| 1 | Invalid - some rows have errors |
| 3 | Error - file not found or unreadable |

**Output (stdout)**:
```
Validating: batting_practice_2026-01-24.xlsx
Schema check... OK
Row validation...
  - Total rows: 153
  - Valid rows: 150
  - Invalid rows: 3
Result: INVALID (see errors below)
```

### status

Check recent pipeline execution status.

**Usage**:
```bash
python -m src.pipeline status [options]
```

**Options**:
| Option | Short | Default | Description |
|--------|-------|---------|-------------|
| --limit | -l | 10 | Number of recent uploads to show |
| --format | | table | Output format: table, json |

**Exit Codes**:
| Code | Meaning |
|------|---------|
| 0 | Success |
| 4 | Error - database connection failed |

**Output (table format)**:
```
Recent Uploads (last 10):
+----------------------------+------------------+--------+-----------+----------+
| Filename                   | Processed At     | Status | Processed | Rejected |
+----------------------------+------------------+--------+-----------+----------+
| bp_2026-01-24.xlsx         | 2026-01-24 10:30 | success| 150       | 0        |
| bp_2026-01-23.xlsx         | 2026-01-23 11:15 | partial| 145       | 5        |
| bp_2026-01-22.xlsx         | 2026-01-22 09:45 | failed | 0         | 0        |
+----------------------------+------------------+--------+-----------+----------+
```

**Output (json format)**:
```json
{
  "uploads": [
    {
      "filename": "bp_2026-01-24.xlsx",
      "processed_at": "2026-01-24T10:30:00",
      "status": "success",
      "rows_processed": 150,
      "rows_rejected": 0
    }
  ]
}
```

### init-db

Initialize database schema (one-time setup).

**Usage**:
```bash
python -m src.pipeline init-db [options]
```

**Options**:
| Option | Short | Default | Description |
|--------|-------|---------|-------------|
| --drop | | false | Drop existing tables before creating (DESTRUCTIVE) |

**Exit Codes**:
| Code | Meaning |
|------|---------|
| 0 | Success - schema created |
| 4 | Error - database connection failed |
| 6 | Error - tables already exist (use --drop to override) |

**Output (stdout)**:
```
Initializing database schema...
Creating table: players... OK
Creating table: practice_sessions... OK
Creating table: batting_records... OK
Creating table: upload_logs... OK
Creating views... OK
Schema initialization complete.
```

## Environment Variables

Required environment variables for database connection:

| Variable | Required | Description | Example |
|----------|----------|-------------|---------|
| DB_HOST | Yes | MySQL server hostname | localhost |
| DB_PORT | No | MySQL server port (default: 3306) | 3306 |
| DB_USER | Yes | Database username | pipeline_user |
| DB_PASSWORD | Yes | Database password | (secret) |
| DB_NAME | Yes | Database name | lmu_baseball |
| LOG_LEVEL | No | Logging level (default: INFO) | DEBUG |

## Example Usage

### Local Development

```bash
# Setup virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt

# Copy environment template
cp .env.example .env
# Edit .env with your database credentials

# Initialize database (first time only)
python -m src.pipeline init-db

# Validate a file
python -m src.pipeline validate data/sample_batting_practice.xlsx

# Process a file
python -m src.pipeline process data/sample_batting_practice.xlsx --verbose

# Check status
python -m src.pipeline status --limit 5
```

### GitHub Actions

```yaml
# .github/workflows/pipeline.yml
- name: Process batting practice data
  env:
    DB_HOST: ${{ secrets.DB_HOST }}
    DB_USER: ${{ secrets.DB_USER }}
    DB_PASSWORD: ${{ secrets.DB_PASSWORD }}
    DB_NAME: ${{ secrets.DB_NAME }}
  run: |
    python -m src.pipeline process ${{ github.event.inputs.file_path }}
```

## Error Messages

### Validation Errors

| Error | Cause | Resolution |
|-------|-------|------------|
| "Required column missing: {column}" | Excel file missing expected column | Add column to Excel file |
| "Row {n}: {field} must be numeric" | Non-numeric value in numeric field | Fix data in Excel file |
| "Row {n}: {field} is required" | Empty value in required field | Fill in required value |
| "Row {n}: date format not recognized" | Date not in YYYY-MM-DD or MM/DD/YYYY | Fix date format |
| "Row {n}: {field} out of range" | Value outside valid range | Fix value to be within range |

### System Errors

| Error | Cause | Resolution |
|-------|-------|------------|
| "Database connection failed" | Cannot connect to MySQL | Check credentials and network |
| "File not found" | Excel file doesn't exist | Check file path |
| "File already processed" | Duplicate file hash detected | Use --force or skip file |
| "Permission denied" | Cannot read file | Check file permissions |
