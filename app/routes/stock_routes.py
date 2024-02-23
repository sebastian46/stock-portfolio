# from flask import Blueprint, jsonify
# from ..stock_data import get_stock_data_api, get_stock_list_returns

# stock_bp = Blueprint('stock', __name__)

# @stock_bp.route('/api/stock-data/<ticker>', methods=['GET'])
# def stock_data(ticker):
#     return get_stock_data_api(ticker)

# @stock_bp.route('/api/stock-list-returns', methods=['POST'])
# def stock_list_returns():
#     return get_stock_list_returns()