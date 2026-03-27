from io import StringIO
from pathlib import Path

import pandas as pd
import requests

EIA_URL = "https://www.eia.gov/totalenergy/data/browser/csv.php?tbl=T07.06"

# Total retail electricity sales across all sectors
TARGET_MSN = "ESTCPUS"


def fetch_electricity_consumption() -> None:
    """Fetch US total electricity retail sales from EIA Monthly Energy Review.

    Uses Table 7.06 (ESTCPUS): Electricity Sales to Ultimate Customers, Total.
    Monthly data in Million Kilowatthours. This measures actual demand (consumption),
    not production — a better proxy for data center power draw.
    """
    data_dir = Path("data/raw/electricity_consumption")
    data_dir.mkdir(parents=True, exist_ok=True)

    print("Downloading electricity consumption data from EIA...")

    response = requests.get(EIA_URL, timeout=30)
    response.raise_for_status()

    df = pd.read_csv(StringIO(response.text))

    # Filter for total retail sales
    total = df[df["MSN"] == TARGET_MSN].copy()

    # Keep only monthly rows (YYYYMM where MM != 13; 13 = annual total)
    total["period"] = total["YYYYMM"].astype(str)
    monthly = total[~total["period"].str.endswith("13")].copy()
    monthly = monthly[monthly["Value"] != "Not Available"]
    monthly["Value"] = pd.to_numeric(monthly["Value"])

    # Parse YYYYMM into date
    monthly["date"] = pd.to_datetime(
        monthly["YYYYMM"].astype(str), format="%Y%m"
    )
    monthly = monthly.sort_values("date").reset_index(drop=True)

    # Keep last 42 months
    monthly = monthly.tail(42).reset_index(drop=True)

    result = monthly[["date", "Value"]].copy()
    result.columns = ["date", "electricity_consumption"]

    print("\nData Summary:")
    print(f"  • Records: {len(result)}")
    print(f"  • Date range: {result['date'].min()} to {result['date'].max()}")
    print(
        f"  • Latest: {result.iloc[-1]['electricity_consumption']:,.0f} "
        f"million kWh ({result.iloc[-1]['date'].strftime('%Y-%m')})"
    )

    output_path = data_dir / "electricity_consumption_last_42_months.csv"
    result.to_csv(output_path, index=False)
    print(f"\n✓ Saved to {output_path}")


if __name__ == "__main__":
    fetch_electricity_consumption()
