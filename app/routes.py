from flask import Blueprint, render_template, jsonify, request
from datetime import date
from .service.asset_service import AssetService
from .service.portfolio_service import PortfolioService

home_bp = Blueprint('home', __name__)

@home_bp.route('/')
def home():
    # This route renders the main page.
    return render_template('index.html')

@home_bp.route('/api/portfolio', methods=['GET', 'POST'])
def portfolio():
    if request.method == 'GET':
        result = PortfolioService.get_all_portfolios()
        return jsonify(result)
    elif request.method == 'POST':
        data = request.json
        portfolio = PortfolioService.create_portfolio(data.get('name'), data.get('assets', []))
        return jsonify({'message': 'Portfolio created successfully', 'id': portfolio.id})

@home_bp.route('/api/available-<asset_type>', methods=['GET'])
def get_available_assets(asset_type):
    search_query = request.args.get('search', '').upper()
    symbols = AssetService.get_assets_by_type(asset_type, search_query)
    return jsonify({asset_type: symbols})

@home_bp.route('/api/asset-data/<asset_type>/<path:identifier>', methods=['GET'])
def asset_data(asset_type, identifier):
    return AssetService.get_asset_data_api(identifier, asset_type)

@home_bp.route('/api/list-returns/<portfolio_id>', methods=['GET'])
def portfolio_returns(portfolio_id):
    # Fetch the start and end dates from query parameters, defaulting if not provided
    start_date = request.args.get('start', '2020-01-06')
    end_date = request.args.get('end', date.today().strftime('%Y-%m-%d'))

    return PortfolioService.get_portfolio_returns(portfolio_id, start_date, end_date)
