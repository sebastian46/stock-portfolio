from ..models import Asset, Portfolio, PortfolioAsset
from .. import db
import pandas as pd
from .asset_service import AssetService

class PortfolioService:
    @staticmethod
    def create_portfolio(name, assets_data):
        new_portfolio = Portfolio(name=name)
        db.session.add(new_portfolio)

        for asset_info in assets_data:
            ticker = asset_info.get('ticker')
            asset_type = asset_info.get('type')
            asset = Asset.query.filter_by(identifier=ticker, type=asset_type).first()
            if not asset:
                asset = Asset(identifier=ticker, type=asset_type)
                db.session.add(asset)
            
            portfolio_asset = PortfolioAsset(portfolio=new_portfolio, asset=asset)
            db.session.add(portfolio_asset)

        db.session.commit()
        return new_portfolio

    @staticmethod
    def get_all_portfolios():
        portfolios = Portfolio.query.all()
        return [{'id': portfolio.id, 'name': portfolio.name} for portfolio in portfolios]

    @staticmethod
    def get_portfolio_returns(portfolio_id, start_date, end_date):
        portfolio = Portfolio.query.get(portfolio_id)
        if not portfolio:
            return {"error": "Portfolio not found"}, 404
        
        prices = pd.DataFrame()
        # Get returns for assets
        for portfolio_asset in portfolio.assets:
            asset = portfolio_asset.asset
            ticker = asset.identifier
            asset_type = asset.type

            data = AssetService.get_asset_data(ticker, asset_type)
            data = pd.Series(data['prices'], index=data['dates'])
            prices[ticker] = data

        if prices.empty:
            return {"error": "No historical data found for the given period"}, 404
        
        # Ensure the index is a DatetimeIndex
        if not isinstance(prices.index, pd.DatetimeIndex):
            prices.index = pd.to_datetime(prices.index)

        returns = prices.pct_change().dropna()
        portfolio_returns = returns.mean(axis=1)
        
        cumulative_returns = (portfolio_returns + 1).cumprod()
        percentage_returns = cumulative_returns * 100 - 100  # Convert to percentage

        response_data = {
            "dates": cumulative_returns.index.strftime('%Y-%m-%d').tolist(),
            "returns": percentage_returns.tolist()
        }
        return response_data