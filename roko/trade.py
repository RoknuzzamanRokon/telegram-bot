from telegram.ext import Updater, CallbackContext, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, ConversationHandler
from telegram import Bot, Update, ForceReply, InlineKeyboardButton, InlineKeyboardMarkup
from coinbase_advanced_trader.config import set_api_credentials
from coinbase_advanced_trader.strategies.market_order_strategies import fiat_market_buy
import time
from dotenv import load_dotenv
import requests
import os 
import logging

load_dotenv()

token_telegram = os.environ.get('TELEGRAM_TOKEN_2')
coinbase_api_key = os.environ.get('COIN_BASE_API_KEY')
coinbase_api_secret=os.environ.get('COIN_BASE_API_SECRET')


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)



user_data = {}

def start(update: Update, context: CallbackContext) -> None:
    keyboard = [[InlineKeyboardButton("Trade", callback_data='trade')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Please choose:', reply_markup=reply_markup)

def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    data = query.data

    if data == 'trade':
        query.edit_message_text(text="Please send your API_KEY")
        return

def collect_info(update: Update, context: CallbackContext) -> None:
    text = update.message.text
    chat_id = update.message.chat_id

    if chat_id not in user_data:
        user_data[chat_id] = {'step': 'API_KEY'}
        update.message.reply_text("Please send your API_SECRET")

    elif user_data[chat_id]['step'] == 'API_KEY':
        user_data[chat_id]['API_KEY'] = text
        user_data[chat_id]['step'] = 'API_SECRET'
        update.message.reply_text("Please send your PRODUCT_ID")
        
    elif user_data[chat_id]['step'] == 'API_SECRET':
        user_data[chat_id]['API_SECRET'] = text
        user_data[chat_id]['step'] = 'PRODUCT_ID'
        update.message.reply_text("Please send your BTC_SIZE")

    elif user_data[chat_id]['step'] == 'PRODUCT_ID':
        user_data[chat_id]['PRODUCT_ID'] = text
        user_data[chat_id]['step'] = 'WAITING_BTC_SIZE'
        update.message.reply_text("Please send your BTC_SIZE")
        
    elif user_data[chat_id]['step'] == 'WAITING_BTC_SIZE':
        user_data[chat_id]['BTC_SIZE'] = text

        update.message.reply_text("Thank you. Processing your trade...")


        api_key = user_data[chat_id]['API_KEY']
        print(f'api key {api_key}')
        api_secret = user_data[chat_id]['API_SECRET']
        print(f'api secret {api_secret}')
        product_id = user_data[chat_id]['PRODUCT_ID']
        print(f'product id {product_id}')
        btc_size = user_data[chat_id]['BTC_SIZE']
        print(f'btc size {btc_size}')

        set_api_credentials(api_key, api_secret)
        market_buy = fiat_market_buy(product_id, btc_size)
        print(market_buy)

        # Clear user data
        del user_data[chat_id]        

def main() -> None:
    TOKEN = token_telegram 
    updater = Updater(TOKEN, use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CallbackQueryHandler(button))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, collect_info))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()