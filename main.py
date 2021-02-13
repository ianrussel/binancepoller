from flask import Flask, request, Response
from datetime import datetime
import os
import json
import requests as req

from pymongo import MongoClient
from database import Connect

connection = Connect.get_connection()
db = connection.webvision
app = Flask(__name__)


@app.route('/')
def index():
    return "Welcome"


@app.route('/api/klines', methods=['GET'])
def getCandleStick():
    limit = request.args.get('limit', '1000')
    if not request.args.get('symbol'):
        return 'symbol is required', 400
    if not request.args.get('interval'):
        return 'interval is required', 400
    res = req.get(
        f'https://api.binance.com/api/v1/klines?symbol={request.args.get("symbol").upper()}USDT&interval={request.args.get("interval")}&limit={limit}')
    print(res.json())
    return json.dumps(res.json())
    # cs = db.candlesticks
    # query = {"symbol": request.args.get("symbol").upper()}
    # response = cs.find_one(query)

    # if not response:
    #     return f'no candlesticks available fro symbol {request.args.get("symbol").upper()}'

    # return json.dumps(response['data'])


if __name__ == "__main__":
    app.run()
