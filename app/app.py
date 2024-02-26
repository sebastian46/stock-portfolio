from flask import Flask
from flask_migrate import Migrate
from app.extensions import db
from app.routes import home_bp

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///portfolio.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    app.register_blueprint(home_bp)

    migrate = Migrate(app, db)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
