#A module that can calculates moving average of a series of data.

series = []

#Add a data point
def add(data):
    global series
    series.append(data)

#Calculate the moving average of specific length
def moving_average(length):
    global series
    length = min(length, len(series))
    return sum(series[len(prices) - length :]) / length

