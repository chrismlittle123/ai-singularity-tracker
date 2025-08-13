# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

The AI Singularity Tracker monitors economic indicators to detect potential signals of AI-driven technological displacement. It tracks three key metrics:

- **Labor Share of Income** (quarterly FRED data)
- **Real GDP per Capita** (quarterly FRED data)  
- **Accountants Employment** (monthly Census CPS data)

The hypothesis: downward trends in labor share + accountants employment combined with upward real GDP trends over 1-3 year periods may signal AI-driven economic transformation.

## Architecture

### Data Pipeline Structure

**Two-stage pipeline:**
1. **Ingestion** (`src/pipeline/ingestion/`) - Downloads raw data from sources
2. **Processing** (`src/pipeline/processing/`) - Transforms into standardized format

**Smart data management:**
- Automatic detection of missing time periods
- Incremental fetching (only downloads missing data)
- FRED data: maintains last 14 quarters 
- CPS data: maintains last 36 months

### Directory Organization

```
data/
├── raw/           # Downloaded source data
└── processed/     # Standardized format (year,month columns)

src/pipeline/
├── utils.py       # Shared utilities (fetch_fred_data, trend analysis)
├── ingestion/     # Data download scripts  
└── processing/    # Data transformation scripts
```

## Common Development Commands

### Package Management (uv)
```bash
uv sync                    # Install dependencies
uv add <package>           # Add dependency
```

### Code Quality
```bash
uv run ruff check          # Lint code
uv run ruff format         # Format code
```

### Data Pipeline Execution
```bash
# Ingestion (downloads missing data automatically)
uv run python src/pipeline/ingestion/fetch_labor_share.py
uv run python src/pipeline/ingestion/fetch_real_gdp_per_capita.py  
uv run python src/pipeline/ingestion/fetch_accountants_employed.py

# Processing (transforms to standardized format)
uv run python src/pipeline/processing/process_labor_share.py
uv run python src/pipeline/processing/process_real_gdp_per_capita.py
uv run python src/pipeline/processing/process_accountants_employed.py
```

## Data Sources & Formats

### FRED Data (Labor Share, Real GDP)
- **Source**: Federal Reserve Economic Data CSV exports
- **Frequency**: Quarterly
- **Processing**: Uses `fetch_fred_data()` utility with automatic trend analysis
- **Output**: `year,month,<metric_name>` format

### CPS Data (Accountants Employment) 
- **Source**: Census Bureau Current Population Survey monthly files
- **URL Pattern**: `https://www2.census.gov/programs-surveys/cps/datasets/{year}/basic/{month}{year}pub.csv`
- **Filter**: Occupation code 800 (Accountants and Auditors)
- **Employment Status**: PEMLR field (1.0 = employed)
- **Output**: `year,month,employed_accountants,unemployed_accountants,total_accountants,employment_rate`

## Key Implementation Details

### Time Period Management
- **Current month excluded** from all data fetching
- **FRED scripts**: Automatically calculate past 14 quarters from current date
- **CPS script**: Automatically calculate past 36 months from current date
- **Missing data detection**: Scans existing files to avoid redundant downloads

### Error Handling
- Network timeouts and retries built into fetch functions
- Graceful handling of missing data fields
- SSL verification disabled for government sites (Census Bureau)

### Data Processing Patterns
1. Load raw CSV files from respective directories
2. Transform date columns into separate year/month columns  
3. Calculate derived metrics (rates, summaries)
4. Save to processed directories with consistent naming

## Development Environment

- **Python**: >=3.12 required
- **Package Manager**: uv (modern pip replacement)
- **Linting**: ruff with 100 character line limit
- **Dependencies**: pandas, requests, python-dateutil

## File Naming Conventions

- **Raw FRED data**: `{data_name}_last_14_quarters.csv`
- **Raw CPS data**: `accountants_{month_abbr}{year_short}.csv` (e.g., `accountants_jul25.csv`)
- **Processed data**: `{data_name}_processed.csv` or `{data_name}_summary.csv`