import ccxt
import pandas as pd
import pandas_ta as ta

def LongCall():
	#candlestick api call
	exchange = ccxt.binance()
	bars = exchange.fetch_ohlcv('BTC/USDT', timeframe="4h", limit=1000)
	df = pd.DataFrame(bars, columns=['time', 'open', 'high', 'low', 'close', 'volume'])

	#computing indicator values
	MACD=ta.macd(df["close"],12,26,9)
	ema9=ta.ema(df["close"],9)
	ema21=ta.ema(df["close"],21)

	#evaluating indicator values for Long call
	if(MACD['MACDh_12_26_9'][1000-1]>0 and MACD["MACDs_12_26_9"][1000-1]>0  and ema9[1000-2] > ema21[1000-2]):
		return True
	return False

print(LongCall())