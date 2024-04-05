import requests
import hmac
import hashlib
import time
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.environ.get('COIN_BASE_API_KEY_1')
API_SECRET = os.environ.get('COIN_BASE_API_SECRET_1')

def generate_signature(timestamp, method, request_path, body=''):
    message = f"{timestamp}{method}{request_path}{body}"
    signature = hmac.new(API_SECRET.encode('utf-8'), message.encode('utf-8'), hashlib.sha256).hexdigest()
    return signature

def get_account_info():
    timestamp = str(int(time.time()))
    method = 'GET'
    request_path = '/v2/accounts'  # Ensure this is the correct endpoint
    signature = generate_signature(timestamp, method, request_path)

    headers = {
        'CB-ACCESS-KEY': API_KEY,
        'CB-ACCESS-SIGN': signature,
        'CB-ACCESS-TIMESTAMP': timestamp,
        'Content-Type': 'application/json'
    }

    url = 'https://api.coinbase.com' + request_path
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        try:
            return response.json()  # Attempt to parse JSON response
        except ValueError:  # Catch JSON decoding errors
            print("Failed to decode JSON from response.")
            return None
    else:
        # Handle non-200 responses
        print(f"Request failed with status code {response.status_code}: {response.text}")
        return None

account_info = get_account_info()
print(account_info)
