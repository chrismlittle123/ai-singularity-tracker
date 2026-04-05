# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

The AI Singularity Tracker monitors economic indicators to detect potential signals of AI-driven technological displacement. It tracks 12 key metrics across four categories, optimized for AI signal-to-noise ratio:

**Structural Shifts (hardest to explain without AI):**
- **TFP Acceleration** (annual FRED data) — productivity signature of AI
- **AI Job Displacement Gap** (monthly FRED CPS/CES) — AI-targetable vs non-automatable occupations
- **Capital-Labor Substitution** (annual FRED data) — firms replacing workers with capital

**Wage & Distribution (who benefits from AI gains):**
- **Real Median Weekly Earnings** (quarterly FRED data) — THE displacement outcome metric
- **College Wage Premium** (quarterly, derived from FRED) — AI-specific wage signal (bachelor's+/HS ratio)
- **Labor Share of Income** (quarterly FRED data)

**Labour Market Health (the human cost):**
- **Prime-Age EPOP** (monthly FRED data) — employment-population ratio for 25-54
- **Quits Rate** (monthly FRED JOLTS) — worker confidence indicator
- **Graduate Unemployment Rate** (monthly FRED data)

**AI Investment Scale (the cause indicators):**
- **NVIDIA Quarterly Revenue** (SEC EDGAR XBRL) — proxy for AI compute investment
- **IT Equipment Investment** (quarterly FRED/BEA data) — hardware side of AI capex
- **Software Investment** (quarterly FRED/BEA data) — software side of AI capex

The hypothesis: declining real wages + compressing college premium + rising AI investment over 1-3 year periods would signal AI-driven structural displacement. The tracker requires multiple independent indicators to move simultaneously — unlikely from confounders alone.

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
uv run python src/pipeline/ingestion/fetch_prime_age_epop.py
uv run python src/pipeline/ingestion/fetch_quits_rate.py
uv run python src/pipeline/ingestion/fetch_it_equipment_investment.py
uv run python src/pipeline/ingestion/fetch_median_wages.py
uv run python src/pipeline/ingestion/fetch_college_wage_premium.py
uv run python src/pipeline/ingestion/fetch_software_investment.py

# Processing (transforms to standardized format)
uv run python src/pipeline/processing/process_labor_share.py
uv run python src/pipeline/processing/process_real_gdp_per_capita.py
uv run python src/pipeline/processing/process_unemployment_rate.py
uv run python src/pipeline/processing/process_electricity_production.py
uv run python src/pipeline/processing/process_nvidia_revenue.py
uv run python src/pipeline/processing/process_business_applications.py
uv run python src/pipeline/processing/process_prime_age_epop.py
uv run python src/pipeline/processing/process_quits_rate.py
uv run python src/pipeline/processing/process_it_equipment_investment.py
uv run python src/pipeline/processing/process_median_wages.py
uv run python src/pipeline/processing/process_college_wage_premium.py
uv run python src/pipeline/processing/process_software_investment.py

# Dashboard
uv run streamlit run src/dashboard/app.py
```

## Data Sources & Formats

### FRED Data (Labor Share, Real GDP, Unemployment, IT Equipment, Median Wages, Software)
- **Source**: Federal Reserve Economic Data CSV exports
- **Series**: PRS85006173 (labor share), A939RX0Q048SBEA (GDP), LNU04027662 (unemployment), Y033RC1Q027SBEA (IT equipment), LES1252881600Q (median wages), B985RC1Q027SBEA (software investment)
- **Frequency**: Quarterly (labor share, GDP, IT equipment, wages, software) or Monthly (unemployment)
- **Processing**: Uses `fetch_fred_data()` utility with automatic trend analysis
- **Output**: `year,month,<metric_name>` format

### College Wage Premium (Derived)
- **Source**: Two FRED series — LEU0252918300Q (bachelor's+) / LEU0252884000Q (HS-only)
- **Frequency**: Quarterly
- **Processing**: Fetches both series, computes ratio as college wage premium
- **Output**: `year,month,bachelor_earnings,highschool_earnings,college_wage_premium`

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
