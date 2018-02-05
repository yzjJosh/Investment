#!/usr/bin/env python
#input: csv file that includes daily stock price downloaded from https://finance.yahoo.com
#output: string that contains randomly generated hourly stock price. Each line represents a day and has 7 price data (mimic 6 hour trading).

import sys
import random

KEY_DATE = "DATE"
KEY_OPEN_PRICE = "OPEN_PRICE"
KEY_HIGH_PRICE = "HIGH_PRICE"
KEY_LOW_PRICE = "LOW_PRICE"
KEY_CLOSE_PRICE = "CLOSE_PRICE"

input_file = sys.argv[1]

#Parse a single line of input file. Returns a dict.
def parse_line(line):
    res = {}
    part = line.split(",")
    res[KEY_DATE] = part[0].strip()
    res[KEY_OPEN_PRICE] = float(part[1].strip())
    res[KEY_HIGH_PRICE] = float(part[2].strip())
    res[KEY_LOW_PRICE] = float(part[3].strip())
    res[KEY_CLOSE_PRICE] = float(part[4].strip())
    return res

#Randomly generate hourly price data in a list with length 7 (mimic 6 hour trading).
def generate_hourly_price(open_price, low_price, high_price, close_price):
    hourly_data = [0] * 7
    for i in range(0, 7):
        hourly_data[i] = low_price + random.random() * (high_price - low_price)
    sample = random.sample(range(1, 6), 2)
    hourly_data[0] = open_price
    hourly_data[sample[0]] = low_price
    hourly_data[sample[1]] = high_price
    hourly_data[6] = close_price
    return hourly_data

with open(input_file, "r") as f:
    for line in f.readlines()[1:]:
        parsed = parse_line(line)
        hourly_data = generate_hourly_price(parsed[KEY_OPEN_PRICE], parsed[KEY_LOW_PRICE], parsed[KEY_HIGH_PRICE], parsed[KEY_CLOSE_PRICE])
        print " ".join(map(lambda x: str(int(x * 100) / 100.0), hourly_data))


