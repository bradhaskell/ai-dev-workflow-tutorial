# Data Model: LMU Baseball Practice Data Pipeline

**Feature**: 001-baseball-pipeline
**Date**: 2026-01-24
**Status**: Complete

## Entity Relationship Diagram

```
┌─────────────────┐       ┌─────────────────────┐
│     players     │       │   practice_sessions │
├─────────────────┤       ├─────────────────────┤
│ id (PK)         │       │ id (PK)             │
│ name            │       │ session_date        │
│ created_at      │       │ created_at          │
│ updated_at      │       │ notes               │
└────────┬────────┘       └──────────┬──────────┘
         │                           │
         │         ┌─────────────────┘
         │         │
         ▼         ▼
┌─────────────────────────────────────┐
│           batting_records           │
├─────────────────────────────────────┤
│ id (PK)                             │
│ player_id (FK → players)            │
│ session_id (FK → practice_sessions) │
│ drill_type                          │
│ exit_velocity                       │
│ launch_angle                        │
│ distance                            │
│ hard_hit_percentage                 │
│ quality_of_contact                  │
│ created_at                          │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│           upload_logs               │
├─────────────────────────────────────┤
│ id (PK)                             │
│ filename                            │
│ file_hash                           │
│ status                              │
│ rows_processed                      │
│ rows_rejected                       │
│ error_details                       │
│ processed_at                        │
└─────────────────────────────────────┘
```

## Table Definitions

### players

Stores unique player information. Players are identified by exact name match from Excel files.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INT | PRIMARY KEY, AUTO_INCREMENT | Unique identifier |
| name | VARCHAR(100) | NOT NULL, UNIQUE | Player's full name (exact match) |
| created_at | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Record creation time |
| updated_at | DATETIME | ON UPDATE CURRENT_TIMESTAMP | Last modification time |

**Indexes**:
- PRIMARY KEY (id)
- UNIQUE INDEX idx_players_name (name)

### practice_sessions

Stores unique practice session dates. One session per date.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INT | PRIMARY KEY, AUTO_INCREMENT | Unique identifier |
| session_date | DATE | NOT NULL, UNIQUE | Practice date (YYYY-MM-DD) |
| created_at | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Record creation time |
| notes | TEXT | NULL | Optional session notes |

**Indexes**:
- PRIMARY KEY (id)
- UNIQUE INDEX idx_sessions_date (session_date)

### batting_records

Stores individual batting practice metrics. Each record represents one swing/rep.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INT | PRIMARY KEY, AUTO_INCREMENT | Unique identifier |
| player_id | INT | NOT NULL, FOREIGN KEY → players(id) | Link to player |
| session_id | INT | NOT NULL, FOREIGN KEY → practice_sessions(id) | Link to session |
| drill_type | VARCHAR(50) | NULL | Drill category (Tee Work, Live BP, Soft Toss) |
| exit_velocity | DECIMAL(5,2) | NOT NULL | Ball speed off bat in mph (0-130) |
| launch_angle | DECIMAL(5,2) | NULL | Vertical angle in degrees (-90 to 90) |
| distance | INT | NULL | Projected distance in feet (0-600) |
| hard_hit_percentage | DECIMAL(5,2) | NULL | Hard-hit % for session (0-100) |
| quality_of_contact | VARCHAR(20) | NULL | Contact quality (Weak, Medium, Hard) |
| created_at | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Record creation time |

**Indexes**:
- PRIMARY KEY (id)
- INDEX idx_records_player (player_id)
- INDEX idx_records_session (session_id)
- INDEX idx_records_drill (drill_type)
- COMPOSITE INDEX idx_records_player_session (player_id, session_id)

**Foreign Keys**:
- player_id REFERENCES players(id) ON DELETE RESTRICT
- session_id REFERENCES practice_sessions(id) ON DELETE RESTRICT

### upload_logs

Tracks pipeline execution history for monitoring and duplicate detection.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INT | PRIMARY KEY, AUTO_INCREMENT | Unique identifier |
| filename | VARCHAR(255) | NOT NULL | Original Excel filename |
| file_hash | CHAR(64) | NOT NULL, UNIQUE | SHA-256 hash of file contents |
| status | ENUM('success', 'partial', 'failed') | NOT NULL | Upload result status |
| rows_processed | INT | NOT NULL, DEFAULT 0 | Count of successfully inserted rows |
| rows_rejected | INT | NOT NULL, DEFAULT 0 | Count of rejected invalid rows |
| error_details | TEXT | NULL | JSON array of error messages |
| processed_at | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Processing timestamp |

**Indexes**:
- PRIMARY KEY (id)
- UNIQUE INDEX idx_logs_hash (file_hash)
- INDEX idx_logs_status (status)
- INDEX idx_logs_processed_at (processed_at)

## Validation Rules

### Field-Level Validation

| Field | Required | Type | Range/Format | Default |
|-------|----------|------|--------------|---------|
| date | Yes | DATE | YYYY-MM-DD or MM/DD/YYYY | - |
| player_name | Yes | VARCHAR | Non-empty, max 100 chars | - |
| drill_type | No | VARCHAR | Tee Work, Live BP, Soft Toss, or NULL | NULL |
| exit_velocity | Yes | DECIMAL | 0.00 - 130.00 | - |
| launch_angle | No | DECIMAL | -90.00 - 90.00 | NULL |
| distance | No | INT | 0 - 600 | NULL |
| hard_hit_percentage | No | DECIMAL | 0.00 - 100.00 | NULL |
| quality_of_contact | No | VARCHAR | Weak, Medium, Hard, or NULL | NULL |

### Business Rules

1. **Player Creation**: If player_name doesn't exist in players table, create new player record automatically
2. **Session Creation**: If session_date doesn't exist in practice_sessions table, create new session record automatically
3. **Duplicate Prevention**: File with same SHA-256 hash cannot be processed twice
4. **Partial Success**: Valid rows are inserted even if some rows fail validation
5. **Atomic Transactions**: All inserts for a single file succeed or fail together (excluding validation failures)

## State Transitions

### Upload Status

```
┌─────────┐
│ pending │ (file detected, not yet processed)
└────┬────┘
     │
     ▼
┌─────────────────────────────────────────────┐
│              PROCESSING                      │
│  - Read Excel file                          │
│  - Validate rows                            │
│  - Insert valid records                     │
└─────────────────────────────────────────────┘
     │
     ├──────────────┬──────────────┐
     │              │              │
     ▼              ▼              ▼
┌─────────┐   ┌─────────┐   ┌─────────┐
│ success │   │ partial │   │ failed  │
│(all ok) │   │(some ok)│   │(none ok)│
└─────────┘   └─────────┘   └─────────┘
```

### Status Definitions

- **success**: All rows validated and inserted successfully
- **partial**: Some rows inserted, some rejected due to validation errors
- **failed**: No rows inserted (file-level error or all rows invalid)

## Sample Data

### Input Excel Row

| date | player_name | drill_type | exit_velocity | launch_angle | distance | hard_hit_percentage | quality_of_contact |
|------|-------------|------------|---------------|--------------|----------|--------------------|--------------------|
| 2026-01-24 | John Smith | Live BP | 95.5 | 12.3 | 385 | 45.0 | Hard |

### Resulting Database Records

**players**:
| id | name | created_at |
|----|------|------------|
| 1 | John Smith | 2026-01-24 10:30:00 |

**practice_sessions**:
| id | session_date | created_at |
|----|--------------|------------|
| 1 | 2026-01-24 | 2026-01-24 10:30:00 |

**batting_records**:
| id | player_id | session_id | drill_type | exit_velocity | launch_angle | distance | hard_hit_percentage | quality_of_contact |
|----|-----------|------------|------------|---------------|--------------|----------|--------------------|--------------------|
| 1 | 1 | 1 | Live BP | 95.50 | 12.30 | 385 | 45.00 | Hard |

## Database Views (for Looker Studio)

### player_metrics_summary

Aggregated metrics per player across all sessions.

```sql
CREATE VIEW player_metrics_summary AS
SELECT
    p.id AS player_id,
    p.name AS player_name,
    COUNT(br.id) AS total_swings,
    ROUND(AVG(br.exit_velocity), 2) AS avg_exit_velocity,
    ROUND(AVG(br.launch_angle), 2) AS avg_launch_angle,
    ROUND(AVG(br.distance), 0) AS avg_distance,
    ROUND(AVG(br.hard_hit_percentage), 2) AS avg_hard_hit_pct,
    MIN(ps.session_date) AS first_session,
    MAX(ps.session_date) AS last_session
FROM players p
JOIN batting_records br ON p.id = br.player_id
JOIN practice_sessions ps ON br.session_id = ps.id
GROUP BY p.id, p.name;
```

### session_metrics_summary

Aggregated metrics per practice session.

```sql
CREATE VIEW session_metrics_summary AS
SELECT
    ps.id AS session_id,
    ps.session_date,
    COUNT(DISTINCT br.player_id) AS players_count,
    COUNT(br.id) AS total_swings,
    ROUND(AVG(br.exit_velocity), 2) AS avg_exit_velocity,
    ROUND(AVG(br.launch_angle), 2) AS avg_launch_angle,
    ROUND(AVG(br.distance), 0) AS avg_distance
FROM practice_sessions ps
JOIN batting_records br ON ps.id = br.session_id
GROUP BY ps.id, ps.session_date;
```

### recent_upload_status

Recent pipeline executions for monitoring.

```sql
CREATE VIEW recent_upload_status AS
SELECT
    filename,
    status,
    rows_processed,
    rows_rejected,
    processed_at,
    CASE
        WHEN status = 'failed' THEN error_details
        ELSE NULL
    END AS error_summary
FROM upload_logs
ORDER BY processed_at DESC
LIMIT 50;
```
