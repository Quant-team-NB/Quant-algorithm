import data, technical_indicators

# Settings
authtoken = (open("authtoken.txt", 'r')).read()
tickers = open("tickers.txt").read()
tickers = tickers.split(", ")
starting_date = "2006-01-01"	#yyyy-mm-dd


for ticker in tickers[:50]:
	indicators = {}
	# gets stock prices
	stock_data = data.get_prices(ticker, authtoken, from_date=starting_date, time_series_id="1W_adj", outputsize="full")
	stock_data.columns = ["OPEN", "HIGH", "LOW" ,"CLOSE", "ADJ CLOSE", "VOLUME", "DIVIDEND"]
	name_of_column = "ADJ CLOSE"
	stock_data = stock_data[[name_of_column]]

	technical_indicators.get_SMA(stock_data, name_of_column, indicators, 9)
	technical_indicators.get_SMA(stock_data, name_of_column, indicators, 50)
	technical_indicators.get_SMA(stock_data, name_of_column, indicators, 200)

	if indicators["SMA-9"] > indicators["SMA-50"] > indicators["SMA-200"]:
		print("BUY: ", end=" ")
		print(ticker, indicators)
	elif indicators["SMA-9"] < indicators["SMA-50"] < indicators["SMA-200"]:
		print("SELL: ", end=" ")
		print(ticker, indicators)
