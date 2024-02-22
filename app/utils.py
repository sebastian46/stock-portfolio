import yfinance as yf

def get_stock_data(ticker):
    stock = yf.Ticker(ticker)
    info = stock.info  # Fetches a lot of information in a single call

    # Get dividend data
    dividends = stock.dividends.tail(1).iloc[-1] if not stock.dividends.empty else 0

    # Calculate percentage changes for various periods
    hist = stock.history(period="5y")  # Fetch history once for all calculations
    pct_change_1m = hist['Close'].pct_change(periods=30).iloc[-1] * 100
    pct_change_6m = hist['Close'].pct_change(periods=180).iloc[-1] * 100
    pct_change_12m = hist['Close'].pct_change(periods=365).iloc[-1] * 100
    pct_change_5y = hist['Close'].iloc[-1] / hist['Close'].iloc[0] * 100 - 100

    # Format market cap
    market_cap = info.get("marketCap", 0)
    if market_cap != 0:
        formatted_market_cap = market_cap / 1_000_000_000
    else:
        formatted_market_cap = 0

    data = {
        "symbol": ticker,
        "current_price": hist["Close"].iloc[-1],
        "fifty_two_week_high": info.get("fiftyTwoWeekHigh",0),
        "fifty_two_week_low": info.get("fiftyTwoWeekLow", 0),
        "dividends": dividends,
        "dividend_yield": info.get("dividendYield", 0) * 100 if info.get("dividendYield") else 0,
        "pe_ratio": info.get("trailingPE", 0),
        "eps": info.get("trailingEps", 0),
        "market_cap": formatted_market_cap,
        "pct_change_1m": pct_change_1m,
        "pct_change_6m": pct_change_6m,
        "pct_change_12m": pct_change_12m,
        "pct_change_5y": pct_change_5y
    }
    return data
