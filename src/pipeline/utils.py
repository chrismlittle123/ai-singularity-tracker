from io import StringIO
from pathlib import Path

import pandas as pd
import requests


def fetch_fred_data(url: str, data_name: str, column_name: str, quarters: int = 14) -> pd.DataFrame:
    """
    Fetch economic data from FRED and save last N quarters to raw directory.

    Args:
        url: FRED CSV download URL
        data_name: Name for the dataset (used in file naming)
        column_name: Name for the data column
        quarters: Number of recent quarters to save (default: 14)

    Returns:
        DataFrame with the last N quarters of data
    """
    # Create data directory
    data_dir = Path(f"data/raw/{data_name}")
    data_dir.mkdir(parents=True, exist_ok=True)

    print(f"Downloading {data_name} data from FRED...")

    # Download the data
    response = requests.get(url)
    response.raise_for_status()

    # Load the data directly from response
    df = pd.read_csv(StringIO(response.text))

    # Rename columns for clarity
    df.columns = ["date", column_name]
    df["date"] = pd.to_datetime(df["date"])

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
    output_path = data_dir / f"{data_name}_last_{quarters}_quarters.csv"
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
