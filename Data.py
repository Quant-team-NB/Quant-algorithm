import pandas as pd
import urllib.request, json
import sys, os, ssl

def get_prices(ticker, authtoken, from_date=None, time_series_id="1W_adj", outputsize="compact"): 

	# Turns off certification authentication
	if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
   	getattr(ssl, '_create_unverified_context', None)): 
		ssl._create_default_https_context = ssl._create_unverified_context

	inter_day_keys = ["1m", "5m", "15m", "30m", "1h"]

	time_series_settings = {
		#		time_series, data_dict_key, (interday_identifier)
		# Interday
		"1m" : ["TIME_SERIES_INTRADAY", "Time Series (1min)", "1min", ],
		"5m" : ["TIME_SERIES_INTRADAY", "Time Series (5min)", "5min"],
		"15m" : ["TIME_SERIES_INTRADAY", "Time Series (15min)", "15min"],
		"30m" : ["TIME_SERIES_INTRADAY", "Time Series (30min)", "30min"],
		"1h" : ["TIME_SERIES_INTRADAY", "Time Series (60min)", "60min"],

		# Longterm (not adjusted)
		"1D" : ["TIME_SERIES_DAILY", "Time Series (Daily)"],
		"1W" : ["TIME_SERIES_WEEKLY", "Weekly Time Series"],
		"1M" : ["TIME_SERIES_MONTHLY", "Monthly Time Series"],

		# Longterm (adjusted)
		"1D_adj" : ["TIME_SERIES_DAILY_ADJUSTED", "Time Series (Daily)"],
		"1W_adj" : ["TIME_SERIES_WEEKLY_ADJUSTED", "Weekly Adjusted Time Series"],
		"1M_adj" : ["TIME_SERIES_MONTHLY_ADJUSTED", "Monthly Adjusted Time Series"]
	}

	time_series = time_series_settings[time_series_id][0]

	if time_series_id in inter_day_keys:
		interday_identifier = "&interval=" + time_series_settings[time_series_id][2]
	else:
		interday_identifier = ""


	# Formatting url request
	api_url = "https://www.alphavantage.co/query?" 
	api_url += "function=" + time_series
	api_url += "&symbol=" + ticker
	api_url += interday_identifier
	api_url += "&outputsize=" + outputsize
	api_url += "&apikey=" + authtoken


	# Opening and formatting data
	with urllib.request.urlopen(api_url) as url:
	    price_data = json.loads(url.read().decode())
	    price_data = price_data[time_series_settings[time_series_id][1]] 

	# Creating dataframe
	df_price = pd.DataFrame(price_data).transpose()
	df_price = df_price.apply(pd.to_numeric)

	# Filtering out data prior to from_date
	if not from_date == None:
		df_price = df_price.truncate(after=from_date)

	return df_price