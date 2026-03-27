import sys
from datetime import datetime
from io import StringIO
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pandas as pd
import requests


def build_fred_url(series_id: str, frequency: str = "Annual") -> str:
    """Build a FRED CSV download URL with dynamic dates."""
    today = datetime.now().strftime("%Y-%m-%d")
    return (
        f"https://fred.stlouisfed.org/graph/fredgraph.csv?"
        f"id={series_id}&cosd=1947-01-01&coed={today}"
        f"&fq={frequency}&fam=avg&fgst=lin&transformation=lin"
        f"&vintage_date={today}&revision_date={today}&nd=1947-01-01"
    )


def fetch_single_series(
    series_id: str, column_name: str, years: int = 15
) -> pd.DataFrame:
    """Fetch a single annual FRED series and return last N years."""
    url = build_fred_url(series_id)
    print(f"  Downloading {series_id}...")

    response = requests.get(url, timeout=30)
    response.raise_for_status()

    df = pd.read_csv(StringIO(response.text))
    df.columns = ["date", column_name]
    df["date"] = pd.to_datetime(df["date"])
    df = df.dropna(subset=["date", column_name])
    df = df.tail(years).copy()

    print(f"  • {column_name}: {len(df)} observations")
    print(f"  • Range: {df['date'].min()} to {df['date'].max()}")
    print(f"  • Latest: {df.iloc[-1][column_name]:.3f}")

    return df


def fetch_capital_labor_data() -> None:
    """Fetch Capital Input and Labor Input from BLS MFP dataset via FRED.

    MPU4910042: Capital Input (Index 2017=100)
    MPU4910052: Labor Input, quality-adjusted (Index 2017=100)

    The ratio Capital/Labor measures capital deepening — firms substituting
    capital (including AI/software) for human labor.
    """
    data_dir = Path("data/raw/capital_labor")
    data_dir.mkdir(parents=True, exist_ok=True)

    print("Fetching capital and labor input data...")

    capital_df = fetch_single_series("MPU4910042", "capital_input", years=15)
    labor_df = fetch_single_series("MPU4910052", "labor_input", years=15)

    # Merge on date
    merged = pd.merge(capital_df, labor_df, on="date", how="inner")
    merged["capital_labor_ratio"] = (
        merged["capital_input"] / merged["labor_input"]
    )

    print("\nCapital-to-Labor Ratio:")
    for _, row in merged.iterrows():
        print(
            f"  • {row['date'].strftime('%Y')}: "
            f"{row['capital_labor_ratio']:.4f} "
            f"(C={row['capital_input']:.1f}, L={row['labor_input']:.1f})"
        )

    output_path = data_dir / "capital_labor_ratio.csv"
    merged.to_csv(output_path, index=False)
    print(f"\n✓ Saved to {output_path}")


if __name__ == "__main__":
    fetch_capital_labor_data()
