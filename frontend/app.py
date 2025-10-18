import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# --- Configuration ---
# Set the base URL for your FastAPI backend
API_BASE_URL = "http://127.0.0.1:8000/api/v1"

st.set_page_config(
    page_title="StockPulse Dashboard",
    page_icon="📈",
    layout="wide"  # Use the full page width
)

# --- Helper Function ---
def create_stock_chart(df, ticker):
    """Creates a Plotly Candlestick chart with Volume."""
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, 
                        vertical_spacing=0.03, subplot_titles=(f'{ticker.upper()} Candlestick', 'Volume'), 
                        row_width=[0.2, 0.7])

    fig.add_trace(go.Candlestick(x=df.index,
                                 open=df['Open'],
                                 high=df['High'],
                                 low=df['Low'],
                                 close=df['Close'],
                                 name="Candlestick"),
                  row=1, col=1)

    fig.add_trace(go.Bar(x=df.index, y=df['Volume'], name="Volume", marker_color='blue'),
                  row=2, col=1)

    fig.update_layout(
        yaxis_title="Stock Price ($)",
        xaxis_rangeslider_visible=False,
        showlegend=False,
        height=700
    )
    fig.update_yaxes(title_text="Volume", row=2, col=1)
    return fig

# --- Main App ---

# 1. (UI) Use the sidebar for controls
st.sidebar.header("📈 StockPulse Controls")
ticker_input = st.sidebar.text_input(
    "Enter Stock Ticker", 
    value="AAPL",  # 2. (UX) Set a default value
    help="Type a ticker (e.g., AAPL, MSFT) and press Enter."
).upper()

# Main page title
st.title(f"StockPulse Dashboard: {ticker_input}")

# 3. (UX) The app logic now runs every time the input changes (no button)
if ticker_input:
    try:
        # --- API Call ---
        with st.spinner(f"Fetching data for {ticker_input}..."):
            response = requests.get(f"{API_BASE_URL}/stock/{ticker_input}")
            
            if response.status_code == 200:
                data = response.json()
                stock_data = data.get("data", {})
                metadata = data.get("metadata", {})
                
                if not stock_data:
                    st.error("No data returned from API. The ticker might be invalid.")
                else:
                    # --- Data Processing ---
                    df = pd.DataFrame.from_dict(stock_data, orient='index')
                    df.index = pd.to_datetime(df.index)
                    
                    # --- 4. (UI) Add Key Metrics ---
                    st.subheader(f"Key Metrics for {ticker_input}")
                    
                    # Get latest and previous day's close
                    latest_close = df['Close'].iloc[-1]
                    prev_close = df['Close'].iloc[-2]
                    
                    # Calculate change
                    change = latest_close - prev_close
                    percent_change = (change / prev_close) * 100
                    
                    # Display metrics in columns
                    col1, col2, col3 = st.columns(3)
                    col1.metric(
                        label="Latest Close",
                        value=f"${latest_close:,.2f}",
                        delta=f"${change:,.2f} ({percent_change:,.2f}%)"
                    )
                    col2.metric(label="Latest Volume", value=f"{df['Volume'].iloc[-1]:,}")
                    col3.metric(label="Last Refreshed", value=metadata.get('last_refreshed', 'N/A'))
                    
                    st.markdown("---") # Visual separator

                    # --- Display Chart ---
                    st.subheader(f"100-Day Performance")
                    fig = create_stock_chart(df, ticker_input)
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # --- Display Raw Data ---
                    with st.expander("View Raw Data (Last 5 Days)"):
                        st.dataframe(df.tail(5))
            
            else:
                # Handle API errors
                error_details = response.json().get("detail", "Unknown error")
                st.error(f"Error fetching data: {error_details} (Status code: {response.status_code})")

    except requests.exceptions.ConnectionError:
        st.error(f"Failed to connect to the API. Is the backend server running?")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
else:
    st.info("Please enter a stock ticker in the sidebar to get started.")
