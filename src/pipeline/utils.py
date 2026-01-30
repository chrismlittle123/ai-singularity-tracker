from io import StringIO
from pathlib import Path
from datetime import datetime
from dateutil.relativedelta import relativedelta

import pandas as pd
import requests


def get_missing_quarters(data_name: str, target_quarters: int = 14) -> list:
    """
    Identify which quarters in the past N quarters are missing from raw data.
    
    Args:
        data_name: Name for the dataset (used in file naming)
        target_quarters: Number of quarters to check (default: 14)
    
    Returns:
        List of (year, quarter) tuples that are missing
    """
    data_dir = Path(f"data/raw/{data_name}")
    
    # Get current quarter and exclude it
    current_date = datetime.now()
    current_quarter = (current_date.month - 1) // 3 + 1
    current_year = current_date.year
    
    # Generate list of past N quarters (excluding current quarter)
    past_quarters = []
    quarter_date = current_date
    for i in range(target_quarters):
        quarter_date = quarter_date - relativedelta(months=3)
        quarter_num = (quarter_date.month - 1) // 3 + 1
        past_quarters.append((quarter_date.year, quarter_num))
    
    # Check existing data to see what quarters we have
    existing_quarters = set()
    if data_dir.exists():
        for file_path in data_dir.glob("*.csv"):
            if "quarters" in file_path.stem:
                # Try to read the file and extract quarters from the data
                try:
                    df = pd.read_csv(file_path)
                    if 'date' in df.columns:
                        df['date'] = pd.to_datetime(df['date'])
                        for _, row in df.iterrows():
                            date = row['date']
                            quarter = (date.month - 1) // 3 + 1
                            existing_quarters.add((date.year, quarter))
                except Exception:
                    pass  # Skip files that can't be read
    
    # Find missing quarters from our target list
    missing_quarters = [q for q in past_quarters if q not in existing_quarters]
    
    print(f"Found data for {len(existing_quarters)} quarters: {sorted(existing_quarters)}")
    print(f"Missing {len(missing_quarters)} quarters from past {target_quarters}: {sorted(missing_quarters)}")
    
    return missing_quarters


def fetch_fred_data(url: str, data_name: str, column_name: str, quarters: int = 14) -> pd.DataFrame:
    """
    Fetch economic data from FRED and save last N quarters to raw directory.
    Only fetches data if we don't already have the past N quarters.

    Args:
        url: FRED CSV download URL
        data_name: Name for the dataset (used in file naming)
        column_name: Name for the data column
        quarters: Number of recent quarters to save (default: 14)

    Returns:
        DataFrame with the last N quarters of data
    """
    # Check if we need to fetch new data
    missing_quarters = get_missing_quarters(data_name, quarters)
    
    data_dir = Path(f"data/raw/{data_name}")
    data_dir.mkdir(parents=True, exist_ok=True)
    
    output_path = data_dir / f"{data_name}_last_{quarters}_quarters.csv"
    
    # If we have all the quarters we need, just load existing data
    if not missing_quarters and output_path.exists():
        print(f"✓ All {quarters} quarters already exist for {data_name}")
        df_existing = pd.read_csv(output_path)
        df_existing['date'] = pd.to_datetime(df_existing['date'])
        print(f"✓ Loaded existing data from {output_path}")
        return df_existing

    print(f"Downloading {data_name} data from FRED...")

    # Download the data
    response = requests.get(url)
    response.raise_for_status()

    # Load the data directly from response
    df = pd.read_csv(StringIO(response.text))

    # Rename columns for clarity
    df.columns = ["date", column_name]
    df["date"] = pd.to_datetime(df["date"])

    # Drop rows with missing dates or values
    df = df.dropna(subset=["date", column_name])

    # Filter for last N quarters
    df_recent = df.tail(quarters).copy()

    print("\nData Summary:")
    print(f"  • Date range: {df['date'].min()} to {df['date'].max()}")
    print(f"  • Number of observations: {len(df)}")
    latest_date = df.iloc[-1]["date"].strftime("%Y-%m-%d")
    print(f"  • Latest value: {df.iloc[-1][column_name]:.2f} ({latest_date})")

    print(f"\nLast {quarters} quarters:")
    for _, row in df_recent.iterrows():
        print(f"  • {row['date'].strftime('%Y Q%q')}: {row[column_name]:.2f}")

    # Save only the last N quarters to raw directory
    df_recent.to_csv(output_path, index=False)
    print(f"\n✓ Last {quarters} quarters saved to {output_path}")

    return df_recent


def analyze_trend(df: pd.DataFrame, column_name: str) -> None:
    """
    Analyze year-over-year trends in the data.

    Args:
        df: DataFrame with date and data columns
        column_name: Name of the column to analyze
    """
    if len(df) >= 8:  # Need at least 8 quarters for 2-year comparison
        current_value = df.iloc[-1][column_name]
        one_year_ago = df.iloc[-5][column_name]  # 4 quarters ago + current
        two_years_ago = df.iloc[-9][column_name]  # 8 quarters ago + current

        one_year_change = ((current_value - one_year_ago) / one_year_ago) * 100
        two_year_change = ((current_value - two_years_ago) / two_years_ago) * 100

        print("\nTrend Analysis:")
        print(f"  • 1-year change: {one_year_change:+.2f}%")
        print(f"  • 2-year change: {two_year_change:+.2f}%")

        if one_year_change < 0 and two_year_change < 0:
            print(f"  ⚠ Both periods show downward trend in {column_name}")
        elif one_year_change > 0 and two_year_change > 0:
            print(f"  ↑ Both periods show upward trend in {column_name}")
        else:
            print(f"  ↔ Mixed trend in {column_name}")
