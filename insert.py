import sys
import pandas as pd
import pymongo
import json
import os
import time

from database import Connect

connection = Connect.get_connection()
db = connection.webvision


def import_content(filepath, symbol):
    start_time = time.time()
    collection_name = symbol
    db_cm = db[collection_name]
    cdir = os.path.dirname(__file__)
    file_res = os.path.join(cdir, filepath)

    data = pd.read_csv(file_res)
    data_json = json.loads(data.to_json(orient='records'))
    db[symbol].drop()
    db_cm.insert_many(data_json)
    print("---------%s seconds" % (time.time() - start_time))


# filepath = 'csv/BTCUSDT-1m-data.csv'
# import_content(filepath, filepath.split('/')[1].split('-')[0])
