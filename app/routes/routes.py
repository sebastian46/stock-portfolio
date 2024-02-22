from flask import Blueprint, render_template, jsonify, request
from ..extensions import db
from ..models import StockList
from ..stock_data import get_stock_data_api, get_stock_list_returns
from datetime import date

home_bp = Blueprint('home', __name__)

@home_bp.route('/')
def home():
    # This route renders the main page.
    return render_template('index.html')

@home_bp.route('/api/stock-data/<ticker>', methods=['GET'])
def stock_data(ticker):
    # This route fetches stock data for a single ticker.
    return get_stock_data_api(ticker)

@home_bp.route('/api/stock-list-returns', methods=['POST'])
def stock_list_returns():
    # This route calculates and returns the returns for a list of stocks.
    return get_stock_list_returns()

@home_bp.route('/api/stock-lists', methods=['GET', 'POST'])
def stock_lists():
    if request.method == 'GET':
        # Fetch all stock lists
        stock_lists = StockList.query.all()
        result = [{'id': lst.id, 'name': lst.name, 'tickers': lst.tickers.split(',')} for lst in stock_lists]
        return jsonify(result)
    elif request.method == 'POST':
        # Create a new stock list
        data = request.json
        name = data.get('name')
        tickers = data.get('tickers', [])
        if not name or not tickers:
            return jsonify({'error': 'Name and tickers are required'}), 400
        stock_list = StockList(name=name, tickers=','.join(tickers))
        db.session.add(stock_list)
        db.session.commit()
        return jsonify({'message': 'Stock list created successfully', 'id': stock_list.id}), 201
