import requests
import os
from dotenv import load_dotenv

load_dotenv()

alpha_api = os.getenv('ALPHA_API')
crypto_compare_api_key = os.getenv('CRYPTO_COMPARE_API')

url = 'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers=AAPL&apikey=alpha_api'

response = requests.get(url)
data = response.json()




def get_latest_crypto_news(api_key):
    url = "https://min-api.cryptocompare.com/data/v2/news/?lang=EN"
    headers = {"authorization": f"Apikey {api_key}"}
    
    response = requests.get(url, headers=headers)
    data = response.json()
    print(data)
    if 'Data' in data and len(data['Data']) > 0:
        latest_news = data['Data'][0]  
        return latest_news
    else:
        return "No news found."

data = get_latest_crypto_news(api_key=crypto_compare_api_key)
print(data)