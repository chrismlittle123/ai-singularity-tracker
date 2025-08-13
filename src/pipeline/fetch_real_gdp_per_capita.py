from .utils import analyze_trend, fetch_fred_data


def fetch_real_gdp_per_capita_data():
    """Fetch real GDP per capita data from FRED and save to data directory."""
    # Exact URL from README for real GDP per capita data (A939RX0Q048SBEA)
    url = "https://fred.stlouisfed.org/graph/fredgraph.csv?bgcolor=%23ebf3fb&chart_type=line&drp=0&fo=open%20sans&graph_bgcolor=%23ffffff&height=450&mode=fred&recession_bars=on&txtcolor=%23444444&ts=12&tts=12&width=1320&nt=0&thu=0&trc=0&show_legend=yes&show_axis_titles=yes&show_tooltip=yes&id=A939RX0Q048SBEA&scale=left&cosd=1947-01-01&coed=2025-04-01&line_color=%230073e6&link_values=false&line_style=solid&mark_type=none&mw=3&lw=3&ost=-99999&oet=99999&mma=0&fml=a&fq=Quarterly&fam=avg&fgst=lin&fgsnd=2020-02-01&line_index=1&transformation=lin&vintage_date=2025-08-13&revision_date=2025-08-13&nd=1947-01-01"

    # Fetch data using utility
    df_recent = fetch_fred_data(
        url=url,
        data_name="real_gdp_per_capita",
        column_name="real_gdp_per_capita",
        quarters=14
    )

    # Analyze trends
    analyze_trend(df_recent, "real_gdp_per_capita")

    return df_recent


if __name__ == "__main__":
    fetch_real_gdp_per_capita_data()
