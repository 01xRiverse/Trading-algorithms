import ccxt
import time
import schedule
from binance.client import Client
from decouple import config
from BinanceRequests.TradeIsActive import TradeIsActive
from BinanceRequests.MakeTrade import MakeTrade
from BinanceRequests.CancelTrade import CancelTrade
from TradeCalls.LongCall import LongCall
from TradeCalls.ShortCall import ShortCall 
from TradeCalls.LongTrendChange import LongTrendChange
from TradeCalls.ShortTrendChange import ShortTrendChange
import os 

def Check():

	client=Client(api_key=config("testnet_api_key"),api_secret=config("testnet_api_secret"),testnet=True)

	if TradeIsActive(client):
		if os.getenv("Long")=="True" and LongTrendChange():
			CancelTrade()
		elif os.getenv("Short")=="True" and ShortTrendChange():
			CancelTrade()

	else:
		if LongCall():
			MakeTrade(client,"LONG")
			os.environ["Long"]="True"
			os.environ["Short"]="False"
		else if ShortCall():
			MakeTrade(client,"SHORT")
			os.environ["Long"]="False"
			os.environ["Short"]="True"



schedule.every().day.at("05:30").do(Check())
schedule.every().day.at("09:30").do(Check())
schedule.every().day.at("13:30").do(Check())
schedule.every().day.at("17:30").do(Check())
schedule.every().day.at("21:30").do(Check())
schedule.every().day.at("21:30").do(Check())



while True:
		schedule.run_pending()
		time.sleep(20)
		break
