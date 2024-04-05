from coinbase.wallet.client import Client
# from dotenv import load_dotenv
# import os

# load_dotenv()

# api_key = os.environ.get('COIN_BASE_API_KEY_1')
# api_secret = os.environ.get('COIN_BASE_API_SECRET_1')

# client = Client(api_key, api_secret)

# def check_account_wallet(api_key, api_secret, product_id = None):
#     client = Client(api_key,api_secret)

#     try:
#         accounts = client.get_accounts()
#         for account in accounts['data']:
#             balance_amount = float(account['balance']['amount'])
#             if balance_amount > 0:
#                 print(f"A\C: {account['name']}, Balance: {account['balance']['amount']} {account['balance']['currency']}")
#     except Exception as e:
#         print("Error:", e)

# def check_account_wallet(api_key, api_secret, product_id=None):
#     client = Client(api_key, api_secret)
#     currencies = product_id.split('-') if product_id else []

#     try:
#         accounts = client.get_accounts()
#         for account in accounts['data']:
#             balance_amount = float(account['balance']['amount'])
#             account_currency = account['balance']['currency']
#             if balance_amount > 0 and (not product_id or account_currency in currencies):
#                 print(f"A\\C: {account['name']}, Balance: {balance_amount} {account_currency}")
#     except Exception as e:
#         print("Error:", e)




def check_account_wallet(api_key, api_secret, product_id=None):
    client = Client(api_key, api_secret)
    currencies = product_id.split('-') if product_id else []
    balances_info = "" 

    try:
        accounts = client.get_accounts()
        for account in accounts['data']:
            balance_amount = float(account['balance']['amount'])
            account_currency = account['balance']['currency']
            if balance_amount > 0 and (not product_id or account_currency in currencies):
                account_info = f"A\\C: {account['name']}, Balance: {balance_amount} {account_currency}\n"
                print(account_info)  
                balances_info += account_info  
    except Exception as e:
        print("Error:", e)
        balances_info += f"Error retrieving account information: {e}\n"  

    return balances_info.strip()  

