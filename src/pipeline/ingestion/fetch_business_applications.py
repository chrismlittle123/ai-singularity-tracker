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


def fetch_business_applications_data():
    """Fetch new business applications data from FRED.

    FRED Series: BABATOTALSAUS — Business Applications for Employer
    Identification Numbers, Total for All NAICS, Seasonally Adjusted.
    Monthly frequency. Source: Census Bureau.

    High new business formation indicates reinstatement is working
    (new tasks/industries emerging to offset displacement).
    Sustained decline alongside displacement signals suggests
    automation without offsetting job creation.

    Reference: Acemoglu & Restrepo (2019) reinstatement effect.
    """
    url = build_fred_url("BABATOTALSAUS", frequency="Monthly")

    df_recent = fetch_fred_data(
        url=url,
        data_name="business_applications",
        column_name="business_applications",
        quarters=42,
    )

    analyze_trend(df_recent, "business_applications")

    return df_recent


if __name__ == "__main__":
    fetch_business_applications_data()
