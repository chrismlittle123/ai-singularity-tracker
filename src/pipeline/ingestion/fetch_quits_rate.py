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


def fetch_quits_rate_data():
    """Fetch total nonfarm quits rate from FRED (JOLTS).

    FRED Series: JTSQUR — Quits: Total Nonfarm, Rate,
    Seasonally Adjusted. Monthly frequency. Source: BLS (JOLTS).

    The earliest sentiment indicator of labour market distress.
    People quit when they're confident they can find something
    better. A falling quits rate in a growing economy means
    workers feel trapped — staying in bad jobs because the
    alternative is worse.

    Pre-pandemic normal: ~2.2-2.4%. Post-pandemic peak: ~3.0%.
    A sustained decline to ~1.4% would signal severe structural
    distress — below even the 2008-2009 trough.
    """
    url = build_fred_url("JTSQUR", frequency="Monthly")

    df_recent = fetch_fred_data(
        url=url,
        data_name="quits_rate",
        column_name="quits_rate",
        quarters=42,
    )

    analyze_trend(df_recent, "quits_rate")

    return df_recent


if __name__ == "__main__":
    fetch_quits_rate_data()
