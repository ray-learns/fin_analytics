import streamlit as st
import pandas as pd
import yfinance as yf

# 1. PAGE SETUP
st.set_page_config(page_title="Corporate Financial Statements", page_icon="📑", layout="wide")

st.title("📑 Corporate Financial Statements Viewer")
st.markdown("View the annual P/L Account, Balance Sheet, and Cash Flow Statement for NIFTY 50 companies.")

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
st.sidebar.header("Select Company")
selected_name = st.sidebar.selectbox("Choose a Ticker", options=list(nifty50_dict.keys()))
ticker_symbol = nifty50_dict[selected_name]

# 4. DATA FETCHING FUNCTION
@st.cache_data
def get_all_statements(ticker):
    try:
        stock = yf.Ticker(ticker)
        # Fetching the three core statements
        income_stmt = stock.financials
        balance_sheet = stock.balance_sheet
        cash_flow = stock.cashflow
        return income_stmt, balance_sheet, cash_flow
    except:
        return None, None, None

# 5. EXECUTION
with st.spinner(f"Fetching financial data for {selected_name}..."):
    income, balance, cash = get_all_statements(ticker_symbol)

if income is not None:
    # Creating Tabs for navigation
    tab1, tab2, tab3 = st.tabs(["Profit & Loss (Income Statement)", "Balance Sheet", "Cash Flow Statement"])

    

    with tab1:
        st.subheader("Profit & Loss Account (Annual)")
        # Display the last 5 columns (Years) if available
        st.dataframe(income.iloc[:, :5].style.format("{:,.0f}"), use_container_width=True)

    with tab2:
        st.subheader("Balance Sheet (Annual)")
        st.dataframe(balance.iloc[:, :5].style.format("{:,.0f}"), use_container_width=True)

    with tab3:
        st.subheader("Cash Flow Statement (Annual)")
        st.dataframe(cash.iloc[:, :5].style.format("{:,.0f}"), use_container_width=True)

    # 6. EXPORT OPTION
    st.write("---")
    if st.button("Download All Statements as Excel"):
        # Logic for creating a multi-sheet Excel could be added here
        st.info("To export, you can copy the data directly from the tables above.")

else:
    st.error("Financial records for this ticker could not be retrieved. Please try another company.")

st.markdown("---")
st.caption("Data provided by Yahoo Finance API | Values in absolute INR")
