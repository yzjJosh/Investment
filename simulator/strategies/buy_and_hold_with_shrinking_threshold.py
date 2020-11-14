#A strategy that buys stocks immediately and holds stock if its price doesn't exceed the threshold.
import decision

MAX_GAIN_PRECENTAGE = 10
MAX_LOSS_PERCENTAGE = 5

has_bought = False
base_price = 0.0
highest_price = 0.0
shares = 0
cash = 0.0

def initialize(init_cash):
    global has_bought, base_price, highest_price, shares, cash
    has_bought = False
    base_price = 0.0
    highest_price = highest_price
    shares = 0
    cash = init_cash

def on_stock_price_change(price):
    global has_bought, base_price, highest_price, shares, cash    
    if not has_bought:
        has_bought = True
        shares = int(cash / price)
        cash = cash - shares * price
        base_price = price
        highest_price = highest_price
        return [(decision.BUY, shares, price)]
    else:
        highest_price = max(price, highest_price)
        if shares > 0 and (price / base_price * 100 >= 100 + MAX_GAIN_PRECENTAGE or price / highest_price * 100 <= 100 - MAX_LOSS_PERCENTAGE):
            shares_to_sell = int(shares / 2)
            if shares_to_sell == 0:
                shares_to_sell = shares
            cash = cash + shares_to_sell * price
            shares = shares - shares_to_sell
            base_price = price
            highest_price = price
            return [(decision.SELL, shares_to_sell, price)]
        else:
            return [(decision.HOLD, 0, price)]


    
