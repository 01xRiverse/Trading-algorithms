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
	balance=int(client.futures_account_balance()[3]['balance'].split(".")[0])

	adjustleverage=0.1
	while(adjustleverage!=0.6):
		try:
			order=client.futures_create_order(symbol=symbol,type="MARKET",side="BUY" if postion=="LONG" else "SELL",quantity=round((balance*(3-adjustleverage))/mark_price,3))
		except:
			adjustleverage+=0.1
	#updating SL and TP
	try:
		stoploss=client.futures_create_order(symbol=symbol,side="SELL",type="STOP_MARKET" if postion=="LONG" else "TAKE_PROFIT_MARKET",stopPrice=str(int(mark_price*0.9)) if postion=="LONG" else str(int(mark_price*1.1)),closePosition=True)
		takeprofit=client.futures_create_order(symbol=symbol,side="SELL",type="TAKE_PROFIT_MARKET" if postion=="LONG" else "STOP_MARKET",stopPrice=str(int(mark_price*1.1)) if postion=="LONG" else str(int(mark_price*0.9)),closePosition=True)

	except:
		print("Trade missed due leverage issuse")


