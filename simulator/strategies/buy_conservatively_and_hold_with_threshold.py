#A strategy that buys stocks when market is not too bad and holds stock if its price doesn't exceed the threshold.
import decision
from collections import deque

#Constants that determines buy decision
MAX_DROP_PERCENTAGE_PER_DAY = 2
MAX_DROP_PERCENTAGE_PER_WEEK = 3
MAX_DROP_PERCENTAGE_PER_THREE_WEEK = 5

#Constants that determines sell decision
MAX_GAIN_PRECENTAGE = 10
MAX_LOSS_PERCENTAGE = 5

price_history = deque()
base_prices = deque()
shares = 0
cash = 0.0

def initialize(init_cash):
    global price_history, base_prices, shares, cash
    price_history = deque()
    base_prices = deque()
    shares = 0
    cash = init_cash

def on_stock_price_change(price):
    global price_history, base_prices, shares, cash    
    
    #Make sell decision.
    shares_to_sell = 0
    if shares > 0:
        l = len(base_prices)
        while l > 0:
            base_price, share_number = base_prices.popleft()
            price_percentage = price / base_price * 100
            if price_percentage >= 100 + MAX_GAIN_PRECENTAGE or price_percentage <= 100 - MAX_LOSS_PERCENTAGE:
                new_sell = max(1, int(share_number / 2))
                shares_to_sell = shares_to_sell + new_sell 
                if share_number - new_sell > 0:
                   base_prices.append((price, share_number - new_sell))
            else:
                base_prices.append((base_price, share_number))
            l = l - 1

    #Make buy decision. 
    shares_to_buy = 0
    price_history.append(price)
    if len(price_history) >= 15 * 7:
        #Remove outdated price history
        if len(price_history) > 15 * 7:
            price_history.popleft();
        day_high = 0.0
        day_drop = 0.0
        week_high = 0.0
        week_drop = 0.0
        three_week_high = 0.0
        three_week_drop = 0.0
        should_buy = True
        i = 0
        for old_price in price_history:
            if day_high > 0:
                day_drop = max(day_drop, (day_high - old_price) / day_high * 100)
            if week_high > 0:
                week_drop = max(week_drop, (week_high - old_price) / week_high * 100)
            if three_week_high > 0:
                three_week_drop = max(three_week_drop, (three_week_high - old_price) / three_week_high * 100)
            if day_drop >= MAX_DROP_PERCENTAGE_PER_DAY or week_drop >= MAX_DROP_PERCENTAGE_PER_WEEK or three_week_drop >= MAX_DROP_PERCENTAGE_PER_THREE_WEEK:
                should_buy = False
                break
            i = i + 1
            if i%7 == 0:
                day_high = 0.0
                day_drop = 0.0
            if i%35 == 0:
                week_high = 0.0
                week_drop = 0.0
            day_high = max(day_high, old_price)
            week_high = max(week_high, old_price)
            three_week_high = max(three_week_high, old_price)

        if should_buy and cash >= price:
            shares_to_buy = max(1, int(cash/2/price))
            base_prices.append((price, shares_to_buy))
            #We should wait for at least another week to make another purchase
            i = 7 * 5
            while i > 0:
                price_history.popleft()
                i = i - 1

    share_change = shares_to_buy - shares_to_sell
    cash = cash - share_change * price
    shares = shares + share_change
   
    assert_share_integrity()

    if share_change == 0:
        return (decision.HOLD, 0)
    elif share_change > 0:
        return (decision.BUY, share_change)
    else:
        return (decision.SELL, - share_change)

   
def assert_share_integrity():
    share_sum = 0
    for e in base_prices:
        share_sum = share_sum + e[1]
    if share_sum != shares:
        raise Exception("Share number mismatch!")

