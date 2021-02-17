import os
import ast
import os.path
import logging

from save import get_all_binance
from apscheduler.schedulers.blocking import BlockingScheduler


sched = BlockingScheduler()
number_minutes = os.getenv('NUMBER_MINUTES', 1)


@sched.scheduled_job('interval', minutes=int(number_minutes))
def timed_job():
    print(f'fetching candlestick run every {number_minutes} minute(s).')
    binance_symbols = ast.literal_eval(os.getenv("BINANCE_SYMBOLS"))
    # print(binance_symbols.partition('_')[2])
    # pass

    for symbol in binance_symbols:
        print(str(symbol.partition('_')[2]))
        print(symbol.partition('_')[0])
        # pass
        try:  # noqa
            get_all_binance(symbol.partition('_')[0], str(symbol.partition('_')[2]), save=True)
        except Exception as e:  # noqa
            print(f'error: {e}')
            # continue
    print("ALL DONE!")


sched.start()
logging.getLogger('apscheduler.executors.default').setLevel(logging.WARNING)
