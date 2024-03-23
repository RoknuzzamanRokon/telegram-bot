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


def get_latest_crypto_news(api_key):
    url = "https://min-api.cryptocompare.com/data/v2/news/?lang=EN"
    headers = {"authorization": f"Apikey {api_key}"}
    
    response = requests.get(url, headers=headers)
    data = response.json()
    if 'Data' in data and len(data['Data']) > 0:
        latest_news = data['Data'][0]  # Assuming the first news is the latest
        return latest_news
    else:
        return "No news found."


latest_news = get_latest_crypto_news(api_key)
print(latest_news)