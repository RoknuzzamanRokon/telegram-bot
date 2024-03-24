import requests
import os


coin_base_api_key = os.getenv('COIN_BASE_API_KEY')

def get_coinbase_price(coin_symbol, api_key):
    url = f'https://api.coinbase.com/v2/prices/{coin_symbol}-USD/spot'

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        data = response.json()
        current_price = data['data']['amount']
        return current_price
    except Exception as e:
        print(f'Error: {str(e)}')
        return None
    

data = get_coinbase_price(coin_symbol='BTC', api_key=coin_base_api_key)
print(data)