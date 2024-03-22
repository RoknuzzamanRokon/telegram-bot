from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters, CallbackContext
from dotenv import load_dotenv
import os
import requests

load_dotenv()

api_alpha = os.environ.get('ALPHA_API')
token_telegram = os.environ.get('TELEGRAM_TOKEN')


def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hello! I am your 🤖🤖trading bot🤖🤖. \n\n'
                              'Use /trade to execute a mock trade.\n'
                              'Use /price to execute price.\n'
                              "Use '/daily_data' to execute daily data.\n"
                              "Use '/market_status' to execute market status.")

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

def get_market_status(api_key):
    url = f'https://www.alphavantage.co/query?function=MARKET_STATUS&apikey={api_key}'
    response = requests.get(url)
    data = response.json()
    return data

def market_status(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Want to know about any region? Write any region name: \n\n Regin name:-👇👇👇👇\n👉👉'United States', 'Canada', 'United Kingdom', 'Germany', 'France', 'Spain', 'Portugal', 'Japan', 'India', 'Mainland China','Hong Kong','Brazil', 'Mexico','South Africa'.👈👈 \n\nWrite billow 👇👇", reply_markup=ForceReply(selective=True))

def handle_response(update: Update, context: CallbackContext) -> None:
    user_response = update.message.text

    data = get_market_status(os.getenv('ALPHA_API'))

    for market in data.get('markets',[]):
        if user_response.lower() in market.get('region', '').lower():
            message = (
                "********* Market Status **********\n\n"
                f"🏕️Region: {market['region']}\n"
                f"💹Market Type: {market['market_type']}\n"
                f"💰Primary Exchanges: {market['primary_exchanges']}\n"
                f"😇Local Open: {market['local_open']}\n"
                f"😔Local Close: {market['local_close']}\n"
                f"🕵️‍♂️Current Status: {market['current_status']}\n"
                f"📒Notes: {market['notes']}"
            )
            update.message.reply_text(message)
            return

    update.message.reply_text("Sorry 🥺, I couldn't find the market information for that region.")


def main():
    updater = Updater(token_telegram, use_context=True)

    print("Bot started")
    updater.start_polling()

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("trade", trade))
    dp.add_handler(CommandHandler("price", price))
    dp.add_handler(CommandHandler("daily_data", daily_data))

    
    dp.add_handler(CommandHandler("market_status", market_status))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_response))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
