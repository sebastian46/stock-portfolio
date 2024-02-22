from . import db

class StockList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    tickers = db.Column(db.String(300), nullable=False)
