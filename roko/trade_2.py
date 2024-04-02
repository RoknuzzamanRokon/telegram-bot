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


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)




# Define states for conversation
FIRST, SECOND, THIRD, FOURTH = range(4)

# Command handler for '/start'
def start(update: Update, context: CallbackContext) -> None:
    keyboard = [
                [InlineKeyboardButton("trade", callback_data='trade')]
                ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Welcome! Please choose an option:', reply_markup=reply_markup)




# CallbackQuery handler for 'Addition' button
def trade(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    query.edit_message_text(text="Give api key:")
    return FIRST

# Handlers for collecting numbers and calculating the sum
def first_number(update: Update, context: CallbackContext) -> int:
    context.user_data['api_key'] = str(update.message.text)
    update.message.reply_text('Give api secret')
    return SECOND

def second_number(update: Update, context: CallbackContext) -> int:
    context.user_data['api_secret'] = str(update.message.text)
    update.message.reply_text('Give product id')
    return THIRD

def third_number(update: Update, context: CallbackContext) -> int:
    context.user_data['product_id'] = str(update.message.text)
    update.message.reply_text('Give usd')
    return FOURTH

def fourth_number(update: Update, context: CallbackContext) -> int:
    context.user_data['usd'] = int(update.message.text)

    api_key = context.user_data['api_key']
    api_secret = context.user_data['api_secret']
    product_id = context.user_data['product_id']
    btc_size = context.user_data['usd']

    # set_api_credentials(api_key, api_secret)
    # market_buy = fiat_market_buy(product_id, btc_size)    
    # update.message.reply_text(f'trade {market_buy}')

    return ConversationHandler.END











# Handler for cancelling the operation
def cancel(update: Update, context: CallbackContext) -> int:
    update.message.reply_text('Operation cancelled.')
    return ConversationHandler.END

def main():
    TOKEN = token_telegram 
    updater = Updater(TOKEN, use_context=True)

    print("start bot 1....")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher
    print("start bot 2....")

    # Define the conversation handler
    conv_handler = ConversationHandler(
        entry_points=[
                    CallbackQueryHandler(trade, pattern='^trade$')
                    ],
        
        states={
            FIRST: [MessageHandler(Filters.text & ~Filters.command, first_number)],
            SECOND: [MessageHandler(Filters.text & ~Filters.command, second_number)],
            THIRD: [MessageHandler(Filters.text & ~Filters.command, third_number)],
            FOURTH: [MessageHandler(Filters.text & ~Filters.command, fourth_number)],


        },
        fallbacks=[CommandHandler('cancel', cancel)],
        per_message=False
    )
    print("start bot 3....")

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(conv_handler)
    print("start bot 4....")

    # Start the Bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()