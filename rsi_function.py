import requests
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta

load_dotenv()
coin_base_api_key = os.getenv('CRYPTO_COMPARE_API')


coin_symbol = 'BTC'

    

def get_last_60_closing_prices(coin_symbol, api_key):
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(minutes=15)
    
    start_time_iso = start_time.isoformat()
    end_time_iso = end_time.isoformat()

    url = f'https://api.pro.coinbase.com/products/{coin_symbol}-USD/candles'
    params = {
        'start': start_time_iso,
        'end': end_time_iso,
        'granularity': 60  # Set granularity to 60 seconds (1 minute)
    }

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        data = response.json()
        
        closing_prices = [candle[4] for candle in data]
        return closing_prices
    except Exception as e:
        return f'Error: {str(e)}'



closing_price = get_last_60_closing_prices(coin_symbol=coin_symbol, api_key=coin_base_api_key)
window_size = 15


def calculate_rsi(closing_prices, window_size):
    diff = [closing_prices[i] - closing_prices[i - 1] for i in range(1, len(closing_prices))]
    gain = [d if d > 0 else 0 for d in diff]
    loss = [-d if d < 0 else 0 for d in diff]

    avg_gain = sum(gain[:window_size]) / window_size
    avg_loss = sum(loss[:window_size]) / window_size

    for i in range(window_size, len(gain)):
        avg_gain = (avg_gain * (window_size - 1) + gain[i]) / window_size
        avg_loss = (avg_loss * (window_size - 1) + loss[i]) / window_size

    rs = avg_gain / avg_loss if avg_loss != 0 else 0
    rsi = 100 - (100 / (1 + rs))
    return rsi


rsi_value = calculate_rsi(closing_prices=closing_price, window_size=window_size)



def get_current_price(coin_symbol):
    url = f'https://api.coinbase.com/v2/prices/{coin_symbol}-USD/spot'

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {coin_base_api_key}'
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        data = response.json()
        current_price = data['data']['amount']
        return current_price
    except Exception as e:
        print(f'Error: {str(e)}')
        return None
    
current_price = get_current_price(coin_symbol=coin_symbol)

if rsi_value < 30:
    print('Buy')
elif rsi_value > 70:
    print('Sell')
else:
    print(f'Witting for Buy sell Signal.\nCurrent {coin_symbol} price is {current_price} USD.\nRSI value is : {round(rsi_value,2)}')

