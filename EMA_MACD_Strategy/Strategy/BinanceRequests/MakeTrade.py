import os
from binance.client import Client


#CHANCE ON INSUFFICIENT FUNDS ON LINE 23

def MakeTrade(client,postion):
	symbol="BTCUSDT"

	#setting leverage
	client.futures_change_leverage(symbol=symbol,leverage=3)

	#fetching mark price
	mark_price=int(client.futures_mark_price(symbol=symbol)["markPrice"].split(".")[0])

	#fetching balance
	balance=int(client.futures_account_balance()[6]['balance'].split(".")[0])

	adjustleverage=0.1
	while(adjustleverage!=0.6):
		try:
			order=client.futures_create_order(symbol=symbol,type="MARKET",side="BUY" if postion=="LONG" else "SELL",quantity=round((balance*(3-adjustleverage))/mark_price,3))
		except:
			adjustleverage+=0.1
	#updating SL and TP
	try:
		mark_price=round(float(client.futures_account()["positions"][158]["entryPrice"]))
		stoploss=client.futures_create_order(symbol=symbol,side="SELL" if postion=="LONG" else "BUY" ,type="STOP_MARKET" ,stopPrice=str(int(mark_price*0.9677)) if postion=="LONG" else str(int(mark_price*1.0334)),closePosition=True)
		takeprofit=client.futures_create_order(symbol=symbol,side="SELL" if postion=="LONG" else "BUY" ,type="TAKE_PROFIT_MARKET",stopPrice=str(int(mark_price*1.0334)) if postion=="LONG" else str(int(mark_price*0.9677)),closePosition=True)

	except:
		print("Trade missed due leverage issuse")


