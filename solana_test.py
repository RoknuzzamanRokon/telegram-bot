# from solana.rpc.api import Client
# from solana.publickey import PublicKey

# solana_client = Client("https://api.mainnet-beta.solana.com")
# account_address = 'ETkQwgyt9z7Azq9wxUqHEyoiQsgvtp5DRMy4siLo5E6s'
# balance = solana_client.get_balance(PublicKey(account_address))
# print(balance['result']['value'])




from solana.rpc.api import Client

client = Client("https://api.mainnet-beta.solana.com")
print(client.get_version())



# import asyncio
# from solana.rpc.async_api import AsyncClient

# async def main():
#     async with AsyncClient("https://api.devnet.solana.com") as client:
#         res = await client.is_connected()
#     print(res)  # True

#     # Alternatively, close the client explicitly instead of using a context manager:
#     client = AsyncClient("https://api.devnet.solana.com")
#     res = await client.is_connected()
#     print(res)  # True
#     await client.close()

# asyncio.run(main())


# import asyncio
# from solana.rpc.api import AsyncClient
# from solana.publickey import PublicKey

# async def main():
#     async with AsyncClient("https://api.devnet.solana.com") as client:
#         account_address = 'ETkQwgyt9z7Azq9wxUqHEyoiQsgvtp5DRMy4siLo5E6s'
#         balance = await client.get_balance(PublicKey(account_address))
#         print(balance['result']['value'])

# asyncio.run(main())





# import asyncio
# from asyncstdlib import enumerate
# from solana.rpc.websocket_api import connect

# async def main():
#     async with connect("wss://api.devnet.solana.com") as websocket:
#         await websocket.logs_subscribe()
#         first_resp = await websocket.recv()
#         subscription_id = first_resp[0].result
#         next_resp = await websocket.recv()
#         print(next_resp)
#         await websocket.logs_unsubscribe(subscription_id)

#     # Alternatively, use the client as an infinite asynchronous iterator:
#     async with connect("wss://api.devnet.solana.com") as websocket:
#         await websocket.logs_subscribe()
#         first_resp = await websocket.recv()
#         subscription_id = first_resp[0].result
#         async for idx, msg in enumerate(websocket):
#             if idx == 3:
#                 break
#             print(msg)
#         await websocket.logs_unsubscribe(subscription_id)

# asyncio.run(main())