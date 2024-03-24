from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import os

def reply_with_user_id(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    update.message.reply_text(f'Your User ID is: {user_id}')

def main():
    TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')  # Make sure your bot token is correctly set in your environment variables
    updater = Updater(TELEGRAM_TOKEN, use_context=True)
    
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, reply_with_user_id))
    
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
