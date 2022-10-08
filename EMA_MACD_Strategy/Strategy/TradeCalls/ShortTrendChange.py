import pandas as pd 
import ccxt
import pandas_ta as ta


def ShortTrendChange():

	exchange = ccxt.binance()
	bars = exchange.fetch_ohlcv('BTC/USDT', timeframe="4h", limit=1000)
	df = pd.DataFrame(bars, columns=['time', 'open', 'high', 'low', 'close', 'volume'])

	ema9=ta.ema(df["close"],9)
	ema21=ta.ema(df["close"],21)


	return True if ema21[1000-2]<ema9[1000-2] else False

