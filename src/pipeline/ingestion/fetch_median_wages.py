import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from utils import analyze_trend, fetch_fred_data


def build_fred_url(series_id, frequency="Quarterly"):
    """Build a FRED CSV download URL with dynamic dates."""
    today = datetime.now().strftime("%Y-%m-%d")
    return (
        f"https://fred.stlouisfed.org/graph/fredgraph.csv?"
        f"id={series_id}&cosd=1947-01-01&coed={today}"
        f"&fq={frequency}&fam=avg&fgst=lin&transformation=lin"
        f"&vintage_date={today}&revision_date={today}&nd=1947-01-01"
    )


def fetch_median_wages_data():
    """Fetch real median usual weekly earnings from FRED.

    FRED Series: LES1252881600Q — Employed full time: Median usual
    weekly real earnings: Wage and salary workers: 16 years and over.
    Quarterly frequency, Seasonally Adjusted. Constant 1982-84 dollars.
    Source: BLS (Current Population Survey).

    THE displacement outcome metric. If AI is replacing workers,
    real wages stagnate or decline even as productivity rises. If AI
    augments workers, wages accelerate. The divergence between TFP
    growth and wage growth is the clearest signal of who benefits
    from technological change.

    Historical growth: ~0.5-1%/yr. A sustained decline during
    productivity growth would be historically unprecedented.
    """
    url = build_fred_url("LES1252881600Q", frequency="Quarterly")

    df_recent = fetch_fred_data(
        url=url,
        data_name="median_wages",
        column_name="median_weekly_earnings",
        quarters=14,
    )

    analyze_trend(df_recent, "median_weekly_earnings")

    return df_recent


if __name__ == "__main__":
    fetch_median_wages_data()
