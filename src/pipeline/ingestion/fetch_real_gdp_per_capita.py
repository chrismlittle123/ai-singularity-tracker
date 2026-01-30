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


def fetch_real_gdp_per_capita_data():
    """Fetch real GDP per capita data from FRED and save to data directory."""
    url = build_fred_url("A939RX0Q048SBEA", frequency="Quarterly")

    # Fetch data using utility
    df_recent = fetch_fred_data(
        url=url, data_name="real_gdp_per_capita", column_name="real_gdp_per_capita", quarters=14
    )

    # Analyze trends
    analyze_trend(df_recent, "real_gdp_per_capita")

    return df_recent


if __name__ == "__main__":
    fetch_real_gdp_per_capita_data()
