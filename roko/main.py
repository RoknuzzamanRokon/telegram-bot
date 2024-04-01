from telegram.ext import Updater, CallbackContext, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, ConversationHandler
from telegram import Bot, Update, ForceReply, InlineKeyboardButton, InlineKeyboardMarkup
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
FIRST, SECOND, THIRD = range(3)
SUB_FIRST, SUB_SECOND = range(4,6)

# Command handler for '/start'
def start(update: Update, context: CallbackContext) -> None:
    keyboard = [
                [InlineKeyboardButton("Addition", callback_data='addition')],
                [InlineKeyboardButton("Subtraction", callback_data='subtraction')]
                ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Welcome! Please choose an option:', reply_markup=reply_markup)




# CallbackQuery handler for 'Addition' button
def addition(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    query.edit_message_text(text="Give the first number:")
    return FIRST

# Handlers for collecting numbers and calculating the sum
def first_number(update: Update, context: CallbackContext) -> int:
    context.user_data['first'] = int(update.message.text)
    update.message.reply_text('Give the second number:')
    return SECOND

def second_number(update: Update, context: CallbackContext) -> int:
    context.user_data['second'] = int(update.message.text)
    update.message.reply_text('Give the third number:')
    return THIRD

def third_number(update: Update, context: CallbackContext) -> int:
    context.user_data['third'] = int(update.message.text)
    total = sum([context.user_data[k] for k in ['first', 'second', 'third']])
    update.message.reply_text(f'Your total number is: {total}')
    return ConversationHandler.END





# Start the subtraction conversation
def subtraction(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    query.edit_message_text(text="Give the first number for subtraction:")
    return SUB_FIRST

# Collect the first number for subtraction
def sub_first_number(update: Update, context: CallbackContext) -> int:
    context.user_data['sub_first'] = int(update.message.text)
    update.message.reply_text('Give the second number for subtraction:')
    return SUB_SECOND

# Collect the second number, calculate the difference, and conclude the conversation
def sub_second_number(update: Update, context: CallbackContext) -> int:
    context.user_data['sub_second'] = int(update.message.text)
    difference = context.user_data['sub_first'] - context.user_data['sub_second']
    update.message.reply_text(f'The difference is: {difference}')
    return ConversationHandler.END










# Handler for cancelling the operation
def cancel(update: Update, context: CallbackContext) -> int:
    update.message.reply_text('Operation cancelled.')
    return ConversationHandler.END

def main():
    TOKEN = token_telegram 
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Define the conversation handler
    conv_handler = ConversationHandler(
        entry_points=[
                    CallbackQueryHandler(addition, pattern='^addition$'),
                    CallbackQueryHandler(subtraction, pattern='^subtraction$')
                    ],
        
        states={
            FIRST: [MessageHandler(Filters.text & ~Filters.command, first_number)],
            SECOND: [MessageHandler(Filters.text & ~Filters.command, second_number)],
            THIRD: [MessageHandler(Filters.text & ~Filters.command, third_number)],
            SUB_FIRST: [MessageHandler(Filters.text & ~Filters.command, sub_first_number)],
            SUB_SECOND: [MessageHandler(Filters.text & ~Filters.command, sub_second_number)]

        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(conv_handler)

    # Start the Bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()