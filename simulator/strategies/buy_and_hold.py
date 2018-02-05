#A strategy that buys stocks immediately and holds stock all the time.
import decision

cash = 0.0

def initialize(init_cash):
    global cash
    cash = init_cash

def on_stock_price_change(price):
    global cash
    if cash > price:
        dec = (decision.BUY, int(cash / price))
        cash = cash - dec[1] * price
        return dec
    else:
        return (decision.HOLD, 0)

