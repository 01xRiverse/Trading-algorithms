import ccxt
import numpy as np
import pandas as pd
import pandas_ta as ta




#Fetching and storing values
exchange = ccxt.binance()
bars = exchange.fetch_ohlcv('BTC/USDT', timeframe="4h", limit=1000)
df = pd.DataFrame(bars, columns=['time', 'open', 'high', 'low', 'close', 'volume'])



#Trade variables
balance=100
leverage=3
SL=10
TP=10


#states
isFirstTrade=True
BullishOverlap=False
BearishOverlap=False
TradeIsOpen=False
entry=0
trades=0
BullMode=False
BearMode=False
hits=0
misses=0
failed=0



#indicators
MACD=ta.macd(df["close"],12,26,9)
ema9=ta.ema(df["close"],9)
ema21=ta.ema(df["close"],21)
# ema9=ta.ema(df["close"],7)
# ema21=ta.ema(df["close"],14)

for i in range(MACD.shape[0]):
	#skipping empty values of the indicators
	if(np.isnan(ema9[i]) or np.isnan(ema21[i]) or np.isnan(MACD["MACDh_12_26_9"][i]) or np.isnan(MACD["MACDs_12_26_9"][i])):
		continue 


	if(isFirstTrade and ema9[i]>ema21[i]):
		isFirstTrade=False
		BullishOverlap=True
		continue

	if(isFirstTrade and ema9[i]<ema21[i]):
		isFirstTrade=False
		BearishOverlap=True
		continue



	if(not TradeIsOpen):
		if(ema9[i-1]>ema21[i-1] and not BullishOverlap and MACD['MACDh_12_26_9'][i]>0 and MACD["MACDs_12_26_9"][i]>0 ):
			entry=df["open"][i]
			BullishOverlap=True
			TradeIsOpen=True
			BearishOverlap=False
			BullMode=True
			BearMode=False
			trades+=1


		if(ema9[i-1]<ema21[i-1] and not BearishOverlap and MACD['MACDh_12_26_9'][i]<0 and MACD["MACDs_12_26_9"][i]<0):
			entry=df["open"][i]
			BearishOverlap=True
			TradeIsOpen=True
			BullishOverlap=False
			BullMode=False
			BearMode=True
			trades+=1



	if(TradeIsOpen):

		if(BullMode):

			if(ema9[i-1]<ema21[i-1]):
				#close trade code
				if(df['open'][i]>entry):
					balance=balance*(1+((df['open'][i]-entry)/entry)*leverage)
					TradeIsOpen=False
				else:
					balance=balance*(1-((entry-df['open'][i])/entry)*leverage)
					TradeIsOpen=False
				failed+=1
				continue

			if(((entry-df['low'][i])/entry)*(100*leverage)>=SL):
				#close trade code
				TradeIsOpen=False
				balance=(1-(SL/100))*balance
				misses+=1
				continue

			if(((df['high'][i]-entry)/entry)*(100*leverage)>=TP):
				#close trade code
				TradeIsOpen=False
				balance=(1+(TP/100))*balance
				hits+=1
				continue







		if(BearMode):
			if(ema9[i-1]>ema21[i-1]):
				#close trade code
				if(df['open'][i]<entry):
					balance=balance*(1+((entry-df['open'][i])/entry)*leverage)
					TradeIsOpen=False
				else:
					balance=balance*(1-((df['open'][i]-entry)/entry)*leverage)
					TradeIsOpen=False
				failed+=1
				continue

			if(((df['high'][i]-entry))/entry*(100*leverage)>=SL):
				#close trade code
				TradeIsOpen=False
				balance=(1-(SL/100))*balance
				misses+=1
				continue

			if(((entry-df['low'][i])/entry)*(100*leverage)>=TP):
				#close trade code 
				TradeIsOpen=False
				balance=(1+(TP/100))*balance
				hits+=1
				continue






print("Balance:",balance)
print("Trades:",trades)
print("Hits:",hits)
print("Misses:",misses)
print("Failed:",failed)