from ..models import Asset
from ..stock_data import get_stock_data_api, get_crypto_data_api
from flask import jsonify

class AssetService:
    @staticmethod
    def get_assets_by_type(asset_type, search_query=None):
        # Ensure we're querying a supported asset type
        if asset_type not in ['stock', 'crypto']:
            return []  # or raise an error
        
        query = Asset.query.filter_by(type=asset_type)
        if search_query:
            query = query.filter(Asset.identifier.like(f"%{search_query}%"))
        assets = query.all()
        return [asset.identifier for asset in assets]
    
    @staticmethod
    def get_asset_data(ticker, asset_type):
        # This method only fetches data and can be used internally
        if asset_type == 'stock':
            return get_stock_data_api(ticker)
        elif asset_type == 'crypto':
            return get_crypto_data_api(ticker)
        else:
            return None  # or raise an Exception

    @staticmethod
    def get_asset_data_api(ticker, asset_type):
        # This method is specifically for the API and returns JSON responses
        data = AssetService.get_asset_data(ticker, asset_type)
        if data is not None:
            return jsonify(data)
        else:
            return jsonify({'error': 'Unsupported asset type'}), 400
