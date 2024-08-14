from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

from models import db, Admin, Manufacturer, Client, Category, Product, Order, OrderDetails, Receipt, Cart, CartItem, Supply, SupplyOrder, Sales

# Initialize extensions
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///distributex.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config.from_object('config.Config')

    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app)

    from manufacturer import manufacturer_bp
    from routes import routes

    app.register_blueprint(routes)
    app.register_blueprint(manufacturer_bp, url_prefix='/api/manufacturers')
    
    with app.app_context():
        db.create_all()  # This ensures tables are created

        # Print all registered routes
        print_routes(app)

    return app

def print_routes(app):
    for rule in app.url_map.iter_rules():
        print(f'{rule.endpoint}: {rule.methods} -> {rule.rule}')

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
