# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Purpose

This is an educational tutorial repository for teaching AI-assisted development workflows. It guides students through building a Streamlit sales dashboard while learning professional tools (GitHub, Jira, spec-kit, Claude Code).

## Project Structure

- `docs/` - Tutorial documentation (read in numbered order: 00-overview → 01-session-1-setup → etc.)
- `prd/ecommerce-analytics.md` - Product Requirements Document for the dashboard project
- `data/sales-data.csv` - Sample e-commerce transaction data (482 orders, 5 categories, 4 regions)

## What Gets Built

Students create a Streamlit dashboard with:
- 2 KPI scorecards (Total Sales ~$650-700K, Total Orders 482)
- Line chart for sales trend over time
- Bar charts for sales by category and region

Tech stack: Python 3.11+, Streamlit, Plotly, Pandas

## Workflow Being Taught

```
PRD → spec-kit → Jira → Code → Commit → Push → Deploy (Streamlit Cloud)
```

Key conventions:
- Jira project key: `ECOM`
- Commit format: `ECOM-1: description`
- All commits should link to Jira issues for traceability

## When Helping Students

1. Follow the spec-driven approach: understand requirements before coding
2. Reference the PRD (`prd/ecommerce-analytics.md`) for dashboard requirements
3. Use the data specification in the PRD to understand CSV structure
4. Keep the dashboard to Phase 1 scope (no auth, no database, no filtering)
