import requests
import os 
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('CRYPTO_COMPARE_API')

def get_latest_crypto_news(api_key):
    url = "https://min-api.cryptocompare.com/data/v2/news/?lang=EN"
    headers = {"authorization": f"Apikey {api_key}"}
    
    response = requests.get(url, headers=headers)
    data = response.json()
    return data


data = get_latest_crypto_news(api_key=api_key)

