import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from utils import analyze_trend, fetch_fred_data


def build_fred_url(series_id, frequency="Monthly"):
    """Build a FRED CSV download URL with dynamic dates."""
    today = datetime.now().strftime("%Y-%m-%d")
    return (
        f"https://fred.stlouisfed.org/graph/fredgraph.csv?"
        f"id={series_id}&cosd=1947-01-01&coed={today}"
        f"&fq={frequency}&fam=avg&fgst=lin&transformation=lin"
        f"&vintage_date={today}&revision_date={today}&nd=1947-01-01"
    )


def fetch_prime_age_epop_data():
    """Fetch prime-age (25-54) employment-population ratio from FRED.

    FRED Series: LNS12300060 — Employment-Population Ratio, 25-54 years.
    Monthly frequency. Source: Bureau of Labor Statistics.

    The single most honest measure of whether working-age people are
    actually working. Not affected by discouraged workers leaving the
    labour force, part-time gig work masking underemployment, or
    definitional games in the unemployment rate.

    Healthy baseline: ~80%. A sustained decline during GDP growth is
    the signature of structural displacement — the economy thriving
    while workers suffer.
    """
    url = build_fred_url("LNS12300060", frequency="Monthly")

    df_recent = fetch_fred_data(
        url=url,
        data_name="prime_age_epop",
        column_name="prime_age_epop",
        quarters=42,
    )

    analyze_trend(df_recent, "prime_age_epop")

    return df_recent


if __name__ == "__main__":
    fetch_prime_age_epop_data()
