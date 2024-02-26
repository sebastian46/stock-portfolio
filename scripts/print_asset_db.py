from app.models import Asset
from app.app import create_app

app = create_app()

with app.app_context():
    assets = Asset.query.all()
    for asset in assets:
        print(asset.identifier, asset.type)
