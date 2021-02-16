import os
import ast
import os.path

from save import get_all_binance
from apscheduler.schedulers.blocking import BlockingScheduler


sched = BlockingScheduler()
number_minutes = os.getenv('NUMBER_MINUTES', 1)


@sched.scheduled_job('interval', minutes=int(number_minutes))
def timed_job():
    print(f'fetching candlestick run every {number_minutes} minute(s).')
    binance_symbols = ast.literal_eval(os.getenv("BINANCE_SYMBOLS"))

    for symbol in binance_symbols:
        print(symbol)
        try:  # noqa
            get_all_binance(symbol, "1m", save=True)
        except:  # noqa
            continue
    print("ALL DONE!")


sched.start()
