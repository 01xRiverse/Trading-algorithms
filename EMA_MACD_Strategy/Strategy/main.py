import ccxt
import time
import schedule



schedule.every().day.at("05:30").do()
schedule.every().day.at("09:30").do()
schedule.every().day.at("13:30").do()
schedule.every().day.at("17:30").do()
schedule.every().day.at("21:30").do()
schedule.every().day.at("21:30").do()



while True:
		schedule.run_pending()
		time.sleep(20)
		break
	