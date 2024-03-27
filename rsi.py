import requests
import os
from dotenv import load_dotenv

load_dotenv()

alpha_api = os.getenv('ALPHA_API')

url = f'https://www.alphavantage.co/query?function=RSI&symbol=IBM&interval=15min&time_period=10&series_type=close&apikey={alpha_api}'
response = requests.get(url)
data = response.json()

# Get the 'Technical Analysis: RSI' part of the data
rsi_data = data.get('Technical Analysis: RSI', {})

# The timestamps in the RSI data are the keys, so get a list of them and sort
timestamps = sorted(rsi_data.keys(), reverse=True)

# The most current timestamp will be the first one in the sorted list
most_current_timestamp = timestamps[0] if timestamps else None

# Get the RSI value for the most current timestamp
current_rsi = rsi_data[most_current_timestamp]['RSI'] if most_current_timestamp else None

if current_rsi:
    print(f"The most current RSI for IBM is {current_rsi} (at {most_current_timestamp})")
else:
    print("RSI data is unavailable.")
