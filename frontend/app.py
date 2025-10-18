import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# --- Configuration ---
# Set the base URL for your FastAPI backend
# If running locally:
API_BASE_URL = "http://127.0.0.1:8000/api/v1"
# If deployed (e.g., on Render):
# API_BASE_URL = "https://your-api-service-name.onrender.com/api/v1"

st.set_page_config(
    page_title="StockPulse Dashboard",
    page_icon="📈",
    layout="wide"
)

# --- Helper Function ---
def create_stock_chart(df, ticker):
    """Creates a Plotly Candlestick chart with Volume."""
    
    # Create figure with secondary y-axis
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, 
                        vertical_spacing=0.03, subplot_titles=(f'{ticker.upper()} Candlestick', 'Volume'), 
                        row_width=[0.2, 0.7])

    # Plot Candlestick
    fig.add_trace(go.Candlestick(x=df.index,
                                 open=df['Open'],
                                 high=df['High'],
                                 low=df['Low'],
                                 close=df['Close'],
                                 name="Candlestick"),
                  row=1, col=1)

    # Plot Volume
    fig.add_trace(go.Bar(x=df.index, y=df['Volume'], name="Volume", marker_color='blue'),
                  row=2, col=1)

    # Update layout
    fig.update_layout(
        title=f"{ticker.upper()} Daily Price and Volume",
        yaxis_title="Stock Price ($)",
        xaxis_rangeslider_visible=False, # Hide range slider on main chart
        showlegend=False
    )
    
    fig.update_yaxes(title_text="Volume", row=2, col=1)
    fig.update_layout(height=700)
    
    return fig

# --- Streamlit App ---
st.title("📈 StockPulse Interactive Dashboard")
st.markdown("Enter a stock ticker to see its 100-day performance.")

# --- User Input ---
ticker_input = st.text_input("Enter Stock Ticker (e.g., AAPL, MSFT, GOOG)", "AAPL").upper()
fetch_button = st.button("Fetch Data")

if fetch_button:
    if not ticker_input:
        st.warning("Please enter a stock ticker.")
    else:
        try:
            # --- API Call ---
            with st.spinner(f"Fetching data for {ticker_input}..."):
                response = requests.get(f"{API_BASE_URL}/stock/{ticker_input}")
                
                # Check for successful response
                if response.status_code == 200:
                    data = response.json()
                    
                    stock_data = data.get("data", {})
                    metadata = data.get("metadata", {})
                    
                    if not stock_data:
                        st.error("No data returned from API. The ticker might be invalid.")
                    else:
                        # --- Data Processing ---
                        # Convert the JSON (dictionary) back into a DataFrame
                        df = pd.DataFrame.from_dict(stock_data, orient='index')
                        df.index = pd.to_datetime(df.index)
                        
                        # --- Display Data ---
                        st.success(f"Successfully fetched data for {metadata.get('symbol', ticker_input)}.")
                        st.markdown(f"**Last Refreshed:** {metadata.get('last_refreshed', 'N/A')}")
                        
                        # Create and display chart
                        fig = create_stock_chart(df, ticker_input)
                        st.plotly_chart(fig, use_container_width=True)
                        
                        # Display raw data in an expander
                        with st.expander("View Raw Data (Last 5 Days)"):
                            st.dataframe(df.tail(5))
                
                else:
                    # Handle API errors
                    error_details = response.json().get("detail", "Unknown error")
                    st.error(f"Error fetching data: {error_details} (Status code: {response.status_code})")

        except requests.exceptions.ConnectionError:
            st.error(f"Failed to connect to the API. Is the backend server running at {API_BASE_URL}?")
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")
