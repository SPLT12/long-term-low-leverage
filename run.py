try:
    import os
    import requests
    import socket
    import urllib3
    import config
    import binance_longterm
    from datetime import datetime
    from termcolor import colored
    from binance.exceptions import BinanceAPIException
    from apscheduler.schedulers.blocking import BlockingScheduler

    if config.live_trade:
        print(colored("LIVE TRADE IS ENABLED\n", "green"))
    else:
        print(colored("THIS IS BACKTESTING\n", "red"))
        # if not os.path.exists("BACKTEST"): os.makedirs("BACKTEST")

    def added_to_job():
        binance_longterm.lets_make_some_money()

    while True:
        try:
            scheduler = BlockingScheduler()
            scheduler.add_job(added_to_job, 'cron', minute='0,10,20,30,40,50')
            scheduler.start()

        except (socket.timeout,
                BinanceAPIException,
                urllib3.exceptions.ProtocolError,
                urllib3.exceptions.ReadTimeoutError,
                requests.exceptions.ConnectionError,
                requests.exceptions.ConnectTimeout,
                requests.exceptions.ReadTimeout,
                ConnectionResetError, KeyError, OSError) as e:

            if not os.path.exists("ERROR"): os.makedirs("ERROR")
            with open((os.path.join("ERROR", config.pairname + ".txt")), "a", encoding="utf-8") as error_message:
                error_message.write("[!] " + config.pairname + " - " + "Created at : " + datetime.today().strftime("%d-%m-%Y @ %H:%M:%S") + "\n")
                error_message.write(str(e) + "\n\n")

except KeyboardInterrupt: print("\n\nAborted.\n")