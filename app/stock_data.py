from flask import jsonify, request
import yfinance as yf
from get_all_tickers import get_tickers as gt

from datetime import date
import pandas as pd
import ccxt

def get_stock_data_api(ticker):
    stock = yf.Ticker(ticker)
    hist = stock.history(start='2020-01-06', end=date.today().strftime('%Y-%m-%d'))
    data = {
        "symbol" : ticker,
        "dates": hist.index.strftime('%Y-%m-%d').tolist(),
        "prices": hist['Close'].tolist()
    }
    return data

def get_crypto_data_api(ticker='ETH/USDT', exchange_id='gemini', timeframe='1d'):
    try:
        # Initialize the exchange
        exchange = getattr(ccxt, exchange_id)()

        # Verify if fetching OHLCV is supported
        if not exchange.has['fetchOHLCV']:
            return {"error": "Exchange does not support OHLCV data fetching."}

        # Fetch the daily OHLCV data
        ohlcv = exchange.fetch_ohlcv(ticker, timeframe)

        # Simplify the data processing by focusing only on the closing prices
        closing_prices = []
        dates = []

        for candle in ohlcv:
            timestamp = candle[0]
            close_price = candle[4]  # The closing price is the fifth element
            date = pd.to_datetime(timestamp, unit='ms').strftime('%Y-%m-%d')
            dates.append(date)
            closing_prices.append(close_price)

        # Prepare the simplified data structure
        data = {
            "symbol": ticker,
            "dates": dates,
            "prices": closing_prices
        }

        return data
    except Exception as e:
        return {"error": str(e)}