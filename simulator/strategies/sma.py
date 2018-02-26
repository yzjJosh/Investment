import moving_average
import decision

short_cash = 0.0
short_share = 0
long_cash = 0.0
long_share = 0
index_of_day = 0
index_of_week = 0
buy_short_in_week = False
sell_short_in_week = False
buy_long_in_week = False
sell_long_in_week = False

def initialize(init_cash):
    global short_cash, short_share, long_cash, long_share, index_of_day, index_of_week, buy_short_in_week, sell_short_in_week, buy_long_in_week, sell_long_in_week
    short_cash = init_cash / 3
    short_share = 0
    long_cash = init_cash - short_cash
    long_share = 0
    index_of_day = 0
    index_of_week = 0
    buy_short_in_week = False
    sell_short_in_week = False
    buy_long_in_week = False
    sell_long_in_week = False
    moving_average.reset()

def on_stock_price_change(price):
    global index_of_day, index_of_week, buy_short_in_week, sell_short_in_week, buy_long_in_week, sell_long_in_week
    index_of_day = (index_of_day + 1) % 7
    if index_of_day == 0:
        index_of_week = (index_of_week + 1) % 5
        if index_of_week == 0:
            buy_short_in_week = False
            sell_short_in_week = False
            buy_long_in_week = False
            sell_long_in_week = False
        moving_average.add(price)
        sma20 = moving_average.moving_average(20)
        sma50 = moving_average.moving_average(50)
        sma200 = moving_average.moving_average(200)
        r = max(price, max(sma20, max(sma50, sma200))) - min(price, min(sma20, min(sma50, sma200)))
        diff_c_20 = price - sma20
        diff_c_50 = price - sma50
        diff_c_200 = price - sma200
        diff_20_50 = sma20 - sma50
        diff_20_200 = sma20 - sma200
        diff_50_200 = sma50 - sma200
        score_20 = diff_c_20 / r if r > 0 else 0
        score_50 = diff_c_50 / r * 0.5 + diff_20_50 / r * 0.5 if r > 0 else 0
        score_200 = diff_c_200 / r * 0.34 + diff_20_200 / r * 0.33 + diff_50_200 / r * 0.33 if r > 0 else 0
        buy = 0
        if score_20 > 0 and score_50 > 0.05 and not buy_short_in_week:
            buy = buy + buy_short(price)
            buy_short_in_week = True
        if score_20 < 0 and score_50 < -0.05 and not sell_short_in_week:
            buy = buy - sell_short(price)
            sell_short_in_week = True
        if score_50 > 0 and score_200 > 0.05 and not buy_long_in_week:
            buy = buy + buy_long(price)
            buy_long_in_week = True
        if score_50 < 0 and score_200 < -0.05 and not sell_long_in_week:
            buy = buy - sell_long(price)
            sell_long_in_week = True
        if buy > 0:
            return (decision.BUY, abs(buy))
        elif buy < 0:
            return (decision.SELL, abs(buy))
        else:
            return (decision.HOLD, 0)
    else:
        return (decision.HOLD, 0)

# Spend half of available short cash to buy. Return shares bought.
def buy_short(price):
    global short_cash, short_share
    if short_cash < price:
        return 0
    share_to_buy = max(1, int(short_cash / 3 / price))
    short_cash = short_cash - share_to_buy * price
    short_share = short_share + share_to_buy
    return share_to_buy

# Sell half of available short shares. Return shares sold.
def sell_short(price):
    global short_cash, short_share
    if short_share == 0:
        return 0
    share_to_sell = max(1, short_share / 3)
    short_share = short_share - share_to_sell
    short_cash = short_cash + share_to_sell * price
    return share_to_sell

# Spend half of available long cash to buy. Return shares bought.
def buy_long(price):
    global long_cash, long_share
    if long_cash < price:
        return 0
    share_to_buy = max(1, int(long_cash / 3 / price))
    long_cash = long_cash - share_to_buy * price
    long_share = long_share + share_to_buy
    return share_to_buy

# Sell half of available long shares. Return shares sold.
def sell_long(price):
    global long_cash, long_share
    if long_share == 0:
        return 0
    share_to_sell = max(1, long_share / 3)
    long_share = long_share - share_to_sell
    long_cash = long_cash + share_to_sell * price
    return share_to_sell

