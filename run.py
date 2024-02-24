from flask import Flask
from flask.cli import with_appcontext
from app.extensions import db
from app.routes import home_bp
import click

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///portfolio.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # app.register_blueprint(stock_bp)
    app.register_blueprint(home_bp)

    with app.app_context():
        db.create_all()  # Create tables based on defined models

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
