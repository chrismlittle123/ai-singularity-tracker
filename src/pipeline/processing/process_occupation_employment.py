from pathlib import Path

import pandas as pd


def process_occupation_employment() -> None:
    """Process occupation employment into indexed displacement gap.

    Creates employment indices (first observation = 100) for AI-targetable
    and non-automatable groups, then computes a displacement gap.
    Positive gap = non-automatable outpacing AI-targetable = displacement signal.
    """
    raw_dir = Path("data/raw/occupation_employment")
    processed_dir = Path("data/processed/occupation_employment")
    processed_dir.mkdir(parents=True, exist_ok=True)

    input_file = raw_dir / "occupation_employment.csv"
    if not input_file.exists():
        print("No occupation_employment.csv found in raw directory")
        return

    print(f"Processing {input_file.name}...")

    df = pd.read_csv(input_file)
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date").reset_index(drop=True)

    print(f"  • Loaded {len(df)} records")

    # Create indices (first observation = 100)
    base_ai = df["ai_targetable"].iloc[0]
    base_non = df["non_automatable"].iloc[0]

    df["ai_targetable_index"] = df["ai_targetable"] / base_ai * 100
    df["non_automatable_index"] = df["non_automatable"] / base_non * 100

    # Displacement gap: positive = non-automatable growing faster
    df["displacement_gap"] = (
        df["non_automatable_index"] - df["ai_targetable_index"]
    )

    # Convert date to year/month
    df["year"] = df["date"].dt.strftime("%Y")
    df["month"] = df["date"].dt.strftime("%m")
    df = df.drop("date", axis=1)

    cols = ["year", "month"] + [
        c for c in df.columns if c not in ["year", "month"]
    ]
    df = df[cols]

    output_path = processed_dir / "occupation_employment_processed.csv"
    df.to_csv(output_path, index=False)

    print(f"✓ Saved to {output_path}")
    print("\nRecent displacement gaps:")
    for _, row in df.tail(6).iterrows():
        print(
            f"  • {row['year']}-{row['month']}: "
            f"AI={row['ai_targetable_index']:.1f}, "
            f"Non-auto={row['non_automatable_index']:.1f}, "
            f"Gap={row['displacement_gap']:+.1f}"
        )


if __name__ == "__main__":
    process_occupation_employment()
