#A strategy that buys stocks immediately and holds stock if its price doesn't exceed the threshold.
import decision

MAX_GAIN_PRECENTAGE = 10
MAX_LOSS_PERCENTAGE = 5

has_bought = False
base_price = 0.0
shares = 0
cash = 0.0

def initialize(init_cash):
    global has_bought, base_price, shares, cash
    has_bought = False
    base_price = 0.0
    shares = 0
    cash = init_cash

def on_stock_price_change(price):
    global has_bought, base_price, shares, cash    
    if not has_bought:
        has_bought = True
        shares = int(cash / price)
        cash = cash - shares * price
        base_price = price
        return (decision.BUY, shares)
    else:
        price_percentage = price / base_price * 100
        if shares > 0 and (price_percentage >= 100 + MAX_GAIN_PRECENTAGE or price_percentage <= 100 - MAX_LOSS_PERCENTAGE):
            shares_to_sell = int(shares / 2)
            if shares_to_sell == 0:
                shares_to_sell = shares
            cash = cash + shares_to_sell * price
            shares = shares - shares_to_sell
            base_price = price
            return (decision.SELL, shares_to_sell)
        else:
            return (decision.HOLD, 0)


    
