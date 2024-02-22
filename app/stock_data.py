from flask import jsonify, request
import yfinance as yf
from datetime import date
import pandas as pd
from .models import StockList
from .extensions import db
import logging
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

def get_stock_data_api(ticker):
    stock = yf.Ticker(ticker)
    hist = stock.history(period="1mo")  # For example, fetch the last month's data
    data = {
        "dates": hist.index.strftime('%Y-%m-%d').tolist(),
        "prices": hist['Close'].tolist()
    }
    return jsonify(data)

def get_stock_list_returns():
    data = request.json
    list_name = data.get('listName')  # Assuming the request contains a 'listName'

    # Query the StockList model to get the list by name
    stock_list = StockList.query.filter_by(name=list_name).first()
    if not stock_list:
        return jsonify({"error": "Stock list not found"}), 404
    
    # Assuming tickers are stored as a comma-separated string
    tickers = stock_list.tickers.replace(' ', '').split(',')
    logging.debug('Tickers: %s', tickers)

    start_date = data.get('start', '2020-01-06')  # Default start date
    end_date = data.get('end', date.today().strftime('%Y-%m-%d'))  # Default end date
    
    prices = pd.DataFrame()
    for ticker in tickers:
        stock = yf.Ticker(ticker)
        hist = stock.history(start=start_date, end=end_date)
        prices[ticker] = hist['Close']
        
    returns = prices.pct_change().dropna()
    portfolio_returns = returns.mean(axis=1)
    
    cumulative_returns = (portfolio_returns + 1).cumprod()
    percentage_returns = cumulative_returns * 100 - 100 # Convert to percentage

    response_data = {
        "dates": cumulative_returns.index.strftime('%Y-%m-%d').tolist(),
        "returns": percentage_returns.tolist()
    }
    return jsonify(response_data)

# def get_stock_data(ticker):
#     stock = yf.Ticker(ticker)
#     info = stock.info  # Fetches a lot of information in a single call

#     # Get dividend data
#     dividends = stock.dividends.tail(1).iloc[-1] if not stock.dividends.empty else 0

#     # Calculate percentage changes for various periods
#     hist = stock.history(period="5y")  # Fetch history once for all calculations
#     pct_change_1m = hist['Close'].pct_change(periods=30).iloc[-1] * 100
#     pct_change_6m = hist['Close'].pct_change(periods=180).iloc[-1] * 100
#     pct_change_12m = hist['Close'].pct_change(periods=365).iloc[-1] * 100
#     pct_change_5y = hist['Close'].iloc[-1] / hist['Close'].iloc[0] * 100 - 100

#     # Format market cap
#     market_cap = info.get("marketCap", 0)
#     if market_cap != 0:
#         formatted_market_cap = market_cap / 1_000_000_000
#     else:
#         formatted_market_cap = 0

#     data = {
#         "symbol": ticker,
#         "current_price": hist["Close"].iloc[-1],
#         "fifty_two_week_high": info.get("fiftyTwoWeekHigh",0),
#         "fifty_two_week_low": info.get("fiftyTwoWeekLow", 0),
#         "dividends": dividends,
#         "dividend_yield": info.get("dividendYield", 0) * 100 if info.get("dividendYield") else 0,
#         "pe_ratio": info.get("trailingPE", 0),
#         "eps": info.get("trailingEps", 0),
#         "market_cap": formatted_market_cap,
#         "pct_change_1m": pct_change_1m,
#         "pct_change_6m": pct_change_6m,
#         "pct_change_12m": pct_change_12m,
#         "pct_change_5y": pct_change_5y
#     }
#     return data