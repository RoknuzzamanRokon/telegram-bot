from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from dotenv import load_dotenv
import os

load_dotenv()

api_alpha = os.environ.get('ALPHA_API')
token_telegram = os.environ.get('TELEGRAME_TOKEN')


def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hello! I am your trading bot. Use /trade to execute a mock trade.')

def trade(update: Update, context: CallbackContext) -> None:
    data = get_market_data()
    if data["trend"] == "upward":
        update.message.reply_text("Executing buy order due to an upward trend.")
    else:
        update.message.reply_text("Executing sell order due to a downward trend.")

def get_market_data():
    return {"price": 100, "trend": "upward"}  # Mocked data for demonstration

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

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
