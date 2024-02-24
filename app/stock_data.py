from flask import jsonify, request
import yfinance as yf
from get_all_tickers import get_tickers as gt

from datetime import date
import pandas as pd
from .models import StockList, Portfolio, PortfolioAsset
from .extensions import db
import ccxt

def get_stock_data_api(ticker):
    stock = yf.Ticker(ticker)
    hist = stock.history(start='2020-01-06', end=date.today().strftime('%Y-%m-%d'))
    data = {
        "symbol" : ticker,
        "dates": hist.index.strftime('%Y-%m-%d').tolist(),
        "prices": hist['Close'].tolist()
    }
    return jsonify(data)

def get_stock_list_returns():
    data = request.json
    portfolio_id  = data.get('listId')  # Assuming the request contains a 'listId'

    # Query the StockList model to get the list by name
    portfolio = Portfolio.query.filter_by(id=portfolio_id).first()
    if not portfolio:
        return jsonify({"error": "Stock list not found"}), 404
    
    start_date = data.get('start', '2020-01-06')  # Default start date
    end_date = data.get('end', date.today().strftime('%Y-%m-%d'))  # Default end date
    
    prices = pd.DataFrame()
    for portfolio_asset in portfolio.assets:
        asset = portfolio_asset.asset
        ticker = asset.identifier  # Use the asset's identifier as the ticker

        # Fetch historical data for the ticker
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

def get_all_crypto_symbols():
    # Initialize the CCXT exchange
    exchange = ccxt.gemini()

    try:
        # Load markets
        markets = exchange.load_markets()

        # Get list of symbols
        symbols = list(markets.keys())

        return {'crypto': symbols}

    except Exception as e:
        # Handle exceptions
        print(f"Error retrieving crypto symbols: {e}")
        return {'error': str(e)}

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