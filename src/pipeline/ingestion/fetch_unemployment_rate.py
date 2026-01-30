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


def fetch_graduate_unemployment_rate_data():
    """Fetch graduate unemployment rate data from FRED and save to data directory."""
    url = build_fred_url("CGAD2534", frequency="Monthly")

    # Fetch data using utility (42 months for 3.5 years of monthly data)
    df_recent = fetch_fred_data(
        url=url, data_name="graduate_unemployment_rate", column_name="graduate_unemployment_rate", quarters=42
    )

    # Analyze trends
    analyze_trend(df_recent, "graduate_unemployment_rate")

    return df_recent


if __name__ == "__main__":
    fetch_graduate_unemployment_rate_data()
