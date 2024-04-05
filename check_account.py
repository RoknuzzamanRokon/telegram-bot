from coinbase.wallet.client import Client
# from dotenv import load_dotenv
# import os

# load_dotenv()

# api_key = os.environ.get('COIN_BASE_API_KEY_1')
# api_secret = os.environ.get('COIN_BASE_API_SECRET_1')

# client = Client(api_key, api_secret)

def check_account_wallet(api_key, api_secret):
    client = Client(api_key,api_secret)

    try:
        accounts = client.get_accounts()
        for account in accounts['data']:
            balance_amount = float(account['balance']['amount'])
            if balance_amount > 0:
                print(f"A\C: {account['name']}, Balance: {account['balance']['amount']} {account['balance']['currency']}")
    except Exception as e:
        print("Error:", e)

