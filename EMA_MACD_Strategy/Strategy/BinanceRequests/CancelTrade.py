from binance.client import Client



def CancelTrade(client,action):

	symbol="BTCUSDT"
	#cancel open position
	if action=="BUY":
		order=client.futures_create_order(symbol=symbol,type="MARKET",side="BUY",quantity=client.futures_account()["positions"][155]["positionAmt"][1:])
	else:
		order=client.futures_create_order(symbol=symbol,type="MARKET",side="SELL",quantity=client.futures_account()["positions"][155]["positionAmt"])

	#cancel Stop Loss and Take Profit orders
	client.futures_cancel_all_open_orders(symbol="BTCUSDT")

	







