import api_binance
import config, strategy
import os, requests, socket, urllib3
from datetime import datetime
from termcolor import colored
from binance.exceptions import BinanceAPIException
print(colored("LIVE TRADE IS ENABLED\n", "green")) if config.live_trade else print(colored("THIS IS BACKTESTING\n", "red")) 

callbackRate = 1

def lets_make_some_money(pair, leverage, quantity): 
    print(pair)
    response = api_binance.position_information(pair)
    if response[0].get('marginType') != "isolated": api_binance.change_margin_to_ISOLATED(pair)
    if int(response[0].get("leverage")) != leverage: api_binance.change_leverage(pair, leverage)
    long_term_low_leverage = strategy.swing_trade(pair)
    # print(long_term_low_leverage)

    if api_binance.LONG_SIDE(response) == "NO_POSITION":
        if long_term_low_leverage["GO_LONG"].iloc[-1]:
            api_binance.trailing_open_long(pair, quantity, callbackRate)
        else: print("_LONG_SIDE : 🐺 WAIT 🐺")

    if api_binance.SHORT_SIDE(response) == "NO_POSITION":
        if long_term_low_leverage["GO_SHORT"].iloc[-1]:
            api_binance.trailing_open_short(pair, quantity, callbackRate)
        else: print("SHORT_SIDE : 🐺 WAIT 🐺")

    print("Last action executed @ " + datetime.now().strftime("%H:%M:%S") + "\n")

try:
    while True:
        try:
            for i in range(len(config.pair)):
                pair     = config.pair[i]
                leverage = config.leverage[i]
                quantity = config.quantity[i]
                lets_make_some_money(pair, leverage, quantity)

        except (socket.timeout,
                BinanceAPIException,
                urllib3.exceptions.ProtocolError,
                urllib3.exceptions.ReadTimeoutError,
                requests.exceptions.ConnectionError,
                requests.exceptions.ConnectTimeout,
                requests.exceptions.ReadTimeout,
                ConnectionResetError, KeyError, OSError) as e:

            if not os.path.exists("ERROR"): os.makedirs("ERROR")
            with open((os.path.join("ERROR", config.pair[i] + ".txt")), "a", encoding="utf-8") as error_message:
                error_message.write("[!] " + config.pair[i] + " - " + "Created at : " + datetime.today().strftime("%d-%m-%Y @ %H:%M:%S") + "\n" + str(e) + "\n\n")
                print(e)

except KeyboardInterrupt: print("\n\nAborted.\n")
