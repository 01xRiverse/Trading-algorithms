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
	#creating a client
	client=Client(api_key=config("testnet_api_key"),api_secret=config("testnet_api_secret"),testnet=True)

	#checking if a trade is active 
	if TradeIsActive(client):

		#backing out of a trade if there is a change in trend
		if os.getenv("Long")=="True" and LongTrendChange():
			CancelTrade(client,"SELL")
		elif os.getenv("Short")=="True" and ShortTrendChange():
			CancelTrade(client,"BUY")

	#checking for trade oppurtunities if there is no trade active
	else:
		if LongCall():
			MakeTrade(client,"LONG")
			os.environ["Long"]="True"
			os.environ["Short"]="False"
		elif ShortCall():
			MakeTrade(client,"SHORT")
			os.environ["Long"]="False"
			os.environ["Short"]="True"



#Scheduling check function for every 4 hours
schedule.every().day.at("05:30").do(Check)
schedule.every().day.at("09:30").do(Check)
schedule.every().day.at("13:30").do(Check)
schedule.every().day.at("17:30").do(Check)
schedule.every().day.at("21:30").do(Check)
schedule.every().day.at("01:30").do(Check)


#executes Check function for every 4 hours
while True:
		schedule.run_pending()
		time.sleep(1)
