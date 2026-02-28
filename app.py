import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go

# 1. PAGE SETUP
st.set_page_config(page_title="Corporate P/L Analyzer", page_icon="📊", layout="wide")

st.title("📊 Corporate Profit & Loss (P/L) Analyzer")
st.markdown("Fetch and analyze the annual Income Statement (P/L) for NIFTY 50 companies directly from Yahoo Finance.")

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

# 3. SIDEBAR CONTROLS
st.sidebar.header("Navigation")
selected_name = st.sidebar.selectbox("Select Company", options=list(nifty50_dict.keys()))
ticker_symbol = nifty50_dict[selected_name]

# 4. DATA FETCHING FUNCTION
@st.cache_data
def get_pl_statement(ticker):
    try:
        stock = yf.Ticker(ticker)
        # .financials returns the annual Income Statement (P/L)
        pl_data = stock.financials
        return pl_data
    except Exception as e:
        return None

# 5. MAIN LOGIC
with st.spinner(f"Loading P/L Statement for {selected_name}..."):
    pl_df = get_pl_statement(ticker_symbol)

if pl_df is not None and not pl_df.empty:
    
    # --- METRICS SUMMARY ---
    # We transpose to get dates as rows for easier extraction
    df_t = pl_df.transpose()
    
    # Clean the index to show only Year
    df_t.index = pd.to_datetime(df_t.index).year
    
    st.subheader(f"Financial Summary: {selected_name}")
    
    # Use fallback names because yfinance headers can vary slightly
    rev_key = next((c for c in df_t.columns if "Total Revenue" in c), None)
    net_key = next((c for c in df_t.columns if "Net Income" in c), None)

    if rev_key and net_key:
        latest_rev = df_t[rev_key].iloc[0]
        latest_net = df_t[net_key].iloc[0]
        margin = (latest_net / latest_rev) * 100

        m1, m2, m3 = st.columns(3)
        m1.metric("Total Revenue (Latest Year)", f"₹{latest_rev/1e7:,.2f} Cr")
        m2.metric("Net Income (Latest Year)", f"₹{latest_net/1e7:,.2f} Cr")
        m3.metric("Net Profit Margin", f"{margin:.2f}%")

    # --- VISUALIZATION ---
    st.write("---")
    st.subheader("Revenue vs. Net Income Growth")
    
    fig = go.Figure()
    fig.add_trace(go.Bar(x=df_t.index, y=df_t[rev_key], name="Total Revenue", marker_color='#00d1ff'))
    fig.add_trace(go.Bar(x=df_t.index, y=df_t[net_key], name="Net Income", marker_color='#00ff88'))
    
    fig.update_layout(
        template="plotly_dark",
        barmode='group',
        xaxis_title="Year",
        yaxis_title="Amount (INR)",
        hovermode="x unified"
    )
    st.plotly_chart(fig, use_container_width=True)

    # --- FULL P/L TABLE ---
    st.write("---")
    st.subheader("Full Income Statement (Annual)")
    st.dataframe(pl_df.style.format("{:,.0f}"), use_container_width=True)

    # --- DOWNLOAD BUTTON ---
    csv = pl_df.to_csv().encode('utf-8')
    st.download_button(
        label="📥 Download P/L Statement as CSV",
        data=csv,
        file_name=f"{selected_name}_PL_Statement.csv",
        mime='text/csv',
    )

else:
    st.error(f"Financial data for {ticker_symbol} is currently unavailable. Some companies may not have updated filings on Yahoo Finance.")

st.markdown("---")
st.caption("Data source: Yahoo Finance API | Figures in Absolute INR (unless stated otherwise)")
