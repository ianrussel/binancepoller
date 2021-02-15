# IMPORTS
import pandas as pd
import math
import os.path
import os
import time
import ast
import json
from binance.client import Client
from datetime import timedelta, datetime
from dateutil import parser
from tqdm import tqdm_notebook  # (Optional, used for progress-bars)
import requests as req
from database import Connect
from insert import import_content

connection = Connect.get_connection()
db = connection.webvision

# CONSTANTS
binsizes = {"1m": 1, "5m": 5, "1h": 60, "1d": 1440}
batch_size = 750

binance_client = Client(os.getenv("BINANCE_API"), os.getenv("BINANCE_SECRET"))


# FUNCTIONS
def minutes_of_new_data(symbol, kline_size, data, source):
    if len(data) > 0:
        old = parser.parse(data["timestamp"].iloc[-1])
    elif source == "binance":
        old = datetime.strptime('1 Jan 2017', '%d %b %Y')
    if source == "binance":
        new = pd.to_datetime(binance_client.get_klines(
            symbol=symbol, interval=kline_size)[-1][0], unit='ms')
    return old, new


def get_all_binance(symbol, kline_size, save=False):
    filename = '%s/%s-%s-data.csv' % ("csv", symbol, kline_size)
    if os.path.isfile(filename):
        data_df = pd.read_csv(filename)
    else:
        data_df = pd.DataFrame()
    oldest_point, newest_point = minutes_of_new_data(
        symbol, kline_size, data_df, source="binance")
    delta_min = (newest_point - oldest_point).total_seconds()/60
    available_data = math.ceil(delta_min/binsizes[kline_size])
    if oldest_point == datetime.strptime('1 Jan 2017', '%d %b %Y'):
        print('Downloading all available %s data for %s. Be patient..!' %
              (kline_size, symbol))
    else:
        print('Downloading %d minutes of new data available for %s, i.e. %d instances of %s data.' % (
            delta_min, symbol, available_data, kline_size))
    klines = binance_client.get_historical_klines(symbol, kline_size, oldest_point.strftime(
        "%d %b %Y %H:%M:%S"), newest_point.strftime("%d %b %Y %H:%M:%S"))
    data = pd.DataFrame(klines, columns=['timestamp', 'open', 'high', 'low', 'close',
                                         'volume', 'close_time', 'quote_av', 'trades', 'tb_base_av', 'tb_quote_av', 'ignore'])
    data['timestamp'] = pd.to_datetime(data['timestamp'], unit='ms')
    if len(data_df) > 0:
        temp_df = pd.DataFrame(data)
        data_df = data_df.append(temp_df)
    else:
        data_df = data
    data_df.set_index('timestamp', inplace=True)
    if save:
        data_df.to_csv(filename)
        symbol = filename.split('/')[1].split('-')[0]
        # if symbol.upper() not in db.list_collection_names():
        """ save to db """
        import_content(filename, symbol)

    print('All caught up..!')
    return data_df


# resp = binance_client .get_products()
# res = resp
# for r in res['data']:
#     print(r['s'])
#     binance_symbols.append(r['s'])
# binance_symbols = ast.literal_eval(os.getenv("BINANCE_SYMBOLS"))

# for symbol in binance_symbols:
#     print(symbol)
#     try:
#         get_all_binance(symbol, "1m", save=True)
#     except:
#         continue
