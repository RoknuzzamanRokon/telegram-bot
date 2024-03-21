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
                              'Use /price to execute price')

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


def main():
    token = '7140481417:AAHGrdKjCCbMguXFIoUaSsuPDzRRaGEN-gI'
    print(token)
    print(token_telegram)
    if token==token_telegram:
        print('true')
    else:
        print('false')
    updater = Updater(token_telegram)

    print("Bot started")
    updater.start_polling()

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("trade", trade))
    dp.add_handler(CommandHandler("price", price))


    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
