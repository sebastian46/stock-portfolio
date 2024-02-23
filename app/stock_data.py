from flask import jsonify, request
import yfinance as yf
from get_all_tickers import get_tickers as gt

from datetime import date
import pandas as pd
from .models import StockList
from .extensions import db

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

def get_all_stocks():
    import pandas as pd
    from yahoo_fin import stock_info as si


    # gather stock symbols from major US exchanges
    df1 = pd.DataFrame( si.tickers_sp500() )
    df2 = pd.DataFrame( si.tickers_nasdaq() )
    df3 = pd.DataFrame( si.tickers_dow() )
    df4 = pd.DataFrame( si.tickers_other() )

    # convert DataFrame to list, then to sets
    sym1 = set( symbol for symbol in df1[0].values.tolist() )
    sym2 = set( symbol for symbol in df2[0].values.tolist() )
    sym3 = set( symbol for symbol in df3[0].values.tolist() )
    sym4 = set( symbol for symbol in df4[0].values.tolist() )

    # join the 4 sets into one. Because it's a set, there will be no duplicate symbols
    symbols = set.union( sym1, sym2, sym3, sym4 )

    return {'stocks': list(symbols)}