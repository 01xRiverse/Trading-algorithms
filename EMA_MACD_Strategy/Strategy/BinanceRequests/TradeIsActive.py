import requests
from binance.client import Client
from decouple import config
import pandas as pd

def TradeIsActive(client):
	symbol="BTCUSDT"

	#fetching all positions 
	positions=client.futures_account()["positions"]

	#checking if position is open 
	return True if positions[155]['initialMargin']!='0' else False






