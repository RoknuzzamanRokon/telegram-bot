import requests
import os
from dotenv import load_dotenv

load_dotenv()

alpha_api = os.getenv('ALPHA_API')

url = 'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers=AAPL&apikey=alpha_api'

response = requests.get(url)
data = response.json()

print(data)
