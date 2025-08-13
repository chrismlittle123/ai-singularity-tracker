from pathlib import Path
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import calendar
import time
from io import BytesIO

import pandas as pd
import requests


def get_missing_months():
    """Identify which months in the past 36 months are missing from raw data."""
    data_dir = Path("data/raw/accountants_employed")
    
    # Get current date and exclude current month
    current_date = datetime.now()
    
    # Generate list of past 40 months (excluding current month)
    # Need 40 months to ensure 14 quarters of quarterly-aligned data
    past_months = []
    for i in range(1, 41):  # 1 to 40 months back, inclusive
        month_date = current_date - relativedelta(months=i)
        past_months.append((month_date.year, month_date.month))
    
    # Check which months already have data
    existing_months = set()
    if data_dir.exists():
        for file_path in data_dir.glob("accountants_*.csv"):
            # Extract month/year from filename (e.g., accountants_jul25.csv)
            filename = file_path.stem
            if filename.startswith("accountants_"):
                month_part = filename.split("_")[1]  # e.g., "jul25"
                if len(month_part) >= 5:
                    month_str = month_part[:3]  # e.g., "jul"
                    year_str = month_part[3:]   # e.g., "25"
                    
                    # Convert month abbreviation to number
                    month_map = {v.lower(): k for k, v in enumerate(calendar.month_abbr) if v}
                    if month_str.lower() in month_map:
                        month_num = month_map[month_str.lower()]
                        # Convert 2-digit year to 4-digit
                        year_num = 2000 + int(year_str) if int(year_str) < 50 else 1900 + int(year_str)
                        existing_months.add((year_num, month_num))
    
    # Find missing months
    missing_months = [month for month in past_months if month not in existing_months]
    
    print(f"Found {len(existing_months)} existing months: {sorted(existing_months)}")
    print(f"Missing {len(missing_months)} months: {sorted(missing_months)}")
    
    return missing_months


def fetch_month_data(year, month):
    """Fetch CPS data for a specific month and year."""
    data_dir = Path("data/raw/accountants_employed")
    data_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate URL for the specific month/year
    month_abbr = calendar.month_abbr[month].lower()
    year_short = str(year)[-2:]  # Last 2 digits of year
    
    url = f"https://www2.census.gov/programs-surveys/cps/datasets/{year}/basic/{month_abbr}{year_short}pub.csv"
    
    print(f"Downloading {calendar.month_name[month]} {year} CPS data from: {url}")
    
    try:
        # Download the data with longer timeout and retry logic
        session = requests.Session()
        session.verify = False  # Disable SSL verification for government site
        
        # Try with progressively longer timeouts
        for attempt, timeout in enumerate([60, 120, 180], 1):
            try:
                print(f"  • Attempt {attempt} (timeout: {timeout}s)...")
                response = session.get(url, timeout=timeout, stream=True)
                response.raise_for_status()
                break
            except requests.exceptions.Timeout:
                if attempt == 3:
                    raise
                print(f"    Timeout after {timeout}s, retrying...")
                continue
        
        # Load data directly from response
        df = pd.read_csv(BytesIO(response.content))
        
        print(f"  • Total records: {len(df):,}")
        
        # Filter for accountants and auditors using PTIO1OCD field
        if "ptio1ocd" in df.columns:
            all_accountants_df = df[df["ptio1ocd"] == 800.0]
            print(f"  • Total accountants and auditors (code 800): {len(all_accountants_df):,}")
            
            if "pemlr" in df.columns:
                employed_accountants_df = all_accountants_df[all_accountants_df["pemlr"] == 1.0]
                print(f"  • Employed accountants and auditors: {len(employed_accountants_df):,}")
                accountants_df = all_accountants_df
            else:
                print("  ⚠ Employment status field (pemlr) not found - using all accountants")
                accountants_df = all_accountants_df
        else:
            print("  ⚠ ptio1ocd column not found")
            return None
        
        if len(accountants_df) > 0:
            # Save filtered data with month/year in filename
            filtered_path = data_dir / f"accountants_{month_abbr}{year_short}.csv"
            accountants_df.to_csv(filtered_path, index=False)
            print(f"✓ Accountants data saved to {filtered_path}")
            return accountants_df
        else:
            print("  ⚠ No accountants found with code 800")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"  ✗ Failed to download data for {calendar.month_name[month]} {year}: {e}")
        return None
    except Exception as e:
        print(f"  ✗ Error processing data for {calendar.month_name[month]} {year}: {e}")
        return None


def fetch_accountants_employed_data():
    """Fetch accountants and auditors employment data for missing months in past 40 months."""
    print("Checking for missing months in past 40 months...")
    
    missing_months = get_missing_months()
    
    if not missing_months:
        print("✓ All months in the past 40 months already have data!")
        return
    
    print(f"\nFetching data for {len(missing_months)} missing months...")
    
    successful_fetches = 0
    failed_fetches = 0
    
    for i, (year, month) in enumerate(sorted(missing_months)):
        result = fetch_month_data(year, month)
        if result is not None:
            successful_fetches += 1
        else:
            failed_fetches += 1
        print()  # Add spacing between months
        
        # Add delay between requests to avoid overwhelming the server
        if i < len(missing_months) - 1:  # Don't delay after the last request
            print("  • Waiting 2 seconds before next request...")
            time.sleep(2)
    
    print(f"Summary:")
    print(f"  • Successfully fetched: {successful_fetches} months")
    print(f"  • Failed to fetch: {failed_fetches} months")
    print(f"  • Total attempted: {len(missing_months)} months")


if __name__ == "__main__":
    fetch_accountants_employed_data()
