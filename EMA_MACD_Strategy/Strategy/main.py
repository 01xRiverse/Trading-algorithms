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
import warnings
warnings.filterwarnings("ignore")

#global variables
Long=True
Short=True

def Check():
	global Short,Long

	#creating a client
	client=Client(api_key=config("api_key"),api_secret=config("api_secret"),testnet=False)

	# checking if a trade is active 
	if TradeIsActive(client):

		#backing out of a trade if there is a change in trend
		if Long=="True" and LongTrendChange():
			CancelTrade(client,"SELL")
		elif Short=="True" and ShortTrendChange():
			CancelTrade(client,"BUY")

	#checking for trade oppurtunities if there is no trade active
	else:
		if  Short and LongCall():
			MakeTrade(client,"LONG")
			Long=True
			Short=False
		elif Long and ShortCall():
			MakeTrade(client,"SHORT")
			Long=False
			Short=True



	print("Trade Status:-")
	if(TradeIsActive(client)):
		print("Time:",datetime.now().strftime("%H:%M:%S"))
		position=client.futures_account()["positions"][158]
		print("PNL:",position["unrealizedProfit"])
		print("Margin:",position["initialMargin"])
		print("*********************")

	else:
		print("Time:",datetime.now().strftime("%H:%M:%S"))
		print("No Trade is acitve.")
		print(int(client.futures_account_balance()[6]['balance'].split(".")[0]))
		print("*********************")



#Scheduling check function for every 4 hours
schedule.every().day.at("00:00").do(Check)
schedule.every().day.at("04:00").do(Check)
schedule.every().day.at("08:00").do(Check)
schedule.every().day.at("12:00").do(Check)
schedule.every().day.at("16:00").do(Check)
schedule.every().day.at("20:00").do(Check)


# executes Check function for every 4 hours
print("************************")
print("STARTED")
print("************************")


Check()
while True:
	schedule.run_pending()
	time.sleep(2)
