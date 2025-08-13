from pathlib import Path

import pandas as pd
import requests


def fetch_accountants_employed_data():
    """Fetch accountants and auditors employment data from CPS July 2025."""
    # Create data directory
    data_dir = Path("data/raw/accountants_employed")
    data_dir.mkdir(parents=True, exist_ok=True)

    # July 2025 CPS data URL from README
    url = "https://www2.census.gov/programs-surveys/cps/datasets/2025/basic/jul25pub.csv"

    print("Downloading July 2025 CPS data...")

    # Download the data (disable SSL verification for government site)
    response = requests.get(url, verify=False)
    response.raise_for_status()

    # Load data directly from response (don't save the full CPS file)
    from io import BytesIO
    df = pd.read_csv(BytesIO(response.content))

    print("\nData Summary:")
    print(f"  • Total records: {len(df):,}")
    print(f"  • Columns: {len(df.columns)}")

    # Filter for accountants and auditors using PTIO1OCD field
    # Based on data dictionary: PTIO1OCD contains 4-digit occupation codes
    # 0800 = Accountants and auditors

    if "ptio1ocd" in df.columns:
        print("  • Found occupation code field: ptio1ocd")

        # Filter for accountants and auditors (occupation code 800)
        all_accountants_df = df[df["ptio1ocd"] == 800.0]
        print(f"  • Total accountants and auditors (code 800): {len(all_accountants_df):,}")

        # Show employment breakdown but save ALL accountants to raw data
        if "pemlr" in df.columns:
            employed_accountants_df = all_accountants_df[all_accountants_df["pemlr"] == 1.0]
            unemployed_accountants_df = all_accountants_df[all_accountants_df["pemlr"] != 1.0]
            print(f"  • Employed accountants and auditors: {len(employed_accountants_df):,}")
            print(f"  • Unemployed/not in labor force: {len(unemployed_accountants_df):,}")
            accountants_df = all_accountants_df  # Save ALL accountants to raw data
        else:
            print("  ⚠ Employment status field (pemlr) not found - using all accountants")
            accountants_df = all_accountants_df

    else:
        print("  ⚠ ptio1ocd column not found")
        occ_columns = [col for col in df.columns if "occ" in col.lower()]
        print(f"  • Available occupation-related columns: {occ_columns}")
        accountants_df = pd.DataFrame()

    print(f"  • Accountants and auditors records: {len(accountants_df):,}")

    if len(accountants_df) > 0:
        # Save filtered data
        filtered_path = data_dir / "accountants_jul25.csv"
        accountants_df.to_csv(filtered_path, index=False)
        print(f"✓ Accountants data saved to {filtered_path}")

        # Additional statistics
        if "prtage" in accountants_df.columns:  # Age field
            avg_age = accountants_df["prtage"].mean()
            print(f"  • Average age: {avg_age:.1f} years")

        if "pesex" in accountants_df.columns:  # Gender field
            gender_dist = accountants_df["pesex"].value_counts()
            print("  • Gender distribution:")
            for gender, count in gender_dist.items():
                print(f"    {gender}: {count:,}")

        return accountants_df
    else:
        print("  ⚠ No accountants found with code 800")
        return df


if __name__ == "__main__":
    fetch_accountants_employed_data()
