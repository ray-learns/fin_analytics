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
        fig.add_trace(go.Scatter
