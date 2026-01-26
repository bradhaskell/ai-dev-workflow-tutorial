# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Purpose

This repository serves two purposes:
1. **Educational Tutorial**: Teaching AI-assisted development workflows using a Streamlit e-commerce dashboard
2. **LMU Baseball Project**: Real-world data pipeline and analytics dashboard for LMU Baseball coaching staff

## Project Structure

```
docs/                    - Tutorial documentation (read in numbered order: 00-overview → 01-session-1-setup → etc.)
prd/
  ecommerce-analytics.md - PRD for e-commerce tutorial dashboard
  lmu-baseball-analytics.md - PRD for LMU Baseball data pipeline & dashboard
data/
  sales-data.csv         - Sample e-commerce data (482 orders, 5 categories, 4 regions)
  schema.sql             - MySQL schema for LMU Baseball database
  sample_batting_practice.csv/xlsx - Sample batting practice data
.specify/
  templates/             - spec-kit templates (spec, plan, tasks, checklist)
  scripts/               - PowerShell automation scripts
  memory/                - Project constitution and context
```

## Projects

### E-Commerce Tutorial (ECOM)
Students create a Streamlit dashboard with:
- 2 KPI scorecards (Total Sales ~$650-700K, Total Orders 482)
- Line chart for sales trend over time
- Bar charts for sales by category and region

**Tech stack**: Python 3.11+, Streamlit, Plotly, Pandas
**Jira key**: `ECOM`

### LMU Baseball Analytics
Automated data pipeline and Looker dashboard for coaching staff:
- Excel → MySQL automated ETL pipeline
- Practice performance dashboard (exit velocity, launch angle, hard-hit %)
- Player comparisons and trend analysis

**Tech stack**: Python, pandas, sqlalchemy, pymysql, MySQL, Looker Studio, GitHub Actions
**Database schema**: See `data/schema.sql`

## Workflow

```
PRD → spec-kit → Jira → Code → Commit → Push → Deploy
```

Key conventions:
- Commit format: `PROJECT-#: description` (e.g., `ECOM-1: Add KPI cards`)
- All commits should link to Jira issues for traceability

## When Helping

1. **Identify the project context** - Check which PRD is relevant to the request
2. Follow the spec-driven approach: understand requirements before coding
3. Reference the appropriate PRD for requirements and data specifications
4. For e-commerce: Keep to Phase 1 scope (no auth, no database, no filtering)
5. For baseball: Follow the MySQL schema in `data/schema.sql`
