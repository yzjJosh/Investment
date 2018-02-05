#!/usr/bin/env python
#Simulate the stock investment
#input:
#   price data file path
#   begin time, as an index of the price data array
#   simulation length, in number of days
#   initial cash
#   strategy, as a string

from strategies import decision
from strategies import buy_and_hold
from strategies import buy_and_hold_with_threshold
from strategies import buy_and_hold_with_shrinking_threshold
from strategies import buy_conservatively_and_hold_with_threshold
from strategies import buy_conservatively_and_hold_with_shrinking_threshold
import matplotlib.pyplot as plt

#Strategy strings.
STRATEGY_BUY_AND_HOLD = "buy_and_hold"
STRATEGY_BUY_AND_HOLD_WITH_THRESHOLD = "buy_and_hold_with_threshold"
STRATEGY_BUY_AND_HOLD_WITH_SHRINKING_THRESHOLD = "buy_and_hold_with_shrinking_threshold"
STRATEGY_BUY_CONSERVATIVELY_WITH_THRESHOLD = "buy_conservatively_and_hold_with_threshold"
STRATEGY_BUY_CONSERVATIVELY_AND_HOLD_WITH_SHRINKING_THRESHOLD = "buy_conservatively_and_hold_with_shrinking_threshold"

#String key of simulation results
KEY_DATE = "DATE"
KEY_TRADE_HISTORY  = "TRADE_HISTORY"
KEY_TRADE_TYPE = "TRADE_TYPE"
KEY_TRADE_SHARE_AMOUNT = "TRADE_SHARE_AMOUNT"
KEY_TRADE_VALUE = "TRADE_VALUE"
KEY_TRADE_TIME = "TRADE_TIME"
KEY_BEGIN_VALUE = "BEGIN_VALUE"
KEY_BEGIN_CASH = "BEGIN_CASH"
KEY_BEGIN_SHARE = "BEGIN_SHARE"
KEY_END_VALUE = "END_VALUE"
KEY_END_CASH = "END_CASH"
KEY_END_SHARE = "END_SHARE"

#Initialize with specific strategy
def initialize(strategy, init_cash):
    if strategy == STRATEGY_BUY_AND_HOLD:
        buy_and_hold.initialize(init_cash)
    elif strategy == STRATEGY_BUY_AND_HOLD_WITH_THRESHOLD:
        buy_and_hold_with_threshold.initialize(init_cash)
    elif strategy == STRATEGY_BUY_CONSERVATIVELY_WITH_THRESHOLD:
        buy_conservatively_and_hold_with_threshold.initialize(init_cash)
    elif strategy == STRATEGY_BUY_AND_HOLD_WITH_SHRINKING_THRESHOLD:
        buy_and_hold_with_shrinking_threshold.initialize(init_cash)
    elif strategy == STRATEGY_BUY_CONSERVATIVELY_AND_HOLD_WITH_SHRINKING_THRESHOLD:
        buy_conservatively_and_hold_with_shrinking_threshold.initialize(init_cash)
    else:
        raise Exception("Unknown strategy " + strategy)

#Make trade decision based on a specific strategy when stock price changes.
def on_stock_price_change(strategy, price):
    if strategy == STRATEGY_BUY_AND_HOLD:
        return buy_and_hold.on_stock_price_change(price)
    elif strategy == STRATEGY_BUY_AND_HOLD_WITH_THRESHOLD:
        return buy_and_hold_with_threshold.on_stock_price_change(price)
    elif strategy == STRATEGY_BUY_CONSERVATIVELY_WITH_THRESHOLD:
        return buy_conservatively_and_hold_with_threshold.on_stock_price_change(price)
    elif strategy == STRATEGY_BUY_AND_HOLD_WITH_SHRINKING_THRESHOLD:
        return buy_and_hold_with_shrinking_threshold.on_stock_price_change(price)
    elif strategy == STRATEGY_BUY_CONSERVATIVELY_AND_HOLD_WITH_SHRINKING_THRESHOLD:
        return buy_conservatively_and_hold_with_shrinking_threshold.on_stock_price_change(price)
    else:
        raise Exception("Unknown strategy " + strategy)

#Simulate the stock investment process with provided price data and strategy
def simulate(price_data, begin_time, simulation_length, init_cash, strategy):
    process = []
    cash = init_cash
    shares = 0
    initialize(strategy, init_cash)
    for date in range(begin_time, begin_time + simulation_length):
        day_investment = {}
        day_investment[KEY_DATE] = date
        day_investment[KEY_BEGIN_VALUE] = cash + shares * price_data[date][0]
        day_investment[KEY_BEGIN_SHARE] = shares
        day_investment[KEY_BEGIN_CASH] = cash
        trade_history = []
        for time in range(0, len(price_data[date])):
            price = price_data[date][time]
            dec, amount = on_stock_price_change(strategy, price)
            if dec == decision.BUY:
                shares = shares + amount
                cash = cash - amount * price
                if cash < 0:
                    raise Exception('Negative cash value!') 
            elif dec == decision.SELL:
                shares = shares - amount
                cash = cash + amount * price
                if shares < 0:
                    raise Exception('Negative share amount!')
            if dec == decision.BUY or dec == decision.SELL:
                trade = {}
                trade[KEY_TRADE_TIME] = time 
                trade[KEY_TRADE_TYPE] = dec
                trade[KEY_TRADE_SHARE_AMOUNT] = amount
                trade[KEY_TRADE_VALUE] = amount * price
                trade_history.append(trade)
        day_investment[KEY_TRADE_HISTORY] = trade_history
        day_investment[KEY_END_CASH] = cash
        day_investment[KEY_END_SHARE] = shares
        day_investment[KEY_END_VALUE] = cash + shares * price_data[date][6]
        process.append(day_investment)
    return process

#Parse a price data file into a two diemnsion array
def parse_price_data_file(file_path):
    price_data = []
    with open(file_path, "r") as f:
        for line in f.readlines():
            prices = line.split(" ")
            prices = map(lambda x: float(x), prices)
            price_data.append(prices)
    return price_data

def plot_investment_line_chart(price_data, strategy, sim):
    begin_time = sim[0][KEY_DATE]
    simulation_length = len(sim)
    price_line = map(lambda p: sum(p)/len(p), price_data[begin_time: begin_time + simulation_length])
    normalized_price_line = map(lambda p: p/max(price_line), price_line)
    value_line = map(lambda inv: (inv[KEY_BEGIN_VALUE] + inv[KEY_END_VALUE])/2, sim)
    normalized_value_line = map(lambda v: v/max(value_line), value_line)
    time_line = range(begin_time, begin_time + simulation_length)
    plt.plot(time_line, normalized_price_line, label="Market Value")
    plt.plot(time_line, normalized_value_line, label="Assets Value")
    plt.legend()
    plt.xlabel('date index')
    plt.ylabel('normalized value')
    plt.title('Simulation Result of Investment Strategy ' + strategy)
    plt.grid(True)


if __name__ == "__main__":
    import sys
    price_data_file = sys.argv[1]
    begin_time = int(sys.argv[2])
    simulation_length = int(sys.argv[3])
    initial_cash = int(sys.argv[4])
    strategy = sys.argv[5]

    price_data = parse_price_data_file(price_data_file)
    
    #Simulate investment.
    res = simulate(price_data, begin_time, simulation_length, initial_cash, strategy)
    
    #Print investment details.
    begin_value = res[0][KEY_BEGIN_VALUE]
    end_value = res[len(res)-1][KEY_END_VALUE]
    for day_investment in res:
        print day_investment
    print "Gain percentage: " + str((end_value - begin_value) / begin_value * 100) + "%"
    
    #Draw line chart.
    plot_investment_line_chart(price_data, strategy, res) 
    plt.show()
