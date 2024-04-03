from telegram.ext import Updater, CallbackContext, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, ConversationHandler
from telegram import Bot, Update, ForceReply, InlineKeyboardButton, InlineKeyboardMarkup
import schedule
import time
import threading
from dotenv import load_dotenv
import requests
import os 
from rsi_function import calculate_rsi, get_last_60_closing_prices
from threading import Thread
import logging




# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


load_dotenv()

crypto_compare_api_key = os.getenv('CRYPTO_COMPARE_API')
api_alpha = os.environ.get('ALPHA_API')
token_telegram = os.environ.get('TELEGRAM_TOKEN')
coin_base_api_key = os.getenv('COIN_BASE_API_KEY')



def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hello! I am your 🤖🤖trading bot🤖🤖. \n\n'
                              'Use /home and go to home page.\n\n'
                              'This section for manually use link'
                              'Use /trade to execute a mock trade.\n'
                              'Use /price to execute price.\n'
                              "Use '/daily_data' to execute daily data.\n"
                              "Use '/market_status' to execute market status.\n"
                              "Use '/check_quick_price' to 'check quick coin price' bot.\n\n\n"
                              "This is for USER Subscriber options\n"
                              "Use '/subscribe' to subscribe bot.\n"
                              "Use '/unsubscribe' to unsubscribe bot.\n"
                              "Use '/csc' to 'check subscriber count' bot.\n\n"

                              "NOTE:- If you subscribe then you get latest news from our channel.")


def trade(update: Update, context: CallbackContext) -> None:
    coin_symbol = 'BTC'
    coin_base_api_key = os.getenv('CRYPTO_COMPARE_API') 
    window_size = 15

    # Fetch the last 60 closing prices
    closing_prices = get_last_60_closing_prices(coin_symbol, coin_base_api_key)
    if not closing_prices or isinstance(closing_prices, str): 
        response_text = "Failed to fetch closing prices."
        update.message.reply_text(response_text)
        return

    # Calculate the RSI value
    rsi_value = calculate_rsi(closing_prices, window_size)

    # Get the current price of the coin
    current_price = get_current_price(coin_symbol)
    if current_price is None:
        response_text = "Failed to fetch the current price."
        update.message.reply_text(response_text)
        return

    # Determine the action based on RSI value
    if rsi_value < 30:
        action = 'Buy signal detected. 📈\n\nCurrent {coin_symbol} price is {current_price} USD.\nRSI value is : {round(rsi_value,2)}'
    elif rsi_value > 70:
        action = f'Sell signal detected. 📉\n\nCurrent {coin_symbol} price is {current_price} USD.\nRSI value is : {round(rsi_value,2)}'
    else:
        action = f'📈📈Witting for Buy sell Signal📉📉.\n\nCurrent {coin_symbol} price is {current_price} USD.\nRSI value is : {round(rsi_value,2)}'

    if update.callback_query:
        context.bot.send_message(chat_id=update.callback_query.message.chat_id, text=action)
    else:
        update.message.reply_text(action)





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

    chat_id = update.callback_query.message.chat_id if update.callback_query else update.message.chat_id

    keyboard = [
        [InlineKeyboardButton("BTC", callback_data='BTC'), InlineKeyboardButton("ETH", callback_data='ETH'), InlineKeyboardButton("USDC", callback_data='USDC')],
        [InlineKeyboardButton("BNB", callback_data='BNB'), InlineKeyboardButton("SOL", callback_data='SOL'), InlineKeyboardButton("SHIB", callback_data='SHIB')],
        [InlineKeyboardButton("RSR", callback_data='RSR')]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
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




def handle_symbol_market_response(update: Update, context: CallbackContext) -> None:
    if context.user_data.get('awaiting_data'):
        try:
            symbol, market = update.message.text.upper().split()
            daily_data_response(update, context, symbol, market)
            context.user_data['awaiting_data'] = False  
        except ValueError:
            update.message.reply_text("Format is incorrect. Please provide SYMBOL MARKET.")

def daily_data_response(update: Update, context: CallbackContext, symbol: str, market: str) -> None:
    api_key = os.getenv('ALPHA_API')  
    
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
    
    if update.callback_query:
        context.bot.send_message(chat_id=update.callback_query.message.chat_id, text=message)
    else:
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
    
    if update.callback_query:
        context.bot.send_message(chat_id=update.callback_query.message.chat_id, text=message)
    else:
        update.message.reply_text(message)





def home(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [InlineKeyboardButton("Trade", callback_data='trade'),
         InlineKeyboardButton("Check Price", callback_data='price')],
        [InlineKeyboardButton("Daily Data", callback_data='daily_data'),
         InlineKeyboardButton("Market Status", callback_data='market_status')],
         [InlineKeyboardButton("Help", callback_data='help')],
         [InlineKeyboardButton("trade now", callback_data='trade_now')],
         [InlineKeyboardButton("Connect Admin", url='https://t.me/Rokon017399?text=👋+Hello')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Please choose an action:', reply_markup=reply_markup)


def button_click_handler(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()

    # This line is the focus: accessing chat_id correctly depending on the type of update
    chat_id = query.message.chat_id if query else update.message.chat_id

    if query.data == 'trade':
        trade(update, context)
    elif query.data == 'price':
        check_quick_price(update, context)
    elif query.data in ['BTC', 'ETH', 'USDC', 'BNB', 'SOL', 'SHIB', 'RSR']:
        check_quick_price_button(update, context)
    elif query.data == 'daily_data':
        context.user_data['awaiting_data'] = True
        context.bot.send_message(chat_id=chat_id, text="Please provide the symbol and market in the format: SYMBOL MARKET")
    elif query.data == 'market_status':
        context.user_data['awaiting_market_status'] = True
        context.bot.send_message(chat_id=chat_id, text="Want to know about any region? Write any region name: \n\nRegion name:-👇👇👇👇\n👉👉'United States', 'Canada', 'United Kingdom', 'Germany', 'France', 'Spain', 'Portugal', 'Japan', 'India', 'Mainland China','Hong Kong','Brazil', 'Mexico','South Africa'.👈👈 \n\nWrite below 👇👇")
    
    elif query.data == 'trade_now':
        if not check_subscription(chat_id):
            context.bot.sendMessage(chat_id=chat_id, text="Please subscribe to initiate trades.")
        else:
            # Instruct the user on what to do next to start the conversation
            context.bot.sendMessage(chat_id=chat_id, text="Please type '/trade_now' to start trading.")
   
    elif query.data == 'help':
        help(update, context)



def help(update: Update, context: CallbackContext) -> None:
    response_text = "If you want to get update news and trade signal then must subscribe.\n Subscribe now for click here 👉 /subscribe"

    if update.callback_query:
        context.bot.send_message(chat_id=update.callback_query.message.chat_id, text=response_text)
    else:
        update.message.reply_text(response_text)







def get_market_status(api_key):
    url = f'https://www.alphavantage.co/query?function=MARKET_STATUS&apikey={api_key}'
    response = requests.get(url)
    data = response.json()
    return data

def market_status(update: Update, context: CallbackContext) -> None:
    context.user_data['awaiting_market_status'] = True
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
    



def generic_text_handler(update: Update, context: CallbackContext) -> None:
    if context.user_data.get('awaiting_market_status'):
        market_status_handle_response(update, context)
        context.user_data.pop('awaiting_market_status', None)  
    elif context.user_data.get('awaiting_data'):
        handle_symbol_market_response(update, context)
        context.user_data.pop('awaiting_data', None)  
    else:
        update.message.reply_text("I'm not sure what you're trying to do. Go to /start option.")




# Global set to store unique chat IDs
user_chat_ids = set()
print(user_chat_ids)

def subscribe(update, context):
    user_chat_id = update.effective_chat.id
    user_chat_ids.add(user_chat_id) 
    context.bot.send_message(chat_id=user_chat_id, text="Welcome!🤝🤝 You're now subscribed to Narutoe AI Bot🥳🥳🥳🥳.")

def unsubscribe(update, context):
    user_chat_id = update.effective_chat.id
    if user_chat_id in user_chat_ids:
        user_chat_ids.remove(user_chat_id)  
        context.bot.send_message(chat_id=user_chat_id, text="You have unsubscribed from crypto news updates.")
    else:
        context.bot.send_message(chat_id=user_chat_id, text="You are not subscribed.")

def check_subscriber_count(update, context):
    ADMIN_CHAT_ID = os.getenv('CHAT_ID')

    user_chat_id = update.effective_chat.id
    if user_chat_id == ADMIN_CHAT_ID:  
        subscriber_count = len(user_chat_ids)
        context.bot.send_message(chat_id=user_chat_id, text=f"Current subscriber count: {subscriber_count}")
    else:
        context.bot.send_message(chat_id=user_chat_id, text="You are not authorized to use this command.")


def check_subscription(chat_id) -> bool:
    return chat_id in user_chat_ids








FIRST, SECOND, THIRD, FOURTH = range(4)

def trade_now(update: Update, context: CallbackContext) -> int:
    # Check if it's called from a button press (callback query)
    if update.callback_query:
        query = update.callback_query
        query.answer()
        chat_id = query.message.chat_id
        # Edit the message if it's from a callback query
        query.edit_message_text(text="Give api key:")
    else:
        # If not from a callback query, assume it's from a command or direct message
        chat_id = update.message.chat_id
        # Send a new message instead of editing
        context.bot.sendMessage(chat_id=chat_id, text="Give api key:")
    return FIRST

def collect_api_key(update: Update, context: CallbackContext) -> int:
    collect_api_key = update.message.text
    context.user_data['collect_api_key'] = collect_api_key

    update.message.reply_text("Give api secret.")
    return SECOND

def collect_api_secret(update: Update, context: CallbackContext) -> int:
    collect_api_secret = update.message.text
    context.user_data['collect_api_secret'] = collect_api_secret

    update.message.reply_text('Give your product key pair.')
    return THIRD

def collect_product_id(update: Update, context: CallbackContext) -> int:
    collect_product_id = update.message.text
    context.user_data['collect_product_id'] = collect_product_id 

    update.message.reply_text("How much would you like to trade?")
    return  FOURTH

def collect_trade_amount(update: Update, context: CallbackContext) -> int:
    collect_trade_amount = update.message.text
    context.user_data['collect_trade_amount'] = collect_trade_amount  

    update.message.reply_text("Trade details saved. Ready to trade!")
    return ConversationHandler.END

def cancel(update: Update, context: CallbackContext) -> int:
    update.message.reply_text('Trade cancelled.')
    return ConversationHandler.END















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




bot = Bot(token=token_telegram)

last_sent_news_id = None


def send_latest_crypto_news(bot, crypto_compare_api_key):
    global last_sent_news_id
    latest_news = get_latest_crypto_news(crypto_compare_api_key)  # This function should return the JSON data shown above
    
    if latest_news and latest_news != "No news found.":
        current_news_id = latest_news.get("id", "")
        if current_news_id and current_news_id != last_sent_news_id:
            news_image_url = latest_news.get("imageurl", None)
            news_title = latest_news.get("title", "")
            news_body = latest_news.get("body", "")
            news_url = latest_news.get("url", "#")
            
            caption = f"{news_title}\n\n{news_body}\n\nRead more: {news_url}"
            if len(caption) > 1024:
                caption = caption[:1021] + "..."
            
            for chat_id in user_chat_ids:
                if news_image_url:
                    bot.send_photo(chat_id=chat_id, photo=news_image_url, caption=caption)
                else:
                    message = f"{news_title}\n\n{news_body}\n\nRead more: {news_url}"
                    bot.send_message(chat_id=chat_id, text=message)
            
            last_sent_news_id = current_news_id


def send_rsi_signals(bot):
    coin_symbol = 'BTC'
    coin_base_api_key = os.getenv('CRYPTO_COMPARE_API') 
    window_size = 15
    closing_prices = get_last_60_closing_prices(coin_symbol, coin_base_api_key)

    if not closing_prices or isinstance(closing_prices, str):
        print("Failed to fetch closing prices for RSI calculation.")
        return

    rsi_value = calculate_rsi(closing_prices, window_size)
    current_price = get_current_price(coin_symbol)

    if current_price is None:
        print("Failed to fetch the current price for RSI signal.")
        return

    if rsi_value < 30:
        message = f"Buy signal detected for {coin_symbol}.\n 📈 Current price: ${current_price} USD.\n RSI value: {round(rsi_value,2)}"
    elif rsi_value > 70:
        message = f"Sell signal detected for {coin_symbol}.\n 📉 Current price: ${current_price} USD.\n RSI value: {round(rsi_value,2)}"
    else:
        return  

    for chat_id in user_chat_ids:
        bot.send_message(chat_id=chat_id, text=message)



def run_continuously(interval=1):
    """Run scheduled jobs in a separate thread."""
    class SchedulerThread(Thread):
        @classmethod
        def run(cls):
            while True:
                schedule.run_pending()
                time.sleep(interval)
    continuous_thread = SchedulerThread()
    continuous_thread.start()











def main():
    updater = Updater(token=token_telegram, use_context=True)
    print('Bot start...')

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))

    dp.add_handler(CommandHandler("home", home))
    dp.add_handler(CallbackQueryHandler(button_click_handler))

    dp.add_handler(CommandHandler("trade", trade))
    dp.add_handler(CommandHandler("price", price))
    dp.add_handler(CommandHandler("daily_data", daily_data, pass_args=True))
    dp.add_handler(CommandHandler("check_quick_price", check_quick_price))


    dp.add_handler(CommandHandler("market_status", market_status))


    dp.add_handler(CommandHandler('subscribe', subscribe))
    dp.add_handler(CommandHandler('unsubscribe', unsubscribe))
    dp.add_handler(CommandHandler('csc', check_subscriber_count))


    # dp.add_handler(CallbackQueryHandler(trade_now, pattern='^trade_now$'))
    trade_conv_handler = ConversationHandler(
    entry_points=[CommandHandler('trade_now', trade_now)],
    states={
        FIRST: [MessageHandler(Filters.text & ~Filters.command, collect_api_key)],
        SECOND: [MessageHandler(Filters.text & ~Filters.command, collect_api_secret)],
        THIRD: [MessageHandler(Filters.text & ~Filters.command, collect_product_id)],
        FOURTH: [MessageHandler(Filters.text & ~Filters.command, collect_trade_amount)],
    },
    fallbacks=[CommandHandler('cancel', cancel)],
    )

    dp.add_handler(trade_conv_handler)

    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, generic_text_handler))


    bot_instance = updater.bot
    crypto_compare_api_key = os.getenv('CRYPTO_COMPARE_API')

    schedule.every(10).minutes.do(lambda: send_latest_crypto_news(bot=bot_instance, crypto_compare_api_key=crypto_compare_api_key))
    schedule.every(3).minutes.do(lambda: send_rsi_signals(bot=bot_instance))

    run_continuously()

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

