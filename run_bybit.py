import api_binanceusdm
import config, strategy
import requests, socket, urllib3
from datetime import datetime
from termcolor import colored
from apscheduler.schedulers.blocking import BlockingScheduler

if config.live_trade: print(colored("LIVE TRADE IS ENABLED\n", "green"))
else: print(colored("THIS IS BACKTESTING\n", "red"))

def lets_make_some_money():
    for i in range(len(config.coin)): 
        dataset = strategy.dataset(i)
        response = api_binanceusdm.position_information(i)
        if response[0].get('leverage') != config.leverage[i]: api_binanceusdm.change_leverage(i)
        if response[1].get('leverage') != config.leverage[i]: api_binanceusdm.change_leverage(i)
        if not response[0].get('is_isolated'): api_binanceusdm.change_margin_to_ISOLATED(i)
        if not response[1].get('is_isolated'): api_binanceusdm.change_margin_to_ISOLATED(i)

        if api_binanceusdm.LONG_SIDE(response) == "NO_POSITION":
            if strategy.GO_LONG_CONDITION(dataset):
                api_binanceusdm.market_open_long(i)
                print(colored("🚀 GO_LONG 🚀", "green"))
            else: print("LONG_SIDE : 🐺 WAIT 🐺")

        if api_binanceusdm.LONG_SIDE(response) == "LONGING":
            if strategy.EXIT_LONG_CONDITION(dataset):
                api_binanceusdm.market_close_long(i, response)
                print("💰 CLOSE_LONG 💰")
            else: print(colored("HOLDING_LONG", "green"))

        if api_binanceusdm.SHORT_SIDE(response) == "NO_POSITION":
            if strategy.GO_SHORT_CONDITION(dataset):
                api_binanceusdm.market__open_short(i)
                print(colored("💥 GO_SHORT 💥", "red"))
            else: print("SHORT_SIDE : 🐺 WAIT 🐺")

        if api_binanceusdm.SHORT_SIDE(response) == "SHORTING":
            if strategy.EXIT_SHORT_CONDITION(dataset):
                api_binanceusdm.market_close_short(i, response)
                print("💰 CLOSE_SHORT 💰")
            else: print(colored("HOLDING_SHORT", "red"))

        print("Last action executed @ " + datetime.now().strftime("%H:%M:%S") + "\n")

try:
    if config.enable_scheduler:
        scheduler = BlockingScheduler()
        scheduler.add_job(lets_make_some_money, 'cron', minute='0,10,20,30,40,50')
        scheduler.start()
    else: lets_make_some_money()

except (socket.timeout,
        urllib3.exceptions.ProtocolError,
        urllib3.exceptions.ReadTimeoutError,
        requests.exceptions.ConnectionError,
        requests.exceptions.ConnectTimeout,
        requests.exceptions.ReadTimeout,
        ConnectionResetError, KeyError, OSError) as e: print(e)

except KeyboardInterrupt: print("\n\nAborted.\n")
