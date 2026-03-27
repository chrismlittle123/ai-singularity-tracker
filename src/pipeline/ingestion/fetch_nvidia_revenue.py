from pathlib import Path

import pandas as pd
import requests

NVIDIA_CIK = "0001045810"
SEC_EDGAR_URL = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{NVIDIA_CIK}.json"

# SEC requires a descriptive User-Agent header
SEC_HEADERS = {
    "User-Agent": "AITracker research@example.com",
    "Accept": "application/json",
}


def fetch_nvidia_revenue():
    """Fetch NVIDIA quarterly revenue from SEC EDGAR XBRL API.

    Uses total revenue (Revenues tag) as proxy for AI compute buildout since
    NVIDIA's Data Center segment is ~90% of revenue. Extracts single-quarter
    entries (90-day periods) from 10-Q and 10-K filings. For Q4, derives the
    value by subtracting the 9-month cumulative from the annual total.
    """
    data_dir = Path("data/raw/nvidia_revenue")
    data_dir.mkdir(parents=True, exist_ok=True)
    output_path = data_dir / "nvidia_quarterly_revenue.csv"

    print("Downloading NVIDIA financial data from SEC EDGAR...")

    response = requests.get(SEC_EDGAR_URL, headers=SEC_HEADERS, timeout=30)
    response.raise_for_status()

    facts = response.json()
    us_gaap = facts.get("facts", {}).get("us-gaap", {})

    # Revenues tag has the most complete data through current filings
    if "Revenues" not in us_gaap:
        print("  ⚠ Could not find Revenues data in XBRL filing")
        return None

    revenue_data = us_gaap["Revenues"]
    usd_data = revenue_data.get("units", {}).get("USD", [])

    if not usd_data:
        print("  ⚠ No USD revenue data found")
        return None

    print("  • Found revenue using XBRL tag: Revenues")

    # Categorize entries by period length
    quarterly = {}  # 90-day periods (single quarter)
    annual = {}  # 363-day periods (full year)
    nine_month = {}  # 272-day periods (3 quarters cumulative)

    for entry in usd_data:
        start = entry.get("start")
        end = entry.get("end")
        val = entry.get("val")
        form = entry.get("form", "")

        if not all([start, end, val]):
            continue
        if form not in ("10-Q", "10-K"):
            continue

        start_date = pd.to_datetime(start)
        end_date = pd.to_datetime(end)
        period_days = (end_date - start_date).days

        key = end_date.strftime("%Y-%m-%d")

        if 80 <= period_days <= 100:
            quarterly[key] = {
                "period_end": end_date,
                "revenue_millions": val / 1_000_000,
            }
        elif 355 <= period_days <= 370:
            annual[key] = {
                "period_end": end_date,
                "revenue_millions": val / 1_000_000,
                "start": start_date,
            }
        elif 265 <= period_days <= 280:
            nine_month[key] = {
                "revenue_millions": val / 1_000_000,
                "start": start_date,
            }

    # Derive Q4 values: annual - 9-month cumulative
    for ann_key, ann_data in annual.items():
        if ann_key in quarterly:
            continue  # Already have a quarterly entry for this end date

        # Find matching 9-month entry (same fiscal year start)
        for nm_data in nine_month.values():
            if nm_data["start"] == ann_data["start"]:
                q4_revenue = ann_data["revenue_millions"] - nm_data["revenue_millions"]
                quarterly[ann_key] = {
                    "period_end": ann_data["period_end"],
                    "revenue_millions": q4_revenue,
                }
                break

    if not quarterly:
        print("  ⚠ No quarterly revenue records found")
        return None

    df = pd.DataFrame(list(quarterly.values()))
    df = df.sort_values("period_end").reset_index(drop=True)

    # Keep last 14 quarters
    df = df.tail(14).reset_index(drop=True)

    # Add date column for consistency with other pipeline scripts
    df["date"] = df["period_end"]
    df = df[["date", "revenue_millions"]]

    print("\nData Summary:")
    print(f"  • Quarters found: {len(df)}")
    print(f"  • Date range: {df['date'].min()} to {df['date'].max()}")
    print(f"  • Latest revenue: ${df.iloc[-1]['revenue_millions']:,.0f}M")

    print("\nQuarterly Revenue:")
    for _, row in df.iterrows():
        print(f"  • {row['date'].strftime('%Y-%m-%d')}: ${row['revenue_millions']:,.0f}M")

    df.to_csv(output_path, index=False)
    print(f"\n✓ Saved to {output_path}")

    return df


if __name__ == "__main__":
    fetch_nvidia_revenue()
