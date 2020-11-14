#A strategy that buys stocks immediately and holds stock all the time.
import decision

cash = 0.0

def initialize(init_cash):
    global cash
    cash = init_cash

def on_stock_price_change(price):
    global cash
    if cash > price:
        amount = int(cash / price)
        dec = [(decision.BUY, amount, price)]
        cash = cash - amount * price
        return dec
    else:
        return [(decision.HOLD, 0, price)]

