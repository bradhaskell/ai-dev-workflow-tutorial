# Quickstart: LMU Baseball Practice Data Pipeline

**Feature**: 001-baseball-pipeline
**Date**: 2026-01-24

## Prerequisites

- Python 3.11 or higher
- Access to LMU MySQL database (credentials from IT)
- Git installed

## Setup (5 minutes)

### 1. Clone and Enter Repository

```bash
git clone https://github.com/bradhaskell/ai-dev-workflow-tutorial.git
cd ai-dev-workflow-tutorial
```

### 2. Create Virtual Environment

**Windows (PowerShell)**:
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Mac/Linux**:
```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your database credentials
# Required values:
#   DB_HOST=your-mysql-host
#   DB_USER=your-username
#   DB_PASSWORD=your-password
#   DB_NAME=lmu_baseball
```

### 5. Initialize Database (First Time Only)

```bash
python -m src.pipeline init-db
```

Expected output:
```
Initializing database schema...
Creating table: players... OK
Creating table: practice_sessions... OK
Creating table: batting_records... OK
Creating table: upload_logs... OK
Creating views... OK
Schema initialization complete.
```

## Usage

### Process a Batting Practice File

```bash
python -m src.pipeline process data/sample_batting_practice.xlsx
```

Expected output:
```
Processing: sample_batting_practice.xlsx
Validating rows... 150 valid, 0 invalid
Inserting records... done
Summary:
  - Rows processed: 150
  - Rows rejected: 0
  - New players created: 5
  - Status: success
```

### Validate Without Uploading

```bash
python -m src.pipeline validate data/sample_batting_practice.xlsx
```

### Check Pipeline Status

```bash
python -m src.pipeline status
```

## Excel File Format

Your batting practice Excel files must have these columns:

| Column | Required | Example |
|--------|----------|---------|
| date | Yes | 2026-01-24 or 01/24/2026 |
| player_name | Yes | John Smith |
| drill_type | No | Live BP, Tee Work, Soft Toss |
| exit_velocity | Yes | 95.5 |
| launch_angle | No | 12.3 |
| distance | No | 385 |
| hard_hit_percentage | No | 45.0 |
| quality_of_contact | No | Hard, Medium, Weak |

## Troubleshooting

### "Database connection failed"

1. Check your `.env` file has correct credentials
2. Verify MySQL server is running
3. Confirm your IP is allowed to connect (check with LMU IT)

### "Required column missing"

Your Excel file is missing a required column. Check that it has at least:
- date
- player_name
- exit_velocity

### "File already processed"

The pipeline prevents duplicate uploads. If you need to re-upload:
```bash
python -m src.pipeline process file.xlsx --force
```

### Virtual Environment Issues

If `pip install` fails, ensure you're in the virtual environment:
```bash
# Check if activated (should show venv path)
which python  # Mac/Linux
where python  # Windows
```

## Next Steps

1. **View Data in Looker Studio**: Ask the team for the dashboard link
2. **Schedule Automated Runs**: See `.github/workflows/pipeline.yml`
3. **Process Real Data**: Replace sample file with actual practice files

## Getting Help

- Check pipeline logs: `python -m src.pipeline status`
- Review documentation: `specs/001-baseball-pipeline/`
- Contact: Bradley or Beckett
