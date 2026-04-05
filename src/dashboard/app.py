from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# Page config
st.set_page_config(
    page_title="AI Singularity Tracker",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.title("🤖 AI Singularity Tracker")
st.markdown(
    "**Monitoring whether AI investment is producing "
    "broad-based gains or concentrated displacement**"
)

# --- Takeoff criteria ---
# Each defines a 3-year threshold that would be historically abnormal.
# Organized into three categories: Smoking Guns, Displacement Effects, Investment Causes.
TAKEOFF_THRESHOLDS = {
    # STRUCTURAL SHIFTS — hardest to explain without AI
    "tfp": {
        "label": "TFP Acceleration",
        "threshold": 6.0,
        "early_threshold": 2.0,
        "unit": "%",
        "direction": "rise",
        "weight": 0.14,
        "frequency": "annual",
        "rationale": (
            "TFP grows ~1%/yr historically. 2%/yr sustained (6% over 3 years) "
            "means more output from the same inputs — the productivity signature of AI."
        ),
    },
    "occupation_gap": {
        "label": "AI Job Displacement Gap",
        "threshold": 15.0,
        "early_threshold": 5.0,
        "unit": "pp",
        "direction": "rise",
        "weight": 0.13,
        "frequency": "quarterly",
        "rationale": (
            "If AI-targetable occupations (office, legal, sales, tech) decline "
            "while non-automatable (construction, healthcare) grow, a 15pp gap "
            "over 3 years would be structural, not cyclical."
        ),
    },
    "capital_labor": {
        "label": "Capital-Labor Substitution",
        "threshold": 12.0,
        "early_threshold": 4.0,
        "unit": "%",
        "direction": "rise",
        "weight": 0.10,
        "frequency": "annual",
        "rationale": (
            "The capital-to-labor ratio rises ~1-2%/yr normally. "
            "4%/yr (12% over 3 years) means firms are actively "
            "replacing workers with capital (AI/software)."
        ),
    },
    # WAGE & DISTRIBUTION — who benefits from AI gains
    "median_wages": {
        "label": "Real Median Wage Decline",
        "threshold": 5.0,
        "early_threshold": 1.5,
        "unit": "%",
        "direction": "decline",
        "weight": 0.09,
        "frequency": "quarterly",
        "rationale": (
            "Real median weekly earnings grow ~0.5-1%/yr historically. "
            "A 5% decline over 3 years during productivity growth would be "
            "THE displacement outcome — the economy growing while workers "
            "get poorer. The single most important metric for whether AI "
            "is helping or hurting people."
        ),
    },
    "info_jobs_per_grad": {
        "label": "Knowledge Jobs per Graduate Decline",
        "threshold": 20.0,
        "early_threshold": 8.0,
        "unit": "%",
        "direction": "decline",
        "weight": 0.07,
        "frequency": "quarterly",
        "rationale": (
            "Information sector employment divided by college-educated "
            "labor force. Directly measures whether the knowledge economy "
            "is creating or destroying demand for graduates. Unlike wages "
            "(which reflect survivors), this catches structural erosion: "
            "fewer knowledge jobs chasing more graduates. A 20% decline "
            "over 3 years would signal the knowledge economy is contracting "
            "relative to the educated workforce — the demand-side "
            "displacement signal that wage data misses entirely."
        ),
    },
    "labor_share": {
        "label": "Labor Share Decline",
        "threshold": 5.0,
        "early_threshold": 1.7,
        "unit": "pp",
        "direction": "decline",
        "weight": 0.06,
        "frequency": "quarterly",
        "rationale": (
            "Labor share declined ~5pp over 15 years (2000-2015). "
            "5pp in 3 years = 5x the historical rate."
        ),
    },
    # LABOUR MARKET HEALTH — the human cost metrics
    "prime_age_epop": {
        "label": "Prime-Age EPOP Decline",
        "threshold": 3.0,
        "early_threshold": 1.0,
        "unit": "pp",
        "direction": "decline",
        "weight": 0.08,
        "frequency": "quarterly",
        "rationale": (
            "Prime-age (25-54) employment-population ratio is ~80% "
            "when healthy. A 3pp decline during GDP growth is the "
            "signature of structural displacement — the economy "
            "thriving while workers suffer. Cannot be gamed by "
            "discouraged workers leaving the labour force."
        ),
    },
    "quits_rate": {
        "label": "Quits Rate Decline",
        "threshold": 0.8,
        "early_threshold": 0.3,
        "unit": "pp",
        "direction": "decline",
        "weight": 0.07,
        "frequency": "quarterly",
        "rationale": (
            "Workers quit when they're confident they can find "
            "something better. A 0.8pp decline (from ~2.2% to ~1.4%) "
            "in a growing economy means workers feel trapped — the "
            "earliest sentiment indicator of labour market distress."
        ),
    },
    "unemployment": {
        "label": "College Unemployment Rise",
        "threshold": 2.0,
        "early_threshold": 0.7,
        "unit": "pp",
        "direction": "rise",
        "weight": 0.07,
        "frequency": "quarterly",
        "rationale": (
            "College-educated unemployment is typically 2-3%. "
            "A 2pp rise (to 4-5%) would be structurally abnormal."
        ),
    },
    # AI INVESTMENT SCALE — the cause indicators
    "nvidia": {
        "label": "NVIDIA Quarterly Revenue",
        "threshold": 200000.0,  # $200B/quarter ($800B/yr)
        "early_threshold": 67000.0,  # ~$67B/quarter
        "unit": "$M",
        "direction": "rise",
        "weight": 0.08,
        "frequency": "quarterly",
        "metric_type": "level",  # Absolute level, not growth rate
        "rationale": (
            "$200B/quarter = ~$800B/yr from one AI chip company. "
            "At that scale, AI compute spending is ~3-4% of US GDP. "
            "Note: revenue measures compute spending, not deployment type — "
            "the same hardware could power automation or augmentation."
        ),
    },
    "it_equipment": {
        "label": "IT Equipment Investment Growth",
        "threshold": 30.0,
        "early_threshold": 10.0,
        "unit": "%",
        "direction": "rise",
        "weight": 0.06,
        "frequency": "quarterly",
        "rationale": (
            "Real private investment in information processing equipment "
            "grows ~3-5%/yr historically. 10%/yr sustained (30% over 3 years) "
            "signals a structural shift toward capital-over-labor. Broader "
            "than NVIDIA alone (captures all vendors). The hardware side "
            "of AI capex."
        ),
    },
    "software_investment": {
        "label": "Software Investment Growth",
        "threshold": 40.0,
        "early_threshold": 15.0,
        "unit": "%",
        "direction": "rise",
        "weight": 0.05,
        "frequency": "quarterly",
        "rationale": (
            "Real private investment in software grows ~5-7%/yr historically. "
            "~12%/yr sustained (40% over 3 years) signals massive capital "
            "reallocation toward AI/software systems. Captures cloud AI, "
            "enterprise platforms, SaaS tools — the software side of AI "
            "capex that hardware metrics miss."
        ),
    },
}

CONSISTENCY_TARGET = 0.75
METRIC_CATEGORIES = {
    "Structural Shifts": ["tfp", "occupation_gap", "capital_labor"],
    "Wage & Distribution": ["median_wages", "info_jobs_per_grad", "labor_share"],
    "Labour Market Health": ["prime_age_epop", "quits_rate", "unemployment"],
    "AI Investment Scale": ["nvidia", "it_equipment", "software_investment"],
}

CATEGORY_ICONS = {
    "Structural Shifts": "🔬",
    "Wage & Distribution": "💰",
    "Labour Market Health": "🏥",
    "AI Investment Scale": "📈",
}


def load_optional(data_dir: Path, subdir: str, filename: str):
    """Load a CSV if it exists, add date column, return df or None."""
    path = data_dir / subdir / filename
    if not path.exists():
        return None
    df = pd.read_csv(path)
    df["date"] = pd.to_datetime(df[["year", "month"]].assign(day=1))
    return df


@st.cache_data(ttl=3600)
def load_data():
    """Load all processed datasets."""
    d = Path("data/processed")

    labor = pd.read_csv(d / "labor_share" / "labor_share_processed.csv")
    labor["date"] = pd.to_datetime(labor[["year", "month"]].assign(day=1))

    gdp = pd.read_csv(d / "real_gdp_per_capita" / "real_gdp_per_capita_processed.csv")
    gdp["date"] = pd.to_datetime(gdp[["year", "month"]].assign(day=1))

    unemp = load_optional(
        d,
        "graduate_unemployment_rate",
        "graduate_unemployment_rate_processed.csv",
    )
    nvidia = load_optional(d, "nvidia_revenue", "nvidia_revenue_processed.csv")
    tfp = load_optional(d, "tfp", "tfp_processed.csv")
    cap_lab = load_optional(d, "capital_labor", "capital_labor_processed.csv")
    occ = load_optional(d, "occupation_employment", "occupation_employment_processed.csv")
    biz_apps = load_optional(d, "business_applications", "business_applications_processed.csv")
    epop = load_optional(d, "prime_age_epop", "prime_age_epop_processed.csv")
    quits = load_optional(d, "quits_rate", "quits_rate_processed.csv")
    it_equip = load_optional(
        d,
        "it_equipment_investment",
        "it_equipment_investment_processed.csv",
    )
    median_wages = load_optional(d, "median_wages", "median_wages_processed.csv")
    info_jobs = load_optional(
        d,
        "info_jobs_per_grad",
        "info_jobs_per_grad_processed.csv",
    )
    software_inv = load_optional(
        d,
        "software_investment",
        "software_investment_processed.csv",
    )

    return {
        "labor_share": labor,
        "gdp_per_capita": gdp,
        "unemployment": unemp,
        "nvidia": nvidia,
        "tfp": tfp,
        "capital_labor": cap_lab,
        "occupation": occ,
        "business_applications": biz_apps,
        "prime_age_epop": epop,
        "quits_rate": quits,
        "it_equipment": it_equip,
        "median_wages": median_wages,
        "info_jobs_per_grad": info_jobs,
        "software_investment": software_inv,
    }


def align_to_quarterly(df):
    """Convert monthly data to quarterly (last month of each quarter)."""
    df_copy = df.copy()
    q = df_copy[df_copy["date"].dt.month.isin([3, 6, 9, 12])].copy()
    return q.sort_values("date").reset_index(drop=True)


def compute_3yr_change(df, col, use_absolute=False, frequency="quarterly"):
    """Compute 3-year change. Handles quarterly (12 periods) and annual (3 periods)."""
    df_sorted = df.sort_values("date").reset_index(drop=True)
    lookback = 3 if frequency == "annual" else 12

    if len(df_sorted) <= lookback:
        return None

    current = df_sorted[col].iloc[-1]
    past = df_sorted[col].iloc[-(lookback + 1)]

    if use_absolute:
        return current - past
    if past == 0:
        return None
    return ((current - past) / past) * 100


def compute_consistency(df, col, direction="rise"):
    """Fraction of period-over-period changes in the expected direction."""
    df_sorted = df.sort_values("date").reset_index(drop=True)
    if len(df_sorted) < 2:
        return None

    changes = df_sorted[col].diff().dropna()
    if len(changes) == 0:
        return None

    if direction == "decline":
        correct = (changes < 0).sum()
    else:
        correct = (changes > 0).sum()
    return correct / len(changes)


def compute_takeoff_metrics(datasets):
    """Compute progress toward takeoff for each metric."""
    results = {}

    # Map threshold keys to (dataframe, column, use_absolute)
    metric_configs = {
        "tfp": ("tfp", "tfp_index", False),
        "occupation_gap": ("occupation_q", "displacement_gap", True),
        "capital_labor": ("capital_labor", "capital_labor_ratio", False),
        "median_wages": ("median_wages", "median_weekly_earnings", False),
        "info_jobs_per_grad": ("info_jobs_per_grad_q", "info_jobs_per_grad", False),
        "labor_share": ("labor_share", "labor_share_index", True),
        "prime_age_epop": ("prime_age_epop_q", "prime_age_epop", True),
        "quits_rate": ("quits_rate_q", "quits_rate", True),
        "unemployment": ("unemployment_q", "graduate_unemployment_rate", True),
        "nvidia": ("nvidia", "revenue_millions", False),
        "it_equipment": ("it_equipment", "it_equipment_investment", False),
        "software_investment": ("software_investment", "software_investment", False),
    }

    for key, (ds_key, col, use_abs) in metric_configs.items():
        df = datasets.get(ds_key)
        if df is None or len(df) == 0:
            continue
        if key not in TAKEOFF_THRESHOLDS:
            continue

        info = TAKEOFF_THRESHOLDS[key]
        freq = info["frequency"]
        metric_type = info.get("metric_type", "change")

        cons = compute_consistency(df, col, direction=info["direction"])
        if cons is None:
            continue

        if metric_type == "level":
            # Absolute level: progress = current value / threshold
            df_sorted = df.sort_values("date").reset_index(drop=True)
            current_val = df_sorted[col].iloc[-1]
            progress = max(0.0, current_val / info["threshold"])
            raw_change = current_val
            effective = current_val
        else:
            # Change-based: progress = 3yr change / threshold
            raw = compute_3yr_change(df, col, use_absolute=use_abs, frequency=freq)
            if raw is None:
                continue
            effective = -raw if info["direction"] == "decline" else raw
            progress = max(0.0, effective / info["threshold"])
            raw_change = raw

        score = progress * cons

        results[key] = {
            "progress": progress,
            "consistency": cons,
            "score": score,
            "raw_change": raw_change,
            "effective_change": effective,
            "threshold": info["threshold"],
        }

    return results


def compute_takeoff_score(metrics):
    """Compute overall takeoff score (0-100)."""
    if not metrics:
        return 0.0

    total_w = 0.0
    weighted_sum = 0.0
    for key, data in metrics.items():
        w = TAKEOFF_THRESHOLDS[key]["weight"]
        weighted_sum += w * min(1.0, data["score"])
        total_w += w

    if total_w == 0:
        return 0.0

    base = weighted_sum / total_w
    active = sum(1 for d in metrics.values() if d["score"] > 0.3)
    coherence = 0.5 + 0.5 * (active / len(TAKEOFF_THRESHOLDS))
    return min(100.0, base * coherence * 100)


def compute_compensation_health(labor_share_df, gdp_df):
    """Derive compensation health from existing labor share and GDP data.

    Positive = gains shared broadly (reinstatement working).
    Negative = gains concentrating in capital (compensation failing).
    Based on Acemoglu-Restrepo (2019) reinstatement framework.
    """
    ls = labor_share_df.sort_values("date").reset_index(drop=True)
    gd = gdp_df.sort_values("date").reset_index(drop=True)

    merged = pd.merge(
        ls[["date", "labor_share_index"]],
        gd[["date", "real_gdp_per_capita"]],
        on="date",
    )

    # YoY changes (4-quarter lag for quarterly data)
    merged["gdp_growth"] = merged["real_gdp_per_capita"].pct_change(4) * 100
    merged["ls_change"] = merged["labor_share_index"].diff(4)
    merged["compensation_health"] = merged["gdp_growth"] + merged["ls_change"]

    return merged.dropna(subset=["compensation_health"])


def compute_diffusion_index(metrics, threshold_level="early"):
    """Count how many metrics simultaneously show signals.

    threshold_level: "early" (progress >= early/full ratio) or "full" (progress >= 1.0)
    Returns (count, total, fraction).
    """
    cutoff = 0.33 if threshold_level == "early" else 1.0
    active = sum(1 for m in metrics.values() if m["progress"] >= cutoff)
    total = len(TAKEOFF_THRESHOLDS)
    return active, total, active / total if total > 0 else 0


def make_chart(df, x, y, title, labels, color, chart_type="line"):
    """Create a styled plotly chart."""
    if chart_type == "bar":
        fig = px.bar(df, x=x, y=y, title=title, labels=labels)
        fig.update_traces(marker_color=color)
    else:
        fig = px.line(df, x=x, y=y, title=title, labels=labels)
        fig.update_traces(line=dict(color=color, width=3))
    fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(size=12),
        showlegend=False,
    )
    return fig


# --- Dashboard rendering ---
try:
    data = load_data()

    tab1, tab2, tab3, tab4 = st.tabs(
        [
            "📈 Time Series Charts",
            "🎯 Transformation Analysis",
            "🔮 Scenario Projections",
            "📚 Methodology",
        ]
    )

    with tab1:
        st.header("Economic Indicators Over Time")

        # Organize charts by category
        st.subheader("🔬 Structural Shift Indicators")

        if data["tfp"] is not None:
            st.plotly_chart(
                make_chart(
                    data["tfp"],
                    "date",
                    "tfp_index",
                    "Total Factor Productivity (2017=100)",
                    {"date": "Date", "tfp_index": "TFP Index"},
                    "#e377c2",
                ),
                use_container_width=True,
            )
            st.caption(
                "📊 [FRED MFPNFBS]"
                "(https://fred.stlouisfed.org/series/MFPNFBS)"
                " — Annual, BLS Multifactor Productivity"
            )

        if data["capital_labor"] is not None:
            st.plotly_chart(
                make_chart(
                    data["capital_labor"],
                    "date",
                    "capital_labor_ratio",
                    "Capital-to-Labor Input Ratio (2017=1.0)",
                    {"date": "Date", "capital_labor_ratio": "Ratio"},
                    "#17becf",
                ),
                use_container_width=True,
            )
            st.caption(
                "📊 [FRED MPU4910042/MPU4910052]"
                "(https://fred.stlouisfed.org/series/MPU4910042)"
                " — Annual, BLS MFP Dataset"
            )

        if data["occupation"] is not None:
            occ = data["occupation"]

            # Primary chart: the displacement gap (shaded area)
            fig_gap = go.Figure()

            # Shaded area between the two lines
            fig_gap.add_trace(
                go.Scatter(
                    x=occ["date"],
                    y=occ["non_automatable_index"],
                    name="Non-Automatable",
                    line=dict(color="#2ca02c", width=3),
                    mode="lines",
                )
            )
            fig_gap.add_trace(
                go.Scatter(
                    x=occ["date"],
                    y=occ["ai_targetable_index"],
                    name="AI-Targetable",
                    line=dict(color="#d62728", width=3),
                    fill="tonexty",
                    fillcolor="rgba(214, 39, 40, 0.15)",
                    mode="lines",
                )
            )
            # Baseline at 100
            fig_gap.add_hline(
                y=100,
                line_dash="dot",
                line_color="#999",
                annotation_text="Baseline",
                annotation_position="bottom left",
            )

            # Annotate the current gap
            latest = occ.iloc[-1]
            gap_val = latest["displacement_gap"]
            fig_gap.add_annotation(
                x=latest["date"],
                y=(latest["non_automatable_index"] + latest["ai_targetable_index"]) / 2,
                text=f"Gap: {gap_val:+.1f}pp",
                showarrow=True,
                arrowhead=2,
                ax=60,
                ay=0,
                font=dict(size=14, color="#d62728"),
                bgcolor="white",
                bordercolor="#d62728",
                borderwidth=1,
            )

            fig_gap.update_layout(
                title="AI Displacement Gap: AI-Targetable vs Non-Automatable Jobs",
                plot_bgcolor="white",
                paper_bgcolor="white",
                font=dict(size=12),
                yaxis_title="Employment Index (start = 100)",
                xaxis_title="Date",
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="center",
                    x=0.5,
                ),
            )
            st.plotly_chart(fig_gap, use_container_width=True)

            # Secondary chart: the gap itself as a bar chart
            fig_gap_bars = go.Figure()
            colors = ["#d62728" if g > 0 else "#2ca02c" for g in occ["displacement_gap"]]
            fig_gap_bars.add_trace(
                go.Bar(
                    x=occ["date"],
                    y=occ["displacement_gap"],
                    marker_color=colors,
                    name="Displacement Gap",
                )
            )
            # Threshold line at 15pp
            fig_gap_bars.add_hline(
                y=15,
                line_dash="dash",
                line_color="red",
                annotation_text="Takeoff threshold (15pp)",
                annotation_position="top left",
            )
            fig_gap_bars.add_hline(y=0, line_color="#999", line_width=1)

            fig_gap_bars.update_layout(
                title="Displacement Gap Over Time (Non-Automatable - AI-Targetable)",
                plot_bgcolor="white",
                paper_bgcolor="white",
                font=dict(size=12),
                yaxis_title="Gap (pp)",
                xaxis_title="Date",
                showlegend=False,
            )
            st.plotly_chart(fig_gap_bars, use_container_width=True)

            st.caption(
                "📊 FRED CPS/CES — **AI-Targetable**: Office/Admin, Legal, "
                "Sales, Computer/Math | **Non-Automatable**: Construction, "
                "Healthcare, Healthcare Support | "
                "Red shading = gap widening (displacement signal)"
            )

        st.subheader("💰 Wage & Distribution")

        if data["median_wages"] is not None:
            st.plotly_chart(
                make_chart(
                    data["median_wages"],
                    "date",
                    "median_weekly_earnings",
                    "Real Median Weekly Earnings (constant 1982-84 $)",
                    {"date": "Date", "median_weekly_earnings": "$ (real)"},
                    "#2ca02c",
                ),
                use_container_width=True,
            )
            st.caption(
                "📊 [FRED LES1252881600Q]"
                "(https://fred.stlouisfed.org/series/LES1252881600Q)"
                " — Quarterly, BLS CPS. THE displacement outcome metric. "
                "Declining real wages during productivity growth = the "
                "economy growing while workers get poorer."
            )

        if data["info_jobs_per_grad"] is not None:
            st.plotly_chart(
                make_chart(
                    data["info_jobs_per_grad"],
                    "date",
                    "info_jobs_per_grad",
                    "Knowledge Jobs per 100 Graduates (Info Sector / College Labor Force)",
                    {"date": "Date", "info_jobs_per_grad": "Jobs per 100 grads"},
                    "#d62728",
                ),
                use_container_width=True,
            )
            st.caption(
                "📊 FRED USINFO / LNS11027662"
                " — Monthly, BLS. Information sector employment divided "
                "by college-educated labor force. Declining ratio = fewer "
                "knowledge jobs chasing more graduates. Unlike wages "
                "(which reflect survivors), this catches structural "
                "demand erosion."
            )

        st.plotly_chart(
            make_chart(
                data["labor_share"],
                "date",
                "labor_share_index",
                "Labor Share of Income Index",
                {"date": "Date", "labor_share_index": "Index"},
                "#1f77b4",
            ),
            use_container_width=True,
        )
        st.caption("📊 [FRED PRS85006173](https://fred.stlouisfed.org/series/PRS85006173)")

        st.subheader("🏥 Labour Market Health")

        if data["prime_age_epop"] is not None:
            st.plotly_chart(
                make_chart(
                    data["prime_age_epop"],
                    "date",
                    "prime_age_epop",
                    "Prime-Age (25-54) Employment-Population Ratio",
                    {"date": "Date", "prime_age_epop": "% Employed"},
                    "#e377c2",
                ),
                use_container_width=True,
            )
            st.caption(
                "📊 [FRED LNS12300060]"
                "(https://fred.stlouisfed.org/series/LNS12300060)"
                " — Monthly, BLS. The most honest measure of whether "
                "working-age people are actually working. Decline during "
                "GDP growth = structural displacement."
            )

        if data["quits_rate"] is not None:
            st.plotly_chart(
                make_chart(
                    data["quits_rate"],
                    "date",
                    "quits_rate",
                    "Quits Rate (Total Nonfarm, JOLTS)",
                    {"date": "Date", "quits_rate": "Rate (%)"},
                    "#17becf",
                ),
                use_container_width=True,
            )
            st.caption(
                "📊 [FRED JTSQUR]"
                "(https://fred.stlouisfed.org/series/JTSQUR)"
                " — Monthly, BLS JOLTS. Workers quit when they can "
                "find something better. Declining quits in a growing "
                "economy = workers feel trapped."
            )

        if data["unemployment"] is not None:
            st.plotly_chart(
                make_chart(
                    data["unemployment"],
                    "date",
                    "graduate_unemployment_rate",
                    "Unemployment: Bachelor's+ (25+)",
                    {"date": "Date", "graduate_unemployment_rate": "%"},
                    "#d62728",
                ),
                use_container_width=True,
            )
            st.caption("📊 [FRED LNU04027662](https://fred.stlouisfed.org/series/LNU04027662)")

        st.subheader("📈 AI Investment Scale")

        if data["nvidia"] is not None:
            st.plotly_chart(
                make_chart(
                    data["nvidia"],
                    "date",
                    "revenue_millions",
                    "NVIDIA Quarterly Revenue",
                    {"date": "Date", "revenue_millions": "Revenue ($M)"},
                    "#76b900",
                    chart_type="bar",
                ),
                use_container_width=True,
            )
            st.caption(
                "📊 [SEC EDGAR XBRL](https://data.sec.gov/api/xbrl/companyfacts/CIK0001045810.json)"
            )
            st.info(
                "**Deployment-blind metric:** NVIDIA revenue measures AI compute "
                "investment, not whether that compute is deployed for worker "
                "augmentation or replacement. The same spending could produce "
                "mass displacement or broad-based productivity gains depending "
                "on institutional choices. Interpret alongside distribution "
                "indicators. (Acemoglu & Johnson, 2023)"
            )

        if data["it_equipment"] is not None:
            st.plotly_chart(
                make_chart(
                    data["it_equipment"],
                    "date",
                    "it_equipment_investment",
                    "Real Private Investment: Information Processing Equipment ($B, 2017)",
                    {"date": "Date", "it_equipment_investment": "Billions (chained 2017$)"},
                    "#636EFA",
                ),
                use_container_width=True,
            )
            st.caption(
                "📊 [FRED Y033RC1Q027SBEA]"
                "(https://fred.stlouisfed.org/series/Y033RC1Q027SBEA)"
                " — Quarterly, BEA. Hardware side of AI capex — servers, "
                "GPUs, networking gear. Broader than NVIDIA alone."
            )

        if data["software_investment"] is not None:
            st.plotly_chart(
                make_chart(
                    data["software_investment"],
                    "date",
                    "software_investment",
                    "Real Private Investment: Software ($B, 2017)",
                    {"date": "Date", "software_investment": "Billions (chained 2017$)"},
                    "#9467bd",
                ),
                use_container_width=True,
            )
            st.caption(
                "📊 [FRED B985RC1Q027SBEA]"
                "(https://fred.stlouisfed.org/series/B985RC1Q027SBEA)"
                " — Quarterly, BEA. Software side of AI capex — cloud AI, "
                "enterprise platforms, SaaS tools."
            )

        # --- Reinstatement & Compensation Indicators ---
        st.subheader("🔄 Reinstatement Indicators")
        st.markdown(
            "*These contextual indicators track whether compensation mechanisms "
            "are working — whether AI-driven gains create new tasks and flow "
            "to workers, or concentrate in capital returns. "
            "(Acemoglu & Restrepo, 2019)*"
        )

        # Compensation Health Index (derived from existing data)
        comp_health = compute_compensation_health(data["labor_share"], data["gdp_per_capita"])
        if len(comp_health) > 0:
            colors = [
                "#2ca02c" if v >= 0 else "#d62728" for v in comp_health["compensation_health"]
            ]
            fig_comp = go.Figure()
            fig_comp.add_trace(
                go.Bar(
                    x=comp_health["date"],
                    y=comp_health["compensation_health"],
                    marker_color=colors,
                    name="Compensation Health",
                )
            )
            fig_comp.add_hline(y=0, line_color="#999", line_width=2)
            fig_comp.update_layout(
                title="Compensation Health Index (GDP Growth + Labor Share Change)",
                plot_bgcolor="white",
                paper_bgcolor="white",
                font=dict(size=12),
                yaxis_title="Index",
                xaxis_title="Date",
                showlegend=False,
            )
            st.plotly_chart(fig_comp, use_container_width=True)
            st.caption(
                "**Green** = economic gains shared with workers. "
                "**Red** = GDP growth concentrating in capital returns "
                "while labor share declines — a sign that reinstatement "
                "(new task creation) is failing to offset automation. "
                "Based on Acemoglu & Restrepo (2019) task framework."
            )

        # Business Applications chart
        if data["business_applications"] is not None:
            st.plotly_chart(
                make_chart(
                    data["business_applications"],
                    "date",
                    "business_applications",
                    "New Business Applications (Employer ID Numbers)",
                    {"date": "Date", "business_applications": "Applications"},
                    "#ff7f0e",
                ),
                use_container_width=True,
            )
            st.caption(
                "📊 [FRED BABATOTALSAUS]"
                "(https://fred.stlouisfed.org/series/BABATOTALSAUS)"
                " — Monthly, Census Bureau. High new business formation "
                "indicates reinstatement is working (new tasks/industries "
                "emerging). Sustained decline alongside displacement signals "
                "suggests automation without offsetting job creation."
            )

    with tab2:
        st.header("🎯 AI Transformation Analysis")
        st.markdown(
            "How close are current indicators to **specific, historically "
            "abnormal** thresholds that would signal structural economic "
            "transformation driven by AI?"
        )

        # Prepare aligned datasets for scoring
        scoring_data = {
            "labor_share": data["labor_share"],
            "nvidia": data["nvidia"],
            "tfp": data["tfp"],
            "capital_labor": data["capital_labor"],
        }

        if data["unemployment"] is not None:
            scoring_data["unemployment_q"] = align_to_quarterly(data["unemployment"])
        if data["occupation"] is not None:
            scoring_data["occupation_q"] = align_to_quarterly(data["occupation"])
        if data["prime_age_epop"] is not None:
            scoring_data["prime_age_epop_q"] = align_to_quarterly(data["prime_age_epop"])
        if data["quits_rate"] is not None:
            scoring_data["quits_rate_q"] = align_to_quarterly(data["quits_rate"])
        if data["it_equipment"] is not None:
            scoring_data["it_equipment"] = data["it_equipment"]
        if data["median_wages"] is not None:
            scoring_data["median_wages"] = data["median_wages"]
        if data["info_jobs_per_grad"] is not None:
            scoring_data["info_jobs_per_grad_q"] = align_to_quarterly(
                data["info_jobs_per_grad"]
            )
        if data["software_investment"] is not None:
            scoring_data["software_investment"] = data["software_investment"]

        takeoff_metrics = compute_takeoff_metrics(scoring_data)
        takeoff_score = compute_takeoff_score(takeoff_metrics)

        # Score display with diffusion index
        if takeoff_score >= 60:
            sc, sl = "🔴", "Rapid Transformation"
        elif takeoff_score >= 30:
            sc, sl = "🟡", "Emerging Signal"
        else:
            sc, sl = "🟢", "No Signal"

        col_score, col_early_d, col_full_d = st.columns(3)
        with col_score:
            st.metric(
                label=f"{sc} AI Transformation Index",
                value=f"{takeoff_score:.1f} / 100",
                help=sl,
            )
        with col_early_d:
            early_n, early_t, _ = compute_diffusion_index(takeoff_metrics, "early")
            st.metric(
                "Early Warning Breadth",
                f"{early_n} / {early_t} metrics",
                help="Metrics above early-warning threshold (~1/3 of full)",
            )
        with col_full_d:
            full_n, full_t, _ = compute_diffusion_index(takeoff_metrics, "full")
            st.metric(
                "Full Threshold Breadth",
                f"{full_n} / {full_t} metrics",
                help="Metrics at or above full transformation threshold",
            )
        st.caption(
            "**Diffusion breadth matters:** 2 metrics at threshold could be "
            "coincidence; 6+ simultaneous signals across independent indicators "
            "would be structurally significant. National averages can mask "
            "concentrated harm — broad diffusion increases confidence that "
            "effects are economy-wide."
        )
        st.divider()

        # --- Radar chart: overall shape of takeoff signal ---
        st.subheader("🕸 Transformation Radar")
        radar_labels = []
        radar_progress = []
        radar_consistency = []
        for key in TAKEOFF_THRESHOLDS:
            if key in takeoff_metrics:
                radar_labels.append(TAKEOFF_THRESHOLDS[key]["label"])
                radar_progress.append(min(100, takeoff_metrics[key]["progress"] * 100))
                radar_consistency.append(takeoff_metrics[key]["consistency"] * 100)

        if radar_labels:
            fig_radar = go.Figure()
            fig_radar.add_trace(
                go.Scatterpolar(
                    r=radar_progress + [radar_progress[0]],
                    theta=radar_labels + [radar_labels[0]],
                    fill="toself",
                    name="Progress toward threshold",
                    fillcolor="rgba(99, 110, 250, 0.2)",
                    line=dict(color="#636EFA", width=2),
                )
            )
            fig_radar.add_trace(
                go.Scatterpolar(
                    r=radar_consistency + [radar_consistency[0]],
                    theta=radar_labels + [radar_labels[0]],
                    fill="toself",
                    name="Trend consistency",
                    fillcolor="rgba(239, 85, 59, 0.15)",
                    line=dict(color="#EF553B", width=2, dash="dot"),
                )
            )
            # 75% consistency target ring
            target_ring = [75] * (len(radar_labels) + 1)
            fig_radar.add_trace(
                go.Scatterpolar(
                    r=target_ring,
                    theta=radar_labels + [radar_labels[0]],
                    name="75% consistency target",
                    line=dict(color="#888", width=1, dash="dash"),
                    fill=None,
                )
            )
            fig_radar.update_layout(
                polar=dict(
                    radialaxis=dict(visible=True, range=[0, 100], ticksuffix="%"),
                ),
                showlegend=True,
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=-0.2,
                    xanchor="center",
                    x=0.5,
                ),
                height=500,
                margin=dict(t=40, b=80),
            )
            st.plotly_chart(fig_radar, use_container_width=True)
            st.caption(
                "Blue fill = progress toward threshold. "
                "Red dotted = trend consistency. "
                "Gray dashed = 75% consistency target."
            )

        st.divider()

        # --- Horizontal bar chart: all metrics progress at a glance ---
        st.subheader("📊 Progress Toward Transformation Thresholds")

        bar_data = []
        for cat_name, cat_keys in METRIC_CATEGORIES.items():
            for key in cat_keys:
                if key not in takeoff_metrics:
                    continue
                m = takeoff_metrics[key]
                info = TAKEOFF_THRESHOLDS[key]
                bar_data.append(
                    {
                        "Metric": info["label"],
                        "Progress (%)": min(100, m["progress"] * 100),
                        "Category": cat_name,
                        "Consistency": m["consistency"] * 100,
                    }
                )

        if bar_data:
            bar_df = pd.DataFrame(bar_data)
            cat_colors = {
                "Structural Shifts": "#636EFA",
                "Wage & Distribution": "#EF553B",
                "Labour Market Health": "#AB63FA",
                "AI Investment Scale": "#00CC96",
            }
            fig_bars = px.bar(
                bar_df,
                x="Progress (%)",
                y="Metric",
                color="Category",
                orientation="h",
                color_discrete_map=cat_colors,
                text="Progress (%)",
            )
            fig_bars.update_traces(texttemplate="%{text:.0f}%", textposition="outside")
            # Early warning line at ~33%
            fig_bars.add_vline(
                x=33,
                line_dash="dot",
                line_color="#ff7f0e",
                annotation_text="Early Warning",
                annotation_position="top left",
            )
            # Full threshold line at 100%
            fig_bars.add_vline(
                x=100,
                line_dash="dash",
                line_color="red",
                annotation_text="Full Threshold",
                annotation_position="top right",
            )
            fig_bars.update_layout(
                xaxis=dict(range=[0, max(110, bar_df["Progress (%)"].max() + 10)]),
                yaxis=dict(autorange="reversed"),
                plot_bgcolor="white",
                paper_bgcolor="white",
                height=400,
                showlegend=True,
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=-0.3,
                    xanchor="center",
                    x=0.5,
                ),
            )
            st.plotly_chart(fig_bars, use_container_width=True)

        st.divider()

        # --- Individual metric gauges with detail ---
        st.subheader("🔍 Metric-by-Metric Detail")

        for cat_name, cat_keys in METRIC_CATEGORIES.items():
            icon = CATEGORY_ICONS.get(cat_name, "")
            st.markdown(f"**{icon} {cat_name}**")

            for key in cat_keys:
                info = TAKEOFF_THRESHOLDS[key]

                if key not in takeoff_metrics:
                    st.warning(f"Insufficient data for {info['label']}")
                    continue

                m = takeoff_metrics[key]
                prog_pct = m["progress"] * 100
                cons_pct = m["consistency"] * 100

                if m["score"] >= 0.75:
                    status = "🔴 At/above threshold"
                elif m["score"] >= 0.30:
                    status = "🟡 Approaching"
                else:
                    status = "🟢 Below threshold"

                unit = info["unit"]
                metric_type = info.get("metric_type", "change")
                if metric_type == "level":
                    change_str = f"${m['raw_change'] / 1000:,.0f}B"
                    thresh_str = f"${info['threshold'] / 1000:,.0f}B"
                elif unit == "pp":
                    change_str = f"{m['raw_change']:+.1f}pp"
                    thresh_str = (
                        f"{info['threshold']:.0f}pp "
                        f"{'decline' if info['direction'] == 'decline' else 'rise'}"
                    )
                else:
                    change_str = f"{m['raw_change']:+.1f}%"
                    thresh_str = (
                        f"{info['threshold']:.0f}% "
                        f"{'decline' if info['direction'] == 'decline' else 'growth'}"
                    )

                with st.container():
                    st.markdown(f"**{info['label']}** — {status}")

                    col_gauge, col_stats = st.columns([3, 2])

                    with col_gauge:
                        # Early warning percentage for this metric
                        early_pct = info["early_threshold"] / info["threshold"] * 100

                        # Bullet gauge for this metric
                        fig_gauge = go.Figure(
                            go.Indicator(
                                mode="gauge+number",
                                value=min(prog_pct, 150),
                                number={"suffix": "%"},
                                gauge=dict(
                                    axis=dict(range=[0, 150]),
                                    bar=dict(
                                        color=(
                                            "#d62728"
                                            if prog_pct >= 100
                                            else "#ff7f0e"
                                            if prog_pct >= early_pct
                                            else "#2ca02c"
                                        )
                                    ),
                                    steps=[
                                        {"range": [0, early_pct], "color": "#f0f0f0"},
                                        {"range": [early_pct, 100], "color": "#fff3e0"},
                                        {"range": [100, 150], "color": "#ffe0e0"},
                                    ],
                                    threshold=dict(
                                        line=dict(color="red", width=3),
                                        thickness=0.8,
                                        value=100,
                                    ),
                                ),
                                title={"text": "Progress"},
                            )
                        )
                        fig_gauge.update_layout(
                            height=200,
                            margin=dict(t=60, b=20, l=30, r=30),
                        )
                        st.plotly_chart(fig_gauge, use_container_width=True)

                    with col_stats:
                        value_label = "Current" if metric_type == "level" else "3yr Change"
                        st.metric(value_label, change_str)
                        st.metric("Threshold", thresh_str)
                        cons_delta = "Above" if cons_pct >= 75 else "Below"
                        st.metric(
                            "Consistency",
                            f"{cons_pct:.0f}%",
                            delta=f"{cons_delta} 75% target",
                            delta_color=("normal" if cons_pct >= 75 else "inverse"),
                        )

                    st.divider()

        # Summary
        st.subheader("🔍 Current Assessment")
        at_thresh = [k for k, v in takeoff_metrics.items() if v["progress"] >= 1.0]
        early_warn = [
            k for k, v in takeoff_metrics.items() if v["progress"] >= 0.33 and v["progress"] < 1.0
        ]
        consistent = [
            k for k, v in takeoff_metrics.items() if v["consistency"] >= CONSISTENCY_TARGET
        ]
        active = [k for k, v in takeoff_metrics.items() if v["score"] > 0.30]
        total = len(TAKEOFF_THRESHOLDS)

        def label_list(keys):
            return ", ".join(TAKEOFF_THRESHOLDS[k]["label"] for k in keys) or "None"

        st.markdown(f"""
        **At/above full threshold:** {label_list(at_thresh)}

        **Early warning (above 1/3 threshold):** {label_list(early_warn)}

        **Consistent trend (>75%):** {label_list(consistent)}

        **Active signal (score > 0.3):** {label_list(active)}

        **Structural transformation requires:** Multiple metrics at threshold
        with >75% consistency. Currently **{len(at_thresh)}/{total}** at
        full threshold, **{len(early_warn)}/{total}** at early warning,
        **{len(consistent)}/{total}** consistent.
        """)

        st.info(
            "**Reinstatement context:** This scoring system measures the "
            "speed of potential displacement but not the reinstatement effect "
            "(new task creation). Check the Reinstatement Indicators in the "
            "Time Series tab — Business Applications and Compensation Health — "
            "to assess whether the economy is creating offsetting new tasks. "
            "Displacement without reinstatement is the critical signal. "
            "(Acemoglu & Restrepo, 2019)"
        )

    with tab3:
        st.header("🔮 Scenario-Based Takeoff Projections")
        st.markdown(
            "Three structural scenarios for how AI transforms the economy. "
            "Each defines *what changes*, not just 'current trends but faster.'"
        )

        # Structural scenarios with per-metric annual rates
        SCENARIOS = {
            "Augmentation": {
                "color": "#2ca02c",
                "description": (
                    "AI augments workers but doesn't replace them. "
                    "Like spreadsheets for accountants. Gradual, "
                    "broad-based, no discontinuity."
                ),
                # Annual rates: what the 3yr window would show per year
                "rates": {
                    "tfp": 1.0,
                    "occupation_gap": 0.5,
                    "capital_labor": 1.5,
                    "median_wages": 0.5,  # Modest real wage growth
                    "info_jobs_per_grad": 2.0,  # Slow decline, demographics
                    "labor_share": 0.3,
                    "prime_age_epop": 0.2,
                    "quits_rate": 0.05,
                    "unemployment": 0.1,
                    "nvidia": 100000,  # Level: $100B/qtr plateau
                    "it_equipment": 4.0,  # ~4%/yr, near historical norm
                    "software_investment": 6.0,  # ~6%/yr, near historical
                },
            },
            "Agent Revolution": {
                "color": "#ff7f0e",
                "description": (
                    "AI agents handle end-to-end knowledge work by ~2028. "
                    "Software economy transforms; physical economy unchanged."
                ),
                "rates": {
                    "tfp": 2.5,
                    "occupation_gap": 4.0,
                    "capital_labor": 4.0,
                    "median_wages": 1.0,  # Stagnating real wages
                    "info_jobs_per_grad": 5.0,  # Knowledge jobs shrinking fast
                    "labor_share": 1.5,
                    "prime_age_epop": 0.8,
                    "quits_rate": 0.2,
                    "unemployment": 0.8,
                    "nvidia": 200000,  # Level: $200B/qtr
                    "it_equipment": 8.0,  # ~8%/yr, double historical
                    "software_investment": 12.0,  # ~12%/yr, double historical
                },
            },
            "Physical AI": {
                "color": "#d62728",
                "description": (
                    "Humanoid robots + autonomous systems + AI agents. "
                    "Both cognitive AND physical work automated by ~2032-35. "
                    "Requires hardware not yet at scale."
                ),
                "rates": {
                    "tfp": 4.0,
                    "occupation_gap": 6.0,
                    "capital_labor": 5.0,
                    "median_wages": 2.0,  # Real wages declining
                    "info_jobs_per_grad": 8.0,  # Knowledge economy contracting
                    "labor_share": 2.5,
                    "prime_age_epop": 1.5,
                    "quits_rate": 0.35,
                    "unemployment": 1.0,
                    "nvidia": 350000,  # Level: $350B/qtr
                    "it_equipment": 12.0,  # ~12%/yr, massive reallocation
                    "software_investment": 16.0,  # ~16%/yr, unprecedented
                },
            },
        }

        for sname, sinfo in SCENARIOS.items():
            st.markdown(f"**{sname}:** {sinfo['description']}")
        st.divider()

        # Project scores at future years
        proj_years = [2027, 2028, 2029, 2030, 2032, 2035, 2040]
        # Current values for level-type metrics
        current_levels = {
            "nvidia": 68127.0,  # Current NVIDIA $M/quarter
        }

        score_rows = []
        metric_rows = []

        for sname, sinfo in SCENARIOS.items():
            rates = sinfo["rates"]

            for yr in proj_years:
                years_out = yr - 2026
                eff_years = min(years_out, 3)

                total_w = 0.0
                w_sum = 0.0
                n_active = 0

                for key, info in TAKEOFF_THRESHOLDS.items():
                    threshold = info["threshold"]
                    weight = info["weight"]
                    m_type = info.get("metric_type", "change")
                    rate = rates.get(key, 0)

                    if m_type == "level":
                        current_val = current_levels.get(key, rate * 0.5)
                        ramp = min(1.0, years_out / 5.0)
                        proj_val = current_val + (rate - current_val) * ramp
                        progress = max(0.0, proj_val / threshold)
                        cons = 0.95 if rate > current_val else 0.5
                    else:
                        proj_3yr = rate * eff_years
                        progress = max(0.0, proj_3yr / threshold)
                        cons = min(0.95, 0.5 + rate / (threshold / 3) * 0.3) if rate > 0 else 0.4

                    score = min(1.0, progress * cons)
                    w_sum += weight * score
                    total_w += weight
                    if score > 0.3:
                        n_active += 1

                    metric_rows.append(
                        {
                            "Scenario": sname,
                            "Year": yr,
                            "Metric": info["label"],
                            "Progress": min(progress * 100, 150),
                        }
                    )

                base = w_sum / total_w if total_w > 0 else 0
                coherence = 0.5 + 0.5 * (n_active / len(TAKEOFF_THRESHOLDS))
                final = min(100.0, base * coherence * 100)

                score_rows.append(
                    {
                        "Scenario": sname,
                        "Year": yr,
                        "Score": final,
                        "Active": n_active,
                    }
                )

        score_df = pd.DataFrame(score_rows)
        metric_df = pd.DataFrame(metric_rows)

        # --- Score trajectory chart ---
        st.subheader("📈 Projected Transformation Score Over Time")

        fig_scores = go.Figure()
        for sname, sinfo in SCENARIOS.items():
            s_df = score_df[score_df["Scenario"] == sname]
            fig_scores.add_trace(
                go.Scatter(
                    x=s_df["Year"],
                    y=s_df["Score"],
                    mode="lines+markers+text",
                    name=sname,
                    line=dict(color=sinfo["color"], width=3),
                    marker=dict(size=8),
                    text=[f"{s:.0f}" for s in s_df["Score"]],
                    textposition="top center",
                    textfont=dict(size=10),
                )
            )

        fig_scores.add_trace(
            go.Scatter(
                x=[2026],
                y=[takeoff_score],
                mode="markers+text",
                name="Current",
                marker=dict(size=14, color="black", symbol="diamond"),
                text=[f"Now: {takeoff_score:.0f}"],
                textposition="bottom center",
                textfont=dict(size=12, color="black"),
            )
        )

        fig_scores.add_hrect(
            y0=60,
            y1=100,
            fillcolor="rgba(214,39,40,0.08)",
            line_width=0,
            annotation_text="Rapid Transformation",
            annotation_position="top left",
        )
        fig_scores.add_hrect(
            y0=30,
            y1=60,
            fillcolor="rgba(255,127,14,0.08)",
            line_width=0,
            annotation_text="Emerging Signal",
            annotation_position="top left",
        )

        fig_scores.update_layout(
            xaxis=dict(title="Year", dtick=2, range=[2025, 2041]),
            yaxis=dict(title="Transformation Score", range=[0, 100]),
            plot_bgcolor="white",
            paper_bgcolor="white",
            height=450,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.2,
                xanchor="center",
                x=0.5,
            ),
        )
        st.plotly_chart(fig_scores, use_container_width=True)
        st.divider()

        # --- Heatmaps per scenario ---
        st.subheader("🗺 Metric Progress Heatmaps")

        for sname, _sinfo in SCENARIOS.items():
            st.markdown(f"**{sname}**")
            s_df = metric_df[metric_df["Scenario"] == sname]
            pivot = s_df.pivot(index="Metric", columns="Year", values="Progress")

            fig_heat = go.Figure(
                data=go.Heatmap(
                    z=pivot.values,
                    x=[str(y) for y in pivot.columns],
                    y=pivot.index,
                    colorscale=[
                        [0, "#f0f0f0"],
                        [0.33, "#fee08b"],
                        [0.66, "#fc8d59"],
                        [1.0, "#d73027"],
                    ],
                    zmin=0,
                    zmax=150,
                    text=[[f"{v:.0f}%" for v in row] for row in pivot.values],
                    texttemplate="%{text}",
                    textfont=dict(size=11),
                    colorbar=dict(title="Progress %"),
                )
            )
            fig_heat.update_layout(
                height=350,
                plot_bgcolor="white",
                paper_bgcolor="white",
                margin=dict(t=30),
            )
            st.plotly_chart(fig_heat, use_container_width=True)

        st.divider()

        # --- Summary cards ---
        st.subheader("📊 Scenario Summary")
        for sname, _sinfo in SCENARIOS.items():
            s_df = score_df[score_df["Scenario"] == sname]
            above_30 = s_df[s_df["Score"] >= 30]
            above_60 = s_df[s_df["Score"] >= 60]
            s2032 = s_df[s_df["Year"] == 2032]["Score"].values
            s2032_str = f"{s2032[0]:.0f}" if len(s2032) > 0 else "N/A"

            st.markdown(f"**{sname}:**")
            c1, c2, c3 = st.columns(3)
            c1.metric(
                "Early Indicators (>30)",
                str(above_30["Year"].min()) if len(above_30) > 0 else ">2040",
            )
            c2.metric(
                "Strong Signal (>60)",
                str(above_60["Year"].min()) if len(above_60) > 0 else ">2040",
            )
            c3.metric("Score in 2032", f"{s2032_str}/100")
            st.divider()

        st.subheader("⚠️ Key Assumptions")
        st.markdown("""
        - **Augmentation** assumes AI follows the historical pattern:
          augments workers, creates new roles, no mass displacement.
        - **Agent Revolution** assumes reliable AI agents deploy at
          enterprise scale by ~2028-2029, automating end-to-end
          knowledge workflows. A capability threshold, not a rate.
        - **Physical AI** assumes humanoid robots and autonomous
          systems enter logistics/manufacturing/service by ~2032-35.
          This is what moves electricity and the full job gap.
        - All scenarios assume no major recession, war, or regulatory
          shutdown.
        - **These are not probabilities.** They describe structurally
          different worlds.
        """)

    with tab4:
        st.header("📚 Methodology")

        st.subheader("What Does This Tracker Measure?")
        st.markdown("""
        This tracker monitors whether AI investment is producing
        **measurable, sustained, historically abnormal** shifts across
        multiple independent economic indicators simultaneously.

        It does **not** predict a "singularity" or claim that AI will
        inevitably cause mass displacement. Instead, it asks: **are
        current economic data consistent with AI-driven structural
        transformation?** The answer can be "no" — and that is a
        valid, informative result.

        The tracker defines **12 metrics** across four categories,
        each with two threshold tiers:
        - **Early warning** (~1/3 of full threshold): calibrated to
          near-term AI productivity estimates (Acemoglu, 2024)
        - **Full threshold**: historically extraordinary rates that
          would indicate structural transformation
        """)

        st.subheader("Thresholds (3-year rolling window)")
        for cat_name, cat_keys in METRIC_CATEGORIES.items():
            icon = CATEGORY_ICONS.get(cat_name, "")
            st.markdown(f"**{icon} {cat_name}:**")
            for key in cat_keys:
                info = TAKEOFF_THRESHOLDS[key]
                arrow = "↓" if info["direction"] == "decline" else "↑"
                st.markdown(
                    f"- {info['label']} {arrow} "
                    f"Early: **{info['early_threshold']}{info['unit']}** / "
                    f"Full: **{info['threshold']}{info['unit']}** "
                    f"({info['frequency']}, weight: {info['weight']:.0%})"
                )
                st.caption(info["rationale"])

        st.subheader("Scoring")
        st.markdown("""
        1. **Progress** = actual 3yr change / full threshold (0-100%+)
        2. **Consistency** = fraction of periods trending correctly
        3. **Metric Score** = Progress x Consistency (capped at 1.0)
        4. **Overall** = weighted average x coherence factor
        5. **Diffusion** = count of metrics above early/full thresholds

        Coherence factor penalizes when few metrics are active.
        Annual metrics (TFP, Capital-Labor) use 3-period lookback;
        quarterly metrics use 12-period lookback.

        **Unemployment uses absolute pp change** (not % of rate)
        to avoid base-rate bias.

        **Early warning thresholds** (~1/3 of full) are calibrated
        to Acemoglu (2024) estimates of near-term AI productivity
        effects (0.66% TFP over 10 years). These detect slow erosion
        that the full thresholds would miss.
        """)

        st.subheader("Causal Limitations")
        st.markdown("""
        This tracker monitors patterns **consistent with** AI-driven
        structural change. It cannot prove causality. Key limitations:

        - **Compute ≠ displacement.** AI investment (NVIDIA revenue,
          electricity) measures scale of spending, not deployment type.
          The same investment could produce worker augmentation or
          replacement depending on corporate strategy, regulation, and
          labor market institutions (Acemoglu & Johnson, 2023).

        - **Multiple confounds.** All tracked indicators are affected by
          monetary policy, globalization, demographics, and pandemic
          recovery. The tracker's strength is requiring multiple
          independent indicators to move simultaneously — unlikely
          to occur from confounders alone.

        - **Reinstatement is not scored.** The composite index measures
          displacement speed but not new task creation. Business
          Applications and Compensation Health provide interpretive
          context but are not incorporated into the score. This is a
          deliberate design choice: displacement and reinstatement
          operate on different timescales and should not be netted.

        - **Aggregates mask distribution.** National-level metrics can
          hide concentrated harm in specific occupations, demographics,
          or regions. The diffusion index partially addresses this by
          requiring breadth across indicators.

        *Reference: Acemoglu, D. & Johnson, S. (2023). Power and Progress.*
        """)

        st.subheader("Data Sources")
        st.markdown("""
        | Metric | Source | Series | Freq |
        |--------|--------|--------|------|
        | TFP | FRED | MFPNFBS | Annual |
        | Capital-Labor | FRED | MPU4910042/MPU4910052 | Annual |
        | Job Displacement | FRED | CPS/CES occupation groups | Monthly→Q |
        | Median Wages | FRED | LES1252881600Q | Quarterly |
        | Knowledge Jobs/Grad | FRED | USINFO/LNS11027662 | Monthly→Q |
        | Labor Share | FRED | PRS85006173 | Quarterly |
        | Prime-Age EPOP | FRED | LNS12300060 | Monthly→Q |
        | Quits Rate | FRED (JOLTS) | JTSQUR | Monthly→Q |
        | Unemployment | FRED | LNU04027662 | Monthly→Q |
        | NVIDIA Revenue | SEC EDGAR | CIK 0001045810 | Quarterly |
        | IT Equipment | FRED | Y033RC1Q027SBEA | Quarterly |
        | Software Invest. | FRED | B985RC1Q027SBEA | Quarterly |
        """)

except FileNotFoundError as e:
    st.error(f"Data not found. Run the pipeline first: {e}")
except KeyError as e:
    st.error(f"Data schema mismatch — column missing: {e}")

st.divider()
st.markdown("*Data: FRED, BLS, BEA, SEC EDGAR XBRL*")
