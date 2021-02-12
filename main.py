from flask import Flask, request, Response
from datetime import datetime
import os
import json

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
    cs = db.candlesticks
    response = cs.find_one({"symbol": request.args.get('symbol').upper()})
    if not response:
        return f'no candlesticks available fro symbol {request.args.get("symbol").upper()}'

    return json.dumps(response['data'])


if __name__ == "__main__":
    app.run()
