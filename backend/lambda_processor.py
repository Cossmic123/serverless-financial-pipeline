# backend/lambda_processor.py (for Polygon.io and Local Testing)
import json
import os
import requests
import pandas as pd
import numpy as np
from datetime import datetime, date, timedelta

# --- Constants ---
RSI_PERIOD = 14
VOLATILITY_PERIOD = 30
SMA_PERIOD = 50
VOLUME_ANOMALY_PERIOD = 30

# --- Environment Variables ---
S3_BUCKET_NAME = os.environ.get('S3_BUCKET_NAME', '')
POLYGON_API_KEY = os.environ.get('POLYGON_API_KEY', '')

# --- KPI Calculation Functions ---
def calculate_rsi(data: pd.DataFrame, period: int = RSI_PERIOD) -> float:
    delta = data['c'].diff()
    gain, loss = delta.where(delta > 0, 0), -delta.where(delta < 0, 0)
    avg_gain, avg_loss = gain.rolling(window=period, min_periods=1).mean(), loss.rolling(window=period, min_periods=1).mean()
    if avg_loss.empty or avg_loss.iloc[-1] == 0: return 100.0
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return round(rsi.iloc[-1], 2)

def calculate_volatility(data: pd.DataFrame, period: int = VOLATILITY_PERIOD) -> float:
    if len(data) < period: return 0.0
    data['daily_return'] = data['c'].pct_change()
    volatility = data['daily_return'].tail(period).std()
    annualized_volatility = volatility * np.sqrt(252)
    return round(annualized_volatility * 100, 2)

def calculate_sma(data: pd.DataFrame, period: int = SMA_PERIOD) -> float:
    if len(data) < period: return 0.0
    sma = data['c'].rolling(window=period).mean()
    return round(sma.iloc[-1], 2)

def check_volume_anomaly(data: pd.DataFrame, period: int = VOLUME_ANOMALY_PERIOD) -> str:
    if len(data) < period: return "No"
    average_volume = data['v'].tail(period).mean()
    latest_volume = data['v'].iloc[-1]
    if average_volume > 0 and latest_volume > (average_volume * 2):
        return "Yes (Significant Spike)"
    return "No"

# --- Main Lambda Handler ---
def lambda_handler(event, context):
    try:
        message = json.loads(event['Records'][0]['Sns']['Message'])
        ticker = message['ticker'].upper()
        
        # --- 1. Fetch Overview Data from Polygon.io ---
        overview_url = f'https://api.polygon.io/v3/reference/tickers/{ticker}?apiKey={POLYGON_API_KEY}'
        overview_data = requests.get(overview_url).json().get('results', {})
        
        if not overview_data.get('name'):
            raise ValueError(f'Failed to get overview for ticker: {ticker}. Check Polygon API Key.')

        # --- 2. Fetch Historical Data from Polygon.io ---
        to_date = date.today().strftime("%Y-%m-%d")
        from_date = (date.today() - timedelta(days=100)).strftime("%Y-%m-%d")
        history_url = f'https://api.polygon.io/v2/aggs/ticker/{ticker}/range/1/day/{from_date}/{to_date}?apiKey={POLYGON_API_KEY}'
        history_data = requests.get(history_url).json().get('results', [])

        rsi_value, volatility_value, sma_50_day, volume_anomaly = "N/A", "N/A", "N/A", "N/A"
        if history_data:
            # Polygon uses 'c' for close, 'v' for volume
            price_df = pd.DataFrame(history_data)
            
            rsi_value = calculate_rsi(price_df)
            volatility_value = calculate_volatility(price_df)
            sma_50_day = calculate_sma(price_df)
            volume_anomaly = check_volume_anomaly(price_df)
        
        # --- 3. Combine All Data ---
        combined_output = {
            'symbol': overview_data.get('ticker'),
            'company_name': overview_data.get('name'),
            'pe_ratio': "N/A (Not in free Polygon)",
            'eps': "N/A (Not in free Polygon)",
            'processed_at': datetime.utcnow().isoformat(),
            'calculated_kpis': {
                'rsi_14_day': rsi_value,
                'historical_volatility_30day_percent': volatility_value,
                'sma_50_day': sma_50_day,
                'dividend_payout_ratio': "N/A (Not in free Polygon)",
                'volume_anomaly_signal': volume_anomaly
            }
        }

        # --- 4. Print output for local testing ---
        print("\n--- Final JSON Output (Local Test with Polygon.io) ---")
        print(json.dumps(combined_output, indent=2))
        
        return {'statusCode': 200, 'body': json.dumps(f'Successfully processed {ticker}')}

    except Exception as e:
        print(f"Error processing event: {str(e)}")
        return {'statusCode': 500, 'body': json.dumps(f'Error: {str(e)}')}