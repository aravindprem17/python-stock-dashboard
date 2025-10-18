import requests
import pandas as pd
from io import StringIO
from fastapi import HTTPException
from cachetools import TTLCache, cached
# NOTE: Get a free API key from https://www.alphavantage.co/support/#api-key
# Store it in a file named .env in the root directory as:
# ALPHA_VANTAGE_API_KEY="YOUR_API_KEY_HERE"

# --- Create a cache ---
# Max 100 tickers, 900 seconds (15 mins) time-to-live
cache = TTLCache(maxsize=100, ttl=900)  # <-- 2. CREATE THE CACHE

BASE_URL = "https://www.alphavantage.co/query"

@cached(cache)
def get_stock_data_service(ticker: str, api_key: str):
    """
    Fetches and processes stock data from Alpha Vantage.
    Results are cached for 15 minutes.
    """
    # Add a print statement to prove the cache is working
    print(f"CACHE MISS: Fetching new data for {ticker} from Alpha Vantage...")
    
    params = {
        "function": "TIME_SERIES_DAILY_ADJUSTED",
        "symbol": ticker,
        "outputsize": "compact",  # 'compact' for last 100 days, 'full' for 20+ years
        "apikey": api_key,
        "datatype": "csv"  # CSV is much easier to parse into Pandas
    }
    
    try:
        response = requests.get(BASE_URL, params=params, timeout=10)
        response.raise_for_status()  # Raise an error for bad responses (4xx or 5xx)

        csv_text = response.text
        
        # Check for Alpha Vantage error message (which they send as 200 OK)
        if "Error Message" in csv_text or "Invalid API call" in csv_text:
            raise HTTPException(status_code=400, detail=f"Invalid ticker symbol or API call: {ticker}")
        
        if "Thank you for using Alpha Vantage" in csv_text:
             raise HTTPException(status_code=429, detail="API limit reached. Please wait a minute.")

        # Read CSV data into a Pandas DataFrame
        df = pd.read_csv(StringIO(csv_text))
        
        # --- Data Cleaning and Preparation ---
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df = df.set_index('timestamp')
        df = df.sort_index(ascending=True) # Sort by date
        
        # Rename columns for Plotly
        df = df.rename(columns={
            'open': 'Open',
            'high': 'High',
            'low': 'Low',
            'close': 'Close',
            'volume': 'Volume'
        })
        
        # Convert data to JSON serializable format (dictionary)
        # This is what the API will return
        data_json = df.to_dict('index')
        
        metadata = {
            "symbol": ticker,
            "last_refreshed": df.index[-1].strftime('%Y-%m-%d'),
            "data_points": len(df)
        }
        
        return data_json, metadata

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=503, detail=f"External API error: {e}")
