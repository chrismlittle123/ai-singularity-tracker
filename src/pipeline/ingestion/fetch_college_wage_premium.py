import sys
from datetime import datetime
from io import StringIO
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pandas as pd
import requests


def build_fred_url(series_id: str, frequency: str = "Quarterly") -> str:
    """Build a FRED CSV download URL with dynamic dates."""
    today = datetime.now().strftime("%Y-%m-%d")
    return (
        f"https://fred.stlouisfed.org/graph/fredgraph.csv?"
        f"id={series_id}&cosd=1947-01-01&coed={today}"
        f"&fq={frequency}&fam=avg&fgst=lin&transformation=lin"
        f"&vintage_date={today}&revision_date={today}&nd=1947-01-01"
    )


def fetch_single_series(
    series_id: str, column_name: str, quarters: int = 14
) -> pd.DataFrame:
    """Fetch a single quarterly FRED series and return last N quarters."""
    url = build_fred_url(series_id)
    print(f"  Downloading {series_id}...")

    response = requests.get(url, timeout=30)
    response.raise_for_status()

    df = pd.read_csv(StringIO(response.text))
    df.columns = ["date", column_name]
    df["date"] = pd.to_datetime(df["date"])
    df = df.dropna(subset=["date", column_name])
    df = df.tail(quarters).copy()

    print(f"  * {column_name}: {len(df)} observations")
    print(f"  * Range: {df['date'].min()} to {df['date'].max()}")
    print(f"  * Latest: {df.iloc[-1][column_name]:.1f}")

    return df


def fetch_college_wage_premium_data() -> None:
    """Fetch median weekly earnings by education level and compute premium.

    LEU0252918300Q: Median usual weekly earnings, Bachelor's degree
    and higher, 25 years and over (nominal $). Source: BLS CPS.

    LEU0252884000Q: Median usual weekly earnings, High school
    graduates no college, 25 years and over (nominal $). Source: BLS CPS.

    The ratio (bachelor's / high-school) is the college wage premium.
    Since both series are nominal and measured at the same date,
    inflation cancels out in the ratio.

    If AI specifically hits knowledge work, this ratio compresses —
    college-educated workers lose their earnings advantage relative
    to non-college workers. A sustained compression would be the
    AI-specific wage signal that aggregate wage data would miss.

    Historical premium: ~1.7-1.8x, remarkably stable for decades.
    A 10% compression (to ~1.55x) in 3 years would be unprecedented.
    """
    data_dir = Path("data/raw/college_wage_premium")
    data_dir.mkdir(parents=True, exist_ok=True)

    print("Fetching college wage premium data...")

    bachelor_df = fetch_single_series(
        "LEU0252918300Q", "bachelor_earnings", quarters=14
    )
    highschool_df = fetch_single_series(
        "LEU0252884000Q", "highschool_earnings", quarters=14
    )

    # Merge on date
    merged = pd.merge(bachelor_df, highschool_df, on="date", how="inner")
    merged["college_wage_premium"] = (
        merged["bachelor_earnings"] / merged["highschool_earnings"]
    )

    print("\nCollege Wage Premium (Bachelor's+ / HS-only):")
    for _, row in merged.iterrows():
        print(
            f"  * {row['date'].strftime('%Y-Q%q')}: "
            f"{row['college_wage_premium']:.3f}x "
            f"(BA=${row['bachelor_earnings']:.0f}, "
            f"HS=${row['highschool_earnings']:.0f})"
        )

    output_path = data_dir / "college_wage_premium.csv"
    merged.to_csv(output_path, index=False)
    print(f"\n✓ Saved to {output_path}")


if __name__ == "__main__":
    fetch_college_wage_premium_data()
