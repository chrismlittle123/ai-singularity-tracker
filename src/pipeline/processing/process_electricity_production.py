from pathlib import Path

import pandas as pd


def process_electricity_consumption() -> None:
    """Process electricity consumption data: split date into year/month."""
    raw_dir = Path("data/raw/electricity_consumption")
    processed_dir = Path("data/processed/electricity_consumption")
    processed_dir.mkdir(parents=True, exist_ok=True)

    input_file = raw_dir / "electricity_consumption_last_42_months.csv"
    if not input_file.exists():
        print("No electricity consumption CSV found in raw directory")
        return

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

    output_path = processed_dir / "electricity_consumption_processed.csv"
    df.to_csv(output_path, index=False)
    print(f"✓ Processed data saved to {output_path}")
    print(df.tail(6).to_string(index=False))


if __name__ == "__main__":
    process_electricity_consumption()
