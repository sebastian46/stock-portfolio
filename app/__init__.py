from flask import Flask
from .extensions import db
# from .routes.stock_routes import stock_bp
from .routes.routes import home_bp

def create_app():
    app = Flask(__name__, template_folder='../templates')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../stocks.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # app.register_blueprint(stock_bp)
    app.register_blueprint(home_bp)

    with app.app_context():
        db.create_all()  # Create tables based on defined models

    return app
