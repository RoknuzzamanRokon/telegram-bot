from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN_2')  # Make sure you've set your bot's token as an environment variable
print(TELEGRAM_TOKEN)
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Send me any message and I will tell you the Chat ID.')

def reply_with_chat_id(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id
    update.message.reply_text(f'Your Chat ID is: {chat_id}')

def main():
    updater = Updater(token=TELEGRAM_TOKEN)
    
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, reply_with_chat_id))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
