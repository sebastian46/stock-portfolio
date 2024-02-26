from . import db

class StockList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    tickers = db.Column(db.String(300), nullable=False)

class Asset(db.Model):
    __tablename__ = 'assets'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String, nullable=False)
    identifier = db.Column(db.String, unique=True, nullable=False)

    portfolios = db.relationship('PortfolioAsset', back_populates='asset')

class Portfolio(db.Model):
    __tablename__ = 'portfolios'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('portfolios.id'), nullable=True)

    children = db.relationship('Portfolio', 
                               backref=db.backref('parent', remote_side=[id]),
                               lazy='dynamic')
    assets = db.relationship('PortfolioAsset', back_populates='portfolio')

class PortfolioAsset(db.Model):
    __tablename__ = 'portfolio_assets'
    portfolio_id = db.Column(db.Integer, db.ForeignKey('portfolios.id'), primary_key=True)
    asset_id = db.Column(db.Integer, db.ForeignKey('assets.id'), primary_key=True)
    weight = db.Column(db.Float, nullable=False, server_default="0.0")

    asset = db.relationship('Asset', back_populates='portfolios')
    portfolio = db.relationship('Portfolio', back_populates='assets')