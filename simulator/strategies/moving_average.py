#A module that can calculates moving average of a series of data.

prices = []

#Add a data point
def add(data):
    global prices
    prices.append(data)

#Calculate the moving average of specific length
def moving_average(length):
    global prices
    length = min(length, len(prices))
    return sum(prices[len(prices) - length :]) / length

