import requests
from binance.client import Client
from decouple import config

def TradeIsActive(client):
	symbol="BTCUSDT"

	positions=client.futures_account()["positions"]

	#checking if position is open 
	#155 for testnet 158 for actual 
	return True if positions[155]['initialMargin']!='0' else False





