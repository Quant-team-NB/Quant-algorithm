import Data

# Settings
authtoken = (open("authtoken.txt", 'r')).read()[:-1]
starting_date = "2017-01-01"	#yyyy-mm-dd
ticker = "MSFT"

# gets stock prices
data = Data.get_prices(ticker, authtoken, from_date=starting_date, time_series_id="1W_adj", outputsize="full")
data.columns = ["OPEN", "HIGH", "LOW" ,"CLOSE", "ADJ CLOSE", "VOLUME", "DIVIDEND"]
data = data[["CLOSE"]]
print(data)
