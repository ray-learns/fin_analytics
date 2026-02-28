import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go

# 1. PAGE SETUP
st.set_page_config(page_title="P/L Trend Analyzer", page_icon="📈", layout="wide")

st.title("📈 Corporate Financial Trend Analyzer")
st.markdown("This app visualizes the movement of **Revenue** and **Cost of Revenue** over the last 5 years.")

# 2. NIFTY 50 TICKER DICTIONARY
nifty50_dict = {
    "Reliance Industries": "RELIANCE.NS", "TCS": "TCS.NS", "HDFC Bank": "HDFCBANK.NS",
    "ICICI Bank": "ICICIBANK.NS", "Infosys": "INFY.NS", "Bharti Airtel": "BHARTIARTL.NS",
    "State Bank of India": "SBIN.NS", "Larsen & Toubro": "LT.NS", "ITC": "ITC.NS",
    "Hindustan Unilever": "HINDUNILVR.NS", "Axis Bank": "AXISBANK.NS", "Adani Enterprises": "ADANIENT.NS",
    "Kotak Mahindra Bank": "KOTAKBANK.NS", "HCL Technologies": "HCLTECH.NS", "Tata Motors": "TATAMOTORS.NS",
    "Sun Pharma": "SUNPHARMA.NS", "NTPC": "NTPC.NS", "Maruti Suzuki": "MARUTI.NS",
    "Titan Company": "TITAN.NS", "UltraTech Cement": "ULTRACEMCO.NS", "Bajaj Finance": "BAJFINANCE.NS",
    "Asian Paints": "ASIANPAINT.NS", "ONGC": "ONGC.NS", "Power Grid": "POWERGRID.NS"
}

# 3. SIDEBAR
st.sidebar.header("Settings")
selected_name = st.sidebar.selectbox("Select Company", options=list(nifty50_dict.keys()))
ticker_symbol = nifty50_dict[selected_name]

# 4. DATA FETCHING
@st.cache_data
def get_financial_trends(ticker):
    try:
        stock = yf.Ticker(ticker)
        # Fetching Annual Income Statement
        df = stock.financials.transpose()
        
        # Clean the Index (Dates) to just show the Year
        df.index = pd.to_datetime(df.index).year
        df = df.sort_index(ascending=True) # Ensure chronological order
        
        # Select the last 5 available years
        df = df.tail(5)
        return df
    except:
        return None

with st.spinner(f"Analyzing {selected_name}..."):
    df = get_financial_trends(ticker_symbol)

if df is not None and not df.empty:
    # 5. COLUMN IDENTIFICATION
    rev_col = next((c for c in df.columns if "Total Revenue" in c), None)
    cost_col = next((c for c in df.columns if "Cost Of Revenue" in c), None)

    # 6. PLOTTING
    fig = go.Figure()

    if rev_col:
        # We plot Revenue (also representing Sales)
        fig.add_trace(go.Scatter(
            x=df.index, y=df[rev_col],
            mode='lines+markers',
            name='Total Revenue / Sales',
            line=dict(color='#00d1ff', width=4)
        ))

    if cost_col:
        # FIXED: This block must be indented
        fig.add_trace(go.Scatter(
            x=df.index, y=df[cost_col],
            mode='lines+markers',
            name='Cost of Revenue',
            line=dict(color='#FF4B4B', width=4, dash='dash')
        ))

    fig.update_layout(
        title=f"5-Year Revenue & Cost Trend: {selected_name}",
        template="plotly_dark",
        xaxis=dict(tickmode='linear', title="Year"),
        yaxis_title="Amount (INR)",
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )

    st.plotly_chart(fig, use_container_width=True)

    # 7. SUMMARY INSIGHT
    if rev_col:
        latest_year = df.index[-1]
        growth = ((df[rev_col].iloc[-1] - df[rev_col].iloc[0]) / df[rev_col].iloc[0]) * 100
        st.info(f"**Quick Insight:** Since {df.index[0]}, {selected_name} has seen a **{growth:.1f}%** change in Total Revenue.")

else:
    st.error("Financial Statement not found for this ticker. Please try another company.")

st.markdown("---")
st.caption("Data: Yahoo Finance | Built with Streamlit")
