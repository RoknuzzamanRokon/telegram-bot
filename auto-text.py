from telegram.ext import Updater, CallbackContext, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import Bot, Update, ForceReply, InlineKeyboardButton, InlineKeyboardMarkup
import schedule
import time
import threading
from dotenv import load_dotenv
import requests
import os 

load_dotenv()

crypto_compare_api_key = os.getenv('CRYPTO_COMPARE_API')
api_alpha = os.environ.get('ALPHA_API')
token_telegram = os.environ.get('TELEGRAM_TOKEN')
coin_base_api_key = os.getenv('COIN_BASE_API_KEY')



def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hello! I am your 🤖🤖trading bot🤖🤖. \n\n'
                              'Use /trade to execute a mock trade.\n'
                              'Use /price to execute price.\n'
                              "Use '/daily_data' to execute daily data.\n"
                              "Use '/market_status' to execute market status.\n"
                              "Use '/check_quick_price' to 'check quick coin price' bot.\n\n"
                              "This is for USER Subscriber options\n"
                              "Use '/naru' to subscribe bot.\n"
                              "Use '/unsub_naru' to unsubscribe bot.\n"
                              "Use '/csc' to 'check subscriber count' bot.\n"
                              "Use '/home_page_button'"
                              "NOTE:- If you subscribe then you get latest news from our channel.")


def trade(update: Update, context: CallbackContext) -> None:
    response_text = "This Section under maintenance......."

    # Check if it's a callback query from a button click
    if update.callback_query:
        # Use context.bot.send_message for callback queries
        context.bot.send_message(chat_id=update.callback_query.message.chat_id, text=response_text)
    else:
        # Use update.message.reply_text for commands
        update.message.reply_text(response_text)





def get_current_price(coin_symbol):
    url = f'https://api.coinbase.com/v2/prices/{coin_symbol}-USD/spot'

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {coin_base_api_key}'
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        data = response.json()
        current_price = data['data']['amount']
        return current_price
    except Exception as e:
        print(f'Error: {str(e)}')
        return None


def check_quick_price(update: Update, context: CallbackContext) -> None:

    # It called from button_click_handler, adjust for callback queries
    chat_id = update.callback_query.message.chat_id if update.callback_query else update.message.chat_id

    keyboard = [
        [InlineKeyboardButton("BTC", callback_data='BTC'), InlineKeyboardButton("ETH", callback_data='ETH'), InlineKeyboardButton("USDC", callback_data='USDC')],
        [InlineKeyboardButton("BNB", callback_data='BNB'), InlineKeyboardButton("SOL", callback_data='SOL'), InlineKeyboardButton("SHIB", callback_data='SHIB')],
        [InlineKeyboardButton("RSR", callback_data='RSR')]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    # Use the correct method to send the message based on the context
    if update.callback_query:
        context.bot.send_message(chat_id=chat_id, text='Please choose:', reply_markup=reply_markup)
    else:
        update.message.reply_text('Please choose:', reply_markup=reply_markup)



def check_quick_price_button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()    
    coin_symbol = query.data
    price = get_current_price(coin_symbol)
    if price:
        message = f"The current price of {coin_symbol} is ${price}."
    else:
        message = "Failed to fetch the current price."
    context.bot.send_message(chat_id=update.callback_query.message.chat_id, text=message)

def price(update: Update, context: CallbackContext) -> None:
    if context.args:
        symbol = context.args[0].upper()
        data = get_current_price(coin_symbol=symbol)
        message = f"The current price of {symbol} is {data} USDT."
    else:
        message = "Please provide a symbol. Usage: /price btc"
    update.message.reply_text(message)


def ron(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [InlineKeyboardButton("Trade", callback_data='trade'),
         InlineKeyboardButton("Check Price", callback_data='price')],
        [InlineKeyboardButton("Daily Data", callback_data='daily_data'),
         InlineKeyboardButton("Market Status", callback_data='market_status')],
        [InlineKeyboardButton("Quick Price Check", callback_data='check_quick_price'),
         InlineKeyboardButton("Subscribe", callback_data='naru')],
        [InlineKeyboardButton("Unsubscribe", callback_data='unsub_naru'),
         InlineKeyboardButton("Subscriber Count", callback_data='csc')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Please choose an action:', reply_markup=reply_markup)


def button_click_handler(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()

    # Call the appropriate function based on the callback data
    if query.data == 'trade':
        trade(update, context)
    elif query.data == 'price':
        check_quick_price(update, context)
    elif query.data in ['BTC', 'ETH', 'USDC', 'BNB', 'SOL', 'SHIB', 'RSR']:
        check_quick_price_button(update, context)
    elif query.data == 'daily_data':
        context.bot.send_message(chat_id=update.callback_query.message.chat_id, text="Please provide the symbol and market in the format: /daily_data SYMBOL MARKET")











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
        update.message.reply_text("Please provide the symbol and market. Usage: /daily_data <SYMBOL> <MARKET>")
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
    
    # update.message.reply_text(message)
    # Check if it's a callback query from a button click
    if update.callback_query:
        # Use context.bot.send_message for callback queries
        context.bot.send_message(chat_id=update.callback_query.message.chat_id, text=message)
    else:
        # Use update.message.reply_text for commands
        update.message.reply_text(message)


def get_market_status(api_key):
    url = f'https://www.alphavantage.co/query?function=MARKET_STATUS&apikey={api_key}'
    response = requests.get(url)
    data = response.json()
    return data

def market_status(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Want to know about any region? Write any region name: \n\n Regin name:-👇👇👇👇\n👉👉'United States', 'Canada', 'United Kingdom', 'Germany', 'France', 'Spain', 'Portugal', 'Japan', 'India', 'Mainland China','Hong Kong','Brazil', 'Mexico','South Africa'.👈👈 \n\nWrite below 👇👇", reply_markup=ForceReply(selective=True))

def market_status_handle_response(update: Update, context: CallbackContext) -> None:
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







bot = Bot(token=token_telegram)


# Global set to store unique chat IDs
user_chat_ids = set()

def naru(update, context):
    user_chat_id = update.effective_chat.id
    user_chat_ids.add(user_chat_id)  # Add the user's chat ID to the set
    context.bot.send_message(chat_id=user_chat_id, text="Welcome!🤝🤝 You're now subscribed to Narutoe AI Bot🥳🥳🥳🥳.")

def unsub_naru(update, context):
    user_chat_id = update.effective_chat.id
    if user_chat_id in user_chat_ids:
        user_chat_ids.remove(user_chat_id)  
        context.bot.send_message(chat_id=user_chat_id, text="You have unsubscribed from crypto news updates.")
    else:
        context.bot.send_message(chat_id=user_chat_id, text="You are not subscribed.")




def get_latest_crypto_news(api_key):
    url = "https://min-api.cryptocompare.com/data/v2/news/?lang=EN"
    headers = {"authorization": f"Apikey {api_key}"}
    
    response = requests.get(url, headers=headers)
    data = response.json()
    if 'Data' in data and len(data['Data']) > 0:
        latest_news = data['Data'][0]  
        return latest_news
    else:
        return "No news found."



last_sent_news_id = None

def send_latest_crypto_news():
    global last_sent_news_id  
    latest_news = get_latest_crypto_news(crypto_compare_api_key)
    if latest_news != "No news found.":
        current_news_id = latest_news.get("id", "")
        if current_news_id != last_sent_news_id:
            news_title = latest_news.get("title", "Latest Crypto News\n")
            news_body = latest_news.get("body", "Check the link for more details.")
            message = f"Title: {news_title}\n\n👉👉👉👉: {news_body}"
            for chat_id in user_chat_ids:
                bot.send_message(chat_id=chat_id, text=message)
            last_sent_news_id = current_news_id  


def run_continuously(interval=1):
    """Run the scheduler continuously on a separate thread."""
    cease_continuous_run = threading.Event()

    class ScheduleThread(threading.Thread):
        @classmethod
        def run(cls):
            while not cease_continuous_run.is_set():
                schedule.run_pending()
                time.sleep(interval)

    continuous_thread = ScheduleThread()
    continuous_thread.start()
    return cease_continuous_run


def check_subscriber_count(update, context):
    ADMIN_CHAT_ID = os.getenv('CHAT_ID')

    user_chat_id = update.effective_chat.id
    if user_chat_id == ADMIN_CHAT_ID:  
        subscriber_count = len(user_chat_ids)
        context.bot.send_message(chat_id=user_chat_id, text=f"Current subscriber count: {subscriber_count}")
    else:
        context.bot.send_message(chat_id=user_chat_id, text="You are not authorized to use this command.")




def main():
    updater = Updater(token=token_telegram, use_context=True)
    print('Bot start...')

    updater.start_polling()
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))

    dp.add_handler(CommandHandler("ron", ron))
    dp.add_handler(CallbackQueryHandler(button_click_handler))

    dp.add_handler(CommandHandler("trade", trade))
    dp.add_handler(CommandHandler("price", price))
    dp.add_handler(CommandHandler("daily_data", daily_data, pass_args=True))
    dp.add_handler(CommandHandler("check_quick_price", check_quick_price))

    # dp.add_handler(CallbackQueryHandler(check_quick_price_button))

    
    dp.add_handler(CommandHandler("market_status", market_status))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, market_status_handle_response))


    dp.add_handler(CommandHandler('naru', naru))
    dp.add_handler(CommandHandler('unsub_naru', unsub_naru))
    dp.add_handler(CommandHandler('csc', check_subscriber_count))

    schedule.every(10).minutes.do(send_latest_crypto_news)

    # Start running the scheduler in a new thread
    run_continuously()

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

