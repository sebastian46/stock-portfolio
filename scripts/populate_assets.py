from app.extensions import db 
from app.models import Asset
from app.app import create_app

app = create_app()

with app.app_context():
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
        import ccxt

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

    def add_asset(identifier, asset_type):
        asset = Asset.query.filter_by(identifier=identifier).first()
        if not asset:
            asset = Asset(identifier=identifier, type=asset_type)
            db.session.add(asset)
        db.session.commit()

    def populate_assets():
        # Populate stocks
        stocks_data = get_all_stocks()
        for stock in stocks_data['stocks']:
            if stock:
                add_asset(identifier=stock, asset_type='stock')

        # Populate cryptos
        cryptos_data = get_all_crypto_symbols()
        for crypto in cryptos_data['crypto']:
            if crypto:
                add_asset(identifier=crypto, asset_type='crypto')

    if __name__ == '__main__':
        populate_assets()