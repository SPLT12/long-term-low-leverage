live_trade = True

lower_EMA  = 3
higher_EMA = 7

coin     = ["BTC", "ETH", "BNB", "DOGE"]
quantity = [0.001, 0.01 , 0.05, 50]

leverage, pair = [], []
for i in range(len(coin)):
    pair.append(coin[i] + "USDT")
    if   coin[i] == "BTC": leverage.append(40)
    elif coin[i] == "ETH": leverage.append(30)
    else: leverage.append(20)

    print("Pair Name        :   " + pair[i])
    print("Trade Quantity   :   " + str(quantity[i]) + " " + coin[i])
    print("Leverage         :   " + str(leverage[i]))
    print()
