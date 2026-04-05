from pathlib import Path

import pandas as pd


def process_info_jobs_per_grad():
    """Process info jobs per grad data by splitting date into year and month columns."""
    raw_dir = Path("data/raw/info_jobs_per_grad")
    processed_dir = Path("data/processed/info_jobs_per_grad")
    processed_dir.mkdir(parents=True, exist_ok=True)

    input_file = raw_dir / "info_jobs_per_grad.csv"

    if not input_file.exists():
        print("No info jobs per grad CSV found in raw directory")
        return

    print(f"Processing {input_file.name}...")

    df = pd.read_csv(input_file)

    print(f"  * Loaded {len(df)} records")
    print(f"  * Columns: {list(df.columns)}")

    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"])

        df["year"] = df["date"].dt.strftime("%Y")
        df["month"] = df["date"].dt.strftime("%m")

        df = df.drop("date", axis=1)

        cols = ["year", "month"] + [col for col in df.columns if col not in ["year", "month"]]
        df = df[cols]

        print("  * Split date into year/month columns")
        print(
            f"  * Date range: {df['year'].min()}-{df['month'].min()} "
            f"to {df['year'].max()}-{df['month'].max()}"
        )
    else:
        print("  ! No 'date' column found")
        return

    output_path = processed_dir / "info_jobs_per_grad_processed.csv"
    df.to_csv(output_path, index=False)

    print(f"Processed data saved to {output_path}")
    print(f"  * Final columns: {list(df.columns)}")

    print("\nSample of processed data:")
    print(df.head().to_string(index=False))

    return df


if __name__ == "__main__":
    process_info_jobs_per_grad()
