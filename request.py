import requests
from dotenv import load_dotenv
import os

load_dotenv()

alpha_api = os.environ.get('ALPHA_API')

url = f'https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_DAILY&symbol=BTC&market=USD&apikey={alpha_api}'

response = requests.get(url)
data = response.json()

# Extract today's date (without time)
today_date = data['Meta Data']['6. Last Refreshed'].split()[0]

# Extract today's data
today_data = data['Time Series (Digital Currency Daily)'][today_date]

print(today_data)

