import sys
from datetime import datetime
from io import StringIO
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pandas as pd
import requests

# FRED series for occupation/industry employment (thousands)
# CPS occupation groups (LNU02032xxx) = household survey, by occupation
# CES industry groups (CEUxxxxxxx) = establishment survey, by industry

AI_TARGETABLE_SERIES = {
    "LNU02032207": ("Office & Admin Support", 1.0),
    "LNU02032213": ("Legal Occupations", 1.0),
    "LNU02032205": ("Sales & Related", 1.0),
    "LNU02034560": ("Computer & Math Occupations", 1.0),
}

# Non-automatable series with demographic correction weights.
# Healthcare growth is ~70% driven by aging population (Census Bureau
# population projections vs BLS healthcare employment projections).
# We downweight healthcare to isolate the automation-resistance signal
# from the demographic tailwind.
NON_AUTOMATABLE_SERIES = {
    "CEU2000000001": ("Construction", 1.0),  # Not demographic
    "CEU7000000001": ("Leisure & Hospitality", 1.0),  # Not demographic
    "CEU4300000001": ("Transportation & Warehousing", 1.0),  # Not demographic
    "CEU6562000001": ("Health Care & Social Assistance", 0.3),  # ~70% demographic
    "LNU02032211": ("Healthcare Support", 0.2),  # ~80% demographic
}


def build_fred_url(series_id: str) -> str:
    """Build a FRED CSV download URL with dynamic dates."""
    today = datetime.now().strftime("%Y-%m-%d")
    return (
        f"https://fred.stlouisfed.org/graph/fredgraph.csv?"
        f"id={series_id}&cosd=2015-01-01&coed={today}"
        f"&fq=Monthly&fam=avg&fgst=lin&transformation=lin"
        f"&vintage_date={today}&revision_date={today}&nd=2015-01-01"
    )


def fetch_series(series_id: str, name: str) -> pd.DataFrame | None:
    """Fetch a single FRED series and return as DataFrame."""
    url = build_fred_url(series_id)
    try:
        resp = requests.get(url, timeout=15)
        resp.raise_for_status()

        if "<!DOCTYPE" in resp.text[:100]:
            print(f"  ⚠ {series_id} ({name}): series not found on FRED")
            return None

        df = pd.read_csv(StringIO(resp.text))
        df.columns = ["date", "employment"]
        df["date"] = pd.to_datetime(df["date"])
        df["employment"] = pd.to_numeric(df["employment"], errors="coerce")
        df = df.dropna()

        if len(df) == 0:
            print(f"  ⚠ {series_id} ({name}): no data")
            return None

        print(
            f"  • {name}: {df['employment'].iloc[0]:.0f}k → "
            f"{df['employment'].iloc[-1]:.0f}k "
            f"({len(df)} months)"
        )
        return df

    except Exception as e:
        print(f"  ⚠ {series_id} ({name}): {e}")
        return None


def fetch_occupation_employment() -> None:
    """Fetch occupation-level employment data from FRED.

    Compares AI-targetable occupations against non-automatable ones,
    with demographic correction weights on healthcare sectors to avoid
    confusing population aging with automation resistance.

    AI-targetable: Office/Admin, Legal, Sales, Computer/Math
    Non-automatable: Construction, Leisure/Hospitality, Transportation,
                     Healthcare (downweighted for demographics)
    """
    data_dir = Path("data/raw/occupation_employment")
    data_dir.mkdir(parents=True, exist_ok=True)

    print("Fetching AI-targetable occupation employment...")
    ai_dfs = []
    for sid, (name, _weight) in AI_TARGETABLE_SERIES.items():
        df = fetch_series(sid, name)
        if df is not None:
            ai_dfs.append(df.rename(columns={"employment": sid}))

    print("\nFetching non-automatable occupation employment...")
    non_dfs = []
    non_weights = {}
    for sid, (name, weight) in NON_AUTOMATABLE_SERIES.items():
        df = fetch_series(sid, name)
        if df is not None:
            non_dfs.append(df.rename(columns={"employment": sid}))
            non_weights[sid] = weight
            if weight < 1.0:
                print(f"    ↳ Demographic correction: weight={weight:.1f}")

    if not ai_dfs or not non_dfs:
        print("  ⚠ Insufficient data to compute displacement index")
        return

    # Merge all AI-targetable series on date, sum employment (equal weight)
    ai_merged = ai_dfs[0]
    for extra_df in ai_dfs[1:]:
        ai_merged = pd.merge(ai_merged, extra_df, on="date", how="inner")

    ai_cols = [c for c in ai_merged.columns if c != "date"]
    ai_merged["ai_targetable"] = ai_merged[ai_cols].sum(axis=1)

    # Merge all non-automatable series, apply demographic correction weights
    non_merged = non_dfs[0]
    for extra_df in non_dfs[1:]:
        non_merged = pd.merge(non_merged, extra_df, on="date", how="inner")

    non_cols = [c for c in non_merged.columns if c != "date"]
    non_merged["non_automatable"] = sum(
        non_merged[col] * non_weights[col] for col in non_cols
    )

    # Combine into single DataFrame
    combined = pd.merge(
        ai_merged[["date", "ai_targetable"]],
        non_merged[["date", "non_automatable"]],
        on="date",
        how="inner",
    )
    combined = combined.sort_values("date").reset_index(drop=True)

    # Keep last 42 months (same as other monthly series)
    combined = combined.tail(42).reset_index(drop=True)

    print(f"\nCombined (demographic-corrected): {len(combined)} months")
    print(
        f"  AI-targetable: {combined['ai_targetable'].iloc[0]:.0f}k → "
        f"{combined['ai_targetable'].iloc[-1]:.0f}k"
    )
    print(
        f"  Non-automatable (weighted): "
        f"{combined['non_automatable'].iloc[0]:.0f}k → "
        f"{combined['non_automatable'].iloc[-1]:.0f}k"
    )

    output_path = data_dir / "occupation_employment.csv"
    combined.to_csv(output_path, index=False)
    print(f"\n✓ Saved to {output_path}")


if __name__ == "__main__":
    fetch_occupation_employment()
