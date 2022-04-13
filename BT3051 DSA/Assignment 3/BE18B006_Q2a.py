# no libraries are allowed

""" Add your functions here """

def optimal_investment_time_series(time_series):
	"""
	(list of int) -> int
	
	>>> optimal_investment_time_series([3,3,0,1,2,5,2,2,4,2,7,0])
	    10
	"""
	""" Add your code here """
	# We have a profit array to keep track of the profit.
	# We run a reversed for loop to calculate the maximum profit at index i in a transaction for
	# the subarray time_series[i:n-1]
	# We run a for loop to calculate the profit at index i such that it is the maximum profit
	# from 2 transactions in subarray time_series[:i]

	l = len(time_series)
	if l == 0: return 0
	profit_arr = [0] * l
	price_max_right = time_series[l - 1]

	print('Input: prices =', time_series)

	for i in range(l - 2, 0, -1):
		if time_series[i] > price_max_right:
			price_max_right = time_series[i]

		profit_arr[i] = max(price_max_right - time_series[i], profit_arr[i + 1])

	price_min_left = time_series[0]

	for j in range(1, l):
		if time_series[j] < price_min_left:
			price_min_left = time_series[j]

		profit_arr[j] = max(profit_arr[j - 1], profit_arr[j] + time_series[j] - price_min_left)

	print('Output:', profit_arr[-1])
	print('Explanation: ')

# Test
optimal_investment_time_series([3,3,0,1,2,5,2,2,4,2,7,0])