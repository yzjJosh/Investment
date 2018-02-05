#!/usr/bin/env python
#Evaluate the effectiveness of an investment strategy
#input:
#   price data file path as simulation data
#   strategy, as a string

import statistics
import simulate
import matplotlib.pyplot as plt

#A data class that associates a value with a simulation
class Node: 
    def __init__(self, value=None, simulation=None):
        self.value = value
        self.simulation = simulation

#A data class that represents statistic data of a certain index
class Stat:
    def __init__(self, max_value, min_value, ava, median, data_size):
        self.max = max_value
        self.min = min_value
        self.ava = ava
        self.median = median
        self.size = data_size

#A data class that represents a analysis result
class Analysis:
    def __init__(self, strategy, sim_times, gain_stat, positive_gain_stat, negative_gain_stat):
        self.strategy = strategy
        self.sim_times = sim_times
        self.gain_stat = gain_stat
        self.positive_gain_stat = positive_gain_stat
        self.negative_gain_stat = negative_gain_stat

def search(arr, t):
    index = 0;
    num = 0
    for i in range(0, len(arr)):
        if arr[i] == t:
            return i
        if abs(arr[i] - t) < abs(num - t):
            num = arr[i]
            index = i
    return index

#Analyze a strategy with specific price data and investment length (in days).
def analyze_fixed_length_investment(price_data, investment_length, strategy):
    init_cash = 100000000
    gain = []
    sims = []
    for begin_time in range(0, len(price_data) - investment_length + 1):
        sim = simulate.simulate(price_data, begin_time, investment_length, init_cash, strategy)
        gain.append((sim[len(sim)-1][simulate.KEY_END_VALUE] - sim[0][simulate.KEY_BEGIN_VALUE]) / init_cash)
        sims.append(sim)
    gain_max = Node(max(gain), sims[search(gain, max(gain))])
    gain_min = Node(min(gain), sims[search(gain, min(gain))])
    gain_ava = Node(sum(gain)/len(gain))
    gain_median = Node(statistics.median(gain), sims[search(gain, statistics.median(gain))])
    gain_stat = Stat(gain_max, gain_min, gain_ava, gain_median, len(gain))
    
    positive_gain = filter(lambda x: x > 0, gain)
    positive_gain_max = Node(max(positive_gain), sims[search(gain, max(positive_gain))])
    positive_gain_min = Node(min(positive_gain), sims[search(gain, min(positive_gain))])
    positive_gain_ava = Node(sum(positive_gain)/len(positive_gain))
    positive_gain_median = Node(statistics.median(positive_gain), sims[search(gain, statistics.median(positive_gain))])
    positive_gain_stat = Stat(positive_gain_max, positive_gain_min, positive_gain_ava, positive_gain_median, len(positive_gain))

    negative_gain = filter(lambda x: x < 0, gain)
    negative_gain_max = Node(max(negative_gain), sims[search(gain, max(negative_gain))])
    negative_gain_min = Node(min(negative_gain), sims[search(gain, min(negative_gain))])
    negative_gain_ava = Node(sum(negative_gain)/len(negative_gain))
    negative_gain_median = Node(statistics.median(negative_gain), sims[search(gain, statistics.median(negative_gain))])
    negative_gain_stat = Stat(negative_gain_max, negative_gain_min, negative_gain_ava, negative_gain_median, len(negative_gain))

    return Analysis(strategy, len(sims), gain_stat, positive_gain_stat, negative_gain_stat)

def show_analysis_result(analysis):
    print "Number of simulations ran:", analysis.sim_times
    print "Maximum gain:", analysis.gain_stat.max.value * 100, "%"
    print "Minimum gain:", analysis.gain_stat.min.value * 100, "%"
    print "Average gain:", analysis.gain_stat.ava.value * 100, "%"
    print "Median gain:", analysis.gain_stat.median.value * 100, "%"
    print "--------------------------------------------------------"
    print "Positive gain percentage:", float(analysis.positive_gain_stat.size) / analysis.gain_stat.size * 100, "%"
    print "Average positive gain:", analysis.positive_gain_stat.ava.value * 100, "%"
    print "Median positive gain:", analysis.positive_gain_stat.median.value * 100, "%"
    print "--------------------------------------------------------"
    print "Negative gain percentage:", float(analysis.negative_gain_stat.size) / analysis.gain_stat.size * 100, "%"
    print "Average negative gain:", analysis.negative_gain_stat.ava.value * 100, "%"
    print "Median negative gain:", analysis.negative_gain_stat.median.value * 100, "%"
    print "--------------------------------------------------------"

    command = raw_input("Do you want to review the line-charts? (Type \"Y\" to confirm) ")
    if command == "Y":
        print "Showing line-charts of max, min, and median profit investments ..."
        plt.figure()
        simulate.plot_investment_line_chart(price_data, analysis.strategy, analysis.gain_stat.max.simulation)
        plt.figure()
        simulate.plot_investment_line_chart(price_data, analysis.strategy, analysis.gain_stat.min.simulation)
        plt.figure()
        simulate.plot_investment_line_chart(price_data, analysis.strategy, analysis.gain_stat.median.simulation)
        plt.show()
    else:
        print "Skip the line-charts."

if __name__ == "__main__":
    import sys
    price_data_file = sys.argv[1]
    strategy = sys.argv[2]

    price_data = simulate.parse_price_data_file(price_data_file)

    #Analyze half-year investment
    print "*********************************************************************"
    print "Analyzing half year investment ..."
    analysis = analyze_fixed_length_investment(price_data, 183, strategy)
    show_analysis_result(analysis) 
    print "*********************************************************************"
    print "Analyzing one year investment ..."
    analysis = analyze_fixed_length_investment(price_data, 365, strategy)
    show_analysis_result(analysis)
    print "*********************************************************************"
    print "Analyzing three year investment ..."
    analysis = analyze_fixed_length_investment(price_data, 1095, strategy)
    show_analysis_result(analysis)
    print "*********************************************************************"
    print "Analyzing five year investment ..."
    analysis = analyze_fixed_length_investment(price_data, 1825, strategy)
    show_analysis_result(analysis)
