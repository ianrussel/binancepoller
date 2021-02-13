from flask import Flask, request, Response
from datetime import datetime
import os
import json
import requests as req

from pymongo import MongoClient
from database import Connect

from binance.client import Client

# initialize binance
client = Client(os.getenv("BINANCE_API"), os.getenv("BINANCE_SECRET"))

# intialized db connection
connection = Connect.get_connection()
db = connection.webvision
app = Flask(__name__)


@app.route('/')
def index():
    return "Welcome"


@app.route('/api/information/products', methods=["GET"])
def getProducts():
    """get all products"""
    return client.get_products()


@app.route('/api/information/symbol/<symbol>', methods=["GET"])
def getSymbolInfo(symbol):
    """get symbol information"""
    response = client.get_symbol_info(symbol.upper())
    if response:
        return response
    return f'Error fetching symbol {symbol}, not found or wrong symbol name', 404


@app.route('/api/client/ping', methods=["GET"])
def pingClient():
    """ping the server"""
    return client.ping()


@app.route('/api/client/servertime', methods=["GET"])
def getClientServerTime():
    """return the binance server time"""
    return client.get_server_time()


@app.route('/api/client/systemstatus')
def getClientSystemStatus():
    """get binance server status"""
    return client.get_system_status()


""" Market data endpoints"""


@app.route('/api/symbol/<symbols>/market-dept', methods=["GET"])
def getMarketDept(symbols):
    """return market depth"""
    try:
        response = client.get_order_book(symbol=symbols)
        return response
    except:
        return f'{symbols} does not exists or undefined', 404


@app.route('/api/symbol/<symbols>/recent-trades', methods=["GET"])
def getSymbolRecentTrades(symbols):
    """get symbol recent trades"""
    try:
        response = client.get_recent_trades(symbol=symbols)
        return json.dumps(response)
    except:
        return f'{symbols} does not exists or undefined', 404


@app.route('/api/symbol/<symbols>/historical_trades', methods=["GET"])
def getSymbolHistoricalTrades(symbols):
    try:
        response = client.get_historical_trades(symbol=symbols)
        return response
    except:
        return f'{symbols} does not exists or undefined', 404

# candlesticks


@app.route('/api/klines', methods=['GET'])
def getCandleStick():
    limit = request.args.get('limit', '1000')
    if not request.args.get('symbol'):
        return 'symbol is required', 400
    if not request.args.get('interval'):
        return 'interval is required', 400
    res = req.get(
        f'https://api.binance.com/api/v1/klines?symbol={request.args.get("symbol").upper()}USDT&interval={request.args.get("interval")}&limit={limit}')
    return json.dumps(res.json())


@app.route('/api/historical_klines', methods=["GET"])
def getHistoricalCandleSticks():
    """ get the hsitorical klines"""
    if not request.args.get('symbol'):
        return 'symbol is required', 400
    limit = request.args.get('limit', 1000)
    if not request.args.get('start'):
        return 'start is required in query params', 400
    if not request.args.get("end"):
        return 'end is required in query params'
    if not request.args.get("symbol"):
        return 'symbol is required in query params', 400
    if datetime.strptime(request.args.get("start"), '%d %b, %Y') > datetime.strptime(request.args.get("end"), '%d %b, %Y'):
        return 'start date should not greater than end date', 400
    try:
        klines = client.get_historical_klines(
            request.args.get('symbol').upper(), request.args.get('interval'), request.args.get("start"), request.args.get("end"), int(limit))
        if klines is None:
            return f'no candlesticks for given start and end dates'
        return json.dumps(klines)
    except TypeError:
        print('error')
        return 'No response'


if __name__ == "__main__":
    app.run()
