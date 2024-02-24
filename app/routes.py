from flask import Blueprint, render_template, jsonify, request
from .extensions import db
from .models import StockList, Asset, Portfolio, PortfolioAsset
from .stock_data import get_stock_data_api, get_stock_list_returns, get_all_stocks, get_all_crypto_symbols, get_crypto_data_api
from datetime import date

home_bp = Blueprint('home', __name__)

@home_bp.route('/')
def home():
    # This route renders the main page.
    return render_template('index.html')

@home_bp.route('/api/create-list', methods=['GET', 'POST'])
def create_list():
    if request.method == 'GET':
        # Fetch all stock lists
        portfolios  = Portfolio.query.all()
        result = [{'id': portfolio.id, 'name': portfolio.name} for portfolio in portfolios]  # Use portfolio.name

        return jsonify(result)
    elif request.method == 'POST':
        data = request.json
        name = data.get('name')
        assets_data = data.get('assets', [])

        if not name or not assets_data:
            return jsonify({'error': 'Name and assets are required'}), 400

        new_portfolio = Portfolio(name=name)
        db.session.add(new_portfolio)

        for asset_info in assets_data:
            ticker = asset_info.get('ticker')
            asset_type = asset_info.get('type')

            # Check if the asset already exists
            asset = Asset.query.filter_by(identifier=ticker, type=asset_type).first()
            if not asset:
                # Create a new Asset if it doesn't exist
                asset = Asset(identifier=ticker, type=asset_type)
                db.session.add(asset)
            
            # Link the asset to the new portfolio
            portfolio_asset = PortfolioAsset(portfolio=new_portfolio, asset=asset)
            db.session.add(portfolio_asset)

        db.session.commit()
        return jsonify({'message': 'Portfolio created successfully', 'id': new_portfolio.id})


@home_bp.route('/api/stock-data/<ticker>', methods=['GET'])
def stock_data(ticker):
    # This route fetches stock data for a single ticker.
    return get_stock_data_api(ticker)

@home_bp.route('/api/stock-list-returns', methods=['POST'])
def stock_list_returns():
    # This route calculates and returns the returns for a list of stocks.
    return get_stock_list_returns()

@home_bp.route('/api/available-stock', methods=['GET'])
def get_stocks():
    search_query = request.args.get('search', '').upper()  # Assuming stock symbols are stored in uppercase
    if search_query:
        # Filter stocks based on the search query
        stock_assets = Asset.query.filter(Asset.type == 'stock', Asset.identifier.like(f"%{search_query}%")).all()
    else:
        # Query the database for all assets of type 'stock'
        stock_assets = Asset.query.filter_by(type='stock').all()

    # Extract the identifier (symbol) from each stock asset
    symbols = [stock.identifier for stock in stock_assets]

    return {'stock': symbols}

    # return get_all_stocks()

@home_bp.route('/api/available-crypto', methods=['GET'])
def get_crypto():
    search_query = request.args.get('search', '').upper()  # Assuming stock symbols are stored in uppercase
    if search_query:
        # Filter crypto based on the search query
        stock_assets = Asset.query.filter(Asset.type == 'crypto', Asset.identifier.like(f"%{search_query}%")).all()
    else:
        # Query the database for all assets of type 'stock'
        stock_assets = Asset.query.filter_by(type='crypto').all()
        print(stock_assets)

    # Extract the identifier (symbol) from each stock asset
    symbols = [stock.identifier for stock in stock_assets]

    return {'crypto': symbols}

@home_bp.route('/api/crypto-data/<ticker1>/<ticker2>', methods=['GET'])
def crypto_data(ticker1, ticker2):
    # This route fetches crypto data for a single ticker.
    ticker = f"{ticker1}/{ticker2}"
    return get_crypto_data_api(ticker)