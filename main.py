from flask import Flask
from datetime import datetime
import os
import json

from pymongo import MongoClient
from database import Connect

connection = Connect.get_connection()
db = connection.webvision
app = Flask(__name__)


@app.route('/')
def getCandleStick():
    cs = db.candlesticks
    response = cs.find_one({"symbol": "BTC"})
    if not response:
        return "no candlesticks available"
    return json.dumps(response['data'])


if __name__ == "__main__":
    app.run()
