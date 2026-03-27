from pathlib import Path

import pandas as pd


def process_nvidia_revenue():
    """
    Process NVIDIA revenue data by splitting date into year and month columns
    and removing the original date column.
    """
    # Setup paths
    raw_dir = Path("data/raw/nvidia_revenue")
    processed_dir = Path("data/processed/nvidia_revenue")
    processed_dir.mkdir(parents=True, exist_ok=True)

    input_file = raw_dir / "nvidia_quarterly_revenue.csv"

    if not input_file.exists():
        print("No NVIDIA revenue CSV file found in raw directory")
        return

    print(f"Processing {input_file.name}...")

    # Load the data
    df = pd.read_csv(input_file)

    print(f"  • Loaded {len(df)} records")
    print(f"  • Columns: {list(df.columns)}")

    # Convert date column to datetime
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"])

        # Extract year and month
        df["year"] = df["date"].dt.strftime("%Y")
        df["month"] = df["date"].dt.strftime("%m")

        # Remove the original date column
        df = df.drop("date", axis=1)

        # Reorder columns to have year and month first
        cols = ["year", "month"] + [col for col in df.columns if col not in ["year", "month"]]
        df = df[cols]

        print("  • Split date into year/month columns")
        print(
            f"  • Date range: {df['year'].min()}-{df['month'].min()} "
            f"to {df['year'].max()}-{df['month'].max()}"
        )

    else:
        print("  ⚠ No 'date' column found")
        return

    # Save processed data
    output_path = processed_dir / "nvidia_revenue_processed.csv"
    df.to_csv(output_path, index=False)

    print(f"✓ Processed data saved to {output_path}")
    print(f"  • Final columns: {list(df.columns)}")

    # Show sample of processed data
    print("\nSample of processed data:")
    print(df.head().to_string(index=False))

    return df


if __name__ == "__main__":
    process_nvidia_revenue()
