#A strategy that buys stocks immediately and holds it unless its price drops below a lower bound. It will re-enter position if price bounces back above the lower bound.
import decision

SELL_LINE = 93
BUY_LINE = 95

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
        if shares > 0 and price_percentage <= SELL_LINE:
            shares_to_sell = shares
            cash = cash + shares_to_sell * price
            shares = 0
            return (decision.SELL, shares_to_sell)
        elif cash >= price and price_percentage >= BUY_LINE:
            shares_to_buy = int(cash / price)
            shares = shares + shares_to_buy
            cash = cash - shares_to_buy * price
            return (decision.BUY, shares_to_buy)
        else:
            return (decision.HOLD, 0)

