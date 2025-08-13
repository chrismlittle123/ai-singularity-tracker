import re
from pathlib import Path

import pandas as pd


def process_accountants_employed():
    """
    Process all accountants_{month}{yy}.csv files in raw/accountants_employed
    and create a summary table with year, month, employed_accountants, unemployed_accountants.
    """
    # Setup paths
    raw_dir = Path("data/raw/accountants_employed")
    processed_dir = Path("data/processed/accountants_employed")
    processed_dir.mkdir(parents=True, exist_ok=True)

    # Find all accountants CSV files (pattern: accountants_{month}{yy}.csv)
    pattern = re.compile(r"accountants_([a-z]{3})(\d{2})\.csv")
    csv_files = []

    for file_path in raw_dir.glob("accountants_*.csv"):
        match = pattern.match(file_path.name)
        if match:
            month_abbr, year_short = match.groups()
            csv_files.append((file_path, month_abbr, year_short))

    if not csv_files:
        print("No accountant CSV files found matching pattern accountants_{month}{yy}.csv")
        return

    print(f"Found {len(csv_files)} accountant data files:")
    for file_path, month_abbr, year_short in csv_files:
        print(f"  • {file_path.name} -> {month_abbr} 20{year_short}")

    # Month mapping
    month_mapping = {
        "jan": "01", "feb": "02", "mar": "03", "apr": "04", "may": "05", "jun": "06",
        "jul": "07", "aug": "08", "sep": "09", "oct": "10", "nov": "11", "dec": "12"
    }

    # Process each file
    summary_data = []

    for file_path, month_abbr, year_short in csv_files:
        print(f"\nProcessing {file_path.name}...")

        # Convert to full year and month
        year_full = f"20{year_short}"
        month_num = month_mapping.get(month_abbr.lower(), "00")

        if month_num == "00":
            print(f"  ⚠ Unknown month abbreviation: {month_abbr}")
            continue

        # Load the data
        df = pd.read_csv(file_path)

        print(f"  • Loaded {len(df):,} records")

        # Count employment status
        # PEMLR = 1 means employed, anything else is not employed
        if "pemlr" in df.columns:
            employed_count = len(df[df["pemlr"] == 1.0])
            unemployed_count = len(df[df["pemlr"] != 1.0])
        else:
            print("  ⚠ No employment status field (pemlr) found")
            employed_count = len(df)  # Assume all are employed if no status field
            unemployed_count = 0

        print(f"  • Employed: {employed_count:,}")
        print(f"  • Unemployed/Not in labor force: {unemployed_count:,}")

        # Add to summary
        summary_data.append({
            "year": year_full,
            "month": month_num,
            "employed_accountants": employed_count,
            "unemployed_accountants": unemployed_count,
            "total_accountants": employed_count + unemployed_count
        })

    # Create summary DataFrame
    if summary_data:
        summary_df = pd.DataFrame(summary_data)

        # Sort by year and month
        summary_df = summary_df.sort_values(["year", "month"]).reset_index(drop=True)

        # Add employment rate to the summary
        summary_df["employment_rate"] = (
            summary_df["employed_accountants"] / summary_df["total_accountants"] * 100
        ).round(1)

        # Save single output file to processed directory
        output_path = processed_dir / "accountants_employment_summary.csv"
        summary_df.to_csv(output_path, index=False)

        print(f"\n✓ Summary saved to {output_path}")
        print("\nSummary table:")
        print(summary_df.to_string(index=False))

        return summary_df
    else:
        print("\n⚠ No data processed")
        return pd.DataFrame()


if __name__ == "__main__":
    process_accountants_employed()
