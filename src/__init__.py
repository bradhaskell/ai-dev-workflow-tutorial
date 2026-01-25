"""
LMU Baseball Practice Data Pipeline

This package provides an automated ETL pipeline for processing batting practice
Excel files, validating data, and storing metrics in MySQL for visualization
in Looker Studio.

Modules:
    extract: Excel file reading and initial parsing
    transform: Data validation, cleaning, and normalization
    load: Database operations with transaction support
    pipeline: Main orchestration and CLI commands
    config: Configuration and environment variable handling
    models: SQLAlchemy ORM models
"""

__version__ = "0.1.0"
__author__ = "LMU Baseball Analytics Team"
