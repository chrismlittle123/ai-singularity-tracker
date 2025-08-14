import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import numpy as np

# Page config
st.set_page_config(
    page_title="AI Singularity Tracker",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Title and description
st.title("🤖 AI Singularity Tracker")
st.markdown("**Monitoring economic indicators for signs of AI-driven technological displacement**")

@st.cache_data
def load_data():
    """Load all four processed datasets."""
    data_dir = Path("data/processed")
    
    # Load labor share data
    labor_share_path = data_dir / "labor_share" / "labor_share_processed.csv"
    labor_share_df = pd.read_csv(labor_share_path)
    labor_share_df['date'] = pd.to_datetime(labor_share_df[['year', 'month']].assign(day=1))
    
    # Load real GDP per capita data  
    gdp_path = data_dir / "real_gdp_per_capita" / "real_gdp_per_capita_processed.csv"
    gdp_df = pd.read_csv(gdp_path)
    gdp_df['date'] = pd.to_datetime(gdp_df[['year', 'month']].assign(day=1))
    
    # Load accountants employment data
    accountants_path = data_dir / "accountants_employed" / "accountants_employed_processed.csv"
    accountants_df = pd.read_csv(accountants_path)
    accountants_df['date'] = pd.to_datetime(accountants_df[['year', 'month']].assign(day=1))
    
    # Load graduate unemployment rate data
    unemployment_path = data_dir / "graduate_unemployment_rate" / "graduate_unemployment_rate_processed.csv"
    unemployment_df = pd.read_csv(unemployment_path) if unemployment_path.exists() else None
    if unemployment_df is not None:
        unemployment_df['date'] = pd.to_datetime(unemployment_df[['year', 'month']].assign(day=1))
    
    return labor_share_df, gdp_df, accountants_df, unemployment_df

def align_to_quarterly(df, metric_col):
    """Convert monthly data to quarterly by taking the last month of each quarter."""
    df['quarter'] = df['date'].dt.quarter
    df['year'] = df['date'].dt.year
    
    # Take the last month of each quarter (March, June, September, December)
    quarterly_data = df[df['date'].dt.month.isin([3, 6, 9, 12])].copy()
    quarterly_data = quarterly_data.sort_values('date').reset_index(drop=True)
    
    return quarterly_data

def calculate_yoy_changes(df, metric_col):
    """Calculate year-over-year changes for quarterly data periods."""
    df_sorted = df.sort_values('date').reset_index(drop=True)
    changes = {}
    
    # For quarterly data: 4 periods = 1 year, 8 periods = 2 years, 12 periods = 3 years
    periods = {'1_year': 4, '2_year': 8, '3_year': 12}
    
    for period_name, period_count in periods.items():
        if len(df_sorted) > period_count:
            current_value = df_sorted[metric_col].iloc[-1]
            past_value = df_sorted[metric_col].iloc[-(period_count+1)]
            change = ((current_value - past_value) / past_value) * 100
            changes[period_name] = change
    
    return changes

def calculate_singularity_score(labor_changes, gdp_changes, accountants_changes, unemployment_changes=None):
    """Calculate AI Singularity Score with proper normalization and weighting."""
    scores = {}
    
    # Define weights for each metric (must sum to 1.0)
    # Higher weight = more important for detecting AI singularity
    weights = {
        'labor_share': 0.30,      # Labor's declining share is critical signal
        'gdp_per_capita': 0.25,   # Rising productivity despite job losses
        'accountants': 0.20,      # Direct measure of AI replacing knowledge workers
        'unemployment': 0.25      # Overall labor market health
    }
    
    # Historical statistics for normalization (based on typical economic ranges)
    # These represent typical standard deviations for % changes
    std_devs = {
        'labor_share': 2.5,       # Labor share typically varies ±2.5% annually
        'gdp_per_capita': 3.0,    # GDP per capita typically varies ±3% annually  
        'accountants': 5.0,       # Employment can vary ±5% annually
        'unemployment': 15.0      # Unemployment rate changes can be volatile
    }
    
    for period in ['1_year', '2_year', '3_year']:
        if all(period in changes for changes in [labor_changes, gdp_changes, accountants_changes]):
            # Calculate z-scores for each metric
            # Z-score = (value - mean) / std_dev, where mean = 0 for % changes
            
            # Labor share: negative change is positive signal
            labor_z = (-labor_changes[period]) / std_devs['labor_share'] if period in labor_changes else 0
            
            # GDP per capita: positive change is positive signal
            gdp_z = gdp_changes[period] / std_devs['gdp_per_capita'] if period in gdp_changes else 0
            
            # Accountants: negative change is positive signal
            accountants_z = (-accountants_changes[period]) / std_devs['accountants'] if period in accountants_changes else 0
            
            # Unemployment: positive change is positive signal (rising unemployment = AI displacement)
            unemployment_z = 0
            if unemployment_changes and period in unemployment_changes:
                unemployment_z = unemployment_changes[period] / std_devs['unemployment']
            
            # Clip z-scores to reasonable range [-3, 3]
            labor_z = np.clip(labor_z, -3, 3)
            gdp_z = np.clip(gdp_z, -3, 3)
            accountants_z = np.clip(accountants_z, -3, 3)
            unemployment_z = np.clip(unemployment_z, -3, 3)
            
            # Calculate weighted average of z-scores
            if unemployment_changes:
                weighted_z = (
                    weights['labor_share'] * labor_z +
                    weights['gdp_per_capita'] * gdp_z +
                    weights['accountants'] * accountants_z +
                    weights['unemployment'] * unemployment_z
                )
            else:
                # Redistribute unemployment weight if data not available
                adjusted_weights = {
                    'labor_share': 0.40,
                    'gdp_per_capita': 0.35,
                    'accountants': 0.25
                }
                weighted_z = (
                    adjusted_weights['labor_share'] * labor_z +
                    adjusted_weights['gdp_per_capita'] * gdp_z +
                    adjusted_weights['accountants'] * accountants_z
                )
            
            # Convert z-score to 0-100 scale
            # z-score of 0 = 50, z-score of ±3 = 0 or 100
            normalized_score = 50 + (weighted_z * 50/3)
            normalized_score = max(0, min(100, normalized_score))
            
            scores[period] = normalized_score
    
    return scores

# Load data
try:
    labor_share_df, gdp_df, accountants_df, unemployment_df = load_data()
    
    # Create tabs
    tab1, tab2 = st.tabs(["📈 Time Series Charts", "📊 Year-over-Year Analysis"])
    
    with tab1:
        st.header("Economic Indicators Over Time")
        
        # Labor Share Chart
        st.subheader("💼 Labor Share of Income")
        fig_labor = px.line(
            labor_share_df, 
            x='date', 
            y='labor_share_index',
            title="Labor Share of Income Index",
            labels={'date': 'Date', 'labor_share_index': 'Labor Share Index'}
        )
        fig_labor.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(size=12),
            showlegend=False
        )
        fig_labor.update_traces(line=dict(color='#1f77b4', width=3))
        st.plotly_chart(fig_labor, use_container_width=True)
        st.caption("📊 **Data Source**: [FRED Series PRS85006173](https://fred.stlouisfed.org/series/PRS85006173) | [Download CSV](https://fred.stlouisfed.org/graph/fredgraph.csv?id=PRS85006173)")
        
        # Real GDP per Capita Chart
        st.subheader("💰 Real GDP per Capita")
        fig_gdp = px.line(
            gdp_df,
            x='date',
            y='real_gdp_per_capita',
            title="Real GDP per Capita",
            labels={'date': 'Date', 'real_gdp_per_capita': 'Real GDP per Capita ($)'}
        )
        fig_gdp.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white', 
            font=dict(size=12),
            showlegend=False
        )
        fig_gdp.update_traces(line=dict(color='#2ca02c', width=3))
        st.plotly_chart(fig_gdp, use_container_width=True)
        st.caption("📊 **Data Source**: [FRED Series A939RX0Q048SBEA](https://fred.stlouisfed.org/series/A939RX0Q048SBEA) | [Download CSV](https://fred.stlouisfed.org/graph/fredgraph.csv?id=A939RX0Q048SBEA)")
        
        # Accountants Employment Chart
        st.subheader("👨‍💼 Accountants Employment")
        
        fig_acc = px.line(
            accountants_df,
            x='date',
            y='employed_accountants',
            title="Employed Accountants",
            labels={'date': 'Date', 'employed_accountants': 'Number of Employed Accountants'}
        )
        fig_acc.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(size=12),
            showlegend=False
        )
        fig_acc.update_traces(line=dict(color='#ff7f0e', width=3))
        
        st.plotly_chart(fig_acc, use_container_width=True)
        st.caption("📊 **Data Source**: [U.S. Census Bureau Current Population Survey](https://www2.census.gov/programs-surveys/cps/datasets/2025/basic/2025_Basic_CPS_Public_Use_Record_Layout_plus_IO_Code_list.txt) | Occupation Code: 0800 (Accountants and Auditors)")
        
        # Graduate Unemployment Rate Chart
        if unemployment_df is not None:
            st.subheader("📉 Graduate Unemployment Rate")
            fig_unemp = px.line(
                unemployment_df,
                x='date',
                y='graduate_unemployment_rate',
                title="Graduate Unemployment Rate",
                labels={'date': 'Date', 'graduate_unemployment_rate': 'Graduate Unemployment Rate (%)'}
            )
            fig_unemp.update_layout(
                plot_bgcolor='white',
                paper_bgcolor='white',
                font=dict(size=12),
                showlegend=False
            )
            fig_unemp.update_traces(line=dict(color='#d62728', width=3))
            st.plotly_chart(fig_unemp, use_container_width=True)
            st.caption("📊 **Data Source**: [FRED Series UNRATE](https://fred.stlouisfed.org/series/UNRATE) | [Download CSV](https://fred.stlouisfed.org/graph/fredgraph.csv?id=UNRATE)")
    
    with tab2:
        st.header("Year-over-Year Analysis & AI Singularity Score")
        
        # Calculate year-over-year changes (align monthly data to quarterly)
        accountants_quarterly = align_to_quarterly(accountants_df, 'employed_accountants')
        
        labor_changes = calculate_yoy_changes(labor_share_df, 'labor_share_index')
        gdp_changes = calculate_yoy_changes(gdp_df, 'real_gdp_per_capita')
        accountants_changes = calculate_yoy_changes(accountants_quarterly, 'employed_accountants')
        
        # Handle graduate unemployment if available
        unemployment_changes = None
        if unemployment_df is not None:
            unemployment_quarterly = align_to_quarterly(unemployment_df, 'graduate_unemployment_rate')
            unemployment_changes = calculate_yoy_changes(unemployment_quarterly, 'graduate_unemployment_rate')
        
        # Calculate singularity scores
        singularity_scores = calculate_singularity_score(
            labor_changes, gdp_changes, accountants_changes, unemployment_changes
        )
        
        # Display AI Singularity Score prominently
        st.subheader("🤖 AI Singularity Score")
        st.markdown("*Higher scores indicate stronger signals of AI-driven economic transformation*")
        
        col1, col2, col3 = st.columns(3)
        
        for i, (period, score) in enumerate(singularity_scores.items()):
            col = [col1, col2, col3][i]
            period_label = period.replace('_', ' ').title()
            
            # Color coding for scores
            if score >= 70:
                color = "🔴"
                status = "High Signal"
            elif score >= 50:
                color = "🟡" 
                status = "Moderate Signal"
            else:
                color = "🟢"
                status = "Low Signal"
            
            col.metric(
                label=f"{color} {period_label}",
                value=f"{score:.1f}/100",
                help=f"AI Singularity Signal: {status}"
            )
        
        st.divider()
        
        # Year-over-Year Changes
        st.subheader("📈 Year-over-Year Changes")
        
        # Create columns for each time period
        periods = ['1_year', '2_year', '3_year']
        period_labels = ['1 Year', '2 Years', '3 Years']
        
        for period, label in zip(periods, period_labels):
            st.markdown(f"**{label} Changes:**")
            
            if unemployment_changes:
                col1, col2, col3, col4 = st.columns(4)
            else:
                col1, col2, col3 = st.columns(3)
            
            # Labor Share
            if period in labor_changes:
                change = labor_changes[period]
                delta_color = "inverse"  # Red for decreases (which is good for singularity)
                col1.metric(
                    "Labor Share Index",
                    f"{change:+.1f}%",
                    delta=f"{change:+.1f}%",
                    delta_color=delta_color
                )
            else:
                col1.metric("Labor Share Index", "N/A")
            
            # Real GDP per Capita  
            if period in gdp_changes:
                change = gdp_changes[period]
                delta_color = "normal"  # Green for increases
                col2.metric(
                    "Real GDP per Capita",
                    f"{change:+.1f}%", 
                    delta=f"{change:+.1f}%",
                    delta_color=delta_color
                )
            else:
                col2.metric("Real GDP per Capita", "N/A")
            
            # Accountants Employment
            if period in accountants_changes:
                change = accountants_changes[period]
                delta_color = "inverse"  # Red for decreases (which would signal singularity)
                col3.metric(
                    "Employed Accountants",
                    f"{change:+.1f}%",
                    delta=f"{change:+.1f}%", 
                    delta_color=delta_color
                )
            else:
                col3.metric("Employed Accountants", "N/A")
            
            # Graduate Unemployment Rate
            if unemployment_changes and period in unemployment_changes:
                change = unemployment_changes[period]
                delta_color = "normal"  # Green for increases (rising unemployment = AI displacement)
                col4.metric(
                    "Graduate Unemployment Rate",
                    f"{change:+.1f}%",
                    delta=f"{change:+.1f}%",
                    delta_color=delta_color
                )
            elif unemployment_changes:
                col4.metric("Graduate Unemployment Rate", "N/A")
            
            st.divider()
        
        # Add explanation
        st.subheader("📚 Methodology")
        with st.expander("How the AI Singularity Score is calculated"):
            st.markdown("""
            The AI Singularity Score uses advanced statistical methods to detect potential AI-driven technological displacement:
            
            **🔢 Data Sources & Frequency:**
            - **Labor Share & GDP**: Quarterly data from Federal Reserve (FRED)
            - **Graduate Unemployment Rate**: Monthly data from Federal Reserve (FRED), aligned to quarterly
            - **Accountants Employment**: Monthly data from Census Bureau (CPS), aligned to quarterly
            - **Time Periods**: All metrics use quarterly alignment - 1-year (4 quarters), 2-year (8 quarters), 3-year (12 quarters)
            
            **📈 Singularity Signal Logic:**
            - 📉 **Labor Share ↓**: AI replacing workers → labor gets smaller slice of economic pie
            - 📈 **GDP per Capita ↑**: AI automation → higher productivity & wealth per person
            - 📉 **Employed Accountants ↓**: AI targets knowledge work → fewer accounting jobs
            - 📈 **Graduate Unemployment Rate ↑**: Rising unemployment despite GDP growth → AI displacement
            
            **🧬 Scientific Methodology:**
            
            1. **Z-Score Normalization**: Each metric is converted to a z-score to enable comparison:
               ```
               z-score = (% change) / (typical standard deviation)
               ```
               This accounts for different volatility levels across metrics.
            
            2. **Weighted Importance**: Metrics are weighted by their significance:
               - Labor Share: 30% (critical long-term indicator)
               - GDP per Capita: 25% (productivity measure)
               - Graduate Unemployment: 25% (immediate labor market impact)
               - Accountants: 20% (specific AI displacement signal)
            
            3. **Directional Adjustments**:
               - Labor Share & Accountants: Negative changes → positive z-scores
               - GDP & Unemployment: Positive changes → positive z-scores
            
            4. **Final Score**: Weighted average of z-scores, scaled to 0-100:
               ```
               Score = 50 + (weighted_z_score × 50/3)
               ```
            
            **📊 Statistical Parameters:**
            - **Labor Share σ**: ±2.5% (typical annual variation)
            - **GDP per Capita σ**: ±3.0% (typical annual variation)
            - **Accountants σ**: ±5.0% (employment volatility)
            - **Graduate Unemployment σ**: ±15.0% (rate change volatility)
            
            **🎯 Score Interpretation:**
            - 🟢 **0-49**: Low Signal - Within normal economic variation
            - 🟡 **50-69**: Moderate Signal - Emerging displacement patterns
            - 🔴 **70-100**: High Signal - Strong AI singularity indicators
            
            **⚠️ Limitations:**
            - Correlation doesn't imply causation
            - Historical volatility estimates may not reflect future patterns
            - Multiple economic factors beyond AI affect these metrics
            - Score is experimental and should be interpreted with caution
            """)

except FileNotFoundError as e:
    st.error(f"Data files not found. Please ensure the processed data files exist: {e}")
except Exception as e:
    st.error(f"Error loading data: {e}")

# Footer
st.divider()
st.markdown("*Data sources: Federal Reserve Economic Data (FRED), U.S. Census Bureau Current Population Survey (CPS)*")