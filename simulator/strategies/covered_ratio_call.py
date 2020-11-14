#!/usr/bin/env python
# A strategy where you buy immediately, then sell a covered call and buy call spreads to boost upside return.

import decision
import options
import math

# Strike price is 5% higher
STRIKE_PRICE_RATIO = 1.05
# A month from expiration
DAYS_TO_EXPIRATION = 20

cash = 0.0
share = 0
covered_share = 0
day_index = 0
hour_counter = 0

def initialize(init_cash):
    global cash, share, covered_share, day_index, hour_counter
    cash = init_cash
    share = 0
    covered_share = 0
    day_index = 0
    hour_counter = 0
    options.initialize()

def on_stock_price_change(price):
    global cash, share, covered_share, day_index, hour_counter
    decisions = []

    # Buy immediately if we can.
    if cash >= price:
        buy_shares(int(cash / price), price, decisions)

    # Sell covered call and buy call spreads if we have enough shares.
    if share - covered_share >= 100:
        # Sell covered call firstly.
        strike_price = price * STRIKE_PRICE_RATIO
        expiration_date = day_index + DAYS_TO_EXPIRATION
        num_of_contract = int((share - covered_share) / 100)
        options.trade_option(options.SELL, options.CALL, strike_price, expiration_date, num_of_contract)
        covered_share = covered_share + num_of_contract * 100

        # Then buy a call spread, assuming the net cost is 0.
        options.trade_option(options.BUY, options.CALL, price, expiration_date, num_of_contract)
        options.trade_option(options.SELL, options.CALL, strike_price, expiration_date, num_of_contract)

    
    # Check assignment or exercise
    events = options.on_stock_price_change(price)
    on_option_events(events, price, decisions)
    
    # Increase day index
    hour_counter = (hour_counter + 1) % 7
    if (hour_counter == 0):
        day_index = day_index + 1
    return decisions

def on_option_events(events, price, decisions):
    global cash, share, covered_share

    # First pass: release covered shares
    total_contracts = 0
    for event in events:
        option = event[0]
        total_contracts = total_contracts + option[options.KEY_NUM_CONTRACT]
    if (total_contracts < 0):
        covered_share = covered_share - abs(total_contracts) * 100

    # Second pass: exercise or assignment
    for event in events:
        option = event[0]
        event_type = event[1]
        contracts = option[options.KEY_NUM_CONTRACT]
        strike_price = option[options.KEY_STRIKE_PRICE]
        if event_type == options.TRIGGERED:
            if contracts > 0:
                # We exercised our call.
                if not buy_shares(contracts * 100, strike_price, decisions):
                    # We don't have enough money to buy, so we sell our shares and retry.
                    shares_to_sell = int(math.ceil(contracts * 100 * strike_price / price))
                    if not (sell_shares(shares_to_sell, price, decisions) and buy_shares(contracts * 100, strike_price, decisions)):
                        raise Exception("Unable to exercise option: " + str(option) + ", cash=" + str(cash) + ", share=" + str(share) + ", price=" + str(price) + ", shares_to_sell=" + str(shares_to_sell) + ", covered_share=" + str(covered_share))
            elif contracts < 0:
                contracts = abs(contracts)
                # We get assigned our call.
                if not sell_shares(contracts * 100, strike_price, decisions):
                    # We don't have enough shares to sell, so we buy shares at market price and retry.
                    if not (buy_shares(contracts * 100, price, decisions) and sell_shares(contracts * 100, strike_price, decisions)):
                        raise Exception("Unable to assign option: " + str(option) + ", cash=" + str(cash) + ", share=" + str(share) + ", price=" + str(price))
    return decisions

def buy_shares(amount, price, decisions):
    global cash, share, covered_share
    if cash >= price * amount:
        cash = cash - price * amount
        share = share + amount
        decisions.append((decision.BUY, amount, price))
        return True
    else:
        return False

def sell_shares(amount, price, decisions):
    global cash, share, covered_share
    if share - covered_share >= amount:
        cash = cash + price * amount
        share = share - amount
        decisions.append((decision.SELL, amount, price))
        return True
    else:
        return False
