# 📈 StockPulse: Full-Stack Python Dashboard

**Live Demo:** [Link to your deployed Streamlit app]
**API Docs:** [Link to your deployed FastAPI /docs]

This is a full-stack financial dashboard built entirely in Python. It features a FastAPI backend that fetches data from the Alpha Vantage API and a Streamlit frontend that provides an interactive visualization.

This project demonstrates:
* **Backend API Development** with **FastAPI**.
* **Frontend Web App Development** with **Streamlit**.
* **Data Analysis and Manipulation** with **Pandas**.
* **Interactive Data Visualization** with **Plotly**.
* **Consuming Third-Party REST APIs** with **Requests**.
* **Environment Management** with `dotenv` and `requirements.txt`.
* **Clear Project Structure** separating backend and frontend concerns.

## Tech Stack

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-green?logo=fastapi)
![Streamlit](https://img.shields.io/badge/Streamlit-1.25%2B-red?logo=streamlit)
![Pandas](https://img.shields.io/badge/Pandas-2.0%2B-purple?logo=pandas)
![Plotly](https://img.shields.io/badge/Plotly-5.15%2B-blue?logo=plotly)

## How to Run This Project Locally

### 1. Prerequisites
* Python 3.10 or newer.
* A free API key from [Alpha Vantage](https://www.alphavantage.co/support/#api-key).

### 2. Setup
1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/your-username/python-stock-dashboard.git](https://github.com/your-username/python-stock-dashboard.git)
    cd python-stock-dashboard
    ```

2.  **Create a virtual environment and install packages:**
    ```bash
    # Create venv
    python -m venv venv
    # Activate venv (Windows)
    .\venv\Scripts\activate
    # Activate venv (macOS/Linux)
    source venv/bin/activate
    
    # Install dependencies
    pip install -r requirements.txt
    ```

3.  **Set up your API Key:**
    Create a file named `.env` in the project's root directory (`python-stock-dashboard/`). Add your API key to it:
    ```
    ALPHA_VANTAGE_API_KEY="YOUR_API_KEY_HERE"
    ```

### 3. Running the Application
You must run two servers in two separate terminals.

**Terminal 1: Run the FastAPI Backend**
```bash
cd backend
uvicorn main:app --reload --port 8000
