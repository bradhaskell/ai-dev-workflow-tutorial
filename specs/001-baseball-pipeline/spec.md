# Feature Specification: LMU Baseball Practice Data Pipeline & Performance Dashboard

**Feature Branch**: `001-baseball-pipeline`
**Created**: 2026-01-24
**Status**: Draft
**Input**: PRD: prd/lmu-baseball-analytics.md - Automated ETL pipeline, MySQL database integration, and Looker Studio dashboard for coaching staff

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Automated Data Upload (Priority: P1)

As a data analyst, I want to process Excel batting practice files automatically so that practice data flows into the database without manual cleaning or data entry.

**Why this priority**: This is the foundational capability that enables all other features. Without automated data ingestion, coaches cannot access any metrics through the dashboard. The PRD identifies reducing manual processing time by 80% as a primary business goal.

**Independent Test**: Can be fully tested by placing a sample Excel file in the input location and verifying the data appears correctly in the database with proper validation logging.

**Acceptance Scenarios**:

1. **Given** a valid Excel file with batting practice data in the expected format, **When** the pipeline processes the file, **Then** all rows are validated, cleaned, and stored in the database with a success log entry showing timestamp, filename, and row count.

2. **Given** an Excel file with some invalid data (e.g., non-numeric exit velocity, missing player names), **When** the pipeline processes the file, **Then** valid rows are stored, invalid rows are rejected, and the log clearly identifies which rows failed validation and why.

3. **Given** an Excel file that was previously uploaded, **When** the pipeline attempts to process the same file again, **Then** the system detects the duplicate and prevents re-upload, logging a warning message.

4. **Given** an Excel file with missing required columns, **When** the pipeline attempts to process it, **Then** the entire file is rejected with a clear error message identifying the missing columns.

---

### User Story 2 - View Key Performance Metrics (Priority: P2)

As a coach, I want to view a dashboard homepage with key batting practice KPIs so that I can quickly assess team and player performance without opening spreadsheets.

**Why this priority**: This delivers immediate value to the primary users (coaches) and represents the core dashboard functionality. The PRD targets 75% coach adoption, which depends on an intuitive entry point showing headline metrics.

**Independent Test**: Can be fully tested by loading the dashboard after data upload and verifying all KPI cards display accurate, current values with clear labels.

**Acceptance Scenarios**:

1. **Given** batting practice data exists in the database, **When** a coach opens the dashboard homepage, **Then** they see KPI cards showing average exit velocity, hard-hit percentage, and average launch angle for the most recent practice session.

2. **Given** multiple practice sessions exist, **When** a coach views the homepage, **Then** they see trend indicators (up/down arrows or sparklines) showing how current metrics compare to the previous session.

3. **Given** a coach wants to understand a metric, **When** they hover over or click on a KPI card label, **Then** they see a tooltip or description explaining the metric (e.g., "Hard-Hit %: Percentage of swings with exit velocity of 95 mph or higher").

4. **Given** the dashboard is accessed, **When** the page loads, **Then** all visualizations render completely within 4 seconds.

---

### User Story 3 - Player Performance Profiles (Priority: P3)

As a coach, I want to view individual player performance profiles so that I can track each hitter's development and make personalized training adjustments.

**Why this priority**: Player-level insights enable targeted coaching decisions. This builds on the homepage KPIs by allowing drill-down into individual performance, supporting the PRD goal of enabling 20% more data-informed decisions.

**Independent Test**: Can be fully tested by selecting a player from the dashboard and verifying their individual metrics, trends, and history display correctly.

**Acceptance Scenarios**:

1. **Given** a coach is on the dashboard, **When** they select a player from a list or dropdown, **Then** they see that player's individual metrics (exit velocity, launch angle, hard-hit %, quality distribution).

2. **Given** a player profile is displayed, **When** the coach views the performance section, **Then** they see a trend chart showing the player's metrics over time (across multiple practice sessions).

3. **Given** a player has data from multiple drill types, **When** viewing their profile, **Then** the coach can filter or segment metrics by drill type (Tee Work, Live BP, Soft Toss).

---

### User Story 4 - Compare Players Side-by-Side (Priority: P4)

As a coach, I want to compare multiple players' metrics side-by-side so that I can identify relative strengths and make lineup decisions.

**Why this priority**: Comparison tools support lineup and strategic decisions. This builds on individual profiles to enable relative analysis, directly supporting the coach goal of identifying trends and opportunities across the roster.

**Independent Test**: Can be fully tested by selecting two or more players and verifying their metrics display in a comparable format.

**Acceptance Scenarios**:

1. **Given** a coach is on the dashboard, **When** they select two or more players to compare, **Then** a comparison view displays their key metrics side-by-side in a table or chart format.

2. **Given** players are being compared, **When** the comparison loads, **Then** each metric shows the player names and values in aligned columns, with visual indicators highlighting the highest/best values.

3. **Given** a comparison view is displayed, **When** the coach wants to share it, **Then** they can export the comparison as a PDF or image for use in team meetings.

---

### User Story 5 - Filter by Date and Session (Priority: P5)

As a coach, I want to filter dashboard data by date range and practice session so that I can analyze specific time periods or sessions.

**Why this priority**: Filtering enables targeted analysis of specific practices or date ranges, supporting deeper investigation beyond headline metrics.

**Independent Test**: Can be fully tested by applying date filters and verifying that all dashboard metrics update to reflect only the filtered data.

**Acceptance Scenarios**:

1. **Given** the dashboard displays data, **When** a coach selects a date range filter, **Then** all metrics and visualizations update to show only data from practice sessions within that range.

2. **Given** multiple practice sessions exist, **When** a coach selects a specific session from a dropdown or calendar, **Then** the dashboard shows metrics for only that session.

3. **Given** filters are applied, **When** the coach clears or resets filters, **Then** the dashboard returns to showing all available data.

---

### User Story 6 - Practice-to-Game Correlation Insights (Priority: P6)

As a coach, I want to see callouts that correlate practice trends with game performance so that I can understand how practice translates to in-game results.

**Why this priority**: This represents an advanced feature that adds strategic value by connecting practice data with game outcomes. The PRD explicitly mentions correlation visualizations as a functional requirement.

**Independent Test**: Can be fully tested by verifying correlation callouts appear when practice trend data aligns with game performance data from The PAW site.

**Acceptance Scenarios**:

1. **Given** a player has shown improvement in practice metrics (e.g., increased exit velocity), **When** that player's profile is viewed, **Then** a callout box displays if corresponding game performance improved (e.g., "Player X's 8% EV increase aligns with higher slugging % in recent games").

2. **Given** correlation insights are displayed, **When** a coach views them, **Then** the callout clearly explains what practice metric is correlated with what game outcome, using plain language.

---

### Edge Cases

- **Empty Excel file**: System rejects file with clear error message ("File contains no data rows")
- **Partially empty rows**: System validates each row independently; rows with all required fields are processed, rows missing required fields are logged and skipped
- **Unexpected columns**: System ignores extra columns not in the expected schema and processes valid columns normally
- **Date format variations**: System auto-detects and normalizes dates in YYYY-MM-DD or MM/DD/YYYY formats; other formats are rejected with specific error
- **Duplicate player names**: System uses exact string matching for player identification; variations (e.g., "John Smith" vs "J. Smith") are treated as different players
- **Very large files**: System handles files up to 10,000 rows without performance degradation
- **Network failure during upload**: Database transaction rolls back completely; no partial data is stored; error is logged
- **Dashboard with no data**: Dashboard displays friendly "No practice data available" message instead of errors or blank charts

## Requirements *(mandatory)*

### Functional Requirements

**Data Pipeline**

- **FR-001**: System MUST accept Excel files (.xlsx) containing batting practice data with columns: date, player_name, drill_type, exit_velocity, launch_angle, distance, hard_hit_percentage, quality_of_contact
- **FR-002**: System MUST validate each row for data type correctness (numeric fields contain numbers, date fields contain valid dates)
- **FR-003**: System MUST reject rows where required fields (date, player_name, exit_velocity) are missing or invalid
- **FR-004**: System MUST log all processing activity including: timestamp, filename, rows processed, rows rejected, specific validation errors
- **FR-005**: System MUST prevent duplicate uploads by tracking processed files (by filename and content hash)
- **FR-006**: System MUST handle missing optional fields by storing null values (distance, hard_hit_percentage, quality_of_contact may be empty)
- **FR-007**: System MUST normalize date formats to a consistent internal format (YYYY-MM-DD)
- **FR-008**: System MUST use database transactions to ensure atomic uploads (all rows succeed or none are committed)

**Database**

- **FR-009**: System MUST store practice session records with unique identifiers linking date, player, and drill type
- **FR-010**: System MUST maintain referential integrity between players and their practice records
- **FR-011**: System MUST support querying by date range, player, and drill type efficiently
- **FR-012**: System MUST store all historical data without automatic deletion (data retention per LMU policies)

**Dashboard**

- **FR-013**: Dashboard MUST display KPI cards for: average exit velocity, hard-hit percentage, average launch angle
- **FR-014**: Dashboard MUST provide a player selection mechanism (dropdown or list) to view individual profiles
- **FR-015**: Dashboard MUST support player comparison with side-by-side metric display for 2-5 players
- **FR-016**: Dashboard MUST provide date range filtering affecting all visualizations
- **FR-017**: Dashboard MUST include trend visualizations (line charts) showing metric changes over time
- **FR-018**: Dashboard MUST include quality-of-contact distribution visualization (bar or pie chart)
- **FR-019**: Dashboard MUST allow exporting views as PDF or image files
- **FR-020**: Dashboard MUST display correlation callouts when practice trends align with game performance data

**Integration**

- **FR-021**: Pipeline MUST support both manual execution and automated scheduling via GitHub Actions
- **FR-022**: Dashboard MUST connect to the MySQL database and reflect data changes without manual refresh configuration
- **FR-023**: System MUST integrate with The PAW site data for game performance correlations (read-only access)

### Key Entities

- **Player**: Represents a team member; identified by full name; has multiple practice records over time
- **Practice Session**: A single practice event on a specific date; contains multiple swing records from multiple players
- **Swing Record**: Individual batting attempt data; linked to one player and one practice session; contains all measured metrics (exit velocity, launch angle, distance, etc.)
- **Drill Type**: Category of practice activity (Tee Work, Live BP, Soft Toss); each swing record is associated with one drill type
- **Upload Log**: Record of pipeline execution; tracks filename, timestamp, success/failure status, row counts, and error details

### Assumptions

- Excel files are provided by the coaching staff or analysts in the expected format (columns may vary in order but names are consistent)
- The PAW site provides read-only access to game performance data; the system does not modify game data
- Player names in Excel files match player names in any existing roster data; no automatic name matching or fuzzy lookup is required
- The MySQL database server is maintained by LMU IT and is available with appropriate credentials
- Coaches access the dashboard via web browser on desktop or laptop computers (mobile optimization is not required for initial release)
- Practice sessions occur regularly enough to generate meaningful trend data (at least weekly during season)

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Analysts can process a practice Excel file from upload to database storage in under 2 minutes (end-to-end, including validation)
- **SC-002**: Manual data processing time is reduced by 80% compared to pre-implementation baseline (measured by analyst time tracking)
- **SC-003**: Pipeline successfully processes 95% or more of valid Excel files without errors (measured over first month of operation)
- **SC-004**: Dashboard loads all visualizations within 4 seconds on standard network connection
- **SC-005**: 75% of coaching staff use the dashboard at least twice per week (measured via Looker usage logs)
- **SC-006**: 90% of coaches rate the dashboard as "easy to use" or better in end-of-season survey
- **SC-007**: Coaches report 20% increase in data-informed lineup/practice decisions (measured via qualitative feedback and meeting notes)
- **SC-008**: All validation errors are logged with sufficient detail to identify and fix source data issues within 5 minutes
- **SC-009**: Zero data corruption incidents occur due to pipeline failures (measured over project lifetime)
- **SC-010**: Player comparison feature allows coaches to compare up to 5 players simultaneously with all key metrics visible
