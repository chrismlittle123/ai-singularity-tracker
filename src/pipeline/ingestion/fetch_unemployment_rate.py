import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from utils import analyze_trend, fetch_fred_data


def fetch_graduate_unemployment_rate_data():
    """Fetch graduate unemployment rate data from FRED and save to data directory."""
    # FRED URL for unemployment rate data (UNRATE) - monthly seasonally adjusted
    url = "https://fred.stlouisfed.org/graph/fredgraph.csv?bgcolor=%23ebf3fb&chart_type=line&drp=0&fo=open%20sans&graph_bgcolor=%23ffffff&height=450&mode=fred&recession_bars=on&txtcolor=%23444444&ts=12&tts=12&width=1320&nt=0&thu=0&trc=0&show_legend=yes&show_axis_titles=yes&show_tooltip=yes&id=UNRATE&scale=left&cosd=1947-01-01&coed=2025-12-01&line_color=%230073e6&link_values=false&line_style=solid&mark_type=none&mw=3&lw=3&ost=-99999&oet=99999&mma=0&fml=a&fq=Monthly&fam=avg&fgst=lin&fgsnd=2020-02-01&line_index=1&transformation=lin&vintage_date=2025-08-14&revision_date=2025-08-14&nd=1947-01-01"

    # Fetch data using utility (42 months for 3.5 years of monthly data)
    df_recent = fetch_fred_data(
        url=url, data_name="graduate_unemployment_rate", column_name="graduate_unemployment_rate", quarters=42
    )

    # Analyze trends
    analyze_trend(df_recent, "graduate_unemployment_rate")

    return df_recent


if __name__ == "__main__":
    fetch_graduate_unemployment_rate_data()