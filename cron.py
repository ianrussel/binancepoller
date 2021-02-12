from database import Connect
from pymongo import MongoClient
from apscheduler.schedulers.blocking import BlockingScheduler
import requests as req
import json

cryptos = ['BNB', 'BTC', 'ETH', 'DOT']

sched = BlockingScheduler()
connection = Connect.get_connection()
db = connection.webvision


@sched.scheduled_job('interval', minutes=1)
def timed_job():
    print('fetching candlestick run every minute(s).')
    for crypto in cryptos:
        resp = req.get(
            f'https://api.binance.com/api/v1/klines?symbol={crypto}USDT&interval=5m&limit=1000')
        res = resp.json()
        db.candlesticks.insert_one(
            {"symbol": crypto,
             "data": res},
        ),


@ sched.scheduled_job('cron', day_of_week='mon-fri', hour=17)
def scheduled_job():
    print('This job is run every weekday at 5pm.')


sched.start()
