# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

The AI Singularity Tracker monitors economic indicators to detect potential signals of AI-driven technological displacement. It tracks five key metrics across two categories:

**Effect Indicators (economic displacement signals):**
- **Labor Share of Income** (quarterly FRED data)
- **Real GDP per Capita** (quarterly FRED data)
- **Graduate Unemployment Rate** (monthly FRED data)

**Cause Indicators (AI compute buildout):**
- **Electricity Production Index** (monthly FRED data) — proxy for data center power demand
- **NVIDIA Quarterly Revenue** (SEC EDGAR XBRL) — proxy for AI compute investment

The hypothesis: declining labor share + rising graduate unemployment combined with rising GDP, electricity demand, and NVIDIA revenue over 1-3 year periods may signal AI-driven economic transformation.

## Architecture

### Data Pipeline Structure

**Two-stage pipeline:**
1. **Ingestion** (`src/pipeline/ingestion/`) - Downloads raw data from sources
2. **Processing** (`src/pipeline/processing/`) - Transforms into standardized format

**Smart data management:**
- Automatic detection of missing time periods
- Incremental fetching (only downloads missing data)
- FRED data: maintains last 14 quarters (quarterly) or 42 months (monthly)
- NVIDIA data: fetches from SEC EDGAR XBRL API (last 14 quarters)

### Directory Organization

```
data/
├── raw/           # Downloaded source data
└── processed/     # Standardized format (year,month columns)

src/
├── dashboard/     # Streamlit visualization app
│   └── app.py     # Interactive dashboard with AI Singularity Score
└── pipeline/
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
uv run python src/pipeline/ingestion/fetch_unemployment_rate.py
uv run python src/pipeline/ingestion/fetch_electricity_production.py
uv run python src/pipeline/ingestion/fetch_nvidia_revenue.py
uv run python src/pipeline/ingestion/fetch_business_applications.py

# Processing (transforms to standardized format)
uv run python src/pipeline/processing/process_labor_share.py
uv run python src/pipeline/processing/process_real_gdp_per_capita.py
uv run python src/pipeline/processing/process_unemployment_rate.py
uv run python src/pipeline/processing/process_electricity_production.py
uv run python src/pipeline/processing/process_nvidia_revenue.py
uv run python src/pipeline/processing/process_business_applications.py

# Dashboard
uv run streamlit run src/dashboard/app.py
```

## Data Sources & Formats

### FRED Data (Labor Share, Real GDP, Graduate Unemployment, Electricity)
- **Source**: Federal Reserve Economic Data CSV exports
- **Series**: PRS85006173 (labor share), A939RX0Q048SBEA (GDP), CGAD2534 (unemployment), IPG2211A2N (electricity)
- **Frequency**: Quarterly (labor share, GDP) or Monthly (unemployment, electricity)
- **Processing**: Uses `fetch_fred_data()` utility with automatic trend analysis
- **Output**: `year,month,<metric_name>` format

### SEC EDGAR Data (NVIDIA Revenue)
- **Source**: SEC EDGAR XBRL API (CIK 0001045810)
- **Frequency**: Quarterly (fiscal quarter filings)
- **Note**: Uses total revenue as proxy (~90% is Data Center segment)
- **Output**: `year,month,revenue_millions` format

## Key Implementation Details

### Time Period Management
- **Current month excluded** from all data fetching
- **FRED scripts**: Automatically calculate past 14 quarters from current date
- **Missing data detection**: Scans existing files to avoid redundant downloads

### Error Handling
- Network timeouts and retries built into fetch functions
- Graceful handling of missing data fields

### Data Processing Patterns
1. Load raw CSV files from respective directories
2. Transform date columns into separate year/month columns
3. Calculate derived metrics (rates, summaries)
4. Save to processed directories with consistent naming

## Development Environment

- **Python**: >=3.12 required
- **Package Manager**: uv (modern pip replacement)
- **Linting**: ruff with 100 character line limit
- **Dependencies**: pandas, requests, python-dateutil, streamlit, plotly

## File Naming Conventions

- **Raw FRED data**: `{data_name}_last_{N}_quarters.csv`
- **Raw NVIDIA data**: `nvidia_quarterly_revenue.csv`
- **Processed data**: `{data_name}_processed.csv`
