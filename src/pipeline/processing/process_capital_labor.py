from pathlib import Path

import pandas as pd


def process_capital_labor() -> None:
    """Process capital-labor ratio data: split date into year/month."""
    raw_dir = Path("data/raw/capital_labor")
    processed_dir = Path("data/processed/capital_labor")
    processed_dir.mkdir(parents=True, exist_ok=True)

    input_file = raw_dir / "capital_labor_ratio.csv"
    if not input_file.exists():
        print("No capital_labor_ratio.csv found in raw directory")
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

    output_path = processed_dir / "capital_labor_processed.csv"
    df.to_csv(output_path, index=False)
    print(f"✓ Processed data saved to {output_path}")
    print(df.to_string(index=False))


if __name__ == "__main__":
    process_capital_labor()
