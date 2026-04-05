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


def fetch_it_equipment_investment_data():
    """Fetch real private fixed investment in information processing equipment.

    FRED Series: Y033RC1Q027SBEA — Real Private Nonresidential Fixed
    Investment: Equipment: Information Processing Equipment.
    Quarterly frequency, Seasonally Adjusted Annual Rate (Billions of
    Chained 2017 Dollars). Source: BEA (NIPA Table 5.3.6).

    Measures capital flowing into compute hardware — servers, GPUs,
    networking equipment. Broader than NVIDIA alone (captures all
    vendors) and directly measures the economy-wide bet on information
    mastery from Castleforge's energy-information framework.

    The Jevons Paradox argument predicts this will keep rising even as
    AI efficiency improves. Sustained acceleration above the historical
    ~3-5%/yr trend signals structural shift toward capital-over-labor.
    """
    url = build_fred_url("Y033RC1Q027SBEA", frequency="Quarterly")

    df_recent = fetch_fred_data(
        url=url,
        data_name="it_equipment_investment",
        column_name="it_equipment_investment",
        quarters=14,
    )

    analyze_trend(df_recent, "it_equipment_investment")

    return df_recent


if __name__ == "__main__":
    fetch_it_equipment_investment_data()
