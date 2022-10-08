from binance.client import Client
from  decouple import config



def CancelTrade():

	client=Client(api_key=config('testnet_api_key'),api_secret=config('testnet_api_secret'),testnet=True)

	#cancel Stop Loss and Take Profit orders
	client.futures_cancel_all_open_orders(symbol="BTCUSDT")


	#cancel open position



CancelTrade()