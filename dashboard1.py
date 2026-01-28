import streamlit as st
import yfinance as yf
import datetime
import plotly.express as px

# App title
st.title("Yahoo Stock Dashboard")
st.sidebar.title("Please provide the following")

# Sidebar inputs
ticker_symbol = st.sidebar.text_input("Enter ticker symbol", "AAPL")

# Default date range
today = datetime.date.today()
start_date = st.sidebar.date_input("Start date", today - datetime.timedelta(days=30))
end_date = st.sidebar.date_input("End date", today)

# Validation
if start_date > end_date:
    st.error("Start date must be before end date")

elif ticker_symbol:

    stock_data = yf.download(ticker_symbol, start=start_date, end=end_date)

    if not stock_data.empty:

        # FIX: remove multi-index columns
        stock_data.columns = stock_data.columns.get_level_values(0)

        st.subheader(f"{ticker_symbol} Stock Overview")

        price_tab, hist_tab, chart_tab = st.tabs(
            ["Price Summary", "Historical Data", "Charts"]
        )

        with price_tab:
            st.write("Latest Price")
            st.dataframe(stock_data.tail(1))

        with hist_tab:
            st.write("Historical Data")
            st.dataframe(stock_data)

        with chart_tab:
            st.write("Stock Price Trend")
            fig = px.line(
                stock_data,
                x=stock_data.index,
                y="Close",
                title=f"{ticker_symbol} Closing Price"
            )
            st.plotly_chart(fig)

    else:
        st.warning("No data found for selected date range")
