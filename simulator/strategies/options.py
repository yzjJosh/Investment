#!/usr/bin/env python
# A simple option simulator which only considers exercise/assignment/expiration, and ignores premium

import decision

BUY = "BUY"
SELL = "SELL"
CALL = "CALL"
PUT = "PUT"

TRIGGERED = "TRIGGERED"
EXPIRED = "EXPIRED"

KEY_TYPE = "TYPE"
KEY_STRIKE_PRICE = "STRIKE_PRICE"
KEY_EXPIRATION_DATE = "EXPIRATION_DATE"
KEY_NUM_CONTRACT = "NUM_CONTRACT"

options = []
day_index = 0
hour_counter = 0

def initialize():
    global options, day_index, hour_counter
    options = []
    day_index = 0
    hour_counter = 0

def trade_option(operation, option_type, strike_price, expiration_date, num_contract):
    global options, day_index
    if expiration_date <= day_index:
        raise Exception('Expiration date must be in the future!') 
    option = {}
    option[KEY_TYPE] = option_type
    option[KEY_STRIKE_PRICE] = strike_price
    option[KEY_EXPIRATION_DATE] = expiration_date
    if operation == BUY:
        option[KEY_NUM_CONTRACT] = num_contract
    else:
        option[KEY_NUM_CONTRACT] = -num_contract
    options.append(option)

# on_stock_price_change should be called after all trade_option calls
def on_stock_price_change(price):
    global day_index, options, hour_counter
    events = []
    hour_counter = (hour_counter + 1) % 7
    if (hour_counter == 0):
        for option in options[:]:
            if day_index == option[KEY_EXPIRATION_DATE]:
                if option[KEY_TYPE] == CALL and price > option[KEY_STRIKE_PRICE]:
                    events.append((option, TRIGGERED))
                elif option[KEY_TYPE] == PUT and price < option[KEY_STRIKE_PRICE]:
                    events.append((option, TRIGGERED))
                else:
                    events.append((option, EXPIRED))
                options.remove(option)
        day_index = day_index + 1
    return events

