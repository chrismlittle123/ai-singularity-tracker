from pathlib import Path

import pandas as pd


def process_tfp() -> None:
    """Process TFP data: split date into year/month, save processed CSV."""
    raw_dir = Path("data/raw/tfp")
    processed_dir = Path("data/processed/tfp")
    processed_dir.mkdir(parents=True, exist_ok=True)

    csv_files = list(raw_dir.glob("tfp_last_*.csv"))
    if not csv_files:
        print("No TFP CSV files found in raw directory")
        return

    input_file = csv_files[0]
    print(f"Processing {input_file.name}...")

    df = pd.read_csv(input_file)
    print(f"  • Loaded {len(df)} records")

    if "date" not in df.columns:
        print("  ⚠ No 'date' column found")
        return

    df["date"] = pd.to_datetime(df["date"])
    df["year"] = df["date"].dt.strftime("%Y")
    df["month"] = df["date"].dt.strftime("%m")
    df = df.drop("date", axis=1)

    cols = ["year", "month"] + [
        c for c in df.columns if c not in ["year", "month"]
    ]
    df = df[cols]

    output_path = processed_dir / "tfp_processed.csv"
    df.to_csv(output_path, index=False)
    print(f"✓ Processed data saved to {output_path}")
    print(df.to_string(index=False))


if __name__ == "__main__":
    process_tfp()
