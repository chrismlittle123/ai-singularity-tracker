import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from utils import analyze_trend, fetch_fred_data


def build_fred_url(series_id: str, frequency: str = "Annual") -> str:
    """Build a FRED CSV download URL with dynamic dates."""
    today = datetime.now().strftime("%Y-%m-%d")
    return (
        f"https://fred.stlouisfed.org/graph/fredgraph.csv?"
        f"id={series_id}&cosd=1947-01-01&coed={today}"
        f"&fq={frequency}&fam=avg&fgst=lin&transformation=lin"
        f"&vintage_date={today}&revision_date={today}&nd=1947-01-01"
    )


def fetch_tfp_data() -> None:
    """Fetch Total Factor Productivity from FRED.

    Series MFPNFBS: Private Nonfarm Business Sector Total Factor Productivity.
    Annual index (2017=100). The smoking gun for AI takeoff — rising TFP
    with declining labor input means more output from less human work.
    """
    url = build_fred_url("MFPNFBS", frequency="Annual")

    df_recent = fetch_fred_data(
        url=url,
        data_name="tfp",
        column_name="tfp_index",
        quarters=15,  # 15 years of annual data
    )

    analyze_trend(df_recent, "tfp_index")


if __name__ == "__main__":
    fetch_tfp_data()
