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
    """Load all three processed datasets."""
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
    
    return labor_share_df, gdp_df, accountants_df

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

def calculate_singularity_score(labor_changes, gdp_changes, accountants_changes):
    """Calculate AI Singularity Score based on directional changes."""
    scores = {}
    
    for period in ['1_year', '2_year', '3_year']:
        if all(period in changes for changes in [labor_changes, gdp_changes, accountants_changes]):
            # Positive signals towards singularity:
            # - Labor share going down (negative change is good)
            # - GDP per capita going up (positive change is good) 
            # - Accountants employment going down (negative change is good)
            
            labor_signal = -labor_changes[period] if period in labor_changes else 0  # Invert: down is good
            gdp_signal = gdp_changes[period] if period in gdp_changes else 0        # Up is good
            accountants_signal = -accountants_changes[period] if period in accountants_changes else 0  # Invert: down is good
            
            # Normalize and combine (simple average for now)
            # Scale to 0-100 range
            raw_score = (labor_signal + gdp_signal + accountants_signal) / 3
            normalized_score = max(0, min(100, 50 + raw_score * 2))  # Center at 50, scale appropriately
            
            scores[period] = normalized_score
    
    return scores

# Load data
try:
    labor_share_df, gdp_df, accountants_df = load_data()
    
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
    
    with tab2:
        st.header("Year-over-Year Analysis & AI Singularity Score")
        
        # Calculate year-over-year changes (align accountants data to quarterly)
        accountants_quarterly = align_to_quarterly(accountants_df, 'employed_accountants')
        
        labor_changes = calculate_yoy_changes(labor_share_df, 'labor_share_index')
        gdp_changes = calculate_yoy_changes(gdp_df, 'real_gdp_per_capita')
        accountants_changes = calculate_yoy_changes(accountants_quarterly, 'employed_accountants')
        
        # Calculate singularity scores
        singularity_scores = calculate_singularity_score(labor_changes, gdp_changes, accountants_changes)
        
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
            
            st.divider()
        
        # Add explanation
        st.subheader("📚 Methodology")
        with st.expander("How the AI Singularity Score is calculated"):
            st.markdown("""
            The AI Singularity Score combines three economic indicators to detect potential AI-driven technological displacement:
            
            **🔢 Data Sources & Frequency:**
            - **Labor Share & GDP**: Quarterly data from Federal Reserve (FRED)
            - **Accountants Employment**: Monthly data from Census Bureau (CPS), aligned to quarterly by using end-of-quarter months (Mar, Jun, Sep, Dec)
            - **Time Periods**: All metrics use quarterly alignment - 1-year (4 quarters), 2-year (8 quarters), 3-year (12 quarters)
            
            **📈 Singularity Signal Logic:**
            - 📉 **Labor Share ↓**: AI replacing workers → labor gets smaller slice of economic pie
            - 📈 **GDP per Capita ↑**: AI automation → higher productivity & wealth per person
            - 📉 **Employed Accountants ↓**: AI targets knowledge work → fewer accounting jobs
            
            **🧮 Score Calculation:**
            1. Calculate year-over-year % change for each metric
            2. Apply directional scoring:
               - Labor Share: Negative change = positive signal (invert sign)
               - GDP per Capita: Positive change = positive signal (keep sign)  
               - Accountants: Negative change = positive signal (invert sign)
            3. Average the three signals: `(labor_signal + gdp_signal + accountants_signal) / 3`
            4. Normalize to 0-100 scale: `50 + (raw_score × 2)`
            
            **🎯 Score Interpretation:**
            - 🟢 **0-49**: Low Signal - Normal economic fluctuations
            - 🟡 **50-69**: Moderate Signal - Some displacement indicators
            - 🔴 **70-100**: High Signal - Strong AI singularity patterns
            
            **⚠️ Limitations:**
            - Correlation doesn't imply causation
            - Many factors affect these metrics beyond AI
            - Score is experimental and should be interpreted carefully
            """)

except FileNotFoundError as e:
    st.error(f"Data files not found. Please ensure the processed data files exist: {e}")
except Exception as e:
    st.error(f"Error loading data: {e}")

# Footer
st.divider()
st.markdown("*Data sources: Federal Reserve Economic Data (FRED), U.S. Census Bureau Current Population Survey (CPS)*")