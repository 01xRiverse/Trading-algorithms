import ccxt
import time
import schedule
from binance.client import Client
from BinanceRequests.TradeIsActive import TradeIsActive
from BinanceRequests.MakeTrade import MakeTrade
from BinanceRequests.CancelTrade import CancelTrade
from TradeCalls.LongCall import LongCall
from TradeCalls.ShortCall import ShortCall 
from TradeCalls.LongTrendChange import LongTrendChange
from TradeCalls.ShortTrendChange import ShortTrendChange
from decouple import config
from datetime import datetime



#global variables
Long="False"
Short="False"

def Check():
	global Short,Long

	#creating a client
	client=Client(api_key=config("testnet_api_key"),api_secret=config("testnet_api_secret"),testnet=True)

	# checking if a trade is active 
	if TradeIsActive(client):

		#backing out of a trade if there is a change in trend
		if Long=="True" and LongTrendChange():
			CancelTrade(client,"SELL")
		elif Short=="True" and ShortTrendChange():
			CancelTrade(client,"BUY")

	#checking for trade oppurtunities if there is no trade active
	else:
		if LongCall():
			MakeTrade(client,"LONG")
			Long="True"
			Short="False"
		elif ShortCall():
			MakeTrade(client,"SHORT")
			Long="False"
			Short="True"



	print("Trade Status:-")
	if(TradeIsActive(client)):
		print("Time:",datetime.now().strftime("%H:%M:%S"))
		position=client.futures_account()["positions"][155]
		print("PNL:",position["unrealizedProfit"])
		print("Margin:",position["initialMargin"])
		print("*********************")

	else:
		print("Time:",datetime.now().strftime("%H:%M:%S"))
		print("No Trade is acitve.")
		print(int(client.futures_account_balance()[3]['balance'].split(".")[0]))
		print("*********************")



#Scheduling check function for every 4 hours
schedule.every().day.at("05:30").do(Check)
schedule.every().day.at("09:30").do(Check)
schedule.every().day.at("13:30").do(Check)
schedule.every().day.at("17:30").do(Check)
schedule.every().day.at("21:30").do(Check)
schedule.every().day.at("01:30").do(Check)


# executes Check function for every 4 hours
print("************************")
print("STARTED")
print("************************")

Check()

while True:
	schedule.run_pending()
	time.sleep(2)
