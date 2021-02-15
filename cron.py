import requests as req
import os
import json
import ast
from datetime import timedelta, datetime
from dateutil import parser
from tqdm import tqdm_notebook  # (Optional, used for progress-bars)
import pandas as pd
import math
import os.path
import time
from bitmex import bitmex

from save import get_all_binance

from database import Connect
from pymongo import MongoClient
from apscheduler.schedulers.blocking import BlockingScheduler
from binance.client import Client

# initialize binance
binance_api_key = os.getenv("BINANCE_API")
binance_api_secret = os.getenv("BINANCE_SECRET")
binance_client = Client(os.getenv("BINANCE_API"), os.getenv("BINANCE_SECRET"))

sched = BlockingScheduler()
connection = Connect.get_connection()
db = connection.webvision


@sched.scheduled_job('interval', minutes=1)
def timed_job():
    print('fetching candlestick run every minute(s).')
    binance_symbols = ast.literal_eval(os.getenv("BINANCE_SYMBOLS"))

    for symbol in binance_symbols:
        print(symbol)
        try:
            get_all_binance(symbol, "1m", save=True)
        except:
            continue


@ sched.scheduled_job('cron', day_of_week='mon-fri', hour=17)
def scheduled_job():
    print('This job is run every weekday at 5pm.')


sched.start()
