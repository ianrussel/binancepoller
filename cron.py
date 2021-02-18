import os
import ast
import os.path
import logging

from save import get_all_binance
from apscheduler.schedulers.blocking import BlockingScheduler


sched = BlockingScheduler()
number_minutes = os.getenv('NUMBER_MINUTES', 1)
number_seconds = os.getenv('NUMBER_SECONDS', 20)


@sched.scheduled_job('interval', minutes=int(number_minutes))
def timed_job():
    binance_symbols = ast.literal_eval(os.getenv("BINANCE_SYMBOLS"))

    for symbol in binance_symbols:
        try:  # noqa
            get_all_binance(symbol.partition('_')[0], str(symbol.partition('_')[2]), save=True)
        except Exception as e:  # noqa
            print(f'error: {e}')
            continue
    print("ALL DONE!")


logging.getLogger('apscheduler.scheduler').setLevel(logging.CRITICAL)
sched.start()
