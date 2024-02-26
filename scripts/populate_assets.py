from app.extensions import db 
from app.models import Asset
from app.stock_data import get_all_stocks, get_all_crypto_symbols
from app.app import create_app

app = create_app()

with app.app_context():
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