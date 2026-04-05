import sys
from datetime import datetime
from io import StringIO
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pandas as pd
import requests


def build_fred_url(series_id: str, frequency: str = "Monthly") -> str:
    """Build a FRED CSV download URL with dynamic dates."""
    today = datetime.now().strftime("%Y-%m-%d")
    return (
        f"https://fred.stlouisfed.org/graph/fredgraph.csv?"
        f"id={series_id}&cosd=1947-01-01&coed={today}"
        f"&fq={frequency}&fam=avg&fgst=lin&transformation=lin"
        f"&vintage_date={today}&revision_date={today}&nd=1947-01-01"
    )


def fetch_single_series(
    series_id: str, column_name: str, months: int = 42
) -> pd.DataFrame:
    """Fetch a single monthly FRED series and return last N months."""
    url = build_fred_url(series_id)
    print(f"  Downloading {series_id}...")

    response = requests.get(url, timeout=30)
    response.raise_for_status()

    df = pd.read_csv(StringIO(response.text))
    df.columns = ["date", column_name]
    df["date"] = pd.to_datetime(df["date"])
    df[column_name] = pd.to_numeric(df[column_name], errors="coerce")
    df = df.dropna(subset=["date", column_name])
    df = df.tail(months).copy()

    print(f"  * {column_name}: {len(df)} observations")
    print(f"  * Range: {df['date'].min()} to {df['date'].max()}")
    print(f"  * Latest: {df.iloc[-1][column_name]:,.1f}")

    return df


def fetch_info_jobs_per_grad_data() -> None:
    """Fetch information sector employment and college labor force, compute ratio.

    USINFO: All Employees, Information (Thousands, SA). Source: BLS CES.
    The information sector includes publishing, software, data processing,
    broadcasting, telecom — the most AI-targetable knowledge economy.

    LNS11027662: Civilian Labor Force, Bachelor's Degree and Higher,
    25 Years and Over (Thousands, SA). Source: BLS CPS.

    The ratio (USINFO / LNS11027662 * 100) = information sector jobs
    per 100 college-educated workers. This directly measures whether
    the knowledge economy is creating or destroying demand for graduates.

    Unlike wages (which reflect survivors), this catches the structural
    erosion: fewer knowledge jobs divided among more graduates. The
    information sector shed ~193k jobs (-6.5%) since Jan 2022 while the
    college labor force grew ~5.4M (+8.7%), producing a -13.9% decline
    in the ratio.
    """
    data_dir = Path("data/raw/info_jobs_per_grad")
    data_dir.mkdir(parents=True, exist_ok=True)

    print("Fetching information sector jobs per graduate data...")

    info_df = fetch_single_series("USINFO", "info_employment", months=42)
    grad_df = fetch_single_series("LNS11027662", "college_labor_force", months=42)

    # Merge on date
    merged = pd.merge(info_df, grad_df, on="date", how="inner")
    merged["info_jobs_per_grad"] = (
        merged["info_employment"] / merged["college_labor_force"] * 100
    )

    print("\nInformation Sector Jobs per 100 Graduates:")
    for _, row in merged.tail(14).iterrows():
        print(
            f"  * {row['date'].strftime('%Y-%m')}: "
            f"{row['info_jobs_per_grad']:.2f} "
            f"(Info={row['info_employment']:,.0f}k, "
            f"Grads={row['college_labor_force']:,.0f}k)"
        )

    # Trend
    first = merged["info_jobs_per_grad"].iloc[0]
    last = merged["info_jobs_per_grad"].iloc[-1]
    pct = (last - first) / first * 100
    print(f"\n  Change over window: {pct:+.1f}%")

    output_path = data_dir / "info_jobs_per_grad.csv"
    merged.to_csv(output_path, index=False)
    print(f"\n✓ Saved to {output_path}")


if __name__ == "__main__":
    fetch_info_jobs_per_grad_data()
