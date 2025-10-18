import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .services import get_stock_data_service
from dotenv import load_dotenv

# Load environment variables from .env file (for API key)
load_dotenv()

app = FastAPI(
    title="StockPulse API",
    description="An API for fetching and analyzing stock market data.",
    version="1.0.0"
)

# Configure CORS (Cross-Origin Resource Sharing)
# This is crucial to allow your Streamlit frontend to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins (for development)
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/")
def read_root():
    return {"message": "Welcome to the StockPulse API. Go to /docs for documentation."}

@app.get("/api/v1/stock/{ticker}")
async def get_stock_data(ticker: str):
    """
    Fetches daily adjusted stock data for a given ticker.
    """
    try:
        # Get API key from environment variable
        api_key = os.getenv("ALPHA_VANTAGE_API_KEY")
        if not api_key:
            raise HTTPException(status_code=500, detail="API key not configured.")
            
        data, metadata = get_stock_data_service(ticker, api_key)
        
        return {
            "metadata": metadata,
            "data": data
        }
    except HTTPException as e:
        # Re-raise HTTP exceptions
        raise e
    except Exception as e:
        # Catch any other errors
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")
