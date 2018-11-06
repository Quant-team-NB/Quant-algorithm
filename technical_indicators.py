def get_SMA(stock_data, name_of_column, indicators, n):

	# If there isn't 20 observations it's not possible to calculate the 20-day moving average
	if len(stock_data) < n:
		raise ValueError("Not enough data to calculate " + str(n) + "-day moving average")

	_sum = 0
	for price in stock_data[name_of_column][:n][::-1]:
		_sum += price
	
	indicators["SMA-"+str(n)] = float("%.2f" % (_sum/n))
