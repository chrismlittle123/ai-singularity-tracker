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


def fetch_software_investment_data():
    """Fetch real private fixed investment in software from FRED.

    FRED Series: B985RC1Q027SBEA — Real Private Nonresidential Fixed
    Investment: Intellectual Property Products: Software.
    Quarterly frequency, Seasonally Adjusted Annual Rate (Billions of
    Chained 2017 Dollars). Source: BEA (NIPA Table 5.3.6).

    Captures the software side of AI capex — cloud AI services,
    enterprise AI platforms, SaaS tools. Complements IT equipment
    investment (hardware). Together they measure total AI-related
    capital spending from both the hardware and software sides.

    Historical growth: ~5-7%/yr. Sustained acceleration to ~12%/yr+
    would signal the economy is structurally shifting spend toward
    AI/information systems.
    """
    url = build_fred_url("B985RC1Q027SBEA", frequency="Quarterly")

    df_recent = fetch_fred_data(
        url=url,
        data_name="software_investment",
        column_name="software_investment",
        quarters=14,
    )

    analyze_trend(df_recent, "software_investment")

    return df_recent


if __name__ == "__main__":
    fetch_software_investment_data()
