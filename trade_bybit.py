import api_bybit
import config
import strategy
import retrieve_klines
from datetime import datetime
from termcolor import colored
from apscheduler.schedulers.blocking import BlockingScheduler

def lets_make_some_money():
    print("_Big_ Timeframe : " + retrieve_klines.big_timeframe)
    print("Entry Timeframe : " + retrieve_klines.entry_timeframe + "\n")

    for i in range(len(config.coin)):
        print(config.pair[i])
        klines = retrieve_klines.retrieve_klines(i)
        swing_trades = strategy.swing_trade(i, klines)
        swing_trades = swing_trades.drop(['volume'], axis=1)
        # print(swing_trades)

        response = api_bybit.position_information(i)
        if response[0].get('leverage') != config.leverage[i]: api_bybit.change_leverage(i)
        if response[1].get('leverage') != config.leverage[i]: api_bybit.change_leverage(i)
        if not response[0].get('is_isolated'): api_bybit.change_margin_to_ISOLATED(i)
        if not response[1].get('is_isolated'): api_bybit.change_margin_to_ISOLATED(i)
        
        if api_bybit.LONG_SIDE(response) == "NO_POSITION":
            if swing_trades["GO_LONG"].iloc[-1]:
                api_bybit.market_open_long(i)
                print(colored("🚀 GO_LONG 🚀", "green"))
            else: print("_LONG_SIDE : 🐺 WAIT 🐺")

        if api_bybit.LONG_SIDE(response) == "LONGING":
            if swing_trades["EXIT_LONG"].iloc[-1]:
                api_bybit.market_close_long(i, response)
                print("💰 CLOSE_LONG 💰")
            else: print(colored("_LONG_SIDE : HOLDING_LONG", "green"))

        if api_bybit.SHORT_SIDE(response) == "NO_POSITION":
            if swing_trades["GO_SHORT"].iloc[-1]:
                api_bybit.market_open_short(i)
                print(colored("💥 GO_SHORT 💥", "red"))
            else: print("SHORT_SIDE : 🐺 WAIT 🐺")

        if api_bybit.SHORT_SIDE(response) == "SHORTING":
            if swing_trades["EXIT_SHORT"].iloc[-1]:
                api_bybit.market_close_short(i, response)
                print("💰 CLOSE_SHORT 💰")
            else: print(colored("SHORT_SIDE : HOLDING_SHORT", "red"))

        print("Last action executed @ " + datetime.now().strftime("%H:%M:%S") + "\n")
print(colored("LIVE TRADE IS ENABLED\n", "green")) if config.live_trade else print(colored("THIS IS A DEMO\n", "red"))
try:
    if config.enable_scheduler:
        scheduler = BlockingScheduler()
        scheduler.add_job(lets_make_some_money, 'cron', minute='1')
        scheduler.start()
    else: lets_make_some_money()

except KeyboardInterrupt: print("\n\nAborted.\n")
