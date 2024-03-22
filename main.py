from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from dotenv import load_dotenv
import os
import requests

load_dotenv()

api_alpha = os.environ.get('ALPHA_API')
token_telegram = os.environ.get('TELEGRAME_TOKEN')


def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hello! I am your trading bot. '
                              'Use /trade to execute a mock trade.'
                              'Use /price to execute price.'
                              "Use '/dailydata' to execute daily data.")

def trade(update: Update, context: CallbackContext) -> None:
    data = get_market_data()
    if data["trend"] == "upward":
        update.message.reply_text("Executing buy order due to an upward trend.")
    else:
        update.message.reply_text("Executing sell order due to a downward trend.")

def get_market_data():
    return {"price": 100, "trend": "upward"}  # Mocked data for demonstration


def get_market_data_2(symbol='USDT'):
    url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={api_alpha}'
    response = requests.get(url)
    data = response.json()
    try:
        price = data['Global Quote']['05. price']
        trend = "upward" if float(data['Global Quote']['09. change']) > 0 else "downward"
        return {"price": price, "trend": trend}
    except KeyError:
        return {"price": "Unavailable", "trend": "Unknown"}
    

def price(update: Update, context: CallbackContext) -> None:
    if context.args:
        symbol = context.args[0].upper()
        data = get_market_data_2(symbol)
        message = f"The current price of {symbol} is {data['price']}, and the trend is {data['trend']}."
    else:
        message = "Please provide a stock symbol. Usage: /price <SYMBOL>"
    update.message.reply_text(message)


def get_daily_crypto_data(api_key, symbol, market):
    url = f'https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_DAILY&symbol={symbol}&market={market}&apikey={api_key}'
    response = requests.get(url)
    data = response.json()
    
    try:
        today_date = data['Meta Data']['6. Last Refreshed'].split()[0]
        
        today_data = data['Time Series (Digital Currency Daily)'][today_date]
        return today_data
    except KeyError:
        return None
    
def daily_data(update: Update, context: CallbackContext) -> None:
    api_key = os.getenv('ALPHA_API')  
    args = context.args
    
    if len(args) >= 2:
        symbol = args[0].upper()
        market = args[1].upper()
    else:
        update.message.reply_text("Please provide the symbol and market. Usage: /dailydata <SYMBOL> <MARKET>")
        return
    
    data = get_daily_crypto_data(api_key, symbol, market)
    if data:
        message = f"""
Today's {symbol} Data in {market}:
💹 Market: {market}
👇👇👇👇👇👇👇
Open: {data.get(f'1a. open ({market})', 'N/A')}
High: {data.get(f'2a. high ({market})', 'N/A')}
Low: {data.get(f'3a. low ({market})', 'N/A')}
Close: {data.get(f'4a. close ({market})', 'N/A')}

⚧ Symbol: {symbol}
👇👇👇👇👇👇👇
Open: {data.get(f'1b. open ({symbol})', 'N/A')}
High: {data.get(f'2b. high ({symbol})', 'N/A')}
Low: {data.get(f'3b. low ({symbol})', 'N/A')}
Close: {data.get(f'4b. close ({symbol})', 'N/A')}

Volume: {data.get('5. volume', 'N/A')}
Market Cap (USD): {data.get('6. market cap (USD)', 'N/A')}
"""
    else:
        message = "Data is currently unavailable. Please try again later or check the symbol and market."
    
    update.message.reply_text(message)



def main():
    updater = Updater(token_telegram, use_context=True)

    print("Bot started")
    updater.start_polling()

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("trade", trade))
    dp.add_handler(CommandHandler("price", price))
    dp.add_handler(CommandHandler("dailydata", daily_data))


    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
