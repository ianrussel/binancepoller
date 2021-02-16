import os
import ast
import os.path

from save import get_all_binance
from apscheduler.schedulers.blocking import BlockingScheduler


sched = BlockingScheduler()
# connection = Connect.get_connection()
# db = connection.webvision


@sched.scheduled_job('interval', minutes=1)
def timed_job():
    print('fetching candlestick run every minute(s).')
    binance_symbols = ast.literal_eval(os.getenv("BINANCE_SYMBOLS"))

    for symbol in binance_symbols:
        print(symbol)
        try:  # noqa
            get_all_binance(symbol, "1m", save=True)
        except:  # noqa
            continue
    print("ALL DONE!")


sched.start()
