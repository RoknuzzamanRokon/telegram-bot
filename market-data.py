import requests 
import os
from dotenv import load_dotenv

load_dotenv()


api_alpha =  os.getenv('ALPHA_API') 

def get_market_data(symbol,market,apikey):
    # url = '&symbol=BTC&market=CNY&apikey=demo'
    url = f'https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_DAILY&symbol={symbol}&market={market}&apikey={apikey}'
    response = requests.get(url)
    data = response.json()
    try:
        today_date = data['Meta Data']['6. Last Refreshed'].split()[0]
        
        today_data = data['Time Series (Digital Currency Daily)'][today_date]
        return today_data
    except KeyError:
        return None

x = get_market_data(symbol='BTC',market='EUR',apikey=api_alpha)
print(x)